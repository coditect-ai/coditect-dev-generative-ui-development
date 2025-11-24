# CODITECT Slash Commands Reference

| Command | Description | Purpose |
|---------|-------------|---------|
| /action | Implementation mode - emits working code in persistent artifacts | Execute implementation tasks with code output in single artifact to prevent state explosion |
| /agent-dispatcher | Intelligent agent selection and invocation syntax generator | Help select and invoke the appropriate specialized agent for a given task |
| /ai_review | AI-Powered Code Review Specialist | Perform AI-assisted code review with quality analysis |
| /analyze | Code review and analysis mode | Evaluate code quality, security, performance, and provide actionable feedback |
| /c4-methodology-skill | C4 Methodology Skill - Enterprise Software Architecture Visualization | Create C4 architecture diagrams (Context, Container, Component, Code) |
| /ci_commit | Commit Changes | Create git commits with conventional commit format |
| /ci_describe_pr | Generate PR Description | Generate pull request descriptions with summary and test plan |
| /code_explain | Code Explanation and Analysis | Explain how code works with detailed analysis |
| /COMMAND-GUIDE | Command Selection Guide | Provide guidance on which command to use for specific tasks |
| /commit | Commit Changes | Standard git commit workflow with message generation |
| /complexity_gauge | Complexity Gauge: Token Budget and Workflow Complexity Monitor | Monitor token usage and workflow complexity for optimization |
| /component_scaffold | React/React Native Component Scaffolding | Generate React/React Native component boilerplate |
| /config_validate | Configuration Validation | Validate configuration files for correctness |
| /context_restore | Context Restoration: Advanced Semantic Memory Rehydration | Restore session context from previous work |
| /context_save | Context Save Tool: Intelligent Context Management Specialist | Save current session context for future restoration |
| /create_handoff | Create Handoff | Create handoff document for session continuity |
| /create_plan | Implementation Plan | Generate detailed implementation plan for features |
| /create_plan_generic | Implementation Plan | Generic implementation plan generation |
| /create_plan_nt | Implementation Plan | No-todo implementation plan variant |
| /create_worktree | Set up worktree for implementation | Create git worktree for isolated implementation work |
| /db_migrations | SQL database migrations with zero-downtime strategies | Design and execute database migrations for PostgreSQL, MySQL, SQL Server |
| /db-performance-analyzer | Database Performance Analyzer Command | Analyze database performance and optimization opportunities |
| /debug | Debug | Debug code issues and errors |
| /deliberation | Pure planning mode - NO code execution | Analyze and plan without executing code, focus on requirements and decomposition |
| /describe_pr | Generate PR Description | Create pull request description with changes summary |
| /doc_generate | Automated Documentation Generation | Generate comprehensive documentation automatically |
| /document | Documentation generation mode | Create API docs, architecture diagrams, runbooks, and user guides |
| /error_analysis | Error Analysis and Resolution | Analyze errors and provide resolution strategies |
| /error_trace | Error Tracking and Monitoring | Track and monitor error patterns |
| /feature_development | Orchestrate end-to-end feature development | Manage complete feature lifecycle from requirements to deployment |
| /founder_mode | Experimental feature development | Work on experimental features without formal ticketing |
| /full_review | Orchestrate comprehensive multi-dimensional code review | Coordinate multiple review agents for thorough code analysis |
| /generate-curriculum-content | Generate comprehensive AI curriculum content | Create multi-level educational content with NotebookLM optimization |
| /hello | A simple hello world command for testing and demonstration. | For testing and demonstration |
| /implement | Production-ready implementation mode | Build production code with error handling, circuit breakers, observability, and tests |
| /implement_plan | Implement Plan | Execute implementation based on existing plan |
| /incident_response | Orchestrate multi-agent incident response with modern SRE practices | Coordinate incident response with rapid resolution strategies |
| /intent-classification-skill | Intent Classification Skill - Smart Research Automation | Classify user intent for intelligent research automation |
| /linear | Linear - Ticket Management | Interact with Linear issue tracking system |
| /local_review | Local Review | Perform local code review before committing |
| /monitor_setup | Monitoring and Observability Setup | Set up monitoring, logging, and observability infrastructure |
| /multi-agent-research | Execute comprehensive multi-agent competitive research workflow | Coordinate multiple agents for comprehensive research tasks |
| /oneshot | Use SlashCommand() to call /ralph_research with ticket number | Single-command workflow for research phase |
| /oneshot_plan | Use SlashCommand() to call /ralph_plan with ticket number | Single-command workflow for planning phase |
| /optimize | Performance optimization mode | Analyze and improve performance, scalability, and resource usage |
| /pr_enhance | Pull Request Enhancement | Enhance pull request with better descriptions and context |
| /prototype | Rapid prototyping mode | Build quick proof-of-concept with focus on core functionality |
| /python_scaffold | Python Project Scaffolding | Generate Python project structure and boilerplate |
| /ralph_impl | PART I - IF A TICKET IS MENTIONED | Ralph implementation workflow triggered by ticket mention |
| /ralph_plan | PART I - IF A TICKET IS MENTIONED | Ralph planning workflow triggered by ticket mention |
| /ralph_research | PART I - IF A LINEAR TICKET IS MENTIONED | Ralph research workflow triggered by Linear ticket mention |
| /README | Custom Commands Directory | Access custom commands directory information |
| /recursive_workflow | Recursive Workflow Manager: FSM-Based Multi-Phase Resolution | Manage complex multi-phase workflows with finite state machine |
| /refactor_clean | Refactor and Clean Code | Refactor code for better quality and maintainability |
| /research | Verification mode | Execute focused verification of assumptions and technical choices |
| /research_codebase | Research Codebase | Research and understand codebase structure and patterns |
| /research_codebase_generic | Research Codebase | Generic codebase research variant |
| /research_codebase_nt | Research Codebase | No-todo codebase research variant |
| /resume_handoff | Resume work from a handoff document | Continue work from previous session using handoff |
| /rust_scaffold | Rust Project Scaffolding | Generate Rust project structure and boilerplate |
| /security_deps | Dependency Vulnerability Scanning | Scan dependencies for security vulnerabilities |
| /security_hardening | Implement comprehensive security hardening | Apply defense-in-depth security strategies |
| /security_sast | Static Application Security Testing (SAST) | Analyze code for security vulnerabilities across multiple languages |
| /slo_implement | SLO Implementation Guide | Implement Service Level Objectives and monitoring |
| /smart_debug | Expert AI-assisted debugging specialist | Debug with deep knowledge of modern debugging tools |
| /smart-research | Smart Research - Intelligent Market Research Automation | Automated intelligent market research workflows |
| /strategy | Architectural planning and system design mode | Create C4 diagrams, multi-agent coordination analysis, and ADRs |
| /suggest-agent | Generate correct agent invocation syntax | Get proper syntax for invoking specialized agents |
| /tdd_cycle | Execute comprehensive Test-Driven Development workflow | Follow strict red-green-refactor TDD discipline |
| /tech_debt | Technical Debt Analysis and Remediation | Analyze and remediate technical debt |
| /test_generate | Automated Unit Test Generation | Generate comprehensive unit tests automatically |
| /typescript_scaffold | TypeScript Project Scaffolding | Generate TypeScript project structure and boilerplate |
| /validate_plan | Validate Plan | Review and validate implementation plans |

---

**Total Commands:** 73

**Usage:** Type `/` in Claude Code to see available commands, or use specific commands for targeted workflows.

**Categories:**
- **Planning & Strategy:** /deliberation, /strategy, /create_plan, /validate_plan
- **Implementation:** /implement, /action, /prototype, /feature_development
- **Code Review:** /analyze, /ai_review, /full_review, /local_review
- **Testing & Quality:** /test_generate, /tdd_cycle, /security_sast
- **Documentation:** /document, /doc_generate
- **Research:** /research, /research_codebase, /multi-agent-research, /smart-research
- **Scaffolding:** /python_scaffold, /rust_scaffold, /typescript_scaffold, /component_scaffold
- **Database:** /db_migrations, /db-performance-analyzer
- **DevOps:** /monitor_setup, /slo_implement
- **Security:** /security_deps, /security_hardening, /security_sast
- **Workflow:** /ralph_research, /ralph_plan, /ralph_impl, /oneshot, /oneshot_plan
- **Context Management:** /context_save, /context_restore, /create_handoff, /resume_handoff
- **Git/Version Control:** /commit, /ci_commit, /describe_pr, /ci_describe_pr, /pr_enhance
