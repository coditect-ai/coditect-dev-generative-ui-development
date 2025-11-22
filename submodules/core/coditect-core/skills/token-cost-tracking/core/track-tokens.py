#!/usr/bin/env python3
"""
Token Cost Tracking Tool

Tracks token usage and costs across different LLM models for budget optimization.

Usage:
    ./track-tokens.py log --session "Build #20" --model claude-sonnet-4 --input-tokens 50000 --output-tokens 15000
    ./track-tokens.py report --period month
    ./track-tokens.py summary
"""

import json
import sys
from pathlib import Path
from datetime import datetime, timedelta
from typing import Dict, List, Optional

# Model pricing ($/1M tokens) - Updated Oct 2025
MODEL_PRICING = {
    "claude-sonnet-4": {"input": 3.00, "output": 15.00},
    "claude-sonnet-4.5": {"input": 3.00, "output": 15.00},
    "claude-opus": {"input": 15.00, "output": 75.00},
    "claude-opus-3.5": {"input": 15.00, "output": 75.00},
    "gpt-4-turbo": {"input": 10.00, "output": 30.00},
    "gpt-4o": {"input": 5.00, "output": 15.00},
    "gemini-1.5-pro": {"input": 1.25, "output": 5.00},
    "lm-studio": {"input": 0.00, "output": 0.00},  # Local, no API cost
}

# Paths
PROJECT_ROOT = Path(__file__).parent.parent.parent.parent.parent
LOG_FILE = PROJECT_ROOT / ".coditect" / "token-usage.jsonl"

def ensure_log_file():
    """Create log file directory if it doesn't exist."""
    LOG_FILE.parent.mkdir(parents=True, exist_ok=True)
    if not LOG_FILE.exists():
        LOG_FILE.touch()

def calculate_cost(model: str, input_tokens: int, output_tokens: int) -> float:
    """Calculate cost in USD for given token usage."""
    if model not in MODEL_PRICING:
        print(f"⚠️  Warning: Unknown model '{model}', using Claude Sonnet 4 pricing")
        model = "claude-sonnet-4"

    pricing = MODEL_PRICING[model]
    input_cost = (input_tokens / 1_000_000) * pricing["input"]
    output_cost = (output_tokens / 1_000_000) * pricing["output"]
    return round(input_cost + output_cost, 4)

def log_session(args):
    """Log a session's token usage."""
    ensure_log_file()

    session = args.session
    model = args.model
    input_tokens = args.input_tokens
    output_tokens = args.output_tokens
    notes = args.notes or ""

    total_tokens = input_tokens + output_tokens
    cost = calculate_cost(model, input_tokens, output_tokens)

    entry = {
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "session": session,
        "model": model,
        "input_tokens": input_tokens,
        "output_tokens": output_tokens,
        "total_tokens": total_tokens,
        "cost_usd": cost,
        "notes": notes
    }

    # Append to log file
    with LOG_FILE.open("a") as f:
        f.write(json.dumps(entry) + "\n")

    print(f"✓ Logged session: {session}")
    print(f"  Model: {model}")
    print(f"  Total tokens: {total_tokens:,}")
    print(f"  Cost: ${cost:.4f} USD")

def load_entries(period: Optional[str] = None, model: Optional[str] = None) -> List[Dict]:
    """Load entries from log file with optional filtering."""
    if not LOG_FILE.exists():
        return []

    entries = []
    with LOG_FILE.open("r") as f:
        for line in f:
            if line.strip():
                entries.append(json.loads(line))

    # Filter by period
    if period:
        now = datetime.utcnow()
        if period == "today":
            cutoff = now.replace(hour=0, minute=0, second=0, microsecond=0)
        elif period == "week":
            cutoff = now - timedelta(days=7)
        elif period == "month":
            cutoff = now - timedelta(days=30)
        else:
            cutoff = None

        if cutoff:
            entries = [e for e in entries if datetime.fromisoformat(e["timestamp"].replace("Z", "")) >= cutoff]

    # Filter by model
    if model:
        entries = [e for e in entries if e["model"] == model]

    return entries

def generate_report(args):
    """Generate usage report."""
    period = args.period
    model = args.model

    entries = load_entries(period, model)

    if not entries:
        print(f"No entries found for period: {period or 'all'}")
        return

    # Calculate totals
    total_sessions = len(entries)
    total_input = sum(e["input_tokens"] for e in entries)
    total_output = sum(e["output_tokens"] for e in entries)
    total_tokens = sum(e["total_tokens"] for e in entries)
    total_cost = sum(e["cost_usd"] for e in entries)

    # Group by model
    by_model = {}
    for e in entries:
        m = e["model"]
        if m not in by_model:
            by_model[m] = {"tokens": 0, "cost": 0, "count": 0}
        by_model[m]["tokens"] += e["total_tokens"]
        by_model[m]["cost"] += e["cost_usd"]
        by_model[m]["count"] += 1

    # Print report
    period_label = period or "all time"
    print(f"\n{'='*60}")
    print(f"Token Usage Report - {period_label}")
    print(f"{'='*60}\n")

    print(f"Total sessions: {total_sessions}")
    print(f"Total tokens: {total_tokens:,} ({total_input:,} input + {total_output:,} output)")
    print(f"Total cost: ${total_cost:.2f} USD\n")

    if len(by_model) > 1:
        print("By model:")
        for m, data in sorted(by_model.items(), key=lambda x: -x[1]["cost"]):
            print(f"  {m}: {data['tokens']:,} tokens (${data['cost']:.2f}, {data['count']} sessions)")
        print()

    # Top sessions
    top_sessions = sorted(entries, key=lambda x: -x["total_tokens"])[:5]
    print("Top sessions by token usage:")
    for i, e in enumerate(top_sessions, 1):
        print(f"  {i}. {e['session']}: {e['total_tokens']:,} tokens (${e['cost_usd']:.4f})")

def show_summary(args):
    """Show quick summary."""
    entries = load_entries()

    if not entries:
        print("No token usage data found. Start logging with 'track-tokens.py log'")
        return

    total_tokens = sum(e["total_tokens"] for e in entries)
    total_cost = sum(e["cost_usd"] for e in entries)

    print(f"\n📊 Token Usage Summary")
    print(f"{'='*60}")
    print(f"Total sessions: {len(entries)}")
    print(f"Total tokens: {total_tokens:,}")
    print(f"Total cost: ${total_cost:.2f} USD")
    print(f"Avg tokens/session: {total_tokens // len(entries):,}")
    print(f"Avg cost/session: ${total_cost / len(entries):.4f} USD")

def export_data(args):
    """Export data to CSV."""
    import csv

    entries = load_entries()
    output_file = args.output

    if not entries:
        print("No data to export")
        return

    with open(output_file, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=["timestamp", "session", "model", "input_tokens", "output_tokens", "total_tokens", "cost_usd", "notes"])
        writer.writeheader()
        writer.writerows(entries)

    print(f"✓ Exported {len(entries)} entries to {output_file}")

def compare_approaches(args):
    """Compare token usage between two approaches."""
    approach1 = args.approach_1
    tokens1 = args.tokens_1
    approach2 = args.approach_2
    tokens2 = args.tokens_2
    model = args.model or "claude-sonnet-4"

    cost1 = calculate_cost(model, tokens1, 0)  # Assume all input for comparison
    cost2 = calculate_cost(model, tokens2, 0)

    savings_tokens = tokens1 - tokens2
    savings_cost = cost1 - cost2
    savings_pct = (savings_tokens / tokens1 * 100) if tokens1 > 0 else 0

    print(f"\n{'='*60}")
    print(f"Comparison Report")
    print(f"{'='*60}\n")

    print(f"{approach1}:")
    print(f"  Tokens: {tokens1:,}")
    print(f"  Cost: ${cost1:.4f} USD\n")

    print(f"{approach2}:")
    print(f"  Tokens: {tokens2:,}")
    print(f"  Cost: ${cost2:.4f} USD\n")

    print(f"Savings: {savings_tokens:,} tokens ({savings_pct:.1f}%), ${savings_cost:.4f} USD")

def main():
    import argparse

    parser = argparse.ArgumentParser(description="Track token usage and costs")
    subparsers = parser.add_subparsers(dest="command", help="Command to run")

    # Log command
    log_parser = subparsers.add_parser("log", help="Log token usage")
    log_parser.add_argument("--session", required=True, help="Session name")
    log_parser.add_argument("--model", required=True, help="Model used")
    log_parser.add_argument("--input-tokens", type=int, required=True)
    log_parser.add_argument("--output-tokens", type=int, required=True)
    log_parser.add_argument("--notes", help="Optional notes")

    # Report command
    report_parser = subparsers.add_parser("report", help="Generate usage report")
    report_parser.add_argument("--period", choices=["today", "week", "month"], help="Time period")
    report_parser.add_argument("--model", help="Filter by model")

    # Summary command
    summary_parser = subparsers.add_parser("summary", help="Quick summary")

    # Export command
    export_parser = subparsers.add_parser("export", help="Export to CSV")
    export_parser.add_argument("--output", required=True, help="Output CSV file")

    # Compare command
    compare_parser = subparsers.add_parser("compare", help="Compare two approaches")
    compare_parser.add_argument("--approach-1", required=True)
    compare_parser.add_argument("--tokens-1", type=int, required=True)
    compare_parser.add_argument("--approach-2", required=True)
    compare_parser.add_argument("--tokens-2", type=int, required=True)
    compare_parser.add_argument("--model", default="claude-sonnet-4")

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        sys.exit(1)

    if args.command == "log":
        log_session(args)
    elif args.command == "report":
        generate_report(args)
    elif args.command == "summary":
        show_summary(args)
    elif args.command == "export":
        export_data(args)
    elif args.command == "compare":
        compare_approaches(args)

if __name__ == "__main__":
    main()
