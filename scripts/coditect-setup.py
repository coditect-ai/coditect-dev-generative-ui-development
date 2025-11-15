#!/usr/bin/env python3

"""
AZ1.AI CODITECT Setup Tool

Copyright © 2025 AZ1.AI INC. All Rights Reserved.
Developed by Hal Casteel, Founder/CEO/CTO, AZ1.AI INC.

Purpose: Automated setup for CODITECT users with cloud platform integration
- User authentication via CODITECT Cloud Platform
- License agreement acceptance (EULA, NDA)
- Token-based framework download
- Workspace initialization
- Tutorial launch
"""

import os
import sys
import subprocess
import json
import hashlib
import platform
from pathlib import Path
from typing import Optional, Dict, Any
import urllib.request
import urllib.parse
import urllib.error
from datetime import datetime

# Configuration
CLOUD_PLATFORM_URL = os.getenv("CODITECT_CLOUD_URL", "https://api.cloud.coditect.ai/v1")
WORKSPACE_DIR = Path.home() / "PROJECTS"
CODITECT_REPO = "https://github.com/coditect-ai/coditect-project-dot-claude.git"
CONFIG_FILE = Path.home() / ".coditect" / "config.json"

# Colors for terminal output
class Colors:
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    END = '\033[0m'


class CoditectSetup:
    """Main setup orchestrator for CODITECT"""

    def __init__(self):
        self.config = self.load_config()
        self.is_offline = os.getenv("CODITECT_OFFLINE", "false").lower() == "true"

    def load_config(self) -> Dict[str, Any]:
        """Load existing configuration if available"""
        if CONFIG_FILE.exists():
            with open(CONFIG_FILE, 'r') as f:
                return json.load(f)
        return {}

    def save_config(self):
        """Save configuration to disk"""
        CONFIG_FILE.parent.mkdir(parents=True, exist_ok=True)
        with open(CONFIG_FILE, 'w') as f:
            json.dump(self.config, f, indent=2)
        os.chmod(CONFIG_FILE, 0o600)  # Restrict permissions

    def print_header(self):
        """Print welcome header"""
        print(f"\n{Colors.CYAN}{Colors.BOLD}{'='*68}{Colors.END}")
        print(f"{Colors.CYAN}{Colors.BOLD}                                                                    {Colors.END}")
        print(f"{Colors.CYAN}{Colors.BOLD}         AZ1.AI CODITECT Setup Tool v1.0                            {Colors.END}")
        print(f"{Colors.CYAN}{Colors.BOLD}                                                                    {Colors.END}")
        print(f"{Colors.CYAN}{Colors.BOLD}   AI-First Project Management & Development Platform               {Colors.END}")
        print(f"{Colors.CYAN}{Colors.BOLD}                                                                    {Colors.END}")
        print(f"{Colors.CYAN}{Colors.BOLD}   Copyright © 2025 AZ1.AI INC. All Rights Reserved.                {Colors.END}")
        print(f"{Colors.CYAN}{Colors.BOLD}   Developed by Hal Casteel, Founder/CEO/CTO                        {Colors.END}")
        print(f"{Colors.CYAN}{Colors.BOLD}                                                                    {Colors.END}")
        print(f"{Colors.CYAN}{Colors.BOLD}{'='*68}{Colors.END}\n")

    def check_prerequisites(self) -> bool:
        """Check system prerequisites"""
        print(f"{Colors.BLUE}{Colors.BOLD}▶ Checking prerequisites...{Colors.END}\n")

        # Check Python version
        if sys.version_info < (3, 8):
            print(f"{Colors.RED}✗ Python 3.8+ required (found {sys.version}){Colors.END}")
            return False
        print(f"{Colors.GREEN}✓ Python {sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}{Colors.END}")

        # Check git
        try:
            result = subprocess.run(['git', '--version'], capture_output=True, text=True)
            if result.returncode == 0:
                print(f"{Colors.GREEN}✓ Git installed: {result.stdout.strip()}{Colors.END}")
            else:
                print(f"{Colors.RED}✗ Git not found{Colors.END}")
                return False
        except FileNotFoundError:
            print(f"{Colors.RED}✗ Git not installed{Colors.END}")
            return False

        # Check internet connectivity (unless offline mode)
        if not self.is_offline:
            try:
                urllib.request.urlopen('https://www.google.com', timeout=5)
                print(f"{Colors.GREEN}✓ Internet connection available{Colors.END}")
            except urllib.error.URLError:
                print(f"{Colors.YELLOW}⚠ No internet connection (offline mode enabled){Colors.END}")
                self.is_offline = True

        return True

    def authenticate_user(self) -> bool:
        """Authenticate user with CODITECT Cloud Platform"""
        if self.is_offline:
            print(f"\n{Colors.YELLOW}ℹ Offline mode: Skipping cloud authentication{Colors.END}")
            return True

        print(f"\n{Colors.BLUE}{Colors.BOLD}▶ Authenticating with CODITECT Cloud Platform...{Colors.END}\n")

        # Check if already authenticated
        if 'access_token' in self.config and 'token_expiry' in self.config:
            # Validate token hasn't expired
            expiry = datetime.fromisoformat(self.config['token_expiry'])
            if datetime.now() < expiry:
                print(f"{Colors.GREEN}✓ Already authenticated as: {self.config.get('user_email')}{Colors.END}")
                return True

        # New authentication flow
        print(f"{Colors.YELLOW}Authentication required.{Colors.END}\n")
        print("Options:")
        print("  1. Login with existing account (via web browser)")
        print("  2. Register new account")
        print("  3. Use access token (if you have one)")

        choice = input("\nSelect option [1-3]: ").strip()

        if choice == '1':
            return self.login_via_browser()
        elif choice == '2':
            return self.register_new_user()
        elif choice == '3':
            return self.login_via_token()
        else:
            print(f"{Colors.RED}Invalid option{Colors.END}")
            return False

    def login_via_browser(self) -> bool:
        """Open browser for OAuth login"""
        print(f"\n{Colors.YELLOW}Opening browser for authentication...{Colors.END}")

        # Generate device code
        try:
            device_code_url = f"{CLOUD_PLATFORM_URL}/auth/device"
            req = urllib.request.Request(device_code_url, method='POST')
            req.add_header('Content-Type', 'application/json')

            with urllib.request.urlopen(req) as response:
                data = json.loads(response.read().decode())
                device_code = data['device_code']
                user_code = data['user_code']
                verification_url = data['verification_url']

            print(f"\n{Colors.BOLD}Please visit: {Colors.CYAN}{verification_url}{Colors.END}")
            print(f"{Colors.BOLD}Enter code: {Colors.CYAN}{user_code}{Colors.END}\n")

            # Try to open browser automatically
            try:
                import webbrowser
                webbrowser.open(verification_url)
            except:
                pass

            # Poll for authentication
            print("Waiting for authentication...")
            return self.poll_for_auth(device_code)

        except Exception as e:
            print(f"{Colors.RED}✗ Authentication failed: {e}{Colors.END}")
            return False

    def poll_for_auth(self, device_code: str) -> bool:
        """Poll API for device code authorization"""
        import time

        poll_url = f"{CLOUD_PLATFORM_URL}/auth/device/poll"
        max_attempts = 60  # 5 minutes with 5-second intervals

        for attempt in range(max_attempts):
            try:
                req = urllib.request.Request(poll_url, method='POST')
                req.add_header('Content-Type', 'application/json')
                data = json.dumps({'device_code': device_code}).encode()

                with urllib.request.urlopen(req, data=data) as response:
                    result = json.loads(response.read().decode())

                    if result['status'] == 'authorized':
                        self.config['access_token'] = result['access_token']
                        self.config['refresh_token'] = result['refresh_token']
                        self.config['token_expiry'] = result['expires_at']
                        self.config['user_email'] = result['user']['email']
                        self.config['user_id'] = result['user']['id']
                        self.save_config()

                        print(f"\n{Colors.GREEN}✓ Authentication successful!{Colors.END}")
                        print(f"{Colors.GREEN}  Welcome, {result['user']['email']}!{Colors.END}")
                        return True

                    elif result['status'] == 'pending':
                        time.sleep(5)
                        continue

                    else:
                        print(f"{Colors.RED}✗ Authentication failed{Colors.END}")
                        return False

            except urllib.error.HTTPError as e:
                if e.code == 400:
                    time.sleep(5)
                    continue
                else:
                    print(f"{Colors.RED}✗ HTTP Error: {e.code}{Colors.END}")
                    return False

        print(f"{Colors.RED}✗ Authentication timeout{Colors.END}")
        return False

    def register_new_user(self) -> bool:
        """Register new user account"""
        print(f"\n{Colors.BLUE}{Colors.BOLD}▶ User Registration{Colors.END}\n")

        email = input("Email address: ").strip()
        if not email or '@' not in email:
            print(f"{Colors.RED}✗ Invalid email address{Colors.END}")
            return False

        full_name = input("Full name: ").strip()
        organization = input("Organization (optional): ").strip() or None

        print("\nUser type:")
        print("  1. Individual developer")
        print("  2. Team")
        print("  3. Business")
        print("  4. Consultant")
        print("  5. Auditor")

        user_type_choice = input("Select [1-5]: ").strip()
        user_type_map = {
            '1': 'individual',
            '2': 'team',
            '3': 'business',
            '4': 'consultant',
            '5': 'auditor'
        }
        user_type = user_type_map.get(user_type_choice, 'individual')

        # Create registration request
        try:
            reg_data = {
                'email': email,
                'full_name': full_name,
                'organization': organization,
                'user_type': user_type
            }

            req = urllib.request.Request(f"{CLOUD_PLATFORM_URL}/auth/register", method='POST')
            req.add_header('Content-Type', 'application/json')
            data = json.dumps(reg_data).encode()

            with urllib.request.urlopen(req, data=data) as response:
                result = json.loads(response.read().decode())

                print(f"\n{Colors.GREEN}✓ Registration successful!{Colors.END}")
                print(f"\n{Colors.YELLOW}Check your email ({email}) to verify your account.{Colors.END}")
                print(f"{Colors.YELLOW}After verification, admin approval may be required.{Colors.END}")

                return True

        except urllib.error.HTTPError as e:
            error_body = e.read().decode()
            print(f"{Colors.RED}✗ Registration failed: {error_body}{Colors.END}")
            return False
        except Exception as e:
            print(f"{Colors.RED}✗ Registration failed: {e}{Colors.END}")
            return False

    def login_via_token(self) -> bool:
        """Login using existing access token"""
        print(f"\n{Colors.YELLOW}Enter your access token:{Colors.END}")
        token = input("Token: ").strip()

        if not token:
            print(f"{Colors.RED}✗ Token required{Colors.END}")
            return False

        # Validate token with API
        try:
            req = urllib.request.Request(f"{CLOUD_PLATFORM_URL}/auth/verify")
            req.add_header('Authorization', f'Bearer {token}')

            with urllib.request.urlopen(req) as response:
                result = json.loads(response.read().decode())

                self.config['access_token'] = token
                self.config['token_expiry'] = result['expires_at']
                self.config['user_email'] = result['user']['email']
                self.config['user_id'] = result['user']['id']
                self.save_config()

                print(f"\n{Colors.GREEN}✓ Token validated!{Colors.END}")
                print(f"{Colors.GREEN}  Welcome, {result['user']['email']}!{Colors.END}")
                return True

        except urllib.error.HTTPError as e:
            print(f"{Colors.RED}✗ Invalid token: {e.code}{Colors.END}")
            return False
        except Exception as e:
            print(f"{Colors.RED}✗ Token validation failed: {e}{Colors.END}")
            return False

    def accept_licenses(self) -> bool:
        """Accept EULA and NDA"""
        if self.is_offline:
            print(f"\n{Colors.YELLOW}ℹ Offline mode: Skipping license acceptance (will be required on first online use){Colors.END}")
            return True

        print(f"\n{Colors.BLUE}{Colors.BOLD}▶ License Agreements{Colors.END}\n")

        # Check if licenses already accepted
        try:
            req = urllib.request.Request(f"{CLOUD_PLATFORM_URL}/licenses/status")
            req.add_header('Authorization', f"Bearer {self.config['access_token']}")

            with urllib.request.urlopen(req) as response:
                result = json.loads(response.read().decode())

                if result.get('eula_accepted') and result.get('nda_accepted'):
                    print(f"{Colors.GREEN}✓ Licenses already accepted{Colors.END}")
                    return True

        except Exception:
            pass  # Continue to accept licenses

        # Fetch and display EULA
        print(f"{Colors.BOLD}End User License Agreement (EULA){Colors.END}\n")
        print("Fetching EULA...")

        try:
            req = urllib.request.Request(f"{CLOUD_PLATFORM_URL}/licenses/eula/latest")
            with urllib.request.urlopen(req) as response:
                eula = json.loads(response.read().decode())
                print(f"\n{eula['content'][:500]}...")  # Show first 500 chars
                print(f"\n[Full EULA: {eula['url']}]\n")

            accept_eula = input("Do you accept the EULA? (yes/no): ").strip().lower()
            if accept_eula != 'yes':
                print(f"{Colors.RED}✗ EULA acceptance required to continue{Colors.END}")
                return False

            # Fetch and display NDA
            print(f"\n{Colors.BOLD}Non-Disclosure Agreement (NDA){Colors.END}\n")
            print("Fetching NDA...")

            req = urllib.request.Request(f"{CLOUD_PLATFORM_URL}/licenses/nda/latest")
            with urllib.request.urlopen(req) as response:
                nda = json.loads(response.read().decode())
                print(f"\n{nda['content'][:500]}...")
                print(f"\n[Full NDA: {nda['url']}]\n")

            accept_nda = input("Do you accept the NDA? (yes/no): ").strip().lower()
            if accept_nda != 'yes':
                print(f"{Colors.RED}✗ NDA acceptance required to continue{Colors.END}")
                return False

            # Submit acceptances
            req = urllib.request.Request(f"{CLOUD_PLATFORM_URL}/licenses/accept", method='POST')
            req.add_header('Authorization', f"Bearer {self.config['access_token']}")
            req.add_header('Content-Type', 'application/json')
            data = json.dumps({
                'eula_version': eula['version'],
                'nda_version': nda['version'],
                'accepted_at': datetime.now().isoformat()
            }).encode()

            with urllib.request.urlopen(req, data=data) as response:
                print(f"\n{Colors.GREEN}✓ Licenses accepted and recorded{Colors.END}")
                return True

        except Exception as e:
            print(f"{Colors.RED}✗ License acceptance failed: {e}{Colors.END}")
            return False

    def create_workspace(self) -> bool:
        """Create PROJECTS workspace structure"""
        print(f"\n{Colors.BLUE}{Colors.BOLD}▶ Creating workspace structure...{Colors.END}\n")

        try:
            # Create workspace directory
            WORKSPACE_DIR.mkdir(parents=True, exist_ok=True)
            print(f"{Colors.GREEN}✓ Created: {WORKSPACE_DIR}{Colors.END}")

            # Initialize git if needed
            if not (WORKSPACE_DIR / ".git").exists():
                subprocess.run(['git', 'init'], cwd=WORKSPACE_DIR, check=True, capture_output=True)
                subprocess.run(['git', 'branch', '-m', 'main'], cwd=WORKSPACE_DIR, check=True, capture_output=True)
                print(f"{Colors.GREEN}✓ Initialized git repository{Colors.END}")

            return True

        except Exception as e:
            print(f"{Colors.RED}✗ Workspace creation failed: {e}{Colors.END}")
            return False

    def download_framework(self) -> bool:
        """Download CODITECT framework"""
        print(f"\n{Colors.BLUE}{Colors.BOLD}▶ Downloading CODITECT framework...{Colors.END}\n")

        coditect_dir = WORKSPACE_DIR / ".coditect"

        try:
            # Remove existing if present
            if coditect_dir.exists():
                print(f"{Colors.YELLOW}ℹ Removing existing .coditect directory{Colors.END}")
                import shutil
                shutil.rmtree(coditect_dir)

            # Add as submodule
            result = subprocess.run(
                ['git', 'submodule', 'add', CODITECT_REPO, '.coditect'],
                cwd=WORKSPACE_DIR,
                capture_output=True,
                text=True
            )

            if result.returncode != 0:
                # Try updating existing submodule
                subprocess.run(
                    ['git', 'submodule', 'update', '--init', '--remote', '.coditect'],
                    cwd=WORKSPACE_DIR,
                    check=True,
                    capture_output=True
                )

            # Log download to cloud platform (if authenticated)
            if not self.is_offline and 'access_token' in self.config:
                try:
                    req = urllib.request.Request(f"{CLOUD_PLATFORM_URL}/framework/log-download", method='POST')
                    req.add_header('Authorization', f"Bearer {self.config['access_token']}")
                    req.add_header('Content-Type', 'application/json')
                    data = json.dumps({'version': 'latest'}).encode()
                    urllib.request.urlopen(req, data=data)
                except:
                    pass  # Don't fail setup if logging fails

            print(f"{Colors.GREEN}✓ CODITECT framework installed{Colors.END}")
            return True

        except Exception as e:
            print(f"{Colors.RED}✗ Framework download failed: {e}{Colors.END}")
            return False

    def setup_llm_symlinks(self) -> bool:
        """Create symlinks for multiple LLM CLIs"""
        print(f"\n{Colors.BLUE}{Colors.BOLD}▶ Setting up multi-LLM CLI integration...{Colors.END}\n")

        llms = ['claude', 'gemini', 'copilot', 'cursor', 'grok', 'cody']

        for llm in llms:
            symlink_path = WORKSPACE_DIR / f".{llm}"

            try:
                if symlink_path.exists() or symlink_path.is_symlink():
                    symlink_path.unlink()

                symlink_path.symlink_to('.coditect')
                print(f"{Colors.GREEN}✓ Created .{llm} → .coditect{Colors.END}")

            except Exception as e:
                print(f"{Colors.YELLOW}⚠ Could not create .{llm} symlink: {e}{Colors.END}")

        return True

    def create_memory_context(self) -> bool:
        """Create MEMORY-CONTEXT directory"""
        print(f"\n{Colors.BLUE}{Colors.BOLD}▶ Creating MEMORY-CONTEXT directory...{Colors.END}\n")

        memory_dir = WORKSPACE_DIR / "MEMORY-CONTEXT"

        try:
            memory_dir.mkdir(exist_ok=True)

            # Copy README template if available
            template = WORKSPACE_DIR / ".coditect" / "templates" / "MEMORY-CONTEXT-README.md"
            readme = memory_dir / "README.md"

            if template.exists() and not readme.exists():
                import shutil
                shutil.copy(template, readme)
                print(f"{Colors.GREEN}✓ Created MEMORY-CONTEXT/README.md from template{Colors.END}")
            else:
                # Create basic README
                with open(readme, 'w') as f:
                    f.write("# MEMORY-CONTEXT\n\n")
                    f.write("**Session Exports and Development History**\n\n")
                    f.write("See ~/PROJECTS/.coditect/MEMORY-CONTEXT-GUIDE.md for usage.\n\n")
                    f.write("**Copyright © 2025 AZ1.AI INC. All Rights Reserved.**\n")
                print(f"{Colors.GREEN}✓ Created MEMORY-CONTEXT directory{Colors.END}")

            return True

        except Exception as e:
            print(f"{Colors.RED}✗ MEMORY-CONTEXT creation failed: {e}{Colors.END}")
            return False

    def configure_gitignore(self) -> bool:
        """Configure .gitignore"""
        print(f"\n{Colors.BLUE}{Colors.BOLD}▶ Configuring .gitignore...{Colors.END}\n")

        gitignore_path = WORKSPACE_DIR / ".gitignore"

        gitignore_content = """# Symlinks to .coditect (project-specific, not version controlled)
.claude
.gemini
.copilot
.cursor
.grok
.cody

# Individual project directories (have their own git repos)
*/

# Memory context files (session exports and summaries)
MEMORY-CONTEXT/

# macOS
.DS_Store

# Keep only the framework structure
!.gitignore
!.gitmodules
!README.md
!SETUP-SUMMARY.md
"""

        try:
            with open(gitignore_path, 'w') as f:
                f.write(gitignore_content)

            print(f"{Colors.GREEN}✓ .gitignore configured{Colors.END}")
            return True

        except Exception as e:
            print(f"{Colors.RED}✗ .gitignore configuration failed: {e}{Colors.END}")
            return False

    def create_workspace_readme(self) -> bool:
        """Create workspace README"""
        print(f"\n{Colors.BLUE}{Colors.BOLD}▶ Creating workspace README...{Colors.END}\n")

        readme_path = WORKSPACE_DIR / "README.md"

        readme_content = f"""# AZ1.AI CODITECT PROJECTS Workspace

**AI-First Project Management & Development Platform**

**Copyright © 2025 AZ1.AI INC. All Rights Reserved.**
**Developed by Hal Casteel, Founder/CEO/CTO, AZ1.AI INC.**

---

## Setup Date

{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

## Quick Start

```bash
# Launch tutorial
.coditect/scripts/coditect-tutorial.sh

# Read quickstart guide
cat .coditect/AZ1.AI-CODITECT-1-2-3-QUICKSTART.md

# Create first project
mkdir my-first-project
cd my-first-project
```

## Documentation

See `.coditect/` directory for complete documentation.

**Built with Excellence by AZ1.AI CODITECT**
"""

        try:
            with open(readme_path, 'w') as f:
                f.write(readme_content)

            print(f"{Colors.GREEN}✓ README.md created{Colors.END}")
            return True

        except Exception as e:
            print(f"{Colors.RED}✗ README creation failed: {e}{Colors.END}")
            return False

    def commit_structure(self) -> bool:
        """Commit workspace structure"""
        print(f"\n{Colors.BLUE}{Colors.BOLD}▶ Committing workspace structure...{Colors.END}\n")

        try:
            subprocess.run(
                ['git', 'add', '.coditect', '.gitignore', '.gitmodules', 'README.md'],
                cwd=WORKSPACE_DIR,
                check=True,
                capture_output=True
            )

            commit_message = """Initialize AZ1.AI CODITECT workspace

- Add .coditect framework as submodule
- Configure multi-LLM CLI symlinks
- Create MEMORY-CONTEXT directory
- Setup workspace structure

Copyright © 2025 AZ1.AI INC. All Rights Reserved."""

            result = subprocess.run(
                ['git', 'commit', '-m', commit_message],
                cwd=WORKSPACE_DIR,
                capture_output=True,
                text=True
            )

            if result.returncode == 0 or "nothing to commit" in result.stdout:
                print(f"{Colors.GREEN}✓ Workspace structure committed{Colors.END}")
                return True

        except Exception as e:
            print(f"{Colors.YELLOW}⚠ Commit failed (non-fatal): {e}{Colors.END}")
            return True  # Non-fatal

    def launch_tutorial(self) -> bool:
        """Launch interactive tutorial"""
        print(f"\n{Colors.BLUE}{Colors.BOLD}▶ Setup complete!{Colors.END}\n")

        print(f"{Colors.GREEN}{Colors.BOLD}╔════════════════════════════════════════════════════════════════╗{Colors.END}")
        print(f"{Colors.GREEN}{Colors.BOLD}║                                                                ║{Colors.END}")
        print(f"{Colors.GREEN}{Colors.BOLD}║                    SETUP COMPLETE! 🎉                          ║{Colors.END}")
        print(f"{Colors.GREEN}{Colors.BOLD}║                                                                ║{Colors.END}")
        print(f"{Colors.GREEN}{Colors.BOLD}╚════════════════════════════════════════════════════════════════╝{Colors.END}\n")

        print(f"{Colors.CYAN}Your CODITECT workspace is ready at: {Colors.BOLD}{WORKSPACE_DIR}{Colors.END}\n")

        response = input(f"{Colors.YELLOW}Launch interactive tutorial now? (y/n): {Colors.END}").strip().lower()

        if response == 'y':
            tutorial_script = WORKSPACE_DIR / ".coditect" / "scripts" / "coditect-tutorial.sh"
            if tutorial_script.exists():
                subprocess.run(['bash', str(tutorial_script)])
            else:
                print(f"{Colors.RED}✗ Tutorial script not found{Colors.END}")
                return False
        else:
            print(f"\n{Colors.YELLOW}You can launch the tutorial later with:{Colors.END}")
            print(f"{Colors.CYAN}  bash {WORKSPACE_DIR}/.coditect/scripts/coditect-tutorial.sh{Colors.END}\n")

        return True

    def run(self) -> int:
        """Main setup flow"""
        self.print_header()

        steps = [
            ("Prerequisites", self.check_prerequisites),
            ("Authentication", self.authenticate_user),
            ("License Acceptance", self.accept_licenses),
            ("Workspace Creation", self.create_workspace),
            ("Framework Download", self.download_framework),
            ("LLM Symlinks", self.setup_llm_symlinks),
            ("MEMORY-CONTEXT", self.create_memory_context),
            ("Gitignore", self.configure_gitignore),
            ("README", self.create_workspace_readme),
            ("Git Commit", self.commit_structure),
        ]

        for step_name, step_func in steps:
            if not step_func():
                print(f"\n{Colors.RED}✗ Setup failed at: {step_name}{Colors.END}")
                return 1

        self.launch_tutorial()
        return 0


def main():
    """Entry point"""
    setup = CoditectSetup()
    sys.exit(setup.run())


if __name__ == '__main__':
    main()
