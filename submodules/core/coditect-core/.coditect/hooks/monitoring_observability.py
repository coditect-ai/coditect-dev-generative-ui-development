#!/usr/bin/env python3
"""
Monitoring & Observability Hook for CODITECT

Provides comprehensive visibility into hook execution, performance, and system health.
Collects metrics, logs traces, and enables debugging and optimization.

Event: PostToolUse (all tools)
Matcher: tool_name = "*" (all tools)
Trigger: After every tool execution for complete observability
"""

import json
import sys
import time
import os
from pathlib import Path
from typing import Dict, Optional
from datetime import datetime
import hashlib


class MonitoringObservability:
    """Monitors hook execution and system observability"""

    def __init__(self, repo_root: str):
        self.repo_root = Path(repo_root)
        self.metrics_file = self.repo_root / '.coditect' / 'hooks' / '.hook-metrics.json'
        self.trace_file = self.repo_root / '.coditect' / 'hooks' / '.hook-traces.jsonl'
        self.health_file = self.repo_root / '.coditect' / 'hooks' / '.hook-health.json'
        self.metrics = self.load_metrics()
        self.start_time = time.time()

    def load_metrics(self) -> Dict:
        """Load existing metrics"""
        if self.metrics_file.exists():
            try:
                with open(self.metrics_file, 'r') as f:
                    import json as json_module
                    return json_module.load(f)
            except Exception:
                return self.init_metrics()
        return self.init_metrics()

    def init_metrics(self) -> Dict:
        """Initialize metrics structure"""
        return {
            'total_executions': 0,
            'hooks_executed': {},
            'total_time': 0.0,
            'errors': 0,
            'successes': 0,
            'start_time': datetime.now().isoformat(),
            'by_tool': {},
            'by_event': {}
        }

    def save_metrics(self):
        """Save metrics to file"""
        try:
            with open(self.metrics_file, 'w') as f:
                import json as json_module
                json_module.dump(self.metrics, f, indent=2)
        except Exception:
            pass

    def record_trace(self, event: str, tool_name: str, duration: float, status: str, details: Optional[Dict] = None):
        """Record execution trace"""
        trace = {
            'timestamp': datetime.now().isoformat(),
            'event': event,
            'tool': tool_name,
            'duration_ms': round(duration * 1000, 2),
            'status': status,
            'details': details or {}
        }

        try:
            with open(self.trace_file, 'a') as f:
                import json as json_module
                f.write(json_module.dumps(trace) + '\n')
        except Exception:
            pass

    def update_health_status(self):
        """Update system health status"""
        health = {
            'status': 'healthy',
            'timestamp': datetime.now().isoformat(),
            'metrics': {
                'total_executions': self.metrics['total_executions'],
                'success_rate': self.metrics['successes'] / max(1, self.metrics['total_executions']),
                'error_rate': self.metrics['errors'] / max(1, self.metrics['total_executions']),
                'avg_execution_time_ms': round(
                    (self.metrics['total_time'] / max(1, self.metrics['total_executions'])) * 1000, 2
                ),
                'hooks_active': len(self.metrics['hooks_executed'])
            }
        }

        # Determine health status
        if health['metrics']['error_rate'] > 0.1:
            health['status'] = 'degraded'
        elif health['metrics']['error_rate'] > 0.05:
            health['status'] = 'warning'

        try:
            with open(self.health_file, 'w') as f:
                import json as json_module
                json_module.dump(health, f, indent=2)
        except Exception:
            pass

        return health

    def get_performance_summary(self) -> Dict:
        """Get performance summary"""
        if self.metrics['total_executions'] == 0:
            return {
                'message': 'No executions recorded yet'
            }

        hooks_by_name = sorted(
            self.metrics['hooks_executed'].items(),
            key=lambda x: x[1]['total_time'],
            reverse=True
        )

        slowest_hooks = hooks_by_name[:5]

        return {
            'total_executions': self.metrics['total_executions'],
            'success_rate': f"{(self.metrics['successes'] / self.metrics['total_executions'] * 100):.1f}%",
            'error_rate': f"{(self.metrics['errors'] / self.metrics['total_executions'] * 100):.1f}%",
            'total_time_seconds': round(self.metrics['total_time'], 2),
            'avg_execution_time_ms': round(
                (self.metrics['total_time'] / self.metrics['total_executions']) * 1000, 2
            ),
            'slowest_hooks': [
                {
                    'name': name,
                    'total_time_ms': round(data['total_time'] * 1000, 2),
                    'execution_count': data['count'],
                    'avg_time_ms': round((data['total_time'] / data['count']) * 1000, 2)
                }
                for name, data in slowest_hooks
            ]
        }

    def monitor_execution(self, hook_input: Dict) -> Dict:
        """Monitor hook execution"""

        event = hook_input.get('event', 'Unknown')
        tool_name = hook_input.get('tool_name', 'Unknown')

        # Create execution ID for tracing
        exec_id = hashlib.md5(
            f"{datetime.now().isoformat()}{tool_name}{event}".encode()
        ).hexdigest()[:8]

        monitoring_data = {
            'execution_id': exec_id,
            'event': event,
            'tool': tool_name,
            'start_time': time.time(),
            'timestamp': datetime.now().isoformat()
        }

        # Track by tool
        if tool_name not in self.metrics['by_tool']:
            self.metrics['by_tool'][tool_name] = {'count': 0, 'total_time': 0}

        self.metrics['by_tool'][tool_name]['count'] += 1

        # Track by event
        if event not in self.metrics['by_event']:
            self.metrics['by_event'][event] = {'count': 0, 'total_time': 0}

        self.metrics['by_event'][event]['count'] += 1

        return monitoring_data

    def record_completion(self, monitoring_data: Dict, status: str = 'success', error: Optional[str] = None):
        """Record hook completion"""

        duration = time.time() - monitoring_data['start_time']

        # Update metrics
        self.metrics['total_executions'] += 1
        self.metrics['total_time'] += duration

        if status == 'success':
            self.metrics['successes'] += 1
        else:
            self.metrics['errors'] += 1

        # Track by tool
        tool = monitoring_data['tool']
        self.metrics['by_tool'][tool]['total_time'] += duration

        # Track by event
        event = monitoring_data['event']
        self.metrics['by_event'][event]['total_time'] += duration

        # Track individual hook
        hook_name = f"{event}_{tool}"
        if hook_name not in self.metrics['hooks_executed']:
            self.metrics['hooks_executed'][hook_name] = {
                'count': 0,
                'total_time': 0,
                'errors': 0
            }

        self.metrics['hooks_executed'][hook_name]['count'] += 1
        self.metrics['hooks_executed'][hook_name]['total_time'] += duration

        if status != 'success':
            self.metrics['hooks_executed'][hook_name]['errors'] += 1

        # Record trace
        self.record_trace(
            event,
            tool,
            duration,
            status,
            {
                'error': error,
                'execution_id': monitoring_data['execution_id']
            }
        )

        # Save metrics
        self.save_metrics()

        # Update health
        self.update_health_status()


def main():
    """Main hook entry point"""
    try:
        # Read hook input from stdin
        hook_input = json.loads(sys.stdin.read())

        # Get repo root
        script_dir = Path(__file__).parent.parent.parent
        repo_root = str(script_dir)

        # Initialize monitoring
        monitor = MonitoringObservability(repo_root)

        # Start monitoring
        monitoring_data = monitor.monitor_execution(hook_input)

        # Return status with execution ID for tracing
        result = {
            "continue": True,
            "suppressOutput": True,
            "metadata": {
                "execution_id": monitoring_data['execution_id'],
                "monitored": True
            }
        }

        # Include health status if there are existing metrics
        if monitor.metrics['total_executions'] > 0:
            health = monitor.update_health_status()
            if health['status'] != 'healthy':
                result['warning'] = f"System health: {health['status']}"

        # Record completion
        monitor.record_completion(monitoring_data, status='success')

        print(json.dumps(result))
        sys.exit(0)

    except json.JSONDecodeError:
        print(json.dumps({"continue": True, "suppressOutput": True}))
        sys.exit(0)
    except Exception as e:
        print(json.dumps({"continue": True, "suppressOutput": True}))
        sys.exit(0)


if __name__ == '__main__':
    main()
