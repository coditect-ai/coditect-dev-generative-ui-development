#!/usr/bin/env python3
"""
Rolling Log Handler with Line-Based Trimming

Maintains a log file with a maximum of 5000 lines. When the limit is reached,
the oldest lines (from the head) are removed to make room for new entries.

This ensures the log file never grows unbounded while preserving the most
recent information for debugging and auditing.

Author: AZ1.AI INC (Hal Casteel)
Framework: CODITECT
License: MIT
"""

import logging
from pathlib import Path
from collections import deque
from threading import Lock
from typing import Optional


class RollingLineFileHandler(logging.FileHandler):
    """
    Custom file handler that maintains a maximum number of lines.

    When the line limit is reached, the oldest lines are trimmed from the head
    of the file, keeping only the most recent lines.
    """

    def __init__(
        self,
        filename: str,
        max_lines: int = 5000,
        mode: str = 'a',
        encoding: Optional[str] = 'utf-8',
        delay: bool = False
    ):
        """
        Initialize rolling line file handler.

        Args:
            filename: Path to log file
            max_lines: Maximum number of lines to keep (default: 5000)
            mode: File mode (default: 'a' for append)
            encoding: File encoding (default: 'utf-8')
            delay: Delay file opening until first emit
        """
        super().__init__(filename, mode, encoding, delay)
        self.max_lines = max_lines
        self.line_count = 0
        self.trim_lock = Lock()
        self.trim_threshold = int(max_lines * 0.9)  # Trim at 90% to avoid constant trimming

        # Count existing lines on initialization
        if Path(filename).exists():
            try:
                with open(filename, 'r', encoding=encoding) as f:
                    self.line_count = sum(1 for _ in f)
            except:
                self.line_count = 0

    def emit(self, record):
        """
        Emit a record, trimming old lines if necessary.

        Args:
            record: LogRecord to emit
        """
        # Emit the record using parent class
        super().emit(record)

        # Increment line count
        self.line_count += 1

        # Check if trimming is needed
        # Only trim when we exceed max_lines (not at threshold)
        if self.line_count > self.max_lines:
            self._trim_old_lines()

    def _trim_old_lines(self):
        """
        Trim old lines from the head of the file.

        Keeps only the most recent (max_lines * 0.8) lines to provide a buffer
        before the next trim is needed.
        """
        with self.trim_lock:
            try:
                # Flush any pending writes
                if hasattr(self.stream, 'flush'):
                    self.stream.flush()

                # Close the file handle temporarily
                self.stream.close()

                # Read all lines
                with open(self.baseFilename, 'r', encoding=self.encoding) as f:
                    lines = f.readlines()

                # Calculate how many lines to keep (80% of max to provide buffer)
                lines_to_keep = int(self.max_lines * 0.8)

                if len(lines) > lines_to_keep:
                    # Keep only the most recent lines
                    kept_lines = lines[-lines_to_keep:]

                    # Add trim indicator at the top
                    trim_marker = (
                        f"=" * 80 + "\n"
                        f"[LOG TRIMMED - Removed {len(lines) - lines_to_keep} oldest lines]\n"
                        f"[Keeping most recent {lines_to_keep} of {len(lines)} total lines]\n"
                        f"[Max capacity: {self.max_lines} lines]\n"
                        f"=" * 80 + "\n"
                    )

                    # Write back the kept lines with marker
                    with open(self.baseFilename, 'w', encoding=self.encoding) as f:
                        f.write(trim_marker)
                        f.writelines(kept_lines)

                    # Update line count (5 lines for marker + kept lines)
                    self.line_count = 5 + len(kept_lines)
                else:
                    # No trimming needed, just reset count to actual line count
                    self.line_count = len(lines)

                # Reopen the file handle in append mode
                self.stream = self._open()

            except Exception as e:
                # If trimming fails, log to stderr and continue
                import sys
                print(f"Warning: Failed to trim log file: {e}", file=sys.stderr)
                try:
                    # Try to reopen the stream
                    self.stream = self._open()
                except:
                    pass


def setup_rolling_logger(
    log_file: Path,
    logger_name: str = "export_dedup",
    max_lines: int = 5000,
    console_level: int = logging.INFO,
    file_level: int = logging.DEBUG
) -> logging.Logger:
    """
    Setup a logger with rolling file handler and console output.

    Args:
        log_file: Path to log file
        logger_name: Name of the logger
        max_lines: Maximum lines in log file
        console_level: Console logging level
        file_level: File logging level

    Returns:
        Configured logger instance
    """
    # Ensure log directory exists
    log_file.parent.mkdir(parents=True, exist_ok=True)

    # Create logger
    logger = logging.getLogger(logger_name)
    logger.setLevel(logging.DEBUG)

    # Remove existing handlers to avoid duplicates
    logger.handlers = []

    # Rolling file handler - detailed logs with line limit
    file_handler = RollingLineFileHandler(
        str(log_file),
        max_lines=max_lines,
        mode='a',
        encoding='utf-8'
    )
    file_handler.setLevel(file_level)
    file_formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )
    file_handler.setFormatter(file_formatter)
    logger.addHandler(file_handler)

    # Console handler - user-friendly output
    console_handler = logging.StreamHandler()
    console_handler.setLevel(console_level)
    console_formatter = logging.Formatter("%(message)s")
    console_handler.setFormatter(console_formatter)
    logger.addHandler(console_handler)

    logger.info(f"Rolling log initialized: {log_file} (max {max_lines} lines)")
    logger.debug(f"File log level: {logging.getLevelName(file_level)}")
    logger.debug(f"Console log level: {logging.getLevelName(console_level)}")

    return logger


if __name__ == "__main__":
    """Test the rolling log handler"""
    import tempfile
    from pathlib import Path

    # Create temporary log file
    with tempfile.TemporaryDirectory() as tmpdir:
        log_file = Path(tmpdir) / "test_rolling.log"

        # Setup logger with small max_lines for testing
        logger = setup_rolling_logger(log_file, max_lines=20)

        # Write 30 lines to trigger trimming
        print("\n" + "=" * 60)
        print("Testing Rolling Log Handler")
        print("=" * 60)
        print(f"Log file: {log_file}")
        print(f"Writing 30 log entries (max 20 lines)...\n")

        for i in range(1, 31):
            logger.info(f"Test log entry {i}")
            if i % 10 == 0:
                logger.debug(f"Debug info at entry {i}")

        # Read final log to verify trimming
        print("\n" + "=" * 60)
        print("Final log contents:")
        print("=" * 60)
        with open(log_file, 'r') as f:
            content = f.read()
            print(content)

        line_count = len(content.splitlines())
        print("=" * 60)
        print(f"Final line count: {line_count}")
        print("Expected: ~16-20 lines (trimmed from 30)")
        print("=" * 60)
