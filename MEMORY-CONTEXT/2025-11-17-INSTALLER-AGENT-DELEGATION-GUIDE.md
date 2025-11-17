# CODITECT Installer - Multi-Agent Task Delegation Guide

**Quick Reference for Executing the Orchestration Plan**

---

## Overview

This guide provides ready-to-execute Task tool invocations for each phase of the CODITECT installer enhancement project.

**Master Plan:** See `2025-11-17-INSTALLER-ORCHESTRATION-PLAN.md` for complete details.

---

## Phase 1: Architecture & Planning

### Task 1.1: Design License Integration Architecture

```python
Task(
    subagent_type="general-purpose",
    description="Design license integration architecture for CODITECT installer",
    prompt="""You are a Senior Architect designing the license integration architecture for the CODITECT modular installer system.

**Context:**
- Existing installer: submodules/coditect-installer/ (production-ready, 38/40 quality score)
- License manager: submodules/coditect-license-manager/ (Python library)
- License server: submodules/coditect-license-server/ (FastAPI server)

**Your Task:**
Design the complete license integration architecture including:

1. **License Client API Design:**
   - activate_license(license_key, hardware_id) -> ActivationResult
   - validate_license(license_key, hardware_id) -> ValidationResult
   - deactivate_license(license_key, hardware_id) -> bool
   - submit_usage_data(usage_data) -> bool
   - start_trial(email) -> TrialLicense

2. **License Validator API Design:**
   - verify_signature(license_data, signature) -> bool
   - check_expiry(license_data) -> bool
   - check_features(license_data, feature) -> bool
   - validate(license_key) -> LicenseStatus

3. **Usage Tracker API Design (Privacy-Compliant):**
   - track_installation(platform, python_version)
   - track_feature_usage(feature)
   - submit(data) - async, fire-and-forget, opt-in only

4. **Integration Points:**
   - How install.py integrates license checking
   - How install_gui.py adds license activation dialog
   - License storage (encrypted, local)
   - Offline vs online validation strategy

5. **Architecture Diagram:**
   - Create Mermaid diagram showing component interactions
   - Show data flow: Installer -> License Client -> License Server
   - Show fallback: Online validation fails -> Offline validation

**Deliverables:**
- Complete API specifications for all components
- Mermaid architecture diagram
- Integration strategy document
- Security considerations (encryption, privacy)

**References:**
- Review: submodules/coditect-installer/CLAUDE.md
- Review: submodules/coditect-license-manager/README.md
- Review: submodules/coditect-license-server/README.md

**Output Format:**
Structured document with:
- API Specifications (function signatures + docstrings)
- Architecture Diagram (Mermaid code)
- Integration Strategy (step-by-step)
- Security Model
- Privacy Compliance Notes
"""
)
```

### Task 1.2: Create Comprehensive Test Plan

```python
Task(
    subagent_type="general-purpose",
    description="Create comprehensive test plan for CODITECT installer",
    prompt="""You are a Senior Architect creating the comprehensive test plan for the CODITECT modular installer system.

**Context:**
- Existing test spec: submodules/coditect-installer/TDD.md
- Target coverage: 95%+ (unit + integration)
- Test pyramid: 70% unit, 20% integration, 10% manual

**Your Task:**
Create detailed test plan covering:

1. **Unit Tests (70% of tests):**
   - test_platform_detection.py (8 tests) - Windows, macOS, Linux detection
   - test_python_version.py (5 tests) - Version checking, parsing
   - test_path_resolution.py (6 tests) - Platform-specific paths
   - test_color_output.py (4 tests) - ANSI color handling
   - test_venv_creation.py (6 tests) - Virtual environment creation
   - test_dependency_installation.py (5 tests) - Pip install, GitPython verification
   - test_license_validation.py (8 tests) - License activation, validation, trial

2. **Integration Tests (20% of tests):**
   - test_cli_full_installation.py (4 tests) - End-to-end CLI flows
   - test_gui_full_installation.py (4 tests) - End-to-end GUI flows
   - test_license_server_communication.py (6 tests) - Online license operations

3. **Manual Tests (10% of tests):**
   - test_windows.md - Windows 10/11 testing checklist
   - test_macos.md - macOS 12/13/14 testing checklist
   - test_linux.md - Ubuntu 22.04/24.04, Fedora testing checklist

4. **Test Infrastructure:**
   - pytest configuration (pytest.ini)
   - coverage configuration (.coveragerc)
   - tox configuration (tox.ini) - Python 3.8-3.12 matrix
   - Mock license server (tests/fixtures/mock_license_server.py)

5. **Platform Coverage Matrix:**
   - Python versions: 3.8, 3.9, 3.10, 3.11, 3.12
   - Operating systems: Windows 10/11, macOS 12/13/14, Ubuntu 22.04/24.04, Fedora 39+

**Deliverables:**
- Detailed test specification for each test file
- pytest.ini, .coveragerc, tox.ini configurations
- Mock license server specification
- Manual test checklists
- Platform coverage matrix

**Output Format:**
Structured document with:
- Test Categories (unit, integration, manual)
- Test File Specifications (test names, assertions, fixtures)
- Configuration Files (pytest.ini, .coveragerc, tox.ini)
- Platform Matrix
- Coverage Strategy
"""
)
```

---

## Phase 2: Testing Infrastructure

### Task 2.1: Implement Unit Tests

```python
Task(
    subagent_type="general-purpose",
    description="Implement comprehensive unit test suite for CODITECT installer",
    prompt="""You are a Testing Specialist implementing the unit test suite for the CODITECT modular installer system.

**Context:**
- Installer code: submodules/coditect-installer/install.py, install_gui.py
- Test plan: (created in Phase 1)
- Target: 95%+ coverage

**Your Task:**
Implement ALL unit tests following the test plan:

1. **Setup Test Infrastructure:**
   - Create tests/unit/ directory
   - Create pytest.ini with appropriate settings
   - Create .coveragerc with coverage targets
   - Create tox.ini for Python 3.8-3.12 testing

2. **Implement Unit Test Files:**

**tests/unit/test_platform_detection.py:**
```python
import pytest
from unittest import mock
from install import CrossPlatformInstaller

def test_detect_windows():
    '''Verify Windows platform detection'''
    with mock.patch('platform.system', return_value='Windows'):
        installer = CrossPlatformInstaller()
        assert installer.os_type == 'Windows'
        assert installer.get_python_executable() == 'python'

def test_detect_macos():
    '''Verify macOS platform detection'''
    with mock.patch('platform.system', return_value='Darwin'):
        installer = CrossPlatformInstaller()
        assert installer.os_type == 'Darwin'
        assert installer.get_python_executable() == 'python3'

# ... (6 more tests)
```

**tests/unit/test_python_version.py:**
```python
def test_python_version_sufficient():
    '''Test Python 3.8+ is accepted'''
    installer = CrossPlatformInstaller()
    with mock.patch('sys.version_info', (3, 11, 0)):
        success, version = installer.check_python_version()
        assert success == True
        assert version == '3.11.0'

def test_python_version_insufficient():
    '''Test Python 3.7 is rejected'''
    installer = CrossPlatformInstaller()
    with mock.patch('sys.version_info', (3, 7, 5)):
        success, message = installer.check_python_version()
        assert success == False
        assert 'Python 3.8+' in message

# ... (3 more tests)
```

**tests/unit/test_venv_creation.py:**
```python
def test_create_venv_success(tmp_path):
    '''Test successful venv creation'''
    installer = CrossPlatformInstaller()
    installer.venv_path = tmp_path / 'venv'

    with mock.patch('subprocess.run') as mock_run:
        mock_run.return_value = mock.Mock(returncode=0)
        result = installer.create_venv(force_recreate=True)

        assert result == True
        assert installer.venv_path.exists()

# ... (5 more tests)
```

**tests/unit/test_dependency_installation.py:**
```python
def test_install_dependencies_success(tmp_path):
    '''Test successful dependency installation'''
    installer = CrossPlatformInstaller()
    installer.venv_path = tmp_path / 'venv'
    installer.venv_path.mkdir()

    with mock.patch('subprocess.run') as mock_run:
        mock_run.return_value = mock.Mock(returncode=0)
        result = installer.install_dependencies()

        assert result == True
        # Verify pip upgrade called
        # Verify requirements install called

# ... (4 more tests)
```

**tests/unit/test_license_validation.py:** (NEW)
```python
def test_license_validation_success():
    '''Test successful license validation'''
    # Mock license client and validator
    # Test activation flow
    pass

def test_license_validation_expired():
    '''Test expired license detection'''
    pass

def test_trial_license_creation():
    '''Test trial license creation'''
    pass

# ... (5 more tests)
```

3. **Test Fixtures:**
   - Create tests/fixtures/mock_requirements.txt
   - Create tests/fixtures/mock_venv/ structure

4. **Run Tests and Verify Coverage:**
   - Run: pytest tests/unit/ -v --cov=. --cov-report=html
   - Verify: 95%+ coverage achieved
   - Generate HTML coverage report

**Deliverables:**
- tests/unit/ with all test files
- pytest.ini, .coveragerc, tox.ini
- Test fixtures
- Coverage report (HTML)
- All tests passing

**Working Directory:** submodules/coditect-installer/

**References:**
- TDD.md for test specifications
- install.py, install_gui.py for code under test
"""
)
```

### Task 2.2: Implement Integration Tests

```python
Task(
    subagent_type="general-purpose",
    description="Implement integration tests for CODITECT installer",
    prompt="""You are a Testing Specialist implementing integration tests for the CODITECT modular installer system.

**Context:**
- Unit tests: (completed in Task 2.1)
- Target: 90%+ integration coverage

**Your Task:**
Implement ALL integration tests:

1. **tests/integration/test_cli_full_installation.py:**

```python
import pytest
import subprocess
from pathlib import Path

def test_cli_full_install_fresh(tmp_path):
    '''Test full CLI installation from scratch'''
    # Change to tmp_path
    # Remove any existing venv
    # Run: python install.py
    # Verify: venv created
    # Verify: dependencies installed
    # Verify: GitPython available
    assert True

def test_cli_venv_only(tmp_path):
    '''Test CLI venv-only mode'''
    # Run: python install.py --venv-only
    # Verify: venv created
    # Verify: dependencies NOT installed

def test_cli_deps_only(tmp_path):
    '''Test CLI deps-only mode'''
    # Pre-create venv
    # Run: python install.py --deps-only
    # Verify: dependencies installed

def test_cli_license_activation(tmp_path):
    '''Test CLI license activation flow'''
    # Mock license server
    # Run installer with license key
    # Verify: license activated
```

2. **tests/integration/test_gui_full_installation.py:**

```python
def test_gui_initialization():
    '''Test GUI window initialization'''
    # Create InstallerGUI instance
    # Verify: window created
    # Verify: widgets present

def test_gui_install_flow(tmp_path):
    '''Test GUI installation flow'''
    # Mock tkinter interactions
    # Simulate install button click
    # Verify: background thread started
    # Verify: progress updates
    # Verify: completion dialog

# ... (2 more tests)
```

3. **tests/integration/test_license_server_communication.py:** (NEW)

```python
def test_activate_license_success():
    '''Test successful license activation'''
    # Start mock license server
    # Call activate_license()
    # Verify: HTTP POST to /activate
    # Verify: license stored locally

def test_validate_license_active():
    '''Test validating active license'''
    # Setup: activated license
    # Call validate_license()
    # Verify: returns valid status

def test_submit_usage_data():
    '''Test usage data submission'''
    # Setup: opt-in enabled
    # Submit usage data
    # Verify: HTTP POST to /usage
    # Verify: privacy compliance (no PII)

# ... (3 more tests)
```

4. **Mock License Server:**

**tests/fixtures/mock_license_server.py:**
```python
from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/activate', methods=['POST'])
def activate():
    '''Mock license activation endpoint'''
    data = request.json
    license_key = data.get('license_key')

    if license_key == 'VALID-KEY':
        return jsonify({'success': True, 'license_data': {...}})
    else:
        return jsonify({'success': False, 'error': 'Invalid key'}), 400

@app.route('/validate', methods=['POST'])
def validate():
    '''Mock license validation endpoint'''
    pass

@app.route('/trial', methods=['POST'])
def trial():
    '''Mock trial creation endpoint'''
    pass

if __name__ == '__main__':
    app.run(port=5001)
```

5. **Run Integration Tests:**
   - Run: pytest tests/integration/ -v
   - Verify: All tests passing
   - Verify: Mock license server works

**Deliverables:**
- tests/integration/ with all test files
- Mock license server (tests/fixtures/mock_license_server.py)
- All integration tests passing

**Working Directory:** submodules/coditect-installer/
"""
)
```

---

## Phase 3: Licensing Integration

### Task 3.1: Implement License Client

```python
Task(
    subagent_type="general-purpose",
    description="Implement license client for CODITECT installer",
    prompt="""You are a Security Specialist implementing the license client for the CODITECT modular installer system.

**Context:**
- Architecture: (designed in Phase 1)
- License server: submodules/coditect-license-server/
- License manager library: submodules/coditect-license-manager/

**Your Task:**
Implement the complete license integration system:

1. **Create Directory Structure:**
```
submodules/coditect-installer/license_integration/
├── __init__.py
├── license_client.py
├── license_validator.py
├── usage_tracker.py
└── trial_manager.py
```

2. **Implement license_client.py:**

```python
import requests
from typing import Optional, Dict
from dataclasses import dataclass

@dataclass
class ActivationResult:
    success: bool
    license_data: Optional[Dict] = None
    error: Optional[str] = None

@dataclass
class ValidationResult:
    is_valid: bool
    license_data: Optional[Dict] = None
    error: Optional[str] = None

class LicenseClient:
    '''Client for CODITECT license server communication'''

    def __init__(self, server_url: str, api_key: str):
        self.server_url = server_url
        self.api_key = api_key
        self.session = requests.Session()
        self.session.headers.update({'X-API-Key': api_key})

    def activate_license(self, license_key: str, hardware_id: str) -> ActivationResult:
        '''Activate license key for this machine'''
        try:
            response = self.session.post(
                f'{self.server_url}/api/v1/activate',
                json={'license_key': license_key, 'hardware_id': hardware_id}
            )

            if response.status_code == 200:
                data = response.json()
                return ActivationResult(success=True, license_data=data)
            else:
                return ActivationResult(success=False, error=response.json().get('error'))

        except Exception as e:
            return ActivationResult(success=False, error=str(e))

    def validate_license(self, license_key: str, hardware_id: str) -> ValidationResult:
        '''Validate existing license (online check)'''
        # Implementation similar to activate_license
        pass

    def deactivate_license(self, license_key: str, hardware_id: str) -> bool:
        '''Deactivate license (for license transfer)'''
        pass

    def submit_usage_data(self, usage_data: dict) -> bool:
        '''Submit usage telemetry (opt-in only, fire-and-forget)'''
        try:
            # Async POST, don't wait for response
            # Never fail installer if telemetry fails
            pass
        except:
            pass  # Silently fail

    def start_trial(self, email: str) -> TrialLicense:
        '''Start trial license (14 days)'''
        pass
```

3. **Implement license_validator.py:**

```python
import json
import base64
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import padding
from datetime import datetime

class LicenseValidator:
    '''Offline license validation with cryptographic verification'''

    def __init__(self, public_key_pem: str):
        from cryptography.hazmat.backends import default_backend
        self.public_key = serialization.load_pem_public_key(
            public_key_pem.encode(),
            backend=default_backend()
        )

    def verify_signature(self, license_data: dict, signature: str) -> bool:
        '''Verify license signature using RSA public key'''
        try:
            # Serialize license data
            data_bytes = json.dumps(license_data, sort_keys=True).encode()

            # Decode signature
            sig_bytes = base64.b64decode(signature)

            # Verify signature
            self.public_key.verify(
                sig_bytes,
                data_bytes,
                padding.PSS(
                    mgf=padding.MGF1(hashes.SHA256()),
                    salt_length=padding.PSS.MAX_LENGTH
                ),
                hashes.SHA256()
            )
            return True

        except Exception:
            return False

    def check_expiry(self, license_data: dict) -> bool:
        '''Check if license is expired'''
        expiry_str = license_data.get('expiry_date')
        if not expiry_str:
            return True  # No expiry = perpetual license

        expiry = datetime.fromisoformat(expiry_str)
        return datetime.utcnow() < expiry

    def check_features(self, license_data: dict, feature: str) -> bool:
        '''Check if license includes feature'''
        features = license_data.get('features', [])
        return feature in features

    def validate(self, license_key: str) -> LicenseStatus:
        '''Full offline license validation'''
        # Parse license key
        # Verify signature
        # Check expiry
        # Return status
        pass
```

4. **Implement usage_tracker.py:**

```python
class UsageTracker:
    '''Privacy-compliant usage tracking (opt-in only)'''

    def __init__(self, opt_in: bool = False):
        self.opt_in = opt_in

    def track_installation(self, platform: str, python_version: str):
        '''Track installation event (no PII)'''
        if not self.opt_in:
            return

        data = {
            'event': 'installation',
            'platform': platform,
            'python_version': python_version,
            'timestamp': datetime.utcnow().isoformat(),
            # NO email, NO IP, NO user info
        }

        self._submit(data)

    def track_feature_usage(self, feature: str):
        '''Track feature usage (no PII)'''
        pass

    def _submit(self, data: dict):
        '''Submit usage data (async, fire-and-forget)'''
        # Never block installation
        # Never fail installer if telemetry fails
        pass
```

5. **Integrate with install.py:**

Modify install.py to add license checking:

```python
class CrossPlatformInstaller:
    def __init__(self):
        # ... existing code ...

        # License integration
        self.license_client = LicenseClient(
            server_url=os.getenv('LICENSE_SERVER_URL', 'https://license.az1.ai'),
            api_key=os.getenv('LICENSE_API_KEY', '')
        )
        self.license_validator = LicenseValidator(public_key=PUBLIC_KEY)
        self.usage_tracker = UsageTracker(opt_in=False)  # Default opt-out

    def run(self, venv_only=False, deps_only=False):
        '''Main installation flow with license checking'''
        self.print_header()

        # Check Python version
        success, message = self.check_python_version()
        if not success:
            self.print_error(message)
            return 1

        # CHECK LICENSE (NEW)
        if not self.check_license():
            self.print_error("Valid license required")
            return 1

        # ... rest of installation ...
```

6. **Write Tests:**
   - tests/unit/test_license_validation.py
   - tests/integration/test_license_server_communication.py

**Deliverables:**
- license_integration/ module with all components
- Modified install.py with license checking
- Tests for license integration
- Documentation

**Working Directory:** submodules/coditect-installer/

**Security Requirements:**
- Use RSA-2048 or RSA-4096 for signatures
- HTTPS only for license server communication
- Encrypt stored licenses (AES-256)
- NO personally identifiable information in telemetry
- Opt-in only for usage tracking
"""
)
```

### Task 3.2: Implement GUI License Dialog

```python
Task(
    subagent_type="general-purpose",
    description="Implement GUI license activation dialog for CODITECT installer",
    prompt="""You are a Frontend Expert implementing the GUI license activation dialog for the CODITECT installer.

**Context:**
- Existing GUI: submodules/coditect-installer/install_gui.py (tkinter)
- License client: (implemented in Task 3.1)

**Your Task:**
Enhance install_gui.py with license activation dialog:

1. **Create LicenseActivationDialog class:**

```python
import tkinter as tk
from tkinter import ttk, messagebox
from license_integration import LicenseClient, get_hardware_id

class LicenseActivationDialog(tk.Toplevel):
    '''License activation dialog'''

    def __init__(self, parent):
        super().__init__(parent)
        self.title("CODITECT License Activation")
        self.geometry("600x400")
        self.resizable(False, False)
        self.result = None

        self.create_widgets()
        self.center_window()

        # Modal dialog
        self.transient(parent)
        self.grab_set()
        parent.wait_window(self)

    def create_widgets(self):
        # Header
        header = tk.Label(
            self,
            text="CODITECT License Activation",
            font=('Helvetica', 18, 'bold'),
            bg='#2c3e50',
            fg='white',
            pady=20
        )
        header.pack(fill=tk.X)

        # Main content frame
        content = tk.Frame(self, padx=40, pady=20)
        content.pack(fill=tk.BOTH, expand=True)

        # Option 1: License key
        tk.Label(
            content,
            text="Option 1: Enter License Key",
            font=('Helvetica', 12, 'bold')
        ).pack(anchor=tk.W, pady=(0, 10))

        tk.Label(content, text="License Key:").pack(anchor=tk.W)
        self.license_key_entry = tk.Entry(content, width=50)
        self.license_key_entry.pack(anchor=tk.W, pady=(0, 10))

        tk.Button(
            content,
            text="Activate License",
            command=self.activate_license,
            bg='#27ae60',
            fg='white',
            padx=20,
            pady=5
        ).pack(anchor=tk.W, pady=(0, 20))

        # Separator
        ttk.Separator(content, orient=tk.HORIZONTAL).pack(fill=tk.X, pady=20)

        # Option 2: Trial license
        tk.Label(
            content,
            text="Option 2: Start 14-Day Trial",
            font=('Helvetica', 12, 'bold')
        ).pack(anchor=tk.W, pady=(0, 10))

        tk.Label(content, text="Email Address:").pack(anchor=tk.W)
        self.trial_email_entry = tk.Entry(content, width=50)
        self.trial_email_entry.pack(anchor=tk.W, pady=(0, 10))

        tk.Button(
            content,
            text="Start Trial",
            command=self.start_trial,
            bg='#3498db',
            fg='white',
            padx=20,
            pady=5
        ).pack(anchor=tk.W, pady=(0, 20))

        # Cancel button
        tk.Button(
            content,
            text="Exit Without License",
            command=self.cancel,
            padx=20,
            pady=5
        ).pack(side=tk.BOTTOM, pady=(20, 0))

    def activate_license(self):
        '''Activate license key'''
        license_key = self.license_key_entry.get().strip()

        if not license_key:
            messagebox.showerror("Error", "Please enter a license key")
            return

        # Show progress dialog
        progress_dialog = self.show_progress("Activating license...")

        try:
            license_client = LicenseClient(
                server_url=os.getenv('LICENSE_SERVER_URL', 'https://license.az1.ai'),
                api_key=os.getenv('LICENSE_API_KEY', '')
            )

            result = license_client.activate_license(license_key, get_hardware_id())

            if result.success:
                self.result = {'type': 'license', 'key': license_key, 'data': result.license_data}
                messagebox.showinfo("Success", "License activated successfully!")
                self.destroy()
            else:
                messagebox.showerror("Error", f"Activation failed:\\n{result.error}")

        except Exception as e:
            messagebox.showerror("Error", f"Activation failed:\\n{str(e)}")

        finally:
            progress_dialog.destroy()

    def start_trial(self):
        '''Start trial license'''
        email = self.trial_email_entry.get().strip()

        if not email or '@' not in email:
            messagebox.showerror("Error", "Please enter a valid email address")
            return

        progress_dialog = self.show_progress("Starting trial...")

        try:
            license_client = LicenseClient(...)
            trial = license_client.start_trial(email)

            self.result = {'type': 'trial', 'license': trial}
            messagebox.showinfo(
                "Success",
                f"Trial license activated!\\n\\nExpires: {trial.expiry_date}\\n\\nA confirmation email has been sent to {email}"
            )
            self.destroy()

        except Exception as e:
            messagebox.showerror("Error", f"Trial activation failed:\\n{str(e)}")

        finally:
            progress_dialog.destroy()

    def show_progress(self, message):
        '''Show indeterminate progress dialog'''
        dialog = tk.Toplevel(self)
        dialog.title("Please Wait")
        dialog.geometry("300x100")
        dialog.resizable(False, False)

        tk.Label(dialog, text=message, pady=20).pack()
        progress = ttk.Progressbar(dialog, mode='indeterminate')
        progress.pack(fill=tk.X, padx=20, pady=10)
        progress.start()

        dialog.transient(self)
        dialog.grab_set()

        return dialog

    def cancel(self):
        '''Cancel activation'''
        if messagebox.askyesno("Confirm Exit", "Exit without activating license?\\n\\nYou will not be able to use CODITECT without a valid license."):
            self.result = None
            self.destroy()

    def center_window(self):
        '''Center dialog on screen'''
        self.update_idletasks()
        width = self.winfo_width()
        height = self.winfo_height()
        x = (self.winfo_screenwidth() // 2) - (width // 2)
        y = (self.winfo_screenheight() // 2) - (height // 2)
        self.geometry(f'{width}x{height}+{x}+{y}')
```

2. **Integrate with InstallerGUI:**

Modify install_gui.py to check license before installation:

```python
class InstallerGUI:
    def __init__(self):
        # ... existing code ...

        # Check license on startup
        self.check_license()

    def check_license(self):
        '''Check for valid license before installation'''
        # Try to load existing license
        license_key = self.load_stored_license()

        if license_key:
            # Validate existing license
            validator = LicenseValidator(public_key=PUBLIC_KEY)
            status = validator.validate(license_key)

            if status.is_valid:
                self.log_message("✓ Valid license found")
                return True

        # No valid license, show activation dialog
        dialog = LicenseActivationDialog(self.window)

        if dialog.result:
            # License activated
            self.save_license(dialog.result)
            self.log_message("✓ License activated")
            return True
        else:
            # User canceled
            messagebox.showwarning("License Required", "A valid license is required to use CODITECT.")
            self.window.quit()
            return False
```

3. **Add "Manage License" Menu:**

Add menu option to view/change license:

```python
# In create_widgets()
menubar = tk.Menu(self.window)
self.window.config(menu=menubar)

license_menu = tk.Menu(menubar, tearoff=0)
menubar.add_cascade(label="License", menu=license_menu)
license_menu.add_command(label="View License Info", command=self.show_license_info)
license_menu.add_command(label="Activate New License", command=self.activate_new_license)
license_menu.add_separator()
license_menu.add_command(label="Deactivate License", command=self.deactivate_license)
```

**Deliverables:**
- Enhanced install_gui.py with LicenseActivationDialog
- License menu integration
- Visual testing (manual test checklist)

**Working Directory:** submodules/coditect-installer/
"""
)
```

---

## Phase 4: CI/CD & Cross-Platform Testing

### Task 4.1: Setup GitHub Actions Workflows

```python
Task(
    subagent_type="general-purpose",
    description="Setup GitHub Actions CI/CD workflows for CODITECT installer",
    prompt="""You are a DevOps Engineer setting up GitHub Actions CI/CD workflows for the CODITECT modular installer system.

**Context:**
- Test suite: (completed in Phase 2)
- License integration: (completed in Phase 3)
- Target platforms: Windows 10/11, macOS 12/13/14, Ubuntu 22.04/24.04
- Python versions: 3.8, 3.9, 3.10, 3.11, 3.12

**Your Task:**
Create complete CI/CD pipeline with GitHub Actions:

1. **Create Workflow Directory:**
```
submodules/coditect-installer/.github/workflows/
├── test-linux.yml
├── test-macos.yml
├── test-windows.yml
└── build-artifacts.yml
```

2. **Implement test-linux.yml:**

See orchestration plan for complete workflow YAML.

Key requirements:
- Matrix: Ubuntu 22.04 + 24.04
- Matrix: Python 3.8-3.12
- Install dependencies
- Run unit tests with coverage
- Run integration tests
- Upload coverage to Codecov
- Cache pip dependencies

3. **Implement test-macos.yml:**

Similar to Linux, but:
- Matrix: macOS-12, macOS-13, macOS-14
- Handle macOS-specific tkinter installation

4. **Implement test-windows.yml:**

Similar to Linux, but:
- Matrix: windows-2019, windows-2022
- Handle Windows path separators
- Use `python` not `python3`

5. **Implement build-artifacts.yml:**

Trigger: On release creation
Jobs:
- build-windows: Create MSI installer
- build-macos: Create DMG installer
- build-linux: Create AppImage + .deb

6. **Setup Codecov Integration:**

Add .codecov.yml:
```yaml
coverage:
  status:
    project:
      default:
        target: 95%
        threshold: 1%
    patch:
      default:
        target: 90%
```

7. **Add Status Badges to README:**

```markdown
![Tests](https://github.com/coditect-ai/coditect-installer/workflows/Test%20Linux/badge.svg)
![Coverage](https://codecov.io/gh/coditect-ai/coditect-installer/branch/main/graph/badge.svg)
```

**Deliverables:**
- .github/workflows/ with all 4 workflow files
- .codecov.yml configuration
- Updated README.md with badges
- All workflows passing

**Working Directory:** submodules/coditect-installer/

**Testing:**
1. Create PR to test workflows
2. Verify all platforms pass
3. Verify coverage uploaded
4. Verify badges display correctly
"""
)
```

---

## Phase 5: Documentation & Deployment

### Task 5.1: Update All Documentation

```python
Task(
    subagent_type="general-purpose",
    description="Update all documentation for CODITECT installer v2.0",
    prompt="""You are a Documentation Specialist updating all documentation for the CODITECT installer v2.0 release.

**Context:**
- Testing complete (Phase 2)
- Licensing complete (Phase 3)
- CI/CD complete (Phase 4)
- Quality score: 40/40 (target achieved)

**Your Task:**
Update ALL documentation to reflect v2.0 enhancements:

1. **Update README.md:**

Add sections:
- License activation instructions
- Trial license instructions
- Testing instructions (pytest, coverage)
- CI/CD status badges
- Updated installation steps with license activation
- Updated system requirements

2. **Update CLAUDE.md:**

Add sections:
- License integration architecture
- Testing infrastructure (pytest, coverage, tox)
- CI/CD workflows
- Mock license server
- Update status to "Production Ready - v2.0"
- Update quality score to 40/40

3. **Update SDD.md:**

Add sections:
- License integration architecture diagrams
- Testing architecture
- CI/CD architecture
- Deployment artifacts (MSI, DMG, AppImage)

4. **Update ADR.md:**

Document decisions:
- ADR-005: License Integration Strategy (online + offline validation)
- ADR-006: Testing Framework Choice (pytest + coverage + tox)
- ADR-007: CI/CD Platform Choice (GitHub Actions)
- ADR-008: Privacy-Compliant Telemetry (opt-in only, no PII)

5. **Update TDD.md:**

- Mark all tests as ✅ Implemented
- Update coverage metrics (95%+ achieved)
- Update test execution time
- Update platform coverage (3/3)

6. **Create Deployment Guide:**

New file: DEPLOYMENT.md

Sections:
- Prerequisites
- Building standalone executables
  - Windows MSI (PyInstaller + WiX)
  - macOS DMG (py2app + create-dmg)
  - Linux AppImage + .deb
- Deployment checklist
- Troubleshooting

7. **Create User Manual:**

New file: USER-MANUAL.md

Sections:
- Installation (GUI + CLI)
- License activation (license key + trial)
- Uninstallation
- Troubleshooting
- FAQ

8. **Create Developer Guide:**

New file: DEVELOPER-GUIDE.md

Sections:
- Development setup
- Running tests
- Adding new tests
- Modifying license integration
- Building artifacts locally
- Contributing guidelines

9. **Create Release Notes:**

New file: RELEASE-NOTES-v2.0.md

Sections:
- What's New in v2.0
  - ✅ 95%+ test coverage
  - ✅ License integration
  - ✅ CI/CD automation
  - ✅ Cross-platform builds
- Breaking Changes
- Migration Guide (v1.0 → v2.0)
- Known Issues

**Deliverables:**
- Updated README.md, CLAUDE.md, SDD.md, ADR.md, TDD.md
- New DEPLOYMENT.md
- New USER-MANUAL.md
- New DEVELOPER-GUIDE.md
- New RELEASE-NOTES-v2.0.md

**Working Directory:** submodules/coditect-installer/

**Quality Standards:**
- Clear, concise writing
- Code examples where appropriate
- Diagrams (Mermaid) for architecture
- Consistent formatting
- No typos or broken links
"""
)
```

---

## Summary: Task Execution Order

**Week 1 (Phase 1):**
1. Task 1.1: Design License Integration Architecture
2. Task 1.2: Create Comprehensive Test Plan
3. Checkpoint 1

**Week 2 (Phase 2 + Phase 3 Start):**
4. Task 2.1: Implement Unit Tests
5. Task 2.2: Implement Integration Tests
6. Checkpoint 2
7. Task 3.1: Implement License Client (starts Day 5)
8. Task 3.2: Implement GUI License Dialog (starts Day 5)

**Week 3 (Phase 3 Complete + Phase 4):**
9. Complete Task 3.1, 3.2
10. Checkpoint 3
11. Task 4.1: Setup GitHub Actions Workflows
12. Checkpoint 4

**Week 4 (Phase 5):**
13. Task 5.1: Update All Documentation
14. Final Quality Review
15. Checkpoint 5 (Production Ready v2.0)

---

## Notes

- All tasks use `subagent_type="general-purpose"` with detailed prompts
- Each task is self-contained with complete context
- Tasks can be executed in parallel where dependencies allow
- Checkpoints created after each major phase
- Total timeline: 3-4 weeks (60-80 engineering hours)

---

**Created:** 2025-11-17
**Status:** Ready for Execution
**Next Step:** Execute Task 1.1 (Design License Integration Architecture)
