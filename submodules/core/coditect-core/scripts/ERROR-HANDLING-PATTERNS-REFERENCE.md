# Error Handling Patterns Reference

**Quick reference guide for implementing production-grade error handling in CODITECT scripts**

---

## Table of Contents

1. [Exception Hierarchy Template](#exception-hierarchy-template)
2. [Logging Configuration](#logging-configuration)
3. [Function Error Handling](#function-error-handling)
4. [main() Function Pattern](#main-function-pattern)
5. [Git Rollback Pattern](#git-rollback-pattern)
6. [Input Validation Pattern](#input-validation-pattern)
7. [Network Resilience Pattern](#network-resilience-pattern)
8. [Exit Codes](#exit-codes)

---

## Exception Hierarchy Template

```python
# Custom Exceptions
class ScriptNameError(Exception):
    """Base exception for script-name errors"""
    pass


class SpecificError1(ScriptNameError):
    """Raised when specific scenario 1 occurs"""
    pass


class SpecificError2(ScriptNameError):
    """Raised when specific scenario 2 occurs"""
    pass


# Add 4-6 specific exceptions per script based on failure modes
```

**Usage:**
```python
try:
    dangerous_operation()
except SomeLibraryError as e:
    logger.error(f"Operation failed: {str(e)}")
    raise SpecificError1(f"Could not complete operation: {str(e)}")
```

---

## Logging Configuration

```python
import logging

# Configure logging at module level (after imports)
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler('script-name.log')
    ]
)
logger = logging.getLogger(__name__)
```

**Usage throughout script:**
```python
logger.debug("Detailed debug information")
logger.info("High-level status information")
logger.warning("Warning about potential issue")
logger.error(f"Error occurred: {error_details}")
logger.exception("Error with full stack trace")  # Use in except blocks
```

---

## Function Error Handling

### Pattern for Regular Functions

```python
def function_name(param1, param2, required_param=None):
    """Function description.

    Args:
        param1: Description
        param2: Description
        required_param: Optional parameter

    Returns:
        Return value description

    Raises:
        SpecificError1: When condition 1 occurs
        SpecificError2: When condition 2 occurs
    """
    # Input validation
    if not param1:
        logger.error("param1 is required")
        raise ValueError("param1 cannot be None or empty")

    if not isinstance(param2, expected_type):
        logger.error(f"param2 has wrong type: {type(param2)}")
        raise TypeError(f"param2 must be {expected_type}, got {type(param2)}")

    # Main logic with error handling
    try:
        logger.debug(f"Processing {param1}...")

        # Potentially failing operation
        result = dangerous_operation(param1, param2)

        logger.info(f"Successfully processed {param1}")
        return result

    except ExpectedError as e:
        logger.error(f"Expected error during processing: {str(e)}")
        raise SpecificError1(f"Failed to process {param1}: {str(e)}")

    except Exception as e:
        logger.exception(f"Unexpected error during processing")
        raise SpecificError2(f"Unexpected error processing {param1}: {str(e)}")
```

### Pattern for Functions with Cleanup

```python
def function_with_resources():
    """Function that allocates resources requiring cleanup."""
    resource = None

    try:
        # Allocate resource
        resource = allocate_resource()
        logger.debug("Resource allocated")

        # Use resource
        result = use_resource(resource)

        return result

    except Exception as e:
        logger.error(f"Error using resource: {str(e)}")
        raise

    finally:
        # Always cleanup
        if resource:
            try:
                cleanup_resource(resource)
                logger.debug("Resource cleaned up")
            except Exception as e:
                logger.warning(f"Failed to cleanup resource: {str(e)}")
```

---

## main() Function Pattern

```python
def main():
    """Main entry point with comprehensive error handling."""
    created_resources = []  # Track for cleanup
    result_data = None

    try:
        logger.info("Starting script execution")

        # Step 1: Validation
        try:
            validate_prerequisites()
            logger.info("Prerequisites validated")
        except PrerequisiteError as e:
            logger.error(f"Prerequisites failed: {str(e)}")
            print_error(f"Prerequisites not met: {str(e)}")
            print_info("Please install required tools and retry.")
            return 1

        # Step 2: Get user input (with cancellation handling)
        try:
            user_input = get_user_input()
            logger.info(f"User input collected: {user_input}")
        except (KeyboardInterrupt, EOFError):
            logger.info("User cancelled input")
            print_warning("Operation cancelled by user")
            return 130

        # Step 3: Process with resource tracking
        try:
            logger.info("Creating resource 1")
            resource1 = create_resource_1()
            created_resources.append(('resource1', resource1))

            logger.info("Creating resource 2")
            resource2 = create_resource_2(resource1)
            created_resources.append(('resource2', resource2))

            logger.info("Processing complete")
            return 0

        except SpecificError1 as e:
            logger.error(f"Resource creation failed: {str(e)}")
            print_error(f"Failed to create resources: {str(e)}")
            print_info("Next steps: ...")
            return 1

        except SpecificError2 as e:
            logger.error(f"Processing failed: {str(e)}")
            print_error(f"Processing failed: {str(e)}")
            print_info("You may need to manually clean up resources.")
            return 1

    except KeyboardInterrupt:
        logger.info("Script interrupted by user (Ctrl+C)")
        print_warning("\nOperation interrupted by user")

        # Show partial completion
        if created_resources:
            print_info(f"Partially created: {len(created_resources)} resources")
            for name, resource in created_resources:
                print_info(f"  - {name}: {resource}")

        return 130

    except Exception as e:
        logger.exception("Unexpected error in main")
        print_error(f"Unexpected error: {str(e)}")
        print_info("Check log file for details: script-name.log")

        # Show created resources for manual cleanup
        if created_resources:
            print_info(f"Created resources (may need cleanup):")
            for name, resource in created_resources:
                print_info(f"  - {name}: {resource}")

        return 1


if __name__ == "__main__":
    try:
        exit_code = main()
        sys.exit(exit_code)
    except Exception as e:
        logger.exception("Fatal error in entry point")
        print(f"Fatal error: {str(e)}")
        sys.exit(1)
```

---

## Git Rollback Pattern

**Use for scripts that modify git state (commits, pushes, etc.)**

```python
class GitTransaction:
    """Context manager for atomic git operations with rollback."""

    def __init__(self, repo_path):
        self.repo_path = repo_path
        self.initial_head = None
        self.initial_branch = None
        self.staged_files = []
        self.committed = False

    def __enter__(self):
        """Capture initial git state."""
        try:
            # Get current HEAD
            result = subprocess.run(
                ['git', 'rev-parse', 'HEAD'],
                cwd=self.repo_path,
                capture_output=True,
                text=True,
                check=True
            )
            self.initial_head = result.stdout.strip()

            # Get current branch
            result = subprocess.run(
                ['git', 'rev-parse', '--abbrev-ref', 'HEAD'],
                cwd=self.repo_path,
                capture_output=True,
                text=True,
                check=True
            )
            self.initial_branch = result.stdout.strip()

            logger.debug(f"Git transaction started: {self.initial_head} on {self.initial_branch}")
            return self

        except subprocess.CalledProcessError as e:
            logger.error(f"Failed to capture initial git state: {e.stderr}")
            raise GitOperationError("Cannot start git transaction")

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Rollback on failure, validate on success."""
        if exc_type and not self.committed:
            # Exception occurred and we haven't committed - rollback
            logger.warning(f"Rolling back git changes due to {exc_type.__name__}: {exc_val}")
            self._rollback()
            return False  # Re-raise exception

        if self.committed:
            logger.info("Git transaction committed successfully")

        return False  # Always re-raise exceptions

    def _rollback(self):
        """Rollback to initial state."""
        try:
            # Reset to initial HEAD
            subprocess.run(
                ['git', 'reset', '--hard', self.initial_head],
                cwd=self.repo_path,
                capture_output=True,
                text=True,
                check=True
            )

            # Checkout initial branch if changed
            subprocess.run(
                ['git', 'checkout', self.initial_branch],
                cwd=self.repo_path,
                capture_output=True,
                text=True,
                check=True
            )

            logger.info(f"Successfully rolled back to {self.initial_head}")

        except subprocess.CalledProcessError as e:
            logger.error(f"CRITICAL: Rollback failed: {e.stderr}")
            logger.error("Manual intervention required!")
            raise GitOperationError(f"Rollback failed: {e.stderr}")

    def mark_committed(self):
        """Mark transaction as successfully committed."""
        self.committed = True


# Usage
def commit_changes(repo_path, message):
    """Commit changes with automatic rollback on failure."""
    with GitTransaction(repo_path) as transaction:
        try:
            # Stage files
            subprocess.run(
                ['git', 'add', '.'],
                cwd=repo_path,
                check=True,
                capture_output=True
            )

            # Commit
            subprocess.run(
                ['git', 'commit', '-m', message],
                cwd=repo_path,
                check=True,
                capture_output=True
            )

            # Mark as successful
            transaction.mark_committed()
            logger.info("Changes committed successfully")

        except subprocess.CalledProcessError as e:
            # Transaction will rollback automatically
            logger.error(f"Commit failed: {e.stderr}")
            raise GitOperationError(f"Failed to commit changes: {e.stderr}")
```

---

## Input Validation Pattern

```python
def validate_path_input(path_str: str, must_exist: bool = False) -> Path:
    """Validate and sanitize path input.

    Args:
        path_str: Path string from user
        must_exist: Whether path must already exist

    Returns:
        Validated Path object

    Raises:
        ValueError: If path is invalid
    """
    # Check not empty
    if not path_str or not path_str.strip():
        raise ValueError("Path cannot be empty")

    # Expand user home directory
    path_str = os.path.expanduser(path_str.strip())

    # Convert to absolute path
    try:
        path = Path(path_str).resolve()
    except Exception as e:
        raise ValueError(f"Invalid path: {str(e)}")

    # Check if must exist
    if must_exist and not path.exists():
        raise ValueError(f"Path does not exist: {path}")

    # Security: Prevent path traversal
    # (Add additional checks based on your security requirements)

    logger.debug(f"Validated path: {path}")
    return path


def validate_string_input(value: str, min_length: int = 1, max_length: int = 1000,
                         allowed_chars: str = None) -> str:
    """Validate and sanitize string input.

    Args:
        value: String from user
        min_length: Minimum allowed length
        max_length: Maximum allowed length
        allowed_chars: Regex pattern for allowed characters

    Returns:
        Validated string

    Raises:
        ValueError: If string is invalid
    """
    # Check type
    if not isinstance(value, str):
        raise ValueError(f"Expected string, got {type(value)}")

    # Strip whitespace
    value = value.strip()

    # Check length
    if len(value) < min_length:
        raise ValueError(f"String too short (min {min_length} chars)")

    if len(value) > max_length:
        raise ValueError(f"String too long (max {max_length} chars)")

    # Check allowed characters
    if allowed_chars:
        import re
        if not re.match(allowed_chars, value):
            raise ValueError(f"String contains invalid characters")

    return value


def validate_choice(value: str, choices: List[str]) -> str:
    """Validate choice from a list.

    Args:
        value: User's choice
        choices: List of valid choices

    Returns:
        Validated choice

    Raises:
        ValueError: If choice is invalid
    """
    value = value.strip().lower()

    if value not in [c.lower() for c in choices]:
        raise ValueError(f"Invalid choice. Must be one of: {', '.join(choices)}")

    # Return original case from choices list
    choice_map = {c.lower(): c for c in choices}
    return choice_map[value]
```

---

## Network Resilience Pattern

```python
import time
import random
from typing import Callable, Any

def retry_with_backoff(
    func: Callable,
    max_retries: int = 3,
    initial_delay: float = 1.0,
    backoff_factor: float = 2.0,
    jitter: bool = True,
    exceptions: tuple = (Exception,)
) -> Any:
    """Execute function with exponential backoff retry.

    Args:
        func: Function to execute
        max_retries: Maximum number of retry attempts
        initial_delay: Initial delay in seconds
        backoff_factor: Multiplier for each retry
        jitter: Add random jitter to prevent thundering herd
        exceptions: Tuple of exceptions to catch and retry

    Returns:
        Function result

    Raises:
        Last exception after all retries exhausted
    """
    delay = initial_delay
    last_exception = None

    for attempt in range(max_retries + 1):
        try:
            return func()

        except exceptions as e:
            last_exception = e

            if attempt == max_retries:
                logger.error(f"All {max_retries + 1} attempts failed")
                raise

            # Calculate delay with optional jitter
            if jitter:
                actual_delay = delay * (0.5 + random.random())
            else:
                actual_delay = delay

            logger.warning(
                f"Attempt {attempt + 1}/{max_retries + 1} failed: {str(e)}. "
                f"Retrying in {actual_delay:.2f}s..."
            )

            time.sleep(actual_delay)
            delay *= backoff_factor

    # Should never reach here, but just in case
    raise last_exception


# Usage example
def fetch_from_github():
    """Fetch data from GitHub with retry logic."""
    def _fetch():
        # Actual network operation
        result = subprocess.run(
            ['gh', 'repo', 'view', 'owner/repo'],
            capture_output=True,
            text=True,
            check=True,
            timeout=30
        )
        return result.stdout

    try:
        return retry_with_backoff(
            _fetch,
            max_retries=3,
            initial_delay=1.0,
            backoff_factor=2.0,
            exceptions=(subprocess.CalledProcessError, subprocess.TimeoutExpired)
        )
    except subprocess.CalledProcessError as e:
        logger.error(f"GitHub operation failed after retries: {e.stderr}")
        raise NetworkError(f"Failed to fetch from GitHub: {e.stderr}")
```

---

## Exit Codes

**Standard exit codes for all CODITECT scripts:**

```python
# Exit codes (standard)
EXIT_SUCCESS = 0           # Successful completion
EXIT_FAILURE = 1           # General failure
EXIT_USER_CANCEL = 130     # User cancelled (Ctrl+C, input cancellation)
EXIT_INVALID_ARGS = 2      # Invalid command-line arguments
EXIT_PREREQUISITE_FAIL = 3 # Prerequisites not met
EXIT_PERMISSION_DENIED = 4 # Permission denied
EXIT_NOT_FOUND = 5         # Required file/resource not found
```

**Usage:**
```python
# At end of main()
logger.info("Script completed successfully")
return EXIT_SUCCESS

# On user cancellation
logger.info("User cancelled operation")
print_warning("Operation cancelled")
return EXIT_USER_CANCEL

# On failure
logger.error("Script failed")
return EXIT_FAILURE
```

---

## Complete Example Script

```python
#!/usr/bin/env python3
"""
Example CODITECT Script with Production Error Handling

Demonstrates all error handling patterns.
"""

import os
import sys
import logging
import subprocess
from pathlib import Path
from typing import Optional

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler('example-script.log')
    ]
)
logger = logging.getLogger(__name__)


# Custom Exceptions
class ScriptError(Exception):
    """Base exception for script errors"""
    pass


class ValidationError(ScriptError):
    """Raised when validation fails"""
    pass


class ProcessingError(ScriptError):
    """Raised when processing fails"""
    pass


def validate_input(value: str) -> str:
    """Validate input with comprehensive checks."""
    if not value or not value.strip():
        raise ValidationError("Input cannot be empty")

    if len(value) > 1000:
        raise ValidationError("Input too long (max 1000 characters)")

    return value.strip()


def process_data(data: str) -> dict:
    """Process data with error handling."""
    try:
        logger.info(f"Processing {len(data)} characters of data")

        # Simulate processing
        result = {
            'status': 'success',
            'data': data.upper(),
            'length': len(data)
        }

        logger.info("Processing completed successfully")
        return result

    except Exception as e:
        logger.exception("Processing failed")
        raise ProcessingError(f"Failed to process data: {str(e)}")


def main():
    """Main entry point with comprehensive error handling."""
    try:
        logger.info("Script started")

        # Get input
        try:
            user_input = input("Enter data: ")
            validated = validate_input(user_input)
        except (KeyboardInterrupt, EOFError):
            logger.info("User cancelled input")
            print("Operation cancelled")
            return 130
        except ValidationError as e:
            logger.error(f"Validation failed: {str(e)}")
            print(f"Invalid input: {str(e)}")
            return 1

        # Process
        try:
            result = process_data(validated)
            print(f"Result: {result}")
            return 0

        except ProcessingError as e:
            logger.error(f"Processing failed: {str(e)}")
            print(f"Processing failed: {str(e)}")
            return 1

    except KeyboardInterrupt:
        logger.info("Script interrupted by user")
        print("\nOperation interrupted")
        return 130

    except Exception as e:
        logger.exception("Unexpected error")
        print(f"Unexpected error: {str(e)}")
        print("Check log file for details: example-script.log")
        return 1


if __name__ == "__main__":
    try:
        exit_code = main()
        sys.exit(exit_code)
    except Exception as e:
        logger.exception("Fatal error")
        print(f"Fatal error: {str(e)}")
        sys.exit(1)
```

---

## Checklist for Adding Error Handling

Use this checklist when enhancing a script:

- [ ] Add custom exception hierarchy (4-6 exceptions)
- [ ] Configure logging (stdout + file)
- [ ] Add input validation to all user-facing functions
- [ ] Wrap subprocess calls with timeout and error handling
- [ ] Add try/except to all major functions
- [ ] Implement resource cleanup in finally blocks
- [ ] Add git rollback logic if script modifies git state
- [ ] Add network retry logic for all network operations
- [ ] Handle KeyboardInterrupt gracefully
- [ ] Handle EOFError for non-interactive environments
- [ ] Track created resources for cleanup guidance
- [ ] Return standard exit codes
- [ ] Log all errors with context
- [ ] Provide user-friendly error messages with next steps
- [ ] Test all error scenarios

---

**Generated:** 2025-11-22
**For:** CODITECT Core Script Error Handling Enhancement
**Status:** Reference Implementation Guide
