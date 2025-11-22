#!/usr/bin/env python3
"""
Extract Mermaid diagrams from markdown documentation and save to separate .mmd files.

Usage:
    python3 extract-diagrams.py <input-md-file> <output-dir>

Example:
    python3 extract-diagrams.py docs/CODITECT-C4-ARCHITECTURE-EVOLUTION.md diagrams/
"""

import sys
import re
from pathlib import Path


def extract_mermaid_diagrams(md_file, output_dir):
    """Extract all mermaid diagrams from markdown file."""

    with open(md_file, 'r', encoding='utf-8') as f:
        content = f.read()

    # Find all mermaid code blocks
    pattern = r'```mermaid\n(.*?)\n```'
    diagrams = re.findall(pattern, content, re.DOTALL)

    print(f"Found {len(diagrams)} mermaid diagrams in {md_file}")

    # Create output directory if it doesn't exist
    Path(output_dir).mkdir(parents=True, exist_ok=True)

    # Save each diagram
    for idx, diagram in enumerate(diagrams, 1):
        output_file = Path(output_dir) / f"diagram-{idx:02d}.mmd"
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(diagram)
        print(f"  Saved: {output_file}")

    return len(diagrams)


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print(__doc__)
        sys.exit(1)

    input_file = sys.argv[1]
    output_dir = sys.argv[2]

    if not Path(input_file).exists():
        print(f"Error: Input file not found: {input_file}")
        sys.exit(1)

    count = extract_mermaid_diagrams(input_file, output_dir)
    print(f"\nExtraction complete: {count} diagrams saved to {output_dir}")
