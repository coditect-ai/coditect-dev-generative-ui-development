# coditect-ops-estimation-engine - Production Directory Structure

## Overview

**Type:** Python calculation engine + REST API + CLI tool + Documentation
**Purpose:** Evidence-based software estimation with industry-standard methodologies
**Framework:** FastAPI (API), Click/Typer (CLI), SQLite (persistence), pytest (testing)

---

## Complete Directory Structure

```
coditect-ops-estimation-engine/
│
├── .coditect -> ../../core/coditect-core          # Distributed intelligence symlink
├── .claude -> .coditect                           # Claude Code compatibility symlink
│
├── README.md                                      # User-facing project overview
├── CLAUDE.md                                      # AI agent operational guidelines
├── PROJECT-PLAN.md                                # Complete implementation roadmap
├── TASKLIST.md                                    # Checkbox-based progress tracking
│
├── pyproject.toml                                 # Modern Python project config (PEP 518)
├── setup.py                                       # Fallback for pip install -e .
├── requirements.txt                               # Production dependencies
├── requirements-dev.txt                           # Development dependencies
├── .python-version                                # Python version specification (3.10+)
│
├── .env.example                                   # Environment variables template
├── .gitignore                                     # Git ignore patterns
├── .dockerignore                                  # Docker ignore patterns
│
├── LICENSE                                        # Apache 2.0 license
├── CONTRIBUTING.md                                # Development guidelines
├── CHANGELOG.md                                   # Version history
├── CODE_OF_CONDUCT.md                             # Community standards
│
├── Dockerfile                                     # Multi-stage production build
├── docker-compose.yml                             # Local development environment
├── Makefile                                       # Common development tasks
│
│
├── src/
│   └── estimation_engine/
│       │
│       ├── __init__.py                            # Package initialization, version
│       ├── __main__.py                            # Entry point for python -m estimation_engine
│       ├── config.py                              # Configuration management (env vars, defaults)
│       ├── exceptions.py                          # Custom exceptions
│       ├── constants.py                           # Global constants (COCOMO coefficients, etc.)
│       │
│       ├── calculators/                           # Estimation methodologies
│       │   ├── __init__.py
│       │   ├── base.py                            # Abstract base calculator class
│       │   ├── cocomo.py                          # COCOMO II (Constructive Cost Model)
│       │   ├── cocomo_intermediate.py             # COCOMO Intermediate (cost drivers)
│       │   ├── function_points.py                 # Function Point Analysis (FPA)
│       │   ├── use_case_points.py                 # Use Case Points (UCP)
│       │   ├── bottom_up.py                       # Bottom-up estimation
│       │   ├── three_point.py                     # Three-point PERT estimation
│       │   ├── analogous.py                       # Analogous (top-down) estimation
│       │   ├── planning_poker.py                  # Planning poker simulation
│       │   └── monte_carlo.py                     # Monte Carlo simulation
│       │
│       ├── analyzers/                             # Codebase analysis tools
│       │   ├── __init__.py
│       │   ├── base.py                            # Abstract base analyzer
│       │   ├── loc_counter.py                     # Lines of Code counter (with language detection)
│       │   ├── complexity_analyzer.py             # Cyclomatic complexity, cognitive complexity
│       │   ├── dependency_analyzer.py             # Dependency graph analysis
│       │   ├── file_type_analyzer.py              # File type distribution
│       │   ├── git_history_analyzer.py            # Git commit history analysis
│       │   └── codebase_scanner.py                # Orchestrator for all analyzers
│       │
│       ├── models/                                # Data models (Pydantic)
│       │   ├── __init__.py
│       │   ├── project.py                         # Project metadata
│       │   ├── estimate.py                        # Estimation results
│       │   ├── actual.py                          # Actual project metrics
│       │   ├── comparison.py                      # Estimate vs Actual comparison
│       │   ├── codebase_metrics.py                # Codebase analysis results
│       │   ├── historical_data.py                 # Historical project data
│       │   └── validation.py                      # Input validation schemas
│       │
│       ├── database/                              # Database layer
│       │   ├── __init__.py
│       │   ├── connection.py                      # SQLite connection manager
│       │   ├── models.py                          # SQLAlchemy ORM models
│       │   ├── migrations/                        # Alembic migrations
│       │   │   ├── env.py
│       │   │   ├── script.py.mako
│       │   │   └── versions/
│       │   │       └── 001_initial_schema.py
│       │   ├── repositories/                      # Repository pattern
│       │   │   ├── __init__.py
│       │   │   ├── base.py                        # Abstract repository
│       │   │   ├── project_repository.py
│       │   │   ├── estimate_repository.py
│       │   │   └── metrics_repository.py
│       │   └── seeds/                             # Sample data
│       │       ├── sample_projects.json
│       │       └── historical_benchmarks.json
│       │
│       ├── api/                                   # FastAPI REST API
│       │   ├── __init__.py
│       │   ├── app.py                             # FastAPI application factory
│       │   ├── dependencies.py                    # Dependency injection
│       │   ├── middleware.py                      # Custom middleware
│       │   ├── routes/                            # API endpoints
│       │   │   ├── __init__.py
│       │   │   ├── health.py                      # Health check endpoint
│       │   │   ├── estimates.py                   # POST /estimates, GET /estimates/{id}
│       │   │   ├── projects.py                    # CRUD for projects
│       │   │   ├── analysis.py                    # POST /analysis (analyze codebase)
│       │   │   ├── comparison.py                  # GET /comparison (estimate vs actual)
│       │   │   └── methodologies.py               # GET /methodologies (list available)
│       │   └── schemas/                           # Request/Response schemas
│       │       ├── __init__.py
│       │       ├── estimate_request.py
│       │       ├── estimate_response.py
│       │       ├── analysis_request.py
│       │       └── analysis_response.py
│       │
│       ├── cli/                                   # Command-line interface
│       │   ├── __init__.py
│       │   ├── main.py                            # CLI entry point (Click/Typer app)
│       │   ├── commands/                          # CLI command groups
│       │   │   ├── __init__.py
│       │   │   ├── estimate.py                    # estimate <method> [options]
│       │   │   ├── analyze.py                     # analyze <path> [options]
│       │   │   ├── compare.py                     # compare <estimate_id> <actual_id>
│       │   │   ├── import_data.py                 # import <file> [--format csv|json]
│       │   │   ├── export.py                      # export <id> [--format csv|json|pdf]
│       │   │   └── benchmark.py                   # benchmark [--methodology]
│       │   └── utils/                             # CLI utilities
│       │       ├── __init__.py
│       │       ├── formatters.py                  # Table/chart formatting
│       │       ├── validators.py                  # Input validation
│       │       └── prompts.py                     # Interactive prompts
│       │
│       ├── utils/                                 # Shared utilities
│       │   ├── __init__.py
│       │   ├── math_helpers.py                    # Statistical functions
│       │   ├── file_helpers.py                    # File I/O utilities
│       │   ├── date_helpers.py                    # Date/time utilities
│       │   ├── validators.py                      # Common validators
│       │   ├── formatters.py                      # Output formatters
│       │   └── logger.py                          # Logging configuration
│       │
│       └── exports/                               # Export formats
│           ├── __init__.py
│           ├── base.py                            # Abstract exporter
│           ├── csv_exporter.py                    # CSV export
│           ├── json_exporter.py                   # JSON export
│           ├── pdf_exporter.py                    # PDF report generation
│           └── excel_exporter.py                  # Excel spreadsheet export
│
│
├── docs/                                          # Comprehensive documentation
│   │
│   ├── README.md                                  # Documentation index
│   ├── ARCHITECTURE.md                            # System architecture overview
│   ├── API.md                                     # API documentation (auto-generated)
│   ├── CLI.md                                     # CLI usage guide
│   ├── DEVELOPMENT.md                             # Developer setup guide
│   ├── DEPLOYMENT.md                              # Deployment guide
│   │
│   ├── methodologies/                             # Estimation methodology explanations
│   │   ├── README.md                              # Methodology overview
│   │   ├── cocomo-ii.md                           # COCOMO II explained
│   │   ├── function-points.md                     # FPA explained
│   │   ├── use-case-points.md                     # UCP explained
│   │   ├── three-point-estimation.md              # PERT explained
│   │   ├── analogous-estimation.md                # Top-down explained
│   │   ├── bottom-up-estimation.md                # Bottom-up explained
│   │   ├── planning-poker.md                      # Planning poker explained
│   │   ├── monte-carlo.md                         # Monte Carlo explained
│   │   └── comparison-matrix.md                   # When to use each method
│   │
│   ├── guides/                                    # User guides
│   │   ├── quickstart.md                          # 5-minute quickstart
│   │   ├── estimating-new-project.md              # How to estimate a new project
│   │   ├── analyzing-codebase.md                  # How to analyze existing code
│   │   ├── importing-historical-data.md           # Import past projects
│   │   ├── comparing-estimates.md                 # Estimate vs actual analysis
│   │   ├── calibrating-models.md                  # Customize coefficients
│   │   └── best-practices.md                      # Estimation best practices
│   │
│   ├── api/                                       # API reference
│   │   ├── README.md                              # API overview
│   │   ├── authentication.md                      # Auth (if applicable)
│   │   ├── endpoints.md                           # All endpoints (auto-generated)
│   │   ├── schemas.md                             # Request/response schemas
│   │   └── examples.md                            # cURL/Python examples
│   │
│   ├── examples/                                  # Real-world examples
│   │   ├── README.md                              # Examples index
│   │   ├── web-application-estimate.md            # Example: Web app estimation
│   │   ├── mobile-app-estimate.md                 # Example: Mobile app estimation
│   │   ├── api-service-estimate.md                # Example: API service estimation
│   │   ├── legacy-migration-estimate.md           # Example: Legacy migration
│   │   └── microservices-estimate.md              # Example: Microservices architecture
│   │
│   ├── research/                                  # Research and validation
│   │   ├── README.md                              # Research overview
│   │   ├── cocomo-validation.md                   # COCOMO accuracy studies
│   │   ├── industry-benchmarks.md                 # Industry data sources
│   │   ├── citations.md                           # Academic citations
│   │   └── accuracy-analysis.md                   # Model accuracy comparisons
│   │
│   └── diagrams/                                  # Architecture diagrams
│       ├── system-context.md                      # C4 Level 1 (Mermaid)
│       ├── container-diagram.md                   # C4 Level 2 (Mermaid)
│       ├── component-diagram.md                   # C4 Level 3 (Mermaid)
│       ├── estimation-flow.md                     # Estimation workflow
│       └── data-model.md                          # Database ERD
│
│
├── tests/                                         # Comprehensive test suite
│   │
│   ├── __init__.py
│   ├── conftest.py                                # pytest fixtures and configuration
│   │
│   ├── unit/                                      # Unit tests
│   │   ├── __init__.py
│   │   ├── calculators/
│   │   │   ├── test_cocomo.py                     # Test COCOMO calculations
│   │   │   ├── test_function_points.py
│   │   │   ├── test_use_case_points.py
│   │   │   ├── test_three_point.py
│   │   │   └── test_monte_carlo.py
│   │   ├── analyzers/
│   │   │   ├── test_loc_counter.py
│   │   │   ├── test_complexity_analyzer.py
│   │   │   └── test_codebase_scanner.py
│   │   ├── models/
│   │   │   ├── test_project.py
│   │   │   ├── test_estimate.py
│   │   │   └── test_validation.py
│   │   └── utils/
│   │       ├── test_math_helpers.py
│   │       └── test_validators.py
│   │
│   ├── integration/                               # Integration tests
│   │   ├── __init__.py
│   │   ├── test_api_estimates.py                  # Test API endpoints
│   │   ├── test_api_projects.py
│   │   ├── test_api_analysis.py
│   │   ├── test_database_operations.py            # Test database layer
│   │   └── test_cli_workflows.py                  # Test CLI commands
│   │
│   ├── e2e/                                       # End-to-end tests
│   │   ├── __init__.py
│   │   ├── test_estimate_workflow.py              # Full estimation workflow
│   │   ├── test_analysis_workflow.py              # Full analysis workflow
│   │   └── test_comparison_workflow.py            # Estimate vs actual workflow
│   │
│   ├── validation/                                # Validation against benchmarks
│   │   ├── __init__.py
│   │   ├── test_cocomo_benchmarks.py              # Compare to published COCOMO data
│   │   ├── test_industry_benchmarks.py            # Compare to industry averages
│   │   └── test_accuracy_metrics.py               # Calculate MMRE, PRED(25)
│   │
│   └── fixtures/                                  # Test data
│       ├── sample_projects.json                   # Sample project data
│       ├── historical_data.csv                    # Historical project data
│       ├── codebase_samples/                      # Sample codebases for analysis
│       │   ├── python_project/
│       │   ├── javascript_project/
│       │   └── java_project/
│       └── expected_results.json                  # Expected calculation results
│
│
├── scripts/                                       # Automation scripts
│   │
│   ├── setup_dev_environment.sh                   # Initialize development environment
│   ├── seed_database.py                           # Populate database with sample data
│   ├── generate_api_docs.py                       # Auto-generate API documentation
│   ├── run_benchmarks.py                          # Performance benchmarking
│   ├── validate_models.py                         # Validate estimation accuracy
│   ├── import_historical_data.py                  # Import CSV/JSON data
│   ├── export_database.py                         # Backup database to JSON
│   ├── update_coefficients.py                     # Update COCOMO/FPA coefficients
│   └── docker_build.sh                            # Build Docker image
│
│
├── data/                                          # Data storage
│   │
│   ├── README.md                                  # Data directory overview
│   │
│   ├── database/                                  # SQLite databases
│   │   ├── .gitignore                             # Ignore actual DB files
│   │   └── estimation.db.example                  # Empty database template
│   │
│   ├── sample_projects/                           # Example projects for testing
│   │   ├── web_application.json                   # Sample web app project
│   │   ├── mobile_app.json                        # Sample mobile app project
│   │   ├── api_service.json                       # Sample API service project
│   │   └── legacy_migration.json                  # Sample migration project
│   │
│   ├── historical_data/                           # Historical benchmarks
│   │   ├── cocomo_81_dataset.csv                  # COCOMO 81 original dataset
│   │   ├── nasa_93_dataset.csv                    # NASA 93 dataset
│   │   ├── industry_benchmarks.csv                # Industry averages
│   │   └── README.md                              # Data sources and citations
│   │
│   ├── templates/                                 # Import/export templates
│   │   ├── project_import_template.csv
│   │   ├── historical_data_template.json
│   │   └── estimate_export_template.xlsx
│   │
│   └── exports/                                   # Generated exports
│       ├── .gitignore                             # Ignore generated files
│       └── README.md                              # Export directory explanation
│
│
├── .github/                                       # GitHub-specific configuration
│   │
│   ├── workflows/                                 # GitHub Actions CI/CD
│   │   ├── test.yml                               # Run test suite
│   │   ├── lint.yml                               # Code quality (black, pylint, mypy)
│   │   ├── docs.yml                               # Build and deploy docs
│   │   ├── publish.yml                            # Publish to PyPI
│   │   └── docker.yml                             # Build and push Docker image
│   │
│   ├── ISSUE_TEMPLATE/                            # Issue templates
│   │   ├── bug_report.md
│   │   ├── feature_request.md
│   │   └── estimation_inaccuracy.md               # Custom template
│   │
│   ├── PULL_REQUEST_TEMPLATE.md                   # PR template
│   └── CODEOWNERS                                 # Code ownership
│
│
├── deployment/                                    # Deployment configurations
│   │
│   ├── docker/                                    # Docker configurations
│   │   ├── Dockerfile.production                  # Production build
│   │   ├── Dockerfile.development                 # Development build
│   │   └── docker-compose.production.yml
│   │
│   ├── kubernetes/                                # Kubernetes manifests
│   │   ├── namespace.yaml
│   │   ├── deployment.yaml
│   │   ├── service.yaml
│   │   ├── ingress.yaml
│   │   └── configmap.yaml
│   │
│   ├── terraform/                                 # Infrastructure as Code
│   │   ├── main.tf
│   │   ├── variables.tf
│   │   ├── outputs.tf
│   │   └── README.md
│   │
│   └── nginx/                                     # NGINX configuration
│       └── nginx.conf                             # Reverse proxy config
│
│
├── examples/                                      # Usage examples
│   │
│   ├── README.md                                  # Examples overview
│   │
│   ├── python_scripts/                            # Python usage examples
│   │   ├── estimate_web_app.py                    # Example: Estimate web app
│   │   ├── analyze_codebase.py                    # Example: Analyze existing code
│   │   ├── compare_methods.py                     # Example: Compare methodologies
│   │   └── batch_import.py                        # Example: Import historical data
│   │
│   ├── api_examples/                              # API usage examples
│   │   ├── curl_examples.sh                       # cURL examples
│   │   ├── python_client.py                       # Python requests examples
│   │   └── postman_collection.json                # Postman collection
│   │
│   └── cli_examples/                              # CLI usage examples
│       ├── basic_estimation.sh                    # Basic CLI usage
│       ├── advanced_analysis.sh                   # Advanced analysis workflow
│       └── batch_processing.sh                    # Batch estimation workflow
│
│
└── notebooks/                                     # Jupyter notebooks (optional)
    │
    ├── README.md                                  # Notebooks overview
    ├── 01_cocomo_exploration.ipynb                # Explore COCOMO calculations
    ├── 02_accuracy_analysis.ipynb                 # Analyze estimation accuracy
    ├── 03_calibration_guide.ipynb                 # Calibrate models
    └── 04_visualization.ipynb                     # Visualize results
```

---

## File-by-File Descriptions

### Root Configuration Files

| File | Description |
|------|-------------|
| **pyproject.toml** | Modern Python project metadata (PEP 518), dependencies, build config, tool settings (black, mypy, pytest) |
| **setup.py** | Fallback for `pip install -e .` in editable mode |
| **requirements.txt** | Production dependencies (FastAPI, SQLAlchemy, Click, etc.) |
| **requirements-dev.txt** | Development dependencies (pytest, black, mypy, sphinx) |
| **.python-version** | Python version specification for pyenv (3.10+) |
| **.env.example** | Template for environment variables (DATABASE_URL, LOG_LEVEL, etc.) |
| **Makefile** | Common tasks: `make test`, `make lint`, `make run`, `make docs` |

### Source Code (`src/estimation_engine/`)

#### Calculators (`calculators/`)
- **base.py** - Abstract base class defining calculator interface
- **cocomo.py** - COCOMO II (Basic, Intermediate, Detailed) implementation
- **function_points.py** - Function Point Analysis with IFPUG/COSMIC methods
- **use_case_points.py** - Use Case Points for object-oriented systems
- **three_point.py** - Three-point PERT estimation (optimistic, pessimistic, most likely)
- **bottom_up.py** - Bottom-up aggregation from task estimates
- **analogous.py** - Analogous (top-down) estimation from similar projects
- **planning_poker.py** - Planning poker simulation with consensus
- **monte_carlo.py** - Monte Carlo simulation for uncertainty

#### Analyzers (`analyzers/`)
- **loc_counter.py** - Count lines of code with language detection (scc/cloc integration)
- **complexity_analyzer.py** - Cyclomatic complexity, cognitive complexity (radon integration)
- **dependency_analyzer.py** - Dependency graph analysis
- **git_history_analyzer.py** - Analyze commit history, churn rate, contributor activity
- **codebase_scanner.py** - Orchestrate all analyzers, generate comprehensive report

#### API (`api/`)
- **app.py** - FastAPI application factory, CORS, middleware setup
- **routes/estimates.py** - POST /estimates (create), GET /estimates/{id} (retrieve)
- **routes/projects.py** - CRUD operations for projects
- **routes/analysis.py** - POST /analysis (analyze codebase directory)
- **routes/comparison.py** - GET /comparison (estimate vs actual accuracy)
- **routes/methodologies.py** - GET /methodologies (list available methods)

#### CLI (`cli/`)
- **main.py** - Click/Typer CLI entry point
- **commands/estimate.py** - `estimate cocomo --kloc 50`
- **commands/analyze.py** - `analyze /path/to/codebase --output json`
- **commands/compare.py** - `compare --estimate-id 1 --actual-id 2`
- **commands/import_data.py** - `import historical_data.csv --format csv`
- **commands/benchmark.py** - `benchmark --methodology cocomo`

### Documentation (`docs/`)

#### Methodologies (`methodologies/`)
- **cocomo-ii.md** - Complete COCOMO II explanation with formulas, coefficients, examples
- **function-points.md** - FPA methodology, complexity weights, adjustment factors
- **comparison-matrix.md** - When to use each method (table with pros/cons)

#### Guides (`guides/`)
- **quickstart.md** - 5-minute quickstart: Install, estimate first project, view results
- **estimating-new-project.md** - Step-by-step guide with decision trees
- **calibrating-models.md** - How to customize coefficients based on organizational data

#### API (`api/`)
- **endpoints.md** - Auto-generated from FastAPI OpenAPI spec
- **examples.md** - cURL, Python requests, JavaScript fetch examples

#### Examples (`examples/`)
- **web-application-estimate.md** - Real-world example: Estimate SaaS web app
- **mobile-app-estimate.md** - Real-world example: Estimate mobile app with backend

### Tests (`tests/`)

#### Unit Tests (`unit/`)
- **test_cocomo.py** - Test COCOMO calculations against known results
- **test_function_points.py** - Test FPA calculations
- **test_loc_counter.py** - Test LOC counting accuracy

#### Integration Tests (`integration/`)
- **test_api_estimates.py** - Test API endpoints with mock database
- **test_database_operations.py** - Test CRUD operations

#### Validation Tests (`validation/`)
- **test_cocomo_benchmarks.py** - Compare to COCOMO 81 dataset (MMRE < 25%)
- **test_accuracy_metrics.py** - Calculate MMRE, PRED(25), MRE

### Data (`data/`)

#### Historical Data (`historical_data/`)
- **cocomo_81_dataset.csv** - Original COCOMO dataset (63 projects)
- **nasa_93_dataset.csv** - NASA 93 dataset (93 projects)
- **industry_benchmarks.csv** - Industry averages by project type

### Scripts (`scripts/`)

| Script | Purpose |
|--------|---------|
| **seed_database.py** | Populate database with sample projects and historical data |
| **generate_api_docs.py** | Generate API documentation from OpenAPI spec |
| **validate_models.py** | Calculate accuracy metrics (MMRE, PRED) against benchmarks |
| **import_historical_data.py** | Import CSV/JSON historical data into database |

### Deployment (`deployment/`)

- **docker/Dockerfile.production** - Multi-stage build (pip install, copy only needed files)
- **kubernetes/deployment.yaml** - K8s deployment with resource limits, health checks
- **terraform/main.tf** - Provision cloud resources (optional)

---

## Production Readiness Checklist

### Code Quality
- ✅ Type hints throughout (mypy strict mode)
- ✅ Docstrings (Google style)
- ✅ Linting (black, pylint, flake8)
- ✅ Code coverage >80% (pytest-cov)

### Documentation
- ✅ User-facing README.md
- ✅ AI agent CLAUDE.md
- ✅ API documentation (auto-generated)
- ✅ Methodology explanations with citations
- ✅ Architecture diagrams (Mermaid)

### Testing
- ✅ Unit tests for all calculators
- ✅ Integration tests for API/CLI
- ✅ Validation tests against industry benchmarks
- ✅ E2E tests for workflows

### Deployment
- ✅ Dockerfile with multi-stage build
- ✅ docker-compose for local development
- ✅ GitHub Actions CI/CD
- ✅ PyPI package configuration

### Security
- ✅ No hardcoded secrets
- ✅ Input validation (Pydantic)
- ✅ SQL injection prevention (ORM)
- ✅ Rate limiting (API)

### Observability
- ✅ Structured logging (JSON)
- ✅ Health check endpoint
- ✅ Metrics (optional: Prometheus)

---

## Key Design Decisions

### 1. **Calculator Base Class**
All estimation methods inherit from `BaseCalculator` with standard interface:
```python
class BaseCalculator(ABC):
    @abstractmethod
    def estimate(self, inputs: dict) -> EstimateResult:
        pass

    @abstractmethod
    def validate_inputs(self, inputs: dict) -> bool:
        pass
```

### 2. **Pydantic Models**
All data models use Pydantic for validation:
```python
class EstimateRequest(BaseModel):
    methodology: str
    inputs: dict
    project_type: Optional[str] = None
```

### 3. **Repository Pattern**
Database access through repositories for testability:
```python
class ProjectRepository:
    def create(self, project: Project) -> Project: ...
    def get(self, id: int) -> Optional[Project]: ...
    def list(self, filters: dict) -> List[Project]: ...
```

### 4. **CLI and API Share Core Logic**
Both interfaces use same calculators/analyzers - no duplication.

### 5. **Historical Data Seeding**
Include industry benchmarks (COCOMO 81, NASA 93) for validation.

### 6. **Export Formats**
Support CSV, JSON, PDF, Excel for integration with PM tools.

---

## Next Steps

1. **Initialize Repository**
   ```bash
   mkdir coditect-ops-estimation-engine
   cd coditect-ops-estimation-engine
   git init
   # Create symlinks
   ln -s ../../core/coditect-core .coditect
   ln -s .coditect .claude
   ```

2. **Create Core Files**
   - Generate README.md, CLAUDE.md, PROJECT-PLAN.md, TASKLIST.md
   - Create pyproject.toml with dependencies
   - Setup .gitignore

3. **Implement Core Calculators**
   - Start with COCOMO II (most widely used)
   - Add Function Points
   - Add Three-point estimation

4. **Build CLI First** (faster feedback loop)
   - Implement `estimate` command
   - Implement `analyze` command

5. **Add API Layer**
   - FastAPI app with basic endpoints
   - OpenAPI documentation

6. **Comprehensive Testing**
   - Unit tests with known results
   - Validation against benchmarks

7. **Documentation**
   - Methodology explanations
   - User guides with examples

---

## Estimated Implementation Effort

| Phase | Tasks | Effort |
|-------|-------|--------|
| **Phase 1: Foundation** | Project setup, core models, base classes | 1 week |
| **Phase 2: Calculators** | COCOMO II, FPA, Three-point | 2 weeks |
| **Phase 3: Analyzers** | LOC counter, complexity analyzer | 1 week |
| **Phase 4: CLI** | Click/Typer CLI with commands | 1 week |
| **Phase 5: API** | FastAPI REST API | 1 week |
| **Phase 6: Database** | SQLite schema, repositories, migrations | 1 week |
| **Phase 7: Testing** | Unit, integration, validation tests | 2 weeks |
| **Phase 8: Documentation** | Methodology docs, guides, examples | 1 week |
| **Phase 9: Deployment** | Docker, CI/CD, PyPI package | 1 week |
| **Total** | | **11 weeks** |

---

**Structure Version:** 1.0
**Last Updated:** 2025-11-22
**Author:** project-structure-optimization-specialist (CODITECT Agent)
**Status:** Production-Ready Blueprint
