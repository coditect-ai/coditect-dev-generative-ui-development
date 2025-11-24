"""
CODITECT REST API - Main Application

FastAPI application for programmatic command execution.

Run with:
    uvicorn api.main:app --reload --host 0.0.0.0 --port 8000
"""

import asyncio
import logging
from contextlib import asynccontextmanager
from datetime import datetime
from typing import Optional, List
from uuid import uuid4

from fastapi import (
    FastAPI,
    HTTPException,
    Depends,
    status,
    Request,
    Query,
)
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError

from .models import (
    CommandRequest,
    CommandResponse,
    CommandStatusResponse,
    CommandListResponse,
    CommandListItem,
    ErrorResponse,
    HealthResponse,
)

# Import orchestration components
from orchestration import (
    get_command_router,
    SlashCommandRouter,
    CommandResult,
    CommandStatus,
)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


# Application state
class AppState:
    """Application state container."""

    def __init__(self):
        self.router: Optional[SlashCommandRouter] = None
        self.active_commands: dict = {}  # command_id -> CommandResult


app_state = AppState()


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan manager."""
    # Startup
    logger.info("Starting CODITECT REST API...")
    app_state.router = get_command_router()
    logger.info("Command router initialized")
    yield
    # Shutdown
    logger.info("Shutting down CODITECT REST API...")


# Create FastAPI application
def create_app() -> FastAPI:
    """Create and configure FastAPI application."""

    app = FastAPI(
        title="CODITECT REST API",
        description="Programmatic access to CODITECT slash commands",
        version="1.0.0",
        docs_url="/docs",
        redoc_url="/redoc",
        lifespan=lifespan,
    )

    # CORS middleware
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],  # Configure appropriately for production
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Exception handlers
    @app.exception_handler(RequestValidationError)
    async def validation_exception_handler(request: Request, exc: RequestValidationError):
        """Handle request validation errors."""
        return JSONResponse(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            content={
                "error": "ValidationError",
                "message": "Invalid request data",
                "details": exc.errors(),
            },
        )

    @app.exception_handler(Exception)
    async def general_exception_handler(request: Request, exc: Exception):
        """Handle general exceptions."""
        logger.error(f"Unhandled exception: {exc}", exc_info=True)
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={
                "error": "InternalServerError",
                "message": "An unexpected error occurred",
                "details": {"error_type": type(exc).__name__},
            },
        )

    # Routes
    @app.get("/", tags=["root"])
    async def root():
        """Root endpoint."""
        return {
            "message": "CODITECT REST API",
            "version": "1.0.0",
            "docs": "/docs",
            "health": "/health",
        }

    @app.get("/health", response_model=HealthResponse, tags=["health"])
    async def health_check():
        """Health check endpoint."""
        return HealthResponse(
            status="healthy",
            version="1.0.0",
            timestamp=datetime.now(),
            services={
                "llm_providers": "healthy",
                "command_router": "healthy" if app_state.router else "unhealthy",
            },
        )

    @app.get(
        "/api/v1/commands",
        response_model=CommandListResponse,
        tags=["commands"],
        summary="List available commands",
        description="Get a list of all available slash commands with their specifications.",
    )
    async def list_commands(
        category: Optional[str] = Query(
            None, description="Filter commands by category (e.g., 'development')"
        )
    ):
        """List available slash commands."""
        if not app_state.router:
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail="Command router not initialized",
            )

        # Get commands from router
        command_specs = app_state.router.list_commands(category=category)

        # Convert to response format
        commands = [
            CommandListItem(
                name=spec.name,
                description=spec.description,
                agent_id=spec.agent_id,
                category=spec.category,
                required_args=spec.required_args or [],
                optional_args=spec.optional_args or [],
                examples=spec.examples or [],
            )
            for spec in command_specs
        ]

        return CommandListResponse(
            commands=commands,
            total_count=len(commands),
            category_filter=category,
        )

    @app.post(
        "/api/v1/commands/execute",
        response_model=CommandResponse,
        tags=["commands"],
        summary="Execute a slash command",
        description="Execute a slash command and return structured results.",
        status_code=status.HTTP_200_OK,
    )
    async def execute_command(request: CommandRequest):
        """Execute a slash command."""
        if not app_state.router:
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail="Command router not initialized",
            )

        # Generate command ID
        command_id = f"CMD-{request.command.lstrip('/')}-{datetime.now().strftime('%Y%m%d-%H%M%S')}-{uuid4().hex[:8]}"

        logger.info(f"Executing command {command_id}: {request.command}")

        try:
            # Execute command via router
            result: CommandResult = await app_state.router.execute(
                command_str=request.command,
                args=request.args,
            )

            # Store result
            app_state.active_commands[command_id] = result

            # Convert to response format
            response = CommandResponse(
                command_id=command_id,
                command=result.command,
                status=result.status.value,
                output=result.output or "",
                agent_used=result.agent_used,
                llm_provider=result.llm_provider,
                llm_model=result.llm_model,
                started_at=result.started_at,
                completed_at=result.completed_at,
                execution_time_seconds=result.execution_time_seconds,
                tokens_used=result.tokens_used,
                estimated_cost=result.estimated_cost,
                structured_data=result.structured_data or {},
                error_message=result.error_message,
                error_type=result.error_type,
                metadata=result.metadata or {},
            )

            logger.info(
                f"Command {command_id} completed with status: {result.status.value}"
            )

            return response

        except Exception as e:
            logger.error(f"Error executing command {command_id}: {e}", exc_info=True)
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail={
                    "error": "ExecutionError",
                    "message": str(e),
                    "command_id": command_id,
                },
            )

    @app.get(
        "/api/v1/commands/{command_id}/status",
        response_model=CommandStatusResponse,
        tags=["commands"],
        summary="Get command execution status",
        description="Check the status of a command execution by its ID.",
    )
    async def get_command_status(command_id: str):
        """Get command execution status."""
        # Check if command exists in active commands
        if command_id not in app_state.active_commands:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Command {command_id} not found",
            )

        result = app_state.active_commands[command_id]

        return CommandStatusResponse(
            command_id=command_id,
            status=result.status.value,
            progress=100.0 if result.status == CommandStatus.SUCCESS else None,
            current_step="Completed" if result.status == CommandStatus.SUCCESS else None,
            started_at=result.started_at,
            estimated_completion=result.completed_at,
        )

    @app.get(
        "/api/v1/commands/{command_id}",
        response_model=CommandResponse,
        tags=["commands"],
        summary="Get command execution result",
        description="Get the full result of a command execution by its ID.",
    )
    async def get_command_result(command_id: str):
        """Get full command execution result."""
        if command_id not in app_state.active_commands:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Command {command_id} not found",
            )

        result = app_state.active_commands[command_id]

        return CommandResponse(
            command_id=command_id,
            command=result.command,
            status=result.status.value,
            output=result.output or "",
            agent_used=result.agent_used,
            llm_provider=result.llm_provider,
            llm_model=result.llm_model,
            started_at=result.started_at,
            completed_at=result.completed_at,
            execution_time_seconds=result.execution_time_seconds,
            tokens_used=result.tokens_used,
            estimated_cost=result.estimated_cost,
            structured_data=result.structured_data or {},
            error_message=result.error_message,
            error_type=result.error_type,
            metadata=result.metadata or {},
        )

    return app


# Create application instance
app = create_app()


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "api.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info",
    )
