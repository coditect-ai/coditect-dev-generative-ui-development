#!/usr/bin/env python3
"""
Unified Logging Module - Dual-Mode (Local + GCP Cloud Logging)

Automatically detects environment and configures appropriate logging backend:
- LOCAL: File-based logging with RollingLineFileHandler
- GCP: Cloud Logging with structured logs, correlation IDs, resource labels

Design principles:
1. Zero code changes between local and GCP environments
2. Structured logging with JSON format
3. Correlation IDs for distributed tracing
4. Resource labels for GKE pod metadata
5. Log-based metrics for monitoring
6. Automatic environment detection

Author: AZ1.AI INC (Hal Casteel)
Framework: CODITECT
License: MIT
"""

import os
import sys
import logging
import json
import uuid
import socket
from pathlib import Path
from typing import Dict, Any, Optional, Union
from datetime import datetime, timezone
from dataclasses import dataclass, field, asdict

# Try to import GCP Cloud Logging (optional - for cloud environments)
try:
    from google.cloud import logging as cloud_logging
    from google.cloud.logging_v2.handlers import CloudLoggingHandler
    GCP_AVAILABLE = True
except ImportError:
    GCP_AVAILABLE = False

# Import local rolling log handler
try:
    from rolling_log_handler import RollingLineFileHandler
    ROLLING_HANDLER_AVAILABLE = True
except ImportError:
    ROLLING_HANDLER_AVAILABLE = False


# ============================================================================
# ENVIRONMENT DETECTION
# ============================================================================

def detect_environment() -> str:
    """
    Detect execution environment.

    Returns:
        'gcp' if running in GCP (GKE, Cloud Run, etc.)
        'local' if running locally
    """
    # Check for GCP environment variables
    gcp_indicators = [
        'KUBERNETES_SERVICE_HOST',  # GKE
        'K_SERVICE',                 # Cloud Run
        'GAE_ENV',                   # App Engine
        'GOOGLE_CLOUD_PROJECT',      # General GCP
    ]

    for indicator in gcp_indicators:
        if os.getenv(indicator):
            return 'gcp'

    return 'local'


def get_gcp_resource_labels() -> Dict[str, str]:
    """
    Extract GCP resource labels from environment.

    Returns:
        Dictionary of resource labels for GKE pod
    """
    return {
        'project_id': os.getenv('GOOGLE_CLOUD_PROJECT', 'unknown'),
        'cluster_name': os.getenv('CLUSTER_NAME', 'unknown'),
        'namespace_name': os.getenv('NAMESPACE', 'default'),
        'pod_name': os.getenv('HOSTNAME', socket.gethostname()),
        'node_name': os.getenv('NODE_NAME', 'unknown'),
    }


# ============================================================================
# STRUCTURED LOG ENTRY
# ============================================================================

@dataclass
class StructuredLogEntry:
    """
    Structured log entry for consistent logging format.

    Compatible with both local JSON logging and GCP Cloud Logging.
    """
    message: str
    severity: str = 'INFO'
    component: str = 'unknown'
    operation: Optional[str] = None
    step: Optional[int] = None
    step_name: Optional[str] = None
    workflow_id: Optional[str] = None
    correlation_id: Optional[str] = None
    duration_ms: Optional[float] = None
    metrics: Optional[Dict[str, Any]] = None
    metadata: Optional[Dict[str, Any]] = None
    timestamp: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary, filtering None values."""
        return {k: v for k, v in asdict(self).items() if v is not None}

    def to_json(self) -> str:
        """Convert to JSON string."""
        return json.dumps(self.to_dict(), default=str)


# ============================================================================
# UNIFIED LOGGER
# ============================================================================

class UnifiedLogger:
    """
    Dual-mode logger that works in both local and GCP environments.

    Automatically detects environment and configures appropriate backend:
    - Local: RollingLineFileHandler with console output
    - GCP: Cloud Logging with structured logs

    Features:
    - Structured logging (JSON format)
    - Correlation IDs for distributed tracing
    - Resource labels (GKE pod metadata)
    - Step-based logging
    - Metrics tracking
    - Automatic environment detection
    """

    def __init__(
        self,
        component: str,
        log_file: Optional[Path] = None,
        max_lines: int = 5000,
        console_level: int = logging.INFO,
        file_level: int = logging.DEBUG,
        workflow_id: Optional[str] = None,
        force_environment: Optional[str] = None
    ):
        """
        Initialize unified logger.

        Args:
            component: Component name (e.g., 'export-dedup', 'create-checkpoint')
            log_file: Local log file path (optional, auto-generated if None)
            max_lines: Max lines for local log file rolling
            console_level: Console logging level
            file_level: File logging level
            workflow_id: Optional workflow ID for correlation
            force_environment: Force 'local' or 'gcp' (overrides auto-detection)
        """
        self.component = component
        self.workflow_id = workflow_id or str(uuid.uuid4())
        self.environment = force_environment or detect_environment()

        # Initialize base logger
        self.logger = logging.getLogger(f"{component}-{self.workflow_id[:8]}")
        self.logger.setLevel(logging.DEBUG)
        self.logger.handlers = []  # Clear existing handlers

        # Configure backend based on environment
        if self.environment == 'gcp' and GCP_AVAILABLE:
            self._configure_gcp_logging()
        else:
            self._configure_local_logging(log_file, max_lines, console_level, file_level)

        # Log initialization
        self.info(f"UnifiedLogger initialized", metadata={
            'environment': self.environment,
            'component': component,
            'workflow_id': self.workflow_id,
            'gcp_available': GCP_AVAILABLE,
            'hostname': socket.gethostname()
        })

    def _configure_local_logging(
        self,
        log_file: Optional[Path],
        max_lines: int,
        console_level: int,
        file_level: int
    ):
        """Configure local file-based logging with rolling handler."""
        # Default log file location
        if log_file is None:
            log_dir = Path.cwd() / "MEMORY-CONTEXT" / "logs"
            log_dir.mkdir(parents=True, exist_ok=True)
            log_file = log_dir / f"{self.component}.log"
        else:
            log_file = Path(log_file)
            log_file.parent.mkdir(parents=True, exist_ok=True)

        # File handler (rolling with line limit)
        if ROLLING_HANDLER_AVAILABLE:
            file_handler = RollingLineFileHandler(
                str(log_file),
                max_lines=max_lines,
                mode='a',
                encoding='utf-8'
            )
        else:
            file_handler = logging.FileHandler(str(log_file), mode='a', encoding='utf-8')

        file_handler.setLevel(file_level)
        file_formatter = logging.Formatter(
            "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S"
        )
        file_handler.setFormatter(file_formatter)
        self.logger.addHandler(file_handler)

        # Console handler
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(console_level)
        console_formatter = logging.Formatter("%(message)s")
        console_handler.setFormatter(console_formatter)
        self.logger.addHandler(console_handler)

        self.log_file = log_file

    def _configure_gcp_logging(self):
        """Configure GCP Cloud Logging with structured logs."""
        # Initialize Cloud Logging client
        self.gcp_client = cloud_logging.Client()
        self.gcp_logger = self.gcp_client.logger(self.component)

        # Add Cloud Logging handler for standard Python logging
        cloud_handler = CloudLoggingHandler(self.gcp_client, name=self.component)
        cloud_handler.setLevel(logging.DEBUG)
        self.logger.addHandler(cloud_handler)

        # Also add console handler for local debugging
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(logging.INFO)
        console_formatter = logging.Formatter("%(message)s")
        console_handler.setFormatter(console_formatter)
        self.logger.addHandler(console_handler)

        # Get resource labels
        self.resource_labels = get_gcp_resource_labels()

    def _log_structured(
        self,
        severity: str,
        message: str,
        operation: Optional[str] = None,
        step: Optional[int] = None,
        step_name: Optional[str] = None,
        correlation_id: Optional[str] = None,
        duration_ms: Optional[float] = None,
        metrics: Optional[Dict[str, Any]] = None,
        metadata: Optional[Dict[str, Any]] = None
    ):
        """
        Log structured entry.

        Works in both local (JSON to file) and GCP (Cloud Logging) modes.
        """
        # Create structured log entry
        entry = StructuredLogEntry(
            message=message,
            severity=severity,
            component=self.component,
            operation=operation,
            step=step,
            step_name=step_name,
            workflow_id=self.workflow_id,
            correlation_id=correlation_id,
            duration_ms=duration_ms,
            metrics=metrics,
            metadata=metadata
        )

        # Log to appropriate backend
        if self.environment == 'gcp' and GCP_AVAILABLE:
            # GCP Cloud Logging (structured)
            self.gcp_logger.log_struct(
                entry.to_dict(),
                severity=severity,
                resource=self._get_gcp_resource()
            )
        else:
            # Local logging (JSON string in file, plain message to console)
            log_method = getattr(self.logger, severity.lower(), self.logger.info)

            # File gets JSON structure
            json_msg = entry.to_json()
            log_method(json_msg)

    def _get_gcp_resource(self) -> Dict[str, Any]:
        """Get GCP resource for log entry."""
        return {
            "type": "k8s_pod",
            "labels": self.resource_labels
        }

    # ========================================================================
    # PUBLIC LOGGING METHODS
    # ========================================================================

    def debug(
        self,
        message: str,
        operation: Optional[str] = None,
        metadata: Optional[Dict[str, Any]] = None
    ):
        """Log DEBUG level message."""
        self._log_structured('DEBUG', message, operation=operation, metadata=metadata)

    def info(
        self,
        message: str,
        operation: Optional[str] = None,
        step: Optional[int] = None,
        metadata: Optional[Dict[str, Any]] = None
    ):
        """Log INFO level message."""
        self._log_structured('INFO', message, operation=operation, step=step, metadata=metadata)

    def warning(
        self,
        message: str,
        operation: Optional[str] = None,
        metadata: Optional[Dict[str, Any]] = None
    ):
        """Log WARNING level message."""
        self._log_structured('WARNING', message, operation=operation, metadata=metadata)

    def error(
        self,
        message: str,
        operation: Optional[str] = None,
        metadata: Optional[Dict[str, Any]] = None,
        exc_info: bool = False
    ):
        """Log ERROR level message."""
        if exc_info:
            # Add exception info to metadata
            import traceback
            metadata = metadata or {}
            metadata['exception'] = traceback.format_exc()

        self._log_structured('ERROR', message, operation=operation, metadata=metadata)

    def critical(
        self,
        message: str,
        operation: Optional[str] = None,
        metadata: Optional[Dict[str, Any]] = None
    ):
        """Log CRITICAL level message."""
        self._log_structured('CRITICAL', message, operation=operation, metadata=metadata)

    # ========================================================================
    # STEP-BASED LOGGING
    # ========================================================================

    def log_step_start(self, step: int, step_name: str) -> datetime:
        """Log the start of a workflow step."""
        start_time = datetime.now(timezone.utc)

        self._log_structured(
            'INFO',
            f"\n{'='*60}\nStep {step}: {step_name}\n{'='*60}",
            operation='step_start',
            step=step,
            step_name=step_name,
            metadata={'start_time': start_time.isoformat()}
        )

        return start_time

    def log_step_success(self, step: int, step_name: str, start_time: datetime):
        """Log successful completion of a step."""
        duration = (datetime.now(timezone.utc) - start_time).total_seconds()

        self._log_structured(
            'INFO',
            f"✅ Step {step} complete: {step_name} ({duration:.2f}s)",
            operation='step_complete',
            step=step,
            step_name=step_name,
            duration_ms=duration * 1000,
            metadata={'success': True}
        )

    def log_step_error(self, step: int, step_name: str, error: Exception):
        """Log step failure with error details."""
        import traceback

        self._log_structured(
            'ERROR',
            f"❌ Step {step} failed: {step_name}",
            operation='step_failed',
            step=step,
            step_name=step_name,
            metadata={
                'success': False,
                'error_type': type(error).__name__,
                'error_message': str(error),
                'traceback': traceback.format_exc()
            }
        )

    def log_checkpoint(self, message: str):
        """Log a checkpoint (verification point) in the workflow."""
        self._log_structured(
            'DEBUG',
            f"✓ CHECKPOINT: {message}",
            operation='checkpoint'
        )

    def log_verification_success(self, what: str, details: str):
        """Log successful verification."""
        self._log_structured(
            'INFO',
            f"  ✓ Verified: {what}",
            operation='verification',
            metadata={'what': what, 'details': details, 'success': True}
        )

    def log_verification_failure(self, what: str, details: str):
        """Log verification failure."""
        self._log_structured(
            'ERROR',
            f"  ✗ Verification failed: {what}",
            operation='verification',
            metadata={'what': what, 'details': details, 'success': False}
        )

    # ========================================================================
    # METRICS LOGGING
    # ========================================================================

    def log_metrics(
        self,
        operation: str,
        metrics: Dict[str, Union[int, float]],
        metadata: Optional[Dict[str, Any]] = None
    ):
        """
        Log metrics for monitoring and alerting.

        In GCP, these become log-based metrics.
        In local mode, these are logged as JSON for later analysis.

        Args:
            operation: Operation name (e.g., 'deduplicate', 'git_staging')
            metrics: Dictionary of metric name -> value
            metadata: Additional metadata
        """
        self._log_structured(
            'INFO',
            f"📊 Metrics: {operation}",
            operation=operation,
            metrics=metrics,
            metadata=metadata
        )

    # ========================================================================
    # GIT OPERATIONS LOGGING
    # ========================================================================

    def log_git_operation(
        self,
        command: str,
        cwd: str,
        exit_code: int,
        output: str,
        duration_ms: float
    ):
        """Log git command execution with full details."""
        success = (exit_code == 0)
        severity = 'INFO' if success else 'ERROR'

        self._log_structured(
            severity,
            f"Git: {command}",
            operation='git_command',
            duration_ms=duration_ms,
            metadata={
                'command': command,
                'cwd': cwd,
                'exit_code': exit_code,
                'output': output[:500] if output else '',  # Truncate long output
                'success': success
            }
        )

    # ========================================================================
    # CORRELATION & TRACING
    # ========================================================================

    def create_child_logger(self, operation: str) -> 'UnifiedLogger':
        """
        Create child logger with same workflow ID for distributed tracing.

        Args:
            operation: Operation name for the child logger

        Returns:
            New UnifiedLogger with correlation to parent
        """
        return UnifiedLogger(
            component=f"{self.component}.{operation}",
            workflow_id=self.workflow_id,
            force_environment=self.environment
        )

    def get_correlation_id(self) -> str:
        """Get correlation ID for this logger (workflow_id)."""
        return self.workflow_id


# ============================================================================
# CONVENIENCE FUNCTIONS
# ============================================================================

def setup_unified_logger(
    component: str,
    log_file: Optional[Path] = None,
    max_lines: int = 5000,
    console_level: int = logging.INFO,
    file_level: int = logging.DEBUG,
    workflow_id: Optional[str] = None
) -> UnifiedLogger:
    """
    Setup unified logger with automatic environment detection.

    Args:
        component: Component name
        log_file: Local log file path (optional)
        max_lines: Max lines for local log rolling
        console_level: Console logging level
        file_level: File logging level
        workflow_id: Optional workflow ID

    Returns:
        Configured UnifiedLogger instance
    """
    return UnifiedLogger(
        component=component,
        log_file=log_file,
        max_lines=max_lines,
        console_level=console_level,
        file_level=file_level,
        workflow_id=workflow_id
    )


# ============================================================================
# TESTING
# ============================================================================

if __name__ == "__main__":
    """Test unified logger in both local and GCP modes."""

    print("\n" + "=" * 80)
    print("Testing Unified Logger")
    print("=" * 80)

    # Test local mode
    print("\n1. Testing LOCAL mode:")
    print("-" * 80)

    logger_local = UnifiedLogger(
        component="test-component",
        force_environment="local"
    )

    logger_local.info("Test info message", operation="test_op", metadata={'key': 'value'})
    logger_local.debug("Test debug message", metadata={'debug_key': 'debug_value'})
    logger_local.warning("Test warning message")
    logger_local.error("Test error message", metadata={'error_code': 500})

    # Test step logging
    step_start = logger_local.log_step_start(1, "Test Step")
    logger_local.log_checkpoint("Checkpoint within step")
    logger_local.log_verification_success("File exists", "test.txt found")
    logger_local.log_step_success(1, "Test Step", step_start)

    # Test metrics logging
    logger_local.log_metrics(
        "test_operation",
        metrics={
            'files_processed': 42,
            'duration_seconds': 1.23,
            'success_rate': 95.5
        },
        metadata={'batch_id': 'batch-123'}
    )

    print(f"\n✅ Local logging test complete")
    print(f"   Log file: {logger_local.log_file}")

    # Test GCP mode (if available)
    if GCP_AVAILABLE:
        print("\n2. Testing GCP mode:")
        print("-" * 80)
        print("⚠️  GCP mode available but requires credentials")
        print("   Set GOOGLE_APPLICATION_CREDENTIALS to test")
    else:
        print("\n2. Testing GCP mode:")
        print("-" * 80)
        print("ℹ️  GCP mode not available (google-cloud-logging not installed)")
        print("   Install with: pip install google-cloud-logging")

    print("\n" + "=" * 80)
    print("✅ Unified Logger Test Complete")
    print("=" * 80 + "\n")
