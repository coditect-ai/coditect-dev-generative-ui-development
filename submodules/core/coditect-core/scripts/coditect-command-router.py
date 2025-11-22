#!/usr/bin/env python3
"""
CODITECT AI Command Router

Simple AI-powered command selection assistant that analyzes your request
and suggests the appropriate slash command or agent invocation.

Usage:
    python3 coditect-command-router.py "I need to add user authentication to my app"
    python3 coditect-command-router.py "Fix the bug in the payment processing code"
    python3 coditect-command-router.py --interactive  # Interactive mode
"""

import os
import sys
import json
import argparse
from pathlib import Path

# Try to import anthropic (Claude API)
try:
    import anthropic
    HAS_ANTHROPIC = True
except ImportError:
    HAS_ANTHROPIC = False
    print("⚠️  Warning: anthropic package not installed. Install with: pip install anthropic")

class CommandRouter:
    """AI-powered command router for CODITECT slash commands"""

    def __init__(self, api_key: str = None):
        self.api_key = api_key or os.environ.get("ANTHROPIC_API_KEY")
        if not self.api_key and HAS_ANTHROPIC:
            print("⚠️  Warning: ANTHROPIC_API_KEY not set. Using fallback heuristics.")

        # Load slash commands reference
        self.commands = self._load_commands_reference()

    def _load_commands_reference(self) -> dict:
        """Load slash commands from reference file"""
        # Try to find SLASH-COMMANDS-REFERENCE.md
        script_dir = Path(__file__).parent.parent
        ref_file = script_dir / "docs" / "SLASH-COMMANDS-REFERENCE.md"

        if not ref_file.exists():
            print(f"⚠️  Warning: {ref_file} not found. Using basic command set.")
            return self._get_basic_commands()

        # Parse markdown table to extract commands
        commands = {}
        try:
            with open(ref_file, 'r') as f:
                lines = f.readlines()
                in_table = False
                for line in lines:
                    if line.startswith('|') and '---' not in line:
                        if not in_table and 'Command' in line:
                            in_table = True
                            continue
                        if in_table:
                            parts = [p.strip() for p in line.split('|') if p.strip()]
                            if len(parts) >= 3:
                                cmd = parts[0]
                                desc = parts[1]
                                purpose = parts[2]
                                commands[cmd] = {
                                    'description': desc,
                                    'purpose': purpose
                                }
        except Exception as e:
            print(f"⚠️  Error loading commands: {e}")
            return self._get_basic_commands()

        return commands

    def _get_basic_commands(self) -> dict:
        """Fallback basic command set"""
        return {
            "/implement": {"description": "Production-ready implementation", "purpose": "Build production code"},
            "/deliberation": {"description": "Planning mode", "purpose": "Analyze and plan"},
            "/debug": {"description": "Debug issues", "purpose": "Fix bugs and errors"},
            "/analyze": {"description": "Code review", "purpose": "Evaluate code quality"},
            "/research": {"description": "Research mode", "purpose": "Verify assumptions"},
            "/document": {"description": "Documentation", "purpose": "Create docs"},
            "/test_generate": {"description": "Test generation", "purpose": "Generate unit tests"},
            "/suggest-agent": {"description": "Agent selection", "purpose": "Get agent syntax"}
        }

    def analyze_request_with_ai(self, request: str) -> dict:
        """Use Claude API to analyze request and suggest command"""
        if not HAS_ANTHROPIC or not self.api_key:
            return self.analyze_request_heuristic(request)

        try:
            client = anthropic.Anthropic(api_key=self.api_key)

            # Build command list for prompt
            commands_list = "\n".join([
                f"- {cmd}: {info['description']}"
                for cmd, info in self.commands.items()
            ])

            prompt = f"""Analyze this user request and recommend the most appropriate CODITECT slash command(s).

User Request: "{request}"

Available Commands:
{commands_list}

Respond with a JSON object containing:
{{
    "primary_command": "command name",
    "reasoning": "why this command is best",
    "alternative_commands": ["cmd1", "cmd2"],
    "agent_recommendation": "if applicable, which specialized agent to use",
    "execution_steps": ["step 1", "step 2"]
}}

Only recommend commands from the list above. Be concise and practical."""

            message = client.messages.create(
                model="claude-sonnet-4-5-20250929",  # Latest Claude Sonnet 4.5 (Sept 2025)
                max_tokens=1000,
                messages=[{"role": "user", "content": prompt}]
            )

            # Parse JSON response
            response_text = message.content[0].text
            # Try to extract JSON from response
            if '{' in response_text:
                json_start = response_text.index('{')
                json_end = response_text.rindex('}') + 1
                json_str = response_text[json_start:json_end]
                return json.loads(json_str)
            else:
                return {"error": "Could not parse AI response", "raw": response_text}

        except Exception as e:
            print(f"⚠️  AI analysis failed: {e}")
            return self.analyze_request_heuristic(request)

    def analyze_request_heuristic(self, request: str) -> dict:
        """Fallback heuristic analysis without AI"""
        request_lower = request.lower()

        # Simple keyword-based routing
        if any(word in request_lower for word in ['implement', 'build', 'create', 'add']):
            return {
                "primary_command": "/implement",
                "reasoning": "Detected implementation request (keywords: implement, build, create, add)",
                "alternative_commands": ["/prototype", "/feature_development"],
                "execution_steps": ["Use /implement for production-ready code"]
            }
        elif any(word in request_lower for word in ['fix', 'bug', 'error', 'debug', 'broken']):
            return {
                "primary_command": "/debug",
                "reasoning": "Detected debugging request (keywords: fix, bug, error, debug)",
                "alternative_commands": ["/error_analysis", "/error_trace"],
                "execution_steps": ["Use /debug to analyze and fix the issue"]
            }
        elif any(word in request_lower for word in ['plan', 'design', 'architecture', 'strategy']):
            return {
                "primary_command": "/deliberation",
                "reasoning": "Detected planning request (keywords: plan, design, architecture)",
                "alternative_commands": ["/strategy", "/create_plan"],
                "execution_steps": ["Use /deliberation for pure planning without code execution"]
            }
        elif any(word in request_lower for word in ['review', 'analyze', 'check', 'quality']):
            return {
                "primary_command": "/analyze",
                "reasoning": "Detected code review request (keywords: review, analyze, check)",
                "alternative_commands": ["/full_review", "/ai_review"],
                "execution_steps": ["Use /analyze for code quality evaluation"]
            }
        elif any(word in request_lower for word in ['test', 'testing', 'unit test', 'tdd']):
            return {
                "primary_command": "/test_generate",
                "reasoning": "Detected testing request (keywords: test, testing, unit test)",
                "alternative_commands": ["/tdd_cycle"],
                "execution_steps": ["Use /test_generate for automated test creation"]
            }
        elif any(word in request_lower for word in ['document', 'docs', 'documentation', 'readme']):
            return {
                "primary_command": "/document",
                "reasoning": "Detected documentation request (keywords: document, docs, documentation)",
                "alternative_commands": ["/doc_generate"],
                "execution_steps": ["Use /document for comprehensive documentation generation"]
            }
        elif any(word in request_lower for word in ['research', 'investigate', 'explore', 'understand']):
            return {
                "primary_command": "/research",
                "reasoning": "Detected research request (keywords: research, investigate, explore)",
                "alternative_commands": ["/research_codebase", "/multi-agent-research"],
                "execution_steps": ["Use /research for focused investigation"]
            }
        elif any(phrase in request_lower for phrase in ['project plan', 'implementation plan', 'specification', 'submodule plan', 'orchestration plan', 'tasklist', 'project specifications']):
            return {
                "primary_command": "/generate-project-plan",
                "reasoning": "Detected project planning request for submodule-level implementation",
                "alternative_commands": ["/create_plan", "/strategy", "/deliberation"],
                "agent_recommendation": "orchestrator (for multi-agent coordination)",
                "execution_steps": [
                    "Navigate to submodule directory",
                    "Run: /generate-project-plan",
                    "Review generated PROJECT-PLAN.md and TASKLIST-WITH-CHECKBOXES.md",
                    "Use orchestrator agent to begin autonomous execution"
                ]
            }
        else:
            return {
                "primary_command": "/suggest-agent",
                "reasoning": "Request unclear - use /suggest-agent to get personalized recommendation",
                "alternative_commands": ["/COMMAND-GUIDE", "/agent-dispatcher"],
                "execution_steps": ["Use /suggest-agent to get specific agent invocation syntax"]
            }

    def format_recommendation(self, analysis: dict) -> str:
        """Format the analysis as human-readable output"""
        output = []
        output.append("\n" + "="*70)
        output.append("🤖 CODITECT AI Command Router")
        output.append("="*70 + "\n")

        if "error" in analysis:
            output.append(f"❌ Error: {analysis['error']}")
            if "raw" in analysis:
                output.append(f"\nRaw response: {analysis['raw']}")
            return "\n".join(output)

        # Primary recommendation
        primary = analysis.get('primary_command', 'Unknown')
        output.append(f"📍 RECOMMENDED COMMAND: {primary}")

        if primary in self.commands:
            cmd_info = self.commands[primary]
            output.append(f"   Description: {cmd_info.get('description', 'N/A')}")
            output.append(f"   Purpose: {cmd_info.get('purpose', 'N/A')}")

        output.append("")

        # Reasoning
        reasoning = analysis.get('reasoning', 'N/A')
        output.append(f"💭 REASONING:")
        output.append(f"   {reasoning}")
        output.append("")

        # Alternative commands
        alternatives = analysis.get('alternative_commands', [])
        if alternatives:
            output.append(f"🔄 ALTERNATIVES:")
            for alt in alternatives:
                if alt in self.commands:
                    alt_info = self.commands[alt]
                    output.append(f"   • {alt}: {alt_info.get('description', 'N/A')}")
                else:
                    output.append(f"   • {alt}")
            output.append("")

        # Agent recommendation
        agent = analysis.get('agent_recommendation')
        if agent:
            output.append(f"🎯 AGENT RECOMMENDATION:")
            output.append(f"   {agent}")
            output.append("")

        # Execution steps
        steps = analysis.get('execution_steps', [])
        if steps:
            output.append(f"📋 NEXT STEPS:")
            for i, step in enumerate(steps, 1):
                output.append(f"   {i}. {step}")
            output.append("")

        # Usage example
        output.append(f"💻 USAGE:")
        output.append(f"   Type in Claude Code: {primary}")
        output.append("")

        output.append("="*70)

        return "\n".join(output)

    def interactive_mode(self):
        """Run in interactive mode"""
        print("\n🤖 CODITECT AI Command Router - Interactive Mode")
        print("="*70)
        print("Type your request, or 'quit' to exit")
        print("="*70 + "\n")

        while True:
            try:
                request = input("📝 What do you want to do? > ").strip()

                if not request:
                    continue

                if request.lower() in ['quit', 'exit', 'q']:
                    print("\n👋 Goodbye!\n")
                    break

                # Analyze and display
                if HAS_ANTHROPIC and self.api_key:
                    print("\n🔄 Analyzing with AI...")
                    analysis = self.analyze_request_with_ai(request)
                else:
                    print("\n🔄 Analyzing with heuristics...")
                    analysis = self.analyze_request_heuristic(request)

                print(self.format_recommendation(analysis))

            except KeyboardInterrupt:
                print("\n\n👋 Goodbye!\n")
                break
            except Exception as e:
                print(f"\n❌ Error: {e}\n")

def main():
    parser = argparse.ArgumentParser(
        description="AI-powered command router for CODITECT",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python3 coditect-command-router.py "Add user authentication to my app"
  python3 coditect-command-router.py "Fix the bug in payment processing"
  python3 coditect-command-router.py --interactive

Environment Variables:
  ANTHROPIC_API_KEY - Your Anthropic API key for AI-powered analysis
        """
    )

    parser.add_argument(
        'request',
        nargs='?',
        help='Your request in natural language'
    )

    parser.add_argument(
        '-i', '--interactive',
        action='store_true',
        help='Run in interactive mode'
    )

    parser.add_argument(
        '--api-key',
        help='Anthropic API key (or set ANTHROPIC_API_KEY env var)'
    )

    args = parser.parse_args()

    # Create router
    router = CommandRouter(api_key=args.api_key)

    # Interactive mode
    if args.interactive:
        router.interactive_mode()
        return

    # Single request mode
    if not args.request:
        parser.print_help()
        return

    # Analyze request
    if HAS_ANTHROPIC and router.api_key:
        print("\n🔄 Analyzing with AI...")
        analysis = router.analyze_request_with_ai(args.request)
    else:
        print("\n🔄 Analyzing with heuristics (install anthropic for AI-powered analysis)...")
        analysis = router.analyze_request_heuristic(args.request)

    # Display recommendation
    print(router.format_recommendation(analysis))

if __name__ == "__main__":
    main()
