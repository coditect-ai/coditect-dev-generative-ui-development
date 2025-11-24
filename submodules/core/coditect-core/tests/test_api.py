"""
Integration tests for CODITECT REST API (Phase 2B.1)

Tests REST API endpoints for command execution.
"""

import pytest
from fastapi.testclient import TestClient

from api.main import create_app


@pytest.fixture
def client():
    """Create test client."""
    app = create_app()
    return TestClient(app)


class TestRootEndpoints:
    """Test root and health endpoints."""

    def test_root_endpoint(self, client):
        """Test root endpoint returns API information."""
        response = client.get("/")

        assert response.status_code == 200
        data = response.json()
        assert "message" in data
        assert "version" in data
        assert data["version"] == "1.0.0"

    def test_health_check(self, client):
        """Test health check endpoint."""
        response = client.get("/health")

        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"
        assert data["version"] == "1.0.0"
        assert "services" in data
        assert "timestamp" in data


class TestCommandListEndpoint:
    """Test command listing endpoint."""

    def test_list_all_commands(self, client):
        """Test listing all available commands."""
        response = client.get("/api/v1/commands")

        assert response.status_code == 200
        data = response.json()

        assert "commands" in data
        assert "total_count" in data
        assert data["total_count"] > 0
        assert len(data["commands"]) > 0

        # Check first command structure
        cmd = data["commands"][0]
        assert "name" in cmd
        assert "description" in cmd
        assert "agent_id" in cmd
        assert cmd["name"].startswith("/")

    def test_list_commands_by_category(self, client):
        """Test filtering commands by category."""
        response = client.get("/api/v1/commands?category=development")

        assert response.status_code == 200
        data = response.json()

        assert data["category_filter"] == "development"
        assert "commands" in data

        # All commands should be development category
        for cmd in data["commands"]:
            assert cmd["category"] == "development"


class TestCommandExecutionEndpoint:
    """Test command execution endpoint."""

    @pytest.mark.asyncio
    async def test_execute_simple_command(self, client):
        """Test executing a simple command."""
        request_data = {
            "command": "/analyze",
            "args": {"target": "tests/test_api.py"},
            "stream": False,
        }

        response = client.post("/api/v1/commands/execute", json=request_data)

        assert response.status_code == 200
        data = response.json()

        # Check response structure
        assert "command_id" in data
        assert "command" in data
        assert "status" in data
        assert "output" in data

        assert data["command"] == "/analyze"
        assert data["command_id"].startswith("CMD-analyze-")

    @pytest.mark.asyncio
    async def test_execute_command_with_args(self, client):
        """Test executing command with arguments."""
        request_data = {
            "command": "/analyze",
            "args": {"target": "src/main.rs", "focus": "security"},
        }

        response = client.post("/api/v1/commands/execute", json=request_data)

        assert response.status_code == 200
        data = response.json()

        assert data["command"] == "/analyze"
        assert "command_id" in data

    def test_execute_unknown_command(self, client):
        """Test executing unknown command returns error."""
        request_data = {"command": "/unknown-command"}

        response = client.post("/api/v1/commands/execute", json=request_data)

        # Should complete but with failed status
        assert response.status_code == 200
        data = response.json()

        assert data["status"] == "failed"
        assert data["error_type"] == "UnknownCommand"
        assert "Unknown command" in data["error_message"]

    def test_execute_command_missing_required_args(self, client):
        """Test executing command with missing required arguments."""
        request_data = {"command": "/implement"}  # Missing required 'description' arg

        response = client.post("/api/v1/commands/execute", json=request_data)

        # Should complete but with failed status
        assert response.status_code == 200
        data = response.json()

        assert data["status"] == "failed"
        assert data["error_type"] == "InvalidArguments"

    def test_execute_invalid_command_format(self, client):
        """Test executing command without leading slash."""
        request_data = {"command": "analyze"}  # Missing leading /

        response = client.post("/api/v1/commands/execute", json=request_data)

        # Should fail validation
        assert response.status_code == 422


class TestCommandStatusEndpoint:
    """Test command status endpoint."""

    @pytest.mark.asyncio
    async def test_get_command_status(self, client):
        """Test getting command execution status."""
        # First execute a command
        request_data = {"command": "/analyze"}
        response = client.post("/api/v1/commands/execute", json=request_data)
        assert response.status_code == 200

        command_id = response.json()["command_id"]

        # Get status
        response = client.get(f"/api/v1/commands/{command_id}/status")

        assert response.status_code == 200
        data = response.json()

        assert data["command_id"] == command_id
        assert "status" in data

    def test_get_status_nonexistent_command(self, client):
        """Test getting status for nonexistent command."""
        response = client.get("/api/v1/commands/nonexistent-id/status")

        assert response.status_code == 404


class TestCommandResultEndpoint:
    """Test command result endpoint."""

    @pytest.mark.asyncio
    async def test_get_command_result(self, client):
        """Test getting full command result."""
        # First execute a command
        request_data = {"command": "/analyze"}
        response = client.post("/api/v1/commands/execute", json=request_data)
        assert response.status_code == 200

        command_id = response.json()["command_id"]

        # Get result
        response = client.get(f"/api/v1/commands/{command_id}")

        assert response.status_code == 200
        data = response.json()

        assert data["command_id"] == command_id
        assert "command" in data
        assert "status" in data
        assert "output" in data

    def test_get_result_nonexistent_command(self, client):
        """Test getting result for nonexistent command."""
        response = client.get("/api/v1/commands/nonexistent-id")

        assert response.status_code == 404


class TestAPIErrorHandling:
    """Test API error handling."""

    def test_invalid_request_data(self, client):
        """Test sending invalid request data."""
        response = client.post("/api/v1/commands/execute", json={"invalid": "data"})

        # Should return validation error
        assert response.status_code == 422
        data = response.json()
        assert "error" in data or "detail" in data

    def test_malformed_json(self, client):
        """Test sending malformed JSON."""
        response = client.post(
            "/api/v1/commands/execute",
            data="not json",
            headers={"Content-Type": "application/json"},
        )

        # Should return validation error
        assert response.status_code == 422


class TestOpenAPIDocumentation:
    """Test OpenAPI documentation."""

    def test_openapi_schema(self, client):
        """Test OpenAPI schema is available."""
        response = client.get("/openapi.json")

        assert response.status_code == 200
        data = response.json()

        assert "openapi" in data
        assert "info" in data
        assert "paths" in data

    def test_swagger_docs(self, client):
        """Test Swagger UI is available."""
        response = client.get("/docs")

        assert response.status_code == 200
        assert "swagger" in response.text.lower() or "openapi" in response.text.lower()

    def test_redoc_docs(self, client):
        """Test ReDoc is available."""
        response = client.get("/redoc")

        assert response.status_code == 200


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
