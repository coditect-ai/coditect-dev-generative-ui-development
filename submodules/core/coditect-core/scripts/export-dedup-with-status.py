#!/usr/bin/env python3
"""
Export Deduplication with Guaranteed Status Report

This wrapper ensures that /export-dedup ALWAYS displays a visible status report
by writing output to:
  1. stdout (for immediate display)
  2. MEMORY-CONTEXT/export-dedup-status.txt (persistent log)
  3. Prints final summary with clear visual markers

Author: Claude + AZ1.AI
License: MIT
"""

import sys
import subprocess
from pathlib import Path
from datetime import datetime
import os
import re

def extract_metric(text, pattern, fallback_pattern=None):
    """
    Extract numeric metric from output text.

    Examples:
        extract_metric(output, "New unique:", "new_unique")
        → Looks for "New unique: 143" and returns 143
    """
    if not text:
        return None

    # Try to find pattern followed by a number
    # Handles formats like:
    # - "New unique: 143"
    # - "New unique messages: 143"
    # - "Total messages: 206"
    match = re.search(rf"{re.escape(pattern)}\s*(\d+)", text)
    if match:
        return int(match.group(1))

    return None

def main():
    """Execute export-dedup.py and ALWAYS display status report"""

    # Paths
    repo_root = Path(__file__).resolve().parent.parent.parent.parent.parent
    script_path = repo_root / "submodules" / "core" / "coditect-core" / "scripts" / "export-dedup.py"
    memory_context = repo_root / "MEMORY-CONTEXT"
    status_log = memory_context / "export-dedup-status.txt"

    # Ensure MEMORY-CONTEXT exists
    memory_context.mkdir(parents=True, exist_ok=True)

    # Timestamp for this execution
    start_time = datetime.now()
    timestamp_str = start_time.isoformat()

    # Build status report header
    header = f"""
{'='*80}
EXPORT-DEDUP EXECUTION REPORT
{'='*80}
Started: {timestamp_str}
Repository: {repo_root.name}
Status Log: {status_log.relative_to(repo_root)}
{'='*80}
"""

    # Print header to stdout immediately
    print(header, flush=True)

    # Execute the actual export-dedup script
    print("\n📦 RUNNING DEDUPLICATION PROCESS...\n", flush=True)

    try:
        result = subprocess.run(
            [sys.executable, str(script_path), "--yes", "--auto-compact"],
            capture_output=True,
            text=True,
            cwd=repo_root
        )

        # Capture all output
        stdout = result.stdout if result.stdout else ""
        stderr = result.stderr if result.stderr else ""

        # Extract key metrics from output
        new_unique_count = extract_metric(stdout, "New unique:", "new_unique")
        duplicates_count = extract_metric(stdout, "Duplicates filtered:", "duplicates_filtered")
        global_unique_count = extract_metric(stdout, "Global unique count:", "global_unique_count")
        total_messages = extract_metric(stdout, "Total messages:", "total_messages")

        # Print script output immediately to stdout
        if stdout:
            print(stdout, flush=True)
        if stderr:
            print(stderr, file=sys.stderr, flush=True)

        # Generate final status
        end_time = datetime.now()
        duration = (end_time - start_time).total_seconds()

        status = "✅ SUCCESS" if result.returncode == 0 else "❌ FAILED"

        # Build prominent metrics display
        metrics_display = f"""
{'🔐'*40}
📊 BACKUP & DEDUPLICATION RESULTS
{'🔐'*40}
"""
        if new_unique_count is not None:
            metrics_display += f"\n🆕 NEW UNIQUE MESSAGES ADDED & BACKED UP: {new_unique_count}\n"
        if duplicates_count is not None:
            metrics_display += f"🔄 Duplicate Messages Filtered: {duplicates_count}\n"
        if total_messages is not None:
            metrics_display += f"📨 Total Messages Processed: {total_messages}\n"
        if global_unique_count is not None:
            metrics_display += f"💾 Total Unique Messages in Storage: {global_unique_count}\n"
        metrics_display += f"{'🔐'*40}\n"

        footer = f"""
{'='*80}
EXECUTION SUMMARY
{'='*80}
Status: {status}
Exit Code: {result.returncode}
Completed: {end_time.isoformat()}
Duration: {duration:.2f} seconds
{'='*80}
"""

        # Print metrics prominently
        print(metrics_display, flush=True)

        # Print footer to stdout
        print(footer, flush=True)

        # Compose complete report for logging (includes metrics display)
        complete_report = header + "\n" + stdout + "\n" + stderr + "\n" + metrics_display + "\n" + footer

        # Write to status log file
        with open(status_log, "a") as f:
            f.write(complete_report)
            f.write("\n\n")

        # Print log location to user
        print(f"\n📝 Full report saved to: {status_log.relative_to(repo_root)}", flush=True)

        # Exit with same code as script
        sys.exit(result.returncode)

    except FileNotFoundError:
        error_msg = f"""
❌ ERROR: export-dedup.py not found at {script_path}

This script is required for deduplication to work.
Make sure submodules are initialized: git submodule update --init --recursive
"""
        print(error_msg, flush=True)

        # Log to file
        with open(status_log, "a") as f:
            f.write(header)
            f.write(error_msg)
            f.write(f"\nCompleted: {datetime.now().isoformat()}\n")
            f.write("="*80 + "\n\n")

        sys.exit(1)
    except Exception as e:
        error_msg = f"""
❌ UNEXPECTED ERROR: {e}

Traceback:
{traceback.format_exc()}
"""
        print(error_msg, flush=True)

        # Log to file
        with open(status_log, "a") as f:
            f.write(header)
            f.write(error_msg)
            f.write(f"\nCompleted: {datetime.now().isoformat()}\n")
            f.write("="*80 + "\n\n")

        sys.exit(1)

if __name__ == "__main__":
    import traceback
    main()
