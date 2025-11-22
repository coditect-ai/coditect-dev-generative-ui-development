#!/usr/bin/env python3
"""
C4 Diagram Generator

Generates C4 architecture diagrams (Context, Container, Component, Code) from codebase analysis.
"""

from enum import Enum
from typing import List, Dict, Optional
from dataclasses import dataclass


class C4Level(Enum):
    """C4 model levels"""
    CONTEXT = 1  # System boundary and external actors
    CONTAINER = 2  # Major components and tech stack
    COMPONENT = 3  # Internal structure of containers
    CODE = 4  # Class/function level details


@dataclass
class Actor:
    """External actor (user, system)"""
    name: str
    type: str  # "Person" or "System"
    description: str


@dataclass
class Container:
    """Deployable unit (web app, API, database)"""
    name: str
    technology: str
    description: str
    port: Optional[int] = None


@dataclass
class Component:
    """Internal component (handler, service, repository)"""
    name: str
    type: str  # "Handler", "Service", "Repository", etc.
    description: str
    dependencies: List[str] = None


@dataclass
class Relationship:
    """Relationship between elements"""
    from_element: str
    to_element: str
    description: str
    protocol: Optional[str] = None


class C4DiagramGenerator:
    """Generate C4 architecture diagrams in Mermaid format"""

    def generate_context_diagram(
        self,
        system_name: str,
        system_description: str,
        actors: List[Actor],
        external_systems: List[Actor],
        relationships: List[Relationship]
    ) -> str:
        """
        Generate Level 1: Context diagram.

        Args:
            system_name: Main system name
            system_description: What the system does
            actors: List of users/actors
            external_systems: External systems interacting with main system
            relationships: How actors/systems interact

        Returns:
            Mermaid diagram string
        """
        lines = ["```mermaid", "graph TB"]

        # Define actors
        for actor in actors:
            lines.append(f"    {actor.name}[{actor.name}<br/>{actor.description}]")

        # Define main system
        lines.append(f"    {system_name.replace(' ', '')}[{system_name}<br/>{system_description}]")

        # Define external systems
        for ext in external_systems:
            lines.append(f"    {ext.name.replace(' ', '')}[{ext.name}<br/>{ext.description}]")

        # Add blank line before relationships
        lines.append("")

        # Define relationships
        for rel in relationships:
            from_node = rel.from_element.replace(' ', '')
            to_node = rel.to_element.replace(' ', '')
            protocol = f" ({rel.protocol})" if rel.protocol else ""
            lines.append(f"    {from_node} -->|{rel.description}{protocol}| {to_node}")

        # Styling
        lines.append("")
        lines.append(f"    style {system_name.replace(' ', '')} fill:#1168bd,color:#fff")
        for actor in actors:
            lines.append(f"    style {actor.name} fill:#08427b,color:#fff")

        lines.append("```")
        return "\n".join(lines)

    def generate_container_diagram(
        self,
        system_name: str,
        containers: List[Container],
        external_systems: List[Container],
        relationships: List[Relationship]
    ) -> str:
        """
        Generate Level 2: Container diagram.

        Args:
            system_name: Main system name
            containers: List of containers in the system
            external_systems: External databases, services, etc.
            relationships: How containers communicate

        Returns:
            Mermaid diagram string
        """
        lines = ["```mermaid", "graph TB"]

        # Define system boundary
        lines.append(f'    subgraph "{system_name}"')

        for container in containers:
            port_str = f"<br/>Port {container.port}" if container.port else ""
            lines.append(
                f"        {container.name.replace(' ', '')}[{container.name}<br/>"
                f"{container.technology}{port_str}<br/>{container.description}]"
            )

        lines.append("    end")
        lines.append("")

        # Define external systems
        for ext in external_systems:
            port_str = f"<br/>Port {ext.port}" if ext.port else ""
            if "Database" in ext.type or "database" in ext.name.lower():
                lines.append(
                    f"    {ext.name.replace(' ', '')}[({ext.name}<br/>"
                    f"{ext.technology}{port_str})]"
                )
            else:
                lines.append(
                    f"    {ext.name.replace(' ', '')}[{ext.name}<br/>"
                    f"{ext.technology}{port_str}]"
                )

        lines.append("")

        # Define relationships
        for rel in relationships:
            from_node = rel.from_element.replace(' ', '')
            to_node = rel.to_element.replace(' ', '')
            protocol = rel.protocol or "HTTP"
            lines.append(f"    {from_node} -->|{protocol}| {to_node}")

        # Styling
        lines.append("")
        for container in containers:
            lines.append(f"    style {container.name.replace(' ', '')} fill:#1168bd,color:#fff")

        lines.append("```")
        return "\n".join(lines)

    def generate_component_diagram(
        self,
        container_name: str,
        components: List[Component],
        relationships: List[Relationship]
    ) -> str:
        """
        Generate Level 3: Component diagram.

        Args:
            container_name: Name of the container being detailed
            components: List of components within the container
            relationships: How components interact

        Returns:
            Mermaid diagram string
        """
        lines = ["```mermaid", "graph TB"]

        # Define container boundary
        lines.append(f'    subgraph "{container_name}"')

        for comp in components:
            lines.append(
                f"        {comp.name.replace(' ', '')}[{comp.name}<br/>{comp.description}]"
            )

        lines.append("    end")
        lines.append("")

        # Define relationships
        for rel in relationships:
            from_node = rel.from_element.replace(' ', '')
            to_node = rel.to_element.replace(' ', '')
            lines.append(f"    {from_node} --> {to_node}")

        # Styling
        lines.append("")
        for comp in components:
            lines.append(f"    style {comp.name.replace(' ', '')} fill:#1168bd,color:#fff")

        lines.append("```")
        return "\n".join(lines)

    def generate_t2_context_diagram(self) -> str:
        """Generate T2 project context diagram"""
        return self.generate_context_diagram(
            system_name="Coditect AI IDE",
            system_description="Multi-LLM Browser IDE",
            actors=[
                Actor("User", "Person", "End User"),
                Actor("Admin", "Person", "System Administrator"),
            ],
            external_systems=[
                Actor("LM Studio", "System", "Local LLM Inference"),
                Actor("FoundationDB", "System", "Persistent Storage"),
            ],
            relationships=[
                Relationship("User", "Coditect AI IDE", "Uses", "HTTPS"),
                Relationship("Admin", "Coditect AI IDE", "Manages", "HTTPS"),
                Relationship("Coditect AI IDE", "LM Studio", "Queries", "OpenAI API"),
                Relationship("Coditect AI IDE", "FoundationDB", "Persists", "FDB Client"),
            ]
        )

    def generate_t2_container_diagram(self) -> str:
        """Generate T2 project container diagram"""
        return self.generate_container_diagram(
            system_name="Coditect AI IDE (T2)",
            containers=[
                Container("Frontend", "React + Vite", "User interface", 5173),
                Container("Theia IDE", "Eclipse Theia 1.65", "Code editor", 3000),
                Container("Backend API", "Rust + Actix-web", "API server", 8080),
                Container("Orchestrator", "Multi-agent system", "Agent coordinator"),
            ],
            external_systems=[
                Container("FoundationDB", "FDB 7.1+", "Database", 4500),
                Container("LM Studio", "Local LLM", "AI inference", 1234),
            ],
            relationships=[
                Relationship("Frontend", "Backend API", "HTTP/WebSocket"),
                Relationship("Theia IDE", "Orchestrator", "MCP/A2A"),
                Relationship("Orchestrator", "Backend API", "REST"),
                Relationship("Backend API", "FoundationDB", "FDB Client"),
                Relationship("Orchestrator", "LM Studio", "OpenAI API"),
            ]
        )

    def generate_t2_backend_component_diagram(self) -> str:
        """Generate T2 backend component diagram"""
        return self.generate_component_diagram(
            container_name="Backend API (Rust)",
            components=[
                Component("Auth Handler", "Handler", "Login, Logout, Refresh"),
                Component("Session Handler", "Handler", "Create, Validate, Invalidate"),
                Component("Auth Middleware", "Middleware", "JWT Validation"),
                Component("FDB Service", "Service", "Connection Pool"),
                Component("User Repository", "Repository", "User CRUD"),
                Component("Session Repository", "Repository", "Session Management"),
            ],
            relationships=[
                Relationship("Auth Handler", "User Repository", "Uses"),
                Relationship("Auth Handler", "Session Repository", "Uses"),
                Relationship("Session Handler", "Session Repository", "Uses"),
                Relationship("Auth Middleware", "Session Repository", "Uses"),
                Relationship("User Repository", "FDB Service", "Uses"),
                Relationship("Session Repository", "FDB Service", "Uses"),
            ]
        )


def main():
    """Example usage"""
    generator = C4DiagramGenerator()

    print("=== C4 Diagram Generator ===\n")

    # Generate T2 diagrams
    print("1. CONTEXT DIAGRAM (Level 1)")
    print("-" * 60)
    print(generator.generate_t2_context_diagram())
    print()

    print("\n2. CONTAINER DIAGRAM (Level 2)")
    print("-" * 60)
    print(generator.generate_t2_container_diagram())
    print()

    print("\n3. COMPONENT DIAGRAM (Level 3 - Backend)")
    print("-" * 60)
    print(generator.generate_t2_backend_component_diagram())
    print()


if __name__ == "__main__":
    main()
