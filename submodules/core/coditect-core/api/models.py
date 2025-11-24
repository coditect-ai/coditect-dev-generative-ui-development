"""
API Data Models

Pydantic models for request/response validation and serialization.
"""

from datetime import datetime
from typing import Optional, Dict, Any, List
from pydantic import BaseModel, Field, validator


class CommandRequest(BaseModel):
    """Request to execute a slash command."""

    command: str = Field(
        ...,
        description="Slash command to execute (e.g., '/analyze', '/implement')",
        example="/analyze",
    )
    args: Optional[Dict[str, Any]] = Field(
        default=None,
        description="Optional arguments for the command",
        example={"target": "src/main.rs", "focus": "security"},
    )
    stream: bool = Field(
        default=False,
        description="Enable streaming results via WebSocket",
    )

    @validator("command")
    def validate_command_format(cls, v):
        """Ensure command starts with /."""
        if not v.startswith("/"):
            raise ValueError("Command must start with '/'")
        return v

    class Config:
        json_schema_extra = {
            "example": {
                "command": "/analyze",
                "args": {"target": "src/main.rs", "focus": "security"},
                "stream": False,
            }
        }


class CommandResponse(BaseModel):
    """Response from command execution."""

    command_id: str = Field(
        ...,
        description="Unique identifier for this command execution",
        example="CMD-analyze-20241123-153045",
    )
    command: str = Field(..., description="Command that was executed")
    status: str = Field(
        ...,
        description="Execution status: success, failed, partial, pending",
        example="success",
    )
    output: str = Field(..., description="Command output text")

    # Optional execution metadata
    agent_used: Optional[str] = Field(None, example="code-reviewer")
    llm_provider: Optional[str] = Field(None, example="anthropic-claude")
    llm_model: Optional[str] = Field(None, example="claude-3-5-haiku-20241022")

    # Timing
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    execution_time_seconds: Optional[float] = Field(None, example=2.45)

    # Resource usage
    tokens_used: Optional[int] = Field(None, example=1250)
    estimated_cost: Optional[float] = Field(None, example=0.0032)

    # Structured data (command-specific)
    structured_data: Optional[Dict[str, Any]] = Field(default_factory=dict)

    # Error information
    error_message: Optional[str] = None
    error_type: Optional[str] = None

    # Metadata
    metadata: Optional[Dict[str, Any]] = Field(default_factory=dict)

    @property
    def success(self) -> bool:
        """Check if command succeeded."""
        return self.status == "success"

    @property
    def cost_formatted(self) -> str:
        """Format cost as currency string."""
        if self.estimated_cost is None:
            return "N/A"
        return f"${self.estimated_cost:.4f}"

    class Config:
        json_schema_extra = {
            "example": {
                "command_id": "CMD-analyze-20241123-153045",
                "command": "/analyze",
                "status": "success",
                "output": "Analysis complete. Code quality: 8.5/10",
                "agent_used": "code-reviewer",
                "llm_provider": "anthropic-claude",
                "llm_model": "claude-3-5-haiku-20241022",
                "execution_time_seconds": 2.45,
                "tokens_used": 1250,
                "estimated_cost": 0.0032,
            }
        }


class CommandStatusResponse(BaseModel):
    """Response for command status check."""

    command_id: str
    status: str
    progress: Optional[float] = Field(
        None, description="Progress percentage (0-100)", ge=0, le=100
    )
    current_step: Optional[str] = None
    started_at: Optional[datetime] = None
    estimated_completion: Optional[datetime] = None

    class Config:
        json_schema_extra = {
            "example": {
                "command_id": "CMD-implement-20241123-153050",
                "status": "pending",
                "progress": 35.5,
                "current_step": "Generating code structure",
                "started_at": "2024-11-23T15:30:50",
                "estimated_completion": "2024-11-23T15:32:30",
            }
        }


class CommandListItem(BaseModel):
    """Item in command list response."""

    name: str = Field(..., description="Command name", example="/analyze")
    description: str = Field(
        ..., description="Command description", example="Analyze code quality"
    )
    agent_id: str = Field(
        ..., description="Agent that handles this command", example="code-reviewer"
    )
    category: Optional[str] = Field(None, example="development")
    required_args: List[str] = Field(default_factory=list)
    optional_args: List[str] = Field(default_factory=list)
    examples: List[str] = Field(default_factory=list)

    class Config:
        json_schema_extra = {
            "example": {
                "name": "/analyze",
                "description": "Analyze code quality, security, and performance",
                "agent_id": "code-reviewer",
                "category": "development",
                "required_args": [],
                "optional_args": ["target", "focus", "depth"],
                "examples": ["/analyze", "/analyze target=src/main.rs focus=security"],
            }
        }


class CommandListResponse(BaseModel):
    """Response for listing available commands."""

    commands: List[CommandListItem]
    total_count: int = Field(..., description="Total number of commands available")
    category_filter: Optional[str] = Field(
        None, description="Category filter applied (if any)"
    )

    class Config:
        json_schema_extra = {
            "example": {
                "commands": [
                    {
                        "name": "/analyze",
                        "description": "Analyze code quality",
                        "agent_id": "code-reviewer",
                        "category": "development",
                    }
                ],
                "total_count": 7,
                "category_filter": None,
            }
        }


class APIKeyRequest(BaseModel):
    """Request to generate a new API key."""

    name: str = Field(
        ...,
        description="Friendly name for the API key",
        example="Production Deployment Bot",
    )
    expires_in_days: Optional[int] = Field(
        None, description="Expiration in days (None = never expires)", example=90
    )
    rate_limit_tier: str = Field(
        default="standard",
        description="Rate limit tier: free, standard, premium",
        example="standard",
    )

    @validator("rate_limit_tier")
    def validate_tier(cls, v):
        """Validate rate limit tier."""
        allowed = ["free", "standard", "premium"]
        if v not in allowed:
            raise ValueError(f"rate_limit_tier must be one of: {allowed}")
        return v

    class Config:
        json_schema_extra = {
            "example": {
                "name": "Production Deployment Bot",
                "expires_in_days": 90,
                "rate_limit_tier": "standard",
            }
        }


class APIKeyResponse(BaseModel):
    """Response with newly generated API key."""

    api_key: str = Field(..., description="The generated API key (save this!)")
    key_id: str = Field(..., description="Unique identifier for this key")
    name: str = Field(..., description="Friendly name")
    created_at: datetime
    expires_at: Optional[datetime] = None
    rate_limit_tier: str

    class Config:
        json_schema_extra = {
            "example": {
                "api_key": "cdt_sk_abc123def456...",
                "key_id": "key_xyz789",
                "name": "Production Deployment Bot",
                "created_at": "2024-11-23T15:30:00",
                "expires_at": "2025-02-21T15:30:00",
                "rate_limit_tier": "standard",
            }
        }


class ErrorResponse(BaseModel):
    """Standard error response."""

    error: str = Field(..., description="Error type")
    message: str = Field(..., description="Error message")
    details: Optional[Dict[str, Any]] = Field(
        default=None, description="Additional error details"
    )
    request_id: Optional[str] = Field(None, description="Request ID for tracking")

    class Config:
        json_schema_extra = {
            "example": {
                "error": "InvalidArguments",
                "message": "Missing required argument: description",
                "details": {"missing_args": ["description"]},
                "request_id": "req_abc123",
            }
        }


class HealthResponse(BaseModel):
    """Health check response."""

    status: str = Field(..., description="Service status", example="healthy")
    version: str = Field(..., description="API version", example="1.0.0")
    timestamp: datetime = Field(..., description="Current server time")
    services: Dict[str, str] = Field(
        ...,
        description="Status of dependent services",
        example={"database": "healthy", "llm_providers": "healthy", "redis": "healthy"},
    )

    class Config:
        json_schema_extra = {
            "example": {
                "status": "healthy",
                "version": "1.0.0",
                "timestamp": "2024-11-23T15:30:00",
                "services": {
                    "llm_providers": "healthy",
                    "redis": "healthy",
                },
            }
        }
