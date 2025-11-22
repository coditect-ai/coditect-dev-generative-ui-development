#!/usr/bin/env python3
"""
Batch Submodule Setup - Multiple Repository Creation

Automates setup of multiple CODITECT submodules from a configuration file,
enabling efficient bulk repository creation with consistent standards.

Usage:
    python3 batch-setup.py --config submodules.yml
    python3 batch-setup.py --config submodules.json

Examples:
    python3 batch-setup.py --config cloud-services.yml
    python3 batch-setup.py --config dev-tools.json --dry-run

Requirements:
    - Python 3.9+
    - All prerequisites for setup-new-submodule.py
    - YAML or JSON configuration file

Configuration Format (YAML):
    submodules:
      - category: cloud
        name: coditect-cloud-gateway
        purpose: API gateway for cloud services
        visibility: public
      - category: dev
        name: coditect-dev-logger
        purpose: Centralized logging utility
        visibility: private

Exit Codes:
    0: Success - All submodules created
    1: Partial failure - Some submodules failed
    2: Usage error - Invalid arguments
    3: Configuration error - Invalid config file
"""

import sys
import argparse
import logging
import subprocess
from pathlib import Path
from typing import List, Dict, Any
import json

# Handle yaml import with auto-installation
try:
    import yaml
except ImportError:
    print("Installing required dependency: pyyaml...")
    subprocess.run([sys.executable, "-m", "pip", "install", "pyyaml"], check=True)
    import yaml

logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')
logger = logging.getLogger(__name__)

GREEN = '\033[0;32m'
YELLOW = '\033[1;33m'
RED = '\033[0;31m'
BLUE = '\033[0;34m'
NC = '\033[0m'


def print_success(msg: str) -> None:
    print(f"{GREEN}✓{NC} {msg}")


def print_error(msg: str) -> None:
    print(f"{RED}✗{NC} {msg}")


def print_info(msg: str) -> None:
    print(f"{BLUE}ℹ{NC} {msg}")


def load_config(config_path: Path) -> List[Dict[str, Any]]:
    """Load submodule configuration from YAML or JSON file."""
    try:
        # Check file exists
        if not config_path.exists():
            raise FileNotFoundError(f"Configuration file not found: {config_path}")

        with open(config_path) as f:
            if config_path.suffix in ['.yml', '.yaml']:
                config = yaml.safe_load(f)
            elif config_path.suffix == '.json':
                config = json.load(f)
            else:
                raise ValueError(f"Unsupported config format: {config_path.suffix}. Use .yml, .yaml, or .json")

        # Validate config structure
        if not isinstance(config, dict):
            raise ValueError("Config file must contain a YAML/JSON object")

        if 'submodules' not in config:
            raise ValueError("Config must contain 'submodules' key with list of submodule definitions")

        if not isinstance(config['submodules'], list):
            raise ValueError("'submodules' must be a list of submodule definitions")

        return config['submodules']

    except (FileNotFoundError, ValueError, json.JSONDecodeError, yaml.YAMLError) as e:
        print_error(f"Configuration error: {e}")
        raise ValueError(f"Failed to load config from {config_path}")
    except Exception as e:
        print_error(f"Unexpected error loading config: {e}")
        raise ValueError(f"Failed to load config from {config_path}: {e}")


def setup_submodule(submodule: Dict[str, Any], dry_run: bool = False) -> bool:
    """Setup a single submodule using setup-new-submodule.py script."""
    try:
        category = submodule['category']
        name = submodule['name']
        purpose = submodule['purpose']
        visibility = submodule.get('visibility', 'public')

        print_info(f"Setting up {category}/{name}...")

        if dry_run:
            print_info(f"  [DRY RUN] Would create: {name}")
            print_info(f"  Purpose: {purpose}")
            print_info(f"  Visibility: {visibility}")
            return True

        # Call setup-new-submodule.py
        cmd = [
            sys.executable,
            '.coditect/scripts/setup-new-submodule.py',
            '--category', category,
            '--name', name,
            '--purpose', purpose,
            '--visibility', visibility
        ]

        result = subprocess.run(cmd, capture_output=True, text=True)

        if result.returncode == 0:
            print_success(f"Created {name}")
            return True
        else:
            print_error(f"Failed to create {name}")
            logger.error(f"Error output: {result.stderr}")
            return False

    except Exception as e:
        print_error(f"Exception setting up {submodule.get('name', 'unknown')}: {e}")
        return False


def main() -> int:
    """Main entry point for batch setup."""
    parser = argparse.ArgumentParser(description='Batch setup CODITECT submodules')
    parser.add_argument('--config', '-c', required=True, help='Path to configuration file (YAML/JSON)')
    parser.add_argument('--dry-run', action='store_true', help='Show what would be created without creating')
    parser.add_argument('--verbose', '-v', action='store_true', help='Verbose output')

    args = parser.parse_args()

    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)

    try:
        # Load configuration
        config_path = Path(args.config)
        if not config_path.exists():
            print_error(f"Config file not found: {config_path}")
            return 2

        print_info(f"Loading configuration from {config_path}...")
        submodules = load_config(config_path)
        print_success(f"Loaded {len(submodules)} submodule definitions")
        print()

        # Show execution plan
        print_info("Batch Setup Plan:")
        print(f"  Total submodules: {len(submodules)}")
        print()
        for i, sub in enumerate(submodules, 1):
            print(f"  {i}. {sub['category']}/{sub['name']} ({sub.get('visibility', 'public')})")
            print(f"     {sub['purpose']}")
        print()

        if args.dry_run:
            print_info("[DRY RUN] No changes will be made")
            return 0

        # Confirm
        if sys.stdin.isatty():
            confirm = input("Continue with batch setup? (y/N): ").strip().lower()
            if confirm != 'y':
                print_info("Batch setup cancelled")
                return 0

        # Execute batch setup
        successful = []
        failed = []

        for sub in submodules:
            if setup_submodule(sub, args.dry_run):
                successful.append(sub['name'])
            else:
                failed.append(sub['name'])

        # Report results
        print()
        print_info("=" * 50)
        print_info("Batch Setup Complete")
        print_info("=" * 50)
        print(f"  Total: {len(submodules)}")
        print(f"  {GREEN}Successful: {len(successful)}{NC}")
        print(f"  {RED}Failed: {len(failed)}{NC}")
        print()

        if successful:
            print_success("Successfully created:")
            for name in successful:
                print(f"    - {name}")
            print()

        if failed:
            print_error("Failed to create:")
            for name in failed:
                print(f"    - {name}")
            print()
            print_info("Retry failed submodules individually with setup-new-submodule.py")
            return 1

        return 0

    except ValueError as e:
        print_error(f"Configuration error: {e}")
        return 3
    except Exception as e:
        logger.exception("Unexpected error")
        print_error(f"Unexpected error: {e}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
