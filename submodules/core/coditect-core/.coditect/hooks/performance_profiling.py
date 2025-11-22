#!/usr/bin/env python3
"""
Performance Profiling & Tuning Hook for CODITECT

Profiles hook execution, identifies bottlenecks, and suggests optimizations.
Provides detailed performance metrics and trend analysis.

Event: PostToolUse (after tool execution)
Matcher: tool_name = "*" (all tools)
Trigger: After every tool execution for complete profiling coverage
"""

import json
import sys
import time
import os
from pathlib import Path
from typing import Dict, Optional, List
from datetime import datetime, timedelta


class PerformanceProfiler:
    """Profiles and optimizes hook performance"""

    def __init__(self, repo_root: str):
        self.repo_root = Path(repo_root)
        self.profile_file = self.repo_root / '.coditect' / 'hooks' / '.performance-profile.json'
        self.bottleneck_file = self.repo_root / '.coditect' / 'hooks' / '.bottlenecks.json'
        self.profiles = self.load_profiles()

    def load_profiles(self) -> Dict:
        """Load existing performance profiles"""
        if self.profile_file.exists():
            try:
                with open(self.profile_file, 'r') as f:
                    import json as json_module
                    return json_module.load(f)
            except Exception:
                return {}
        return {}

    def save_profiles(self):
        """Save performance profiles"""
        try:
            with open(self.profile_file, 'w') as f:
                import json as json_module
                json_module.dump(self.profiles, f, indent=2)
        except Exception:
            pass

    def record_execution(self, tool_name: str, event: str, duration: float, details: Optional[Dict] = None):
        """Record execution metrics"""

        key = f"{event}_{tool_name}"

        if key not in self.profiles:
            self.profiles[key] = {
                'executions': [],
                'total_time': 0,
                'count': 0,
                'min_time': float('inf'),
                'max_time': 0,
                'avg_time': 0,
                'p95_time': 0,
                'p99_time': 0,
                'recent_trend': 'stable'
            }

        profile = self.profiles[key]

        # Add execution
        profile['executions'].append({
            'timestamp': datetime.now().isoformat(),
            'duration': duration,
            'details': details or {}
        })

        # Keep only last 100 executions
        if len(profile['executions']) > 100:
            profile['executions'] = profile['executions'][-100:]

        # Update statistics
        profile['total_time'] += duration
        profile['count'] += 1
        profile['min_time'] = min(profile['min_time'], duration)
        profile['max_time'] = max(profile['max_time'], duration)
        profile['avg_time'] = profile['total_time'] / profile['count']

        # Calculate percentiles
        if len(profile['executions']) >= 95:
            sorted_times = sorted([e['duration'] for e in profile['executions']])
            profile['p95_time'] = sorted_times[int(len(sorted_times) * 0.95)]
            profile['p99_time'] = sorted_times[int(len(sorted_times) * 0.99)]

        # Detect trend
        if len(profile['executions']) > 10:
            recent = [e['duration'] for e in profile['executions'][-10:]]
            older = [e['duration'] for e in profile['executions'][-20:-10]]

            recent_avg = sum(recent) / len(recent)
            older_avg = sum(older) / len(older) if older else recent_avg

            if recent_avg > older_avg * 1.2:
                profile['recent_trend'] = 'degrading'
            elif recent_avg < older_avg * 0.8:
                profile['recent_trend'] = 'improving'
            else:
                profile['recent_trend'] = 'stable'

        self.save_profiles()

    def identify_bottlenecks(self) -> List[Dict]:
        """Identify performance bottlenecks"""

        bottlenecks = []

        for hook_name, profile in self.profiles.items():
            if profile['count'] == 0:
                continue

            # Slow hooks (>500ms avg)
            if profile['avg_time'] > 0.5:
                bottlenecks.append({
                    'hook': hook_name,
                    'issue': 'slow_execution',
                    'metric': f"{profile['avg_time']*1000:.0f}ms avg",
                    'severity': 'high' if profile['avg_time'] > 1.0 else 'medium',
                    'recommendation': f"Optimize {hook_name} - currently taking {profile['avg_time']*1000:.0f}ms"
                })

            # Degrading performance
            if profile['recent_trend'] == 'degrading':
                bottlenecks.append({
                    'hook': hook_name,
                    'issue': 'degrading_performance',
                    'metric': f"Recent trend: {profile['recent_trend']}",
                    'severity': 'medium',
                    'recommendation': f"{hook_name} performance degrading. Check for resource leaks or inefficient patterns."
                })

            # High variance (inconsistent performance)
            if profile['count'] > 5:
                variance = (profile['max_time'] - profile['min_time']) / max(profile['min_time'], 0.001)
                if variance > 2.0:
                    bottlenecks.append({
                        'hook': hook_name,
                        'issue': 'high_variance',
                        'metric': f"min: {profile['min_time']*1000:.0f}ms, max: {profile['max_time']*1000:.0f}ms",
                        'severity': 'low',
                        'recommendation': f"{hook_name} has high execution time variance. Investigate edge cases."
                    })

        return sorted(bottlenecks, key=lambda x: x['severity'] == 'high', reverse=True)

    def get_optimization_suggestions(self, hook_name: str, profile: Dict) -> List[str]:
        """Get optimization suggestions for hook"""

        suggestions = []

        # Based on execution time
        if profile['avg_time'] > 1.0:
            suggestions.append("Consider caching results to avoid redundant processing")
            suggestions.append("Profile code to identify hot paths")

        if profile['avg_time'] > 0.5:
            suggestions.append("Reduce validation overhead if not critical")
            suggestions.append("Consider async processing for blocking operations")

        # Based on variance
        recent_times = [e['duration'] for e in profile['executions'][-10:]] if profile['executions'] else []
        if recent_times:
            recent_avg = sum(recent_times) / len(recent_times)
            if max(recent_times) > recent_avg * 2:
                suggestions.append("Investigate outlier executions - may indicate edge cases")

        # Based on trend
        if profile['recent_trend'] == 'degrading':
            suggestions.append("Check for resource leaks or accumulating state")
            suggestions.append("Monitor system resources (CPU, memory, disk)")

        return suggestions

    def get_performance_report(self) -> Dict:
        """Generate performance report"""

        report = {
            'timestamp': datetime.now().isoformat(),
            'summary': {
                'total_hooks': len(self.profiles),
                'total_executions': sum(p['count'] for p in self.profiles.values()),
                'avg_execution_time_ms': round(
                    sum(p['avg_time'] for p in self.profiles.values()) / max(1, len(self.profiles)) * 1000, 2
                ),
                'slowest_hook': None,
                'fastest_hook': None
            },
            'bottlenecks': self.identify_bottlenecks(),
            'hook_details': {}
        }

        # Find slowest and fastest
        if self.profiles:
            slowest = max(self.profiles.items(), key=lambda x: x[1]['avg_time'])
            fastest = min(self.profiles.items(), key=lambda x: x[1]['avg_time'])
            report['summary']['slowest_hook'] = slowest[0]
            report['summary']['fastest_hook'] = fastest[0]

        # Hook details
        for hook_name, profile in list(self.profiles.items())[:10]:  # Top 10 hooks
            report['hook_details'][hook_name] = {
                'executions': profile['count'],
                'avg_time_ms': round(profile['avg_time'] * 1000, 2),
                'p95_time_ms': round(profile['p95_time'] * 1000, 2),
                'p99_time_ms': round(profile['p99_time'] * 1000, 2),
                'trend': profile['recent_trend'],
                'suggestions': self.get_optimization_suggestions(hook_name, profile)
            }

        return report


def main():
    """Main hook entry point"""
    try:
        # Read hook input from stdin
        hook_input = json.loads(sys.stdin.read())

        # Extract information
        tool_name = hook_input.get('tool_name', 'Unknown')
        event = hook_input.get('event', 'PostToolUse')
        duration = hook_input.get('duration', 0)  # Duration in seconds
        details = hook_input.get('details', {})

        # Get repo root
        script_dir = Path(__file__).parent.parent.parent
        repo_root = str(script_dir)

        # Initialize profiler
        profiler = PerformanceProfiler(repo_root)

        # Record execution
        profiler.record_execution(tool_name, event, duration, details)

        # Get performance report
        report = profiler.get_performance_report()

        # Log report if there are bottlenecks
        if report['bottlenecks']:
            bottleneck_file = repo_root + '/.performance-bottlenecks.txt'
            try:
                with open(bottleneck_file, 'w') as f:
                    f.write("Performance Bottlenecks Report\n")
                    f.write(f"Generated: {datetime.now().isoformat()}\n\n")

                    for bottleneck in report['bottlenecks']:
                        f.write(f"Hook: {bottleneck['hook']}\n")
                        f.write(f"Issue: {bottleneck['issue']}\n")
                        f.write(f"Metric: {bottleneck['metric']}\n")
                        f.write(f"Severity: {bottleneck['severity']}\n")
                        f.write(f"Recommendation: {bottleneck['recommendation']}\n\n")
            except Exception:
                pass

        # Always allow operation (non-blocking hook)
        print(json.dumps({"continue": True, "suppressOutput": True}))
        sys.exit(0)

    except json.JSONDecodeError:
        print(json.dumps({"continue": True, "suppressOutput": True}))
        sys.exit(0)
    except Exception as e:
        print(json.dumps({"continue": True, "suppressOutput": True}))
        sys.exit(0)


if __name__ == '__main__':
    main()
