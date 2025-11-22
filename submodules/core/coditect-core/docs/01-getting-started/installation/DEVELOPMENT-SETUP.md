# CODITECT Framework - Development Environment Setup

**Last Updated:** 2025-11-17
**Python Version:** 3.9+ (tested with 3.14.0)
**Status:** ✅ Production Ready

---

## Quick Start

### 1. Automated Setup (Recommended)

```bash
# Clone repository (if not already done)
git clone <repository-url>
cd coditect-core

# Run setup script
./setup.sh

# Activate virtual environment
source venv/bin/activate

# Verify installation
pytest tests/ -v
```

**That's it!** The setup script handles everything: Python version check, venv creation, and dependency installation.

---

## Manual Setup

### 1. Check Python Version

```bash
python3 --version  # Should be 3.9 or higher
```

### 2. Create Virtual Environment

```bash
python3 -m venv venv
```

### 3. Activate Virtual Environment

**macOS/Linux:**
```bash
source venv/bin/activate
```

**Windows:**
```powershell
venv\Scripts\activate
```

### 4. Install Dependencies

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### 5. Verify Installation

```bash
# Check installed packages
pip list

# Run tests
pytest tests/ -v --cov=scripts/ --cov-report=term-missing
```

---

## Setup Script Options

The `setup.sh` script supports multiple modes:

```bash
./setup.sh              # Full setup (venv + dependencies)
./setup.sh --venv-only  # Create venv only
./setup.sh --deps-only  # Install dependencies only
./setup.sh --test       # Run test suite
./setup.sh --clean      # Remove venv and start fresh
./setup.sh --help       # Show usage information
```

---

## Installed Dependencies

### Core Dependencies

| Package | Version | Purpose |
|---------|---------|---------|
| `gitpython` | ≥3.1.0 | Git operations (80x faster than subprocess) |

### Testing & Quality Assurance

| Package | Version | Purpose |
|---------|---------|---------|
| `pytest` | ≥7.4.0 | Modern test runner |
| `pytest-cov` | ≥4.1.0 | Code coverage reporting |
| `pytest-asyncio` | ≥0.21.0 | Async test support |
| `coverage` | ≥7.0.0 | Standalone coverage tool |
| `black` | ≥23.0.0 | Code formatting |
| `flake8` | ≥6.0.0 | Linting |
| `mypy` | ≥1.0.0 | Static type checking |
| `isort` | ≥5.12.0 | Import sorting |

### Database (Phase 2)

| Package | Version | Purpose |
|---------|---------|---------|
| `psycopg2-binary` | ≥2.9.0 | PostgreSQL adapter |

### Development Tools

| Package | Version | Purpose |
|---------|---------|---------|
| `ipython` | ≥8.12.0 | Enhanced interactive Python shell |

---

## Verification Checklist

After setup, verify everything works:

- [ ] **Python version** ≥ 3.9
  ```bash
  python --version
  ```

- [ ] **Virtual environment** activated
  ```bash
  which python  # Should point to venv/bin/python
  ```

- [ ] **Dependencies** installed
  ```bash
  pip list | grep pytest  # Should show pytest 9.0+
  ```

- [ ] **Tests** passing
  ```bash
  pytest tests/ -v
  ```

- [ ] **Code quality tools** working
  ```bash
  black --check scripts/
  flake8 scripts/
  mypy scripts/
  ```

---

## Directory Structure

```
coditect-core/
├── venv/                      # Virtual environment (created by setup)
├── scripts/                   # Python scripts
│   ├── core/                  # Core modules
│   │   ├── conversation_deduplicator.py  # Deduplication engine
│   │   └── __init__.py
│   └── process_exports_poc.py # Demo scripts
├── tests/                     # Test suite
│   └── test_conversation_deduplicator.py
├── MEMORY-CONTEXT/            # Context storage
│   └── dedup_state/           # Deduplication state
│       ├── watermarks.json
│       ├── content_hashes.json
│       └── conversation_log.jsonl
├── requirements.txt           # Python dependencies
├── setup.sh                   # Automated setup script
├── DEVELOPMENT-SETUP.md       # This file
└── README.md                  # Project documentation
```

---

## Common Tasks

### Running Tests

```bash
# Run all tests
pytest tests/ -v

# Run with coverage
pytest tests/ --cov=scripts/ --cov-report=term-missing

# Run specific test
pytest tests/test_conversation_deduplicator.py::test_process_export -v

# Run with output capture disabled (see print statements)
pytest tests/ -v -s
```

### Code Quality Checks

```bash
# Format code with black
black scripts/ tests/

# Check formatting (CI mode)
black --check scripts/ tests/

# Lint with flake8
flake8 scripts/ tests/

# Type check with mypy
mypy scripts/

# Sort imports with isort
isort scripts/ tests/
```

### Dependency Management

```bash
# Install new dependency
pip install <package-name>

# Add to requirements.txt
echo "<package-name>>=<version>" >> requirements.txt

# Update all dependencies
pip install --upgrade -r requirements.txt

# Generate frozen requirements (exact versions)
pip freeze > requirements.lock.txt

# Show dependency tree
pip install pipdeptree
pipdeptree
```

### Using the CLI Tool

The `deduplicate_export.py` CLI tool provides a user-friendly interface for conversation export deduplication.

#### Quick Start

```bash
# Process single file
python scripts/deduplicate_export.py --file MEMORY-CONTEXT/exports/2025-11-17-EXPORT.txt

# Process all files in directory (batch mode)
python scripts/deduplicate_export.py --batch MEMORY-CONTEXT/exports/

# Dry run (preview without saving)
python scripts/deduplicate_export.py --file export.txt --dry-run --verbose

# Show statistics for a session
python scripts/deduplicate_export.py --stats --session-id rollout-master

# Run integrity check
python scripts/deduplicate_export.py --integrity --verbose
```

#### CLI Modes

**Single File Mode:**
```bash
python scripts/deduplicate_export.py \
  --file MEMORY-CONTEXT/exports/export.txt \
  --session-id my-session \
  --verbose
```

**Batch Directory Mode:**
```bash
python scripts/deduplicate_export.py \
  --batch MEMORY-CONTEXT/exports/ \
  --dry-run
```

**Statistics Mode:**
```bash
python scripts/deduplicate_export.py \
  --stats \
  --session-id my-session
```

**Integrity Check Mode:**
```bash
python scripts/deduplicate_export.py \
  --integrity \
  --storage-dir MEMORY-CONTEXT/dedup_state \
  --verbose
```

#### CLI Options

**Mode Selection (required, mutually exclusive):**
- `--file, -f PATH` - Process single export file
- `--batch, -b PATH` - Process all files in directory
- `--stats` - Show statistics for a session
- `--integrity` - Run integrity check on all conversations

**Common Options:**
- `--session-id, -s ID` - Session identifier (auto-detected if not provided)
- `--storage-dir, -d PATH` - Storage directory for deduplication state (default: `../../MEMORY-CONTEXT/dedup_state`)
- `--dry-run` - Preview changes without modifying storage
- `--verbose, -v` - Verbose output
- `--quiet, -q` - Minimal output (errors only)
- `--no-color` - Disable colored output
- `--output, -o PATH` - Write results to JSON file

#### Auto-Detection Features

**Session ID Auto-Detection:**
The CLI automatically extracts session IDs from filenames:
- `2025-11-17-EXPORT-ROLLOUT-MASTER.txt` → `2025-11-17-rollout-master`
- `2025-11-16-EXPORT-CHECKPOINT.txt` → `2025-11-16-checkpoint`
- `export-session-001.json` → `export-session-001`

**File Format Detection:**
The CLI automatically detects file formats:
- JSON files (with `messages` array)
- Plain text Claude exports (with ⏺ and ⎿ markers)

#### Example Workflows

**Process Historical Exports:**
```bash
# 1. Dry run to preview
python scripts/deduplicate_export.py --batch MEMORY-CONTEXT/ --dry-run --verbose

# 2. Process for real
python scripts/deduplicate_export.py --batch MEMORY-CONTEXT/ --verbose

# 3. Verify with integrity check
python scripts/deduplicate_export.py --integrity --verbose
```

**Daily Export Deduplication:**
```bash
# After /export command in Claude Code
python scripts/deduplicate_export.py \
  --file MEMORY-CONTEXT/exports/$(date +%Y-%m-%d)-EXPORT.txt \
  --verbose
```

**Generate Statistics Report:**
```bash
# Get statistics and save to JSON
python scripts/deduplicate_export.py \
  --stats \
  --session-id rollout-master \
  --output stats-report.json
```

#### Expected Results

**First Run (No Duplicates):**
```
Total: 51 | New: 51 | Duplicates: 0
Deduplication: 0.0%
```

**Second Run (All Duplicates):**
```
Total: 51 | New: 0 | Duplicates: 51
Deduplication: 100.0%
```

**Batch Processing Summary:**
```
Batch Processing Summary
========================
Total files: 15
Successful: 15
Failed: 0

Total messages: 1291
New messages: 0
Duplicates filtered: 1291
Overall deduplication rate: 100.0%
```

---

## Troubleshooting

### Issue: `command not found: python3`

**Solution:** Install Python 3.9 or higher

**macOS (Homebrew):**
```bash
brew install python@3.9
```

**Ubuntu/Debian:**
```bash
sudo apt update
sudo apt install python3.9 python3.9-venv python3-pip
```

---

### Issue: `pip: command not found`

**Solution:** Install pip

**macOS/Linux:**
```bash
python3 -m ensurepip --upgrade
```

**Ubuntu/Debian:**
```bash
sudo apt install python3-pip
```

---

### Issue: Virtual environment activation not working

**Symptom:** `which python` still points to system Python

**Solution:**
1. Deactivate existing venv: `deactivate`
2. Remove venv: `rm -rf venv`
3. Recreate: `./setup.sh --clean && ./setup.sh`

---

### Issue: `ImportError: No module named 'pytest'`

**Symptom:** Tests fail with import errors

**Solution:** Ensure venv is activated and dependencies installed
```bash
source venv/bin/activate
pip install -r requirements.txt
```

---

### Issue: PostgreSQL dependency fails (psycopg2-binary)

**Symptom:** `Error: pg_config executable not found`

**Solution:**

**macOS:**
```bash
brew install postgresql
```

**Ubuntu/Debian:**
```bash
sudo apt install libpq-dev
```

**Alternative:** Use pure Python fallback (slower)
```bash
pip install psycopg2-binary --no-binary psycopg2-binary
```

---

## Development Workflow

### 1. Start New Work Session

```bash
cd /path/to/coditect-core
source venv/bin/activate
```

### 2. Make Changes

Edit code in `scripts/` or `tests/`

### 3. Run Tests

```bash
# Quick test (specific module)
pytest tests/test_conversation_deduplicator.py -v

# Full test suite
pytest tests/ -v --cov=scripts/
```

### 4. Quality Checks

```bash
# Format and lint
black scripts/ tests/
flake8 scripts/ tests/
mypy scripts/
```

### 5. Commit Changes

```bash
git add .
git commit -m "Description of changes"
```

### 6. End Work Session

```bash
deactivate  # Exit virtual environment
```

---

## CI/CD Integration

### GitHub Actions Example

```yaml
name: Test

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3

      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.9'

      - name: Install dependencies
        run: |
          python -m pip install --upgrade pip
          pip install -r requirements.txt

      - name: Run tests
        run: |
          pytest tests/ -v --cov=scripts/ --cov-report=xml

      - name: Upload coverage
        uses: codecov/codecov-action@v3
```

---

## Environment Variables

### Optional Configuration

```bash
# Set in your shell profile (~/.bashrc, ~/.zshrc, etc.)

# PostgreSQL connection (Phase 2)
export CODITECT_DB_HOST="localhost"
export CODITECT_DB_PORT="5432"
export CODITECT_DB_NAME="coditect"
export CODITECT_DB_USER="coditect_user"
export CODITECT_DB_PASSWORD="<secure-password>"

# Memory-Context storage location
export CODITECT_MEMORY_CONTEXT_DIR="/path/to/MEMORY-CONTEXT"

# Logging level
export CODITECT_LOG_LEVEL="INFO"  # DEBUG, INFO, WARNING, ERROR, CRITICAL

# Test mode (skip expensive operations)
export CODITECT_TEST_MODE="true"
```

---

## Performance Optimization

### For Large Repositories

```bash
# Increase pytest timeout
pytest tests/ -v --timeout=300

# Run tests in parallel
pip install pytest-xdist
pytest tests/ -v -n auto  # auto-detect CPU count
```

### For Development Speed

```bash
# Install development dependencies
pip install pytest-watch

# Auto-run tests on file changes
ptw -- tests/ -v
```

---

## Updating the Environment

### When requirements.txt Changes

```bash
# Pull latest changes
git pull

# Update dependencies
source venv/bin/activate
pip install --upgrade -r requirements.txt

# Verify
pytest tests/ -v
```

### Major Version Upgrades

```bash
# Clean slate approach
./setup.sh --clean
./setup.sh
```

---

## Support & Resources

### Documentation
- **CODITECT Framework:** `README.md`
- **Conversation Deduplication:** `MEMORY-CONTEXT/DEDUPLICATION-POC-FINAL-REPORT.md`
- **Implementation Plan:** `docs/CONVERSATION-DEDUPLICATION-IMPLEMENTATION-PLAN.md`

### External Resources
- [Python Virtual Environments](https://docs.python.org/3/tutorial/venv.html)
- [pytest Documentation](https://docs.pytest.org/)
- [Black Code Formatter](https://black.readthedocs.io/)
- [Flake8 Linter](https://flake8.pycqa.org/)
- [mypy Type Checker](https://mypy.readthedocs.io/)

---

## Contributing

### Before Submitting PR

1. ✅ All tests pass: `pytest tests/ -v`
2. ✅ Code formatted: `black scripts/ tests/`
3. ✅ No linting errors: `flake8 scripts/ tests/`
4. ✅ Type checks pass: `mypy scripts/`
5. ✅ Coverage ≥ 90%: `pytest --cov=scripts/ --cov-report=term-missing`

### Adding New Dependencies

1. Add to `requirements.txt` with version constraint
2. Update `DEVELOPMENT-SETUP.md` (this file) in Dependencies table
3. Run `./setup.sh --deps-only` to verify
4. Document any platform-specific requirements in Troubleshooting section

---

**Last Updated:** 2025-11-17
**Maintained By:** CODITECT Framework Team
**Questions?** Create an issue on GitHub or see `README.md`
