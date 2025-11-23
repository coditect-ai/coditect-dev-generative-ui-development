#!/usr/bin/env python3

"""
AZ1.AI CODITECT Git Helper

Copyright © 2025 AZ1.AI INC. All Rights Reserved.
Developed by Hal Casteel, Founder/CEO/CTO, AZ1.AI INC.

Purpose: Automated Git workflow management for non-Git-expert users
- Automatic session management with branches
- Regular auto-commits during work sessions
- Branch management (create, switch, merge)
- Pull request creation
- Sync with GitHub (push/pull)
- Safe, beginner-friendly Git operations
"""

import os
import sys
import subprocess
import json
import logging
from pathlib import Path
from datetime import datetime
from typing import Optional, List, Dict, Any
import time

# Custom Exceptions
class GitHelperError(Exception):
    """Base exception for Git Helper errors."""
    pass


class GitOperationError(GitHelperError):
    """Raised when git operation fails."""
    pass


class GitHubOperationError(GitHelperError):
    """Raised when GitHub operation fails."""
    pass


class SessionError(GitHelperError):
    """Raised when session management fails."""
    pass


class ValidationError(GitHelperError):
    """Raised when input validation fails."""
    pass


class NetworkError(GitHelperError):
    """Raised when network operations fail."""
    pass


class ConfigurationError(GitHelperError):
    """Raised when configuration is invalid."""
    pass


# Colors
class Colors:
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BOLD = '\033[1m'
    END = '\033[0m'


# Dual Logging Setup
def setup_logging(project_dir: Path) -> logging.Logger:
    """
    Setup dual logging to both file and stdout.

    Args:
        project_dir: Project directory path

    Returns:
        Configured logger instance
    """
    # Create logs directory
    logs_dir = project_dir / 'logs'
    logs_dir.mkdir(exist_ok=True)

    # Create log file with timestamp
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    log_file = logs_dir / f'coditect-git-helper_{timestamp}.log'

    # Configure logger
    logger = logging.getLogger('GitHelper')
    logger.setLevel(logging.DEBUG)

    # File handler - detailed logging
    file_handler = logging.FileHandler(log_file)
    file_handler.setLevel(logging.DEBUG)
    file_formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    file_handler.setFormatter(file_formatter)

    # Console handler - user-friendly logging
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(logging.INFO)
    console_formatter = logging.Formatter('%(message)s')
    console_handler.setFormatter(console_formatter)

    # Add handlers
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    logger.info(f"Logging initialized: {log_file}")

    return logger


def retry_operation(max_retries: int = 3, delay: float = 1.0, backoff: float = 2.0):
    """
    Decorator for retrying operations with exponential backoff.

    Args:
        max_retries: Maximum number of retry attempts
        delay: Initial delay in seconds
        backoff: Backoff multiplier for each retry

    Returns:
        Decorated function with retry logic
    """
    def decorator(func):
        def wrapper(*args, **kwargs):
            current_delay = delay
            for attempt in range(max_retries):
                try:
                    return func(*args, **kwargs)
                except (NetworkError, subprocess.CalledProcessError) as e:
                    if attempt == max_retries - 1:
                        raise
                    logger = logging.getLogger('GitHelper')
                    logger.warning(
                        f"Attempt {attempt + 1}/{max_retries} failed: {e}. "
                        f"Retrying in {current_delay:.1f}s..."
                    )
                    time.sleep(current_delay)
                    current_delay *= backoff
            return func(*args, **kwargs)
        return wrapper
    return decorator


class GitHelper:
    """Automated Git workflow manager"""

    def __init__(self, project_dir: Path = None):
        self.project_dir = project_dir or Path.cwd()
        self.config_file = self.project_dir / ".coditect-git-config.json"
        self.session_file = self.project_dir / ".coditect-session.json"
        self.session_backup_file = self.project_dir / ".coditect-session-backup.json"

        # Initialize logger
        self.logger = setup_logging(self.project_dir)

        # Load configuration and session with error handling
        try:
            self.config = self.load_config()
            self.session = self.load_session()
            self.logger.debug("GitHelper initialized successfully")
        except Exception as e:
            self.logger.error(f"Failed to initialize GitHelper: {e}")
            raise ConfigurationError(f"Initialization failed: {e}")

    def load_config(self) -> Dict[str, Any]:
        """Load Git helper configuration"""
        if self.config_file.exists():
            with open(self.config_file, 'r') as f:
                return json.load(f)

        # Default configuration
        return {
            'auto_commit_interval': 15,  # minutes
            'auto_push_interval': 30,    # minutes
            'branch_naming_pattern': '{date}-{description}',
            'commit_message_template': '{action}: {description}\n\nSession: {session_id}\nTimestamp: {timestamp}',
            'main_branch': 'main',
            'enable_auto_sync': True,
            'enable_branch_per_session': True,
            'enable_auto_cleanup': True
        }

    def save_config(self):
        """Save configuration with error handling."""
        try:
            with open(self.config_file, 'w') as f:
                json.dump(self.config, f, indent=2)
            self.logger.debug("Configuration saved successfully")
        except Exception as e:
            self.logger.error(f"Failed to save configuration: {e}")
            raise ConfigurationError(f"Failed to save configuration: {e}")

    def load_session(self) -> Dict[str, Any]:
        """Load current session with backup recovery."""
        try:
            if self.session_file.exists():
                with open(self.session_file, 'r') as f:
                    session = json.load(f)
                    self.logger.debug("Session loaded successfully")
                    return session
        except Exception as e:
            self.logger.warning(f"Failed to load session file: {e}")
            # Try to recover from backup
            if self.session_backup_file.exists():
                try:
                    self.logger.info("Attempting to recover from session backup...")
                    with open(self.session_backup_file, 'r') as f:
                        session = json.load(f)
                    self.logger.info("Session recovered from backup")
                    return session
                except Exception as backup_error:
                    self.logger.error(f"Failed to recover from backup: {backup_error}")

        return {}

    def save_session(self):
        """Save session state with backup."""
        try:
            # Create backup of existing session if it exists
            if self.session_file.exists():
                import shutil
                shutil.copy(self.session_file, self.session_backup_file)
                self.logger.debug("Session backup created")

            # Save new session state
            with open(self.session_file, 'w') as f:
                json.dump(self.session, f, indent=2)
            self.logger.debug("Session saved successfully")
        except Exception as e:
            self.logger.error(f"Failed to save session: {e}")
            raise SessionError(f"Failed to save session: {e}")

    def run_git(self, args: List[str], check=True, capture_output=True) -> subprocess.CompletedProcess:
        """
        Run git command with error handling and logging.

        Args:
            args: Git command arguments
            check: Raise exception on non-zero exit
            capture_output: Capture stdout/stderr

        Returns:
            CompletedProcess result

        Raises:
            GitOperationError: If git command fails
        """
        try:
            self.logger.debug(f"Running git command: {' '.join(args)}")
            result = subprocess.run(
                ['git'] + args,
                cwd=self.project_dir,
                check=check,
                capture_output=capture_output,
                text=True
            )
            self.logger.debug(f"Git command completed: {result.returncode}")
            return result
        except subprocess.CalledProcessError as e:
            if not check:
                return e
            error_msg = f"Git command failed: {' '.join(args)}"
            self.logger.error(error_msg)
            self.logger.error(f"Exit code: {e.returncode}")
            self.logger.error(f"Error output: {e.stderr}")
            print(f"{Colors.RED}✗ {error_msg}{Colors.END}")
            print(f"{Colors.RED}  Error: {e.stderr}{Colors.END}")
            raise GitOperationError(f"{error_msg}: {e.stderr}")
        except Exception as e:
            error_msg = f"Unexpected error running git command: {e}"
            self.logger.error(error_msg)
            raise GitOperationError(error_msg)

    def is_git_repo(self) -> bool:
        """Check if directory is a Git repository"""
        return (self.project_dir / ".git").exists()

    def get_current_branch(self) -> str:
        """Get current Git branch"""
        result = self.run_git(['branch', '--show-current'])
        return result.stdout.strip()

    def get_remote_url(self) -> Optional[str]:
        """Get remote repository URL"""
        try:
            result = self.run_git(['remote', 'get-url', 'origin'], check=False)
            if result.returncode == 0:
                return result.stdout.strip()
        except:
            pass
        return None

    def has_uncommitted_changes(self) -> bool:
        """Check for uncommitted changes"""
        result = self.run_git(['status', '--porcelain'])
        return bool(result.stdout.strip())

    def has_unpushed_commits(self) -> bool:
        """Check for unpushed commits"""
        try:
            # Check if remote tracking branch exists
            self.run_git(['rev-parse', '--abbrev-ref', '@{u}'])

            # Compare local with remote
            result = self.run_git(['rev-list', '@{u}..HEAD', '--count'])
            return int(result.stdout.strip()) > 0
        except:
            # No remote tracking branch
            return True

    def initialize_repo(self):
        """Initialize Git repository if needed"""
        print(f"{Colors.BLUE}▶ Initializing Git repository...{Colors.END}")

        if not self.is_git_repo():
            self.run_git(['init'])
            self.run_git(['branch', '-m', self.config['main_branch']])
            print(f"{Colors.GREEN}✓ Git repository initialized{Colors.END}")

            # Create initial .gitignore
            self.create_gitignore()
        else:
            print(f"{Colors.GREEN}✓ Git repository already initialized{Colors.END}")

    def create_gitignore(self):
        """Create project .gitignore from CODITECT template"""
        gitignore_path = self.project_dir / ".gitignore"

        # Try to use CODITECT universal template if available
        template_path = self.project_dir / ".coditect" / "templates" / "gitignore-universal-template"

        if template_path.exists():
            # Copy universal template
            import shutil
            shutil.copy(template_path, gitignore_path)
            print(f"{Colors.GREEN}✓ Created .gitignore from CODITECT universal template{Colors.END}")
        elif not gitignore_path.exists():
            # Fallback to basic gitignore
            gitignore_content = """# CODITECT Session Files
.coditect-session.json
.coditect-git-config.json

# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
venv/
env/

# Node
node_modules/
npm-debug.log*

# IDEs
.vscode/
.idea/
*.swp
*.swo

# OS
.DS_Store
Thumbs.db

# Build outputs
dist/
build/
*.egg-info/

# Logs
*.log
logs/

# Environment
.env
.env.local
"""
            with open(gitignore_path, 'w') as f:
                f.write(gitignore_content)
            print(f"{Colors.GREEN}✓ Created basic .gitignore{Colors.END}")

    def setup_remote(self, remote_url: str):
        """Setup GitHub remote"""
        print(f"{Colors.BLUE}▶ Setting up GitHub remote...{Colors.END}")

        current_remote = self.get_remote_url()

        if current_remote:
            if current_remote == remote_url:
                print(f"{Colors.GREEN}✓ Remote already configured{Colors.END}")
            else:
                print(f"{Colors.YELLOW}⚠ Updating remote URL{Colors.END}")
                self.run_git(['remote', 'set-url', 'origin', remote_url])
        else:
            self.run_git(['remote', 'add', 'origin', remote_url])
            print(f"{Colors.GREEN}✓ Remote 'origin' added{Colors.END}")

    def start_session(self, description: str = "work session"):
        """Start new work session"""
        print(f"\n{Colors.BLUE}{Colors.BOLD}▶ Starting work session...{Colors.END}\n")

        # Generate session ID
        session_id = datetime.now().strftime("%Y%m%d-%H%M%S")

        # Create session branch if enabled
        branch_name = self.config['main_branch']
        if self.config.get('enable_branch_per_session', True):
            date_str = datetime.now().strftime("%Y-%m-%d")
            branch_name = f"session/{date_str}-{description.replace(' ', '-')}"

            # Create and checkout branch
            current_branch = self.get_current_branch()
            if current_branch != branch_name:
                try:
                    self.run_git(['checkout', '-b', branch_name])
                    print(f"{Colors.GREEN}✓ Created session branch: {branch_name}{Colors.END}")
                except:
                    # Branch might already exist
                    self.run_git(['checkout', branch_name])
                    print(f"{Colors.GREEN}✓ Switched to branch: {branch_name}{Colors.END}")

        # Store session info
        self.session = {
            'session_id': session_id,
            'description': description,
            'branch': branch_name,
            'started_at': datetime.now().isoformat(),
            'last_commit': None,
            'last_push': None,
            'commit_count': 0,
            'push_count': 0
        }
        self.save_session()

        print(f"{Colors.GREEN}✓ Session started: {session_id}{Colors.END}")
        print(f"{Colors.CYAN}  Branch: {branch_name}{Colors.END}")
        print(f"{Colors.CYAN}  Description: {description}{Colors.END}\n")

        return session_id

    def auto_commit(self, message: str = None):
        """Perform automatic commit"""
        if not self.has_uncommitted_changes():
            print(f"{Colors.YELLOW}ℹ No changes to commit{Colors.END}")
            return False

        # Generate commit message
        if not message:
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            session_id = self.session.get('session_id', 'unknown')

            message = f"""Auto-save: Work in progress

Session: {session_id}
Timestamp: {timestamp}

🤖 Generated with AZ1.AI CODITECT Git Helper

Co-Authored-By: Claude <noreply@anthropic.com>"""

        # Stage all changes
        self.run_git(['add', '-A'])

        # Commit
        self.run_git(['commit', '-m', message])

        # Update session
        self.session['last_commit'] = datetime.now().isoformat()
        self.session['commit_count'] = self.session.get('commit_count', 0) + 1
        self.save_session()

        print(f"{Colors.GREEN}✓ Auto-committed changes (commit #{self.session['commit_count']}){Colors.END}")
        return True

    @retry_operation(max_retries=3, delay=2.0)
    def auto_push(self):
        """Perform automatic push to remote with retry logic."""
        if not self.has_unpushed_commits():
            print(f"{Colors.YELLOW}ℹ No commits to push{Colors.END}")
            self.logger.info("No commits to push")
            return False

        branch = self.get_current_branch()

        try:
            self.logger.info(f"Pushing to origin/{branch}...")
            # Push with --set-upstream for new branches
            self.run_git(['push', '-u', 'origin', branch])

            # Update session
            self.session['last_push'] = datetime.now().isoformat()
            self.session['push_count'] = self.session.get('push_count', 0) + 1
            self.save_session()

            print(f"{Colors.GREEN}✓ Pushed to origin/{branch} (push #{self.session['push_count']}){Colors.END}")
            self.logger.info(f"Push successful (push #{self.session['push_count']})")
            return True

        except GitOperationError as e:
            error_msg = f"Push failed: {e}"
            self.logger.error(error_msg)
            print(f"{Colors.RED}✗ {error_msg}{Colors.END}")
            print(f"{Colors.YELLOW}⚠ You may need to authenticate with GitHub{Colors.END}")
            print(f"{Colors.YELLOW}  Run: gh auth login{Colors.END}")
            raise NetworkError(error_msg)

    @retry_operation(max_retries=3, delay=2.0)
    def sync_with_remote(self):
        """Pull latest changes from remote with retry logic."""
        print(f"{Colors.BLUE}▶ Syncing with remote...{Colors.END}")
        self.logger.info("Starting sync with remote...")

        branch = self.get_current_branch()

        try:
            # Fetch latest
            self.logger.debug("Fetching from origin...")
            self.run_git(['fetch', 'origin'])

            # Pull with rebase to keep clean history
            self.logger.debug(f"Pulling from origin/{branch} with rebase...")
            self.run_git(['pull', '--rebase', 'origin', branch])

            print(f"{Colors.GREEN}✓ Synced with origin/{branch}{Colors.END}")
            self.logger.info("Sync completed successfully")
            return True

        except GitOperationError as e:
            self.logger.warning(f"Could not sync with remote: {e}")
            print(f"{Colors.YELLOW}⚠ Could not sync with remote (may not exist yet){Colors.END}")
            return False

    def create_pr(self, title: str, description: str = None):
        """Create pull request using GitHub CLI"""
        print(f"\n{Colors.BLUE}{Colors.BOLD}▶ Creating pull request...{Colors.END}\n")

        # Check if gh CLI is installed
        try:
            subprocess.run(['gh', '--version'], check=True, capture_output=True)
        except FileNotFoundError:
            print(f"{Colors.RED}✗ GitHub CLI (gh) not installed{Colors.END}")
            print(f"{Colors.YELLOW}  Install: brew install gh{Colors.END}")
            return False

        # Ensure changes are pushed
        if self.has_uncommitted_changes():
            print(f"{Colors.YELLOW}⚠ Committing changes before creating PR...{Colors.END}")
            self.auto_commit(f"{title}\n\n{description or ''}")

        if self.has_unpushed_commits():
            print(f"{Colors.YELLOW}⚠ Pushing changes before creating PR...{Colors.END}")
            self.auto_push()

        # Create PR
        branch = self.get_current_branch()
        base_branch = self.config['main_branch']

        pr_body = description or f"Pull request for {branch}"

        try:
            result = subprocess.run(
                ['gh', 'pr', 'create',
                 '--title', title,
                 '--body', pr_body,
                 '--base', base_branch],
                cwd=self.project_dir,
                check=True,
                capture_output=True,
                text=True
            )

            pr_url = result.stdout.strip()
            print(f"{Colors.GREEN}✓ Pull request created!{Colors.END}")
            print(f"{Colors.CYAN}  URL: {pr_url}{Colors.END}")

            return True

        except subprocess.CalledProcessError as e:
            print(f"{Colors.RED}✗ PR creation failed: {e.stderr}{Colors.END}")
            return False

    def end_session(self, merge_to_main: bool = False, create_pr_flag: bool = False):
        """End work session"""
        print(f"\n{Colors.BLUE}{Colors.BOLD}▶ Ending work session...{Colors.END}\n")

        # Final commit
        if self.has_uncommitted_changes():
            print(f"{Colors.YELLOW}⚠ Committing final changes...{Colors.END}")
            self.auto_commit("End of work session - final commit")

        # Final push
        if self.has_unpushed_commits():
            print(f"{Colors.YELLOW}⚠ Pushing final changes...{Colors.END}")
            self.auto_push()

        # Create PR if requested
        if create_pr_flag:
            session_desc = self.session.get('description', 'work session')
            self.create_pr(
                title=f"Session: {session_desc}",
                description=f"Work from session {self.session.get('session_id')}"
            )

        # Merge to main if requested
        if merge_to_main:
            self.merge_session_to_main()

        # Session summary
        duration = None
        if 'started_at' in self.session:
            start = datetime.fromisoformat(self.session['started_at'])
            duration = datetime.now() - start

        print(f"\n{Colors.GREEN}{Colors.BOLD}Session Summary:{Colors.END}")
        print(f"  Session ID: {self.session.get('session_id')}")
        print(f"  Duration: {duration}")
        print(f"  Commits: {self.session.get('commit_count', 0)}")
        print(f"  Pushes: {self.session.get('push_count', 0)}")
        print(f"  Branch: {self.session.get('branch')}\n")

        # Clear session
        if self.session_file.exists():
            self.session_file.unlink()
        self.session = {}

    def merge_session_to_main(self):
        """Merge current branch to main with rollback on failure."""
        print(f"{Colors.BLUE}▶ Merging to {self.config['main_branch']}...{Colors.END}")
        self.logger.info("Starting merge to main branch...")

        current_branch = self.get_current_branch()
        main_branch = self.config['main_branch']

        if current_branch == main_branch:
            print(f"{Colors.YELLOW}ℹ Already on {main_branch}{Colors.END}")
            self.logger.info("Already on main branch")
            return True

        # Store original branch for rollback
        original_branch = current_branch

        try:
            # Switch to main
            self.logger.debug(f"Switching to {main_branch}...")
            self.run_git(['checkout', main_branch])

            # Pull latest
            self.logger.debug("Pulling latest changes...")
            self.run_git(['pull', 'origin', main_branch], check=False)

            # Get main branch HEAD for rollback
            main_head_before = self.run_git(['rev-parse', 'HEAD']).stdout.strip()
            self.logger.debug(f"Main branch HEAD before merge: {main_head_before}")

            # Merge session branch
            self.logger.info(f"Merging {current_branch} into {main_branch}...")
            self.run_git(['merge', '--no-ff', current_branch, '-m', f'Merge session: {current_branch}'])

            # Push merged changes
            self.logger.debug("Pushing merged changes...")
            self.run_git(['push', 'origin', main_branch])

            print(f"{Colors.GREEN}✓ Merged {current_branch} → {main_branch}{Colors.END}")
            self.logger.info("Merge completed successfully")

            # Cleanup session branch if configured
            if self.config.get('enable_auto_cleanup', True):
                self.run_git(['branch', '-d', current_branch])
                print(f"{Colors.GREEN}✓ Cleaned up local branch: {current_branch}{Colors.END}")
                self.logger.info(f"Cleaned up branch: {current_branch}")

            return True

        except GitOperationError as e:
            error_msg = f"Merge failed: {e}"
            self.logger.error(error_msg)
            print(f"{Colors.RED}✗ {error_msg}{Colors.END}")
            print(f"{Colors.YELLOW}⚠ Attempting rollback...{Colors.END}")

            # Rollback merge
            try:
                self.logger.info("Rolling back merge...")
                # Abort merge if in progress
                self.run_git(['merge', '--abort'], check=False)

                # Reset to HEAD before merge if we're still on main
                current = self.get_current_branch()
                if current == main_branch and 'main_head_before' in locals():
                    self.run_git(['reset', '--hard', main_head_before])
                    self.logger.info("Rolled back to state before merge")

                # Switch back to original branch
                self.run_git(['checkout', original_branch])
                print(f"{Colors.YELLOW}✓ Rolled back to {original_branch}{Colors.END}")
                self.logger.info(f"Switched back to {original_branch}")

                print(f"{Colors.YELLOW}⚠ You may need to resolve conflicts manually{Colors.END}")
                print(f"{Colors.YELLOW}  Merge conflicts can be resolved with:{Colors.END}")
                print(f"{Colors.YELLOW}    git checkout {main_branch}{Colors.END}")
                print(f"{Colors.YELLOW}    git merge {original_branch}{Colors.END}")
                print(f"{Colors.YELLOW}    # Resolve conflicts{Colors.END}")
                print(f"{Colors.YELLOW}    git add .{Colors.END}")
                print(f"{Colors.YELLOW}    git commit{Colors.END}")

            except Exception as rollback_error:
                self.logger.error(f"Rollback failed: {rollback_error}")
                print(f"{Colors.RED}✗ Rollback failed: {rollback_error}{Colors.END}")
                print(f"{Colors.YELLOW}⚠ Manual intervention required{Colors.END}")

            return False

    def status(self):
        """Show Git status with session info"""
        print(f"\n{Colors.BLUE}{Colors.BOLD}Git & Session Status{Colors.END}\n")

        # Git repository info
        if self.is_git_repo():
            print(f"{Colors.GREEN}✓ Git repository initialized{Colors.END}")
            print(f"  Branch: {Colors.CYAN}{self.get_current_branch()}{Colors.END}")

            remote = self.get_remote_url()
            if remote:
                print(f"  Remote: {Colors.CYAN}{remote}{Colors.END}")
        else:
            print(f"{Colors.RED}✗ Not a Git repository{Colors.END}")
            return

        # Changes status
        if self.has_uncommitted_changes():
            print(f"\n{Colors.YELLOW}⚠ Uncommitted changes detected{Colors.END}")
            result = self.run_git(['status', '--short'])
            print(result.stdout)
        else:
            print(f"\n{Colors.GREEN}✓ Working tree clean{Colors.END}")

        # Unpushed commits
        if self.has_unpushed_commits():
            result = self.run_git(['log', '@{u}..HEAD', '--oneline'], check=False)
            if result.returncode == 0:
                commit_count = len(result.stdout.strip().split('\n'))
                print(f"\n{Colors.YELLOW}⚠ {commit_count} unpushed commit(s){Colors.END}")
        else:
            print(f"{Colors.GREEN}✓ All commits pushed{Colors.END}")

        # Session info
        if self.session:
            print(f"\n{Colors.BOLD}Active Session:{Colors.END}")
            print(f"  Session ID: {self.session.get('session_id')}")
            print(f"  Description: {self.session.get('description')}")
            print(f"  Branch: {self.session.get('branch')}")
            print(f"  Commits: {self.session.get('commit_count', 0)}")
            print(f"  Pushes: {self.session.get('push_count', 0)}")
        else:
            print(f"\n{Colors.YELLOW}ℹ No active session{Colors.END}")

    def interactive_menu(self):
        """Interactive menu for Git operations"""
        while True:
            print(f"\n{Colors.CYAN}{Colors.BOLD}═══ CODITECT Git Helper ═══{Colors.END}\n")
            print("1. Start work session")
            print("2. Commit changes")
            print("3. Push to GitHub")
            print("4. Sync with remote")
            print("5. Create pull request")
            print("6. End session")
            print("7. Show status")
            print("8. Exit")

            choice = input(f"\n{Colors.YELLOW}Select option [1-8]: {Colors.END}").strip()

            if choice == '1':
                desc = input("Session description: ").strip() or "work session"
                self.start_session(desc)

            elif choice == '2':
                msg = input("Commit message (optional): ").strip() or None
                self.auto_commit(msg)

            elif choice == '3':
                self.auto_push()

            elif choice == '4':
                self.sync_with_remote()

            elif choice == '5':
                title = input("PR title: ").strip()
                desc = input("PR description (optional): ").strip() or None
                self.create_pr(title, desc)

            elif choice == '6':
                create_pr = input("Create pull request? (y/n): ").lower() == 'y'
                merge = input("Merge to main? (y/n): ").lower() == 'y'
                self.end_session(merge_to_main=merge, create_pr_flag=create_pr)

            elif choice == '7':
                self.status()

            elif choice == '8':
                print(f"\n{Colors.GREEN}Goodbye!{Colors.END}\n")
                break

            else:
                print(f"{Colors.RED}Invalid option{Colors.END}")


def main():
    """
    Entry point with error handling and exit codes.

    Exit codes:
        0: Success
        1: General error
        2: Validation error
        3: Git operation error
        4: GitHub operation error
        5: Network error
        130: User cancelled (Ctrl+C)
    """
    import argparse

    parser = argparse.ArgumentParser(
        description='CODITECT Git Helper - Automated Git workflow management',
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument('command', nargs='?', choices=[
        'init', 'start', 'commit', 'push', 'sync', 'pr', 'end', 'status', 'menu'
    ], help='Command to execute')
    parser.add_argument('--message', '-m', help='Commit message')
    parser.add_argument('--description', '-d', help='Session/PR description')
    parser.add_argument('--title', '-t', help='PR title')
    parser.add_argument('--merge', action='store_true', help='Merge to main on end')
    parser.add_argument('--remote', '-r', help='GitHub remote URL')
    parser.add_argument('--verbose', '-v', action='store_true', help='Verbose output')

    args = parser.parse_args()

    try:
        # Initialize helper
        helper = GitHelper()

        # Set logging level
        if args.verbose:
            helper.logger.setLevel(logging.DEBUG)

        # Execute command
        if not args.command or args.command == 'menu':
            helper.interactive_menu()

        elif args.command == 'init':
            helper.initialize_repo()
            if args.remote:
                helper.setup_remote(args.remote)

        elif args.command == 'start':
            desc = args.description or 'work session'
            if not desc.strip():
                raise ValidationError("Session description cannot be empty")
            helper.start_session(desc)

        elif args.command == 'commit':
            helper.auto_commit(args.message)

        elif args.command == 'push':
            helper.auto_push()

        elif args.command == 'sync':
            helper.sync_with_remote()

        elif args.command == 'pr':
            title = args.title or input("PR title: ")
            if not title.strip():
                raise ValidationError("PR title cannot be empty")
            helper.create_pr(title, args.description)

        elif args.command == 'end':
            helper.end_session(merge_to_main=args.merge)

        elif args.command == 'status':
            helper.status()

        helper.logger.info("Command completed successfully")
        return 0

    except KeyboardInterrupt:
        print(f"\n{Colors.YELLOW}⚠ Operation cancelled by user{Colors.END}")
        return 130

    except ValidationError as e:
        print(f"{Colors.RED}✗ Validation error: {e}{Colors.END}")
        logger = logging.getLogger('GitHelper')
        logger.error(f"Validation error: {e}")
        return 2

    except GitOperationError as e:
        print(f"{Colors.RED}✗ Git operation failed: {e}{Colors.END}")
        logger = logging.getLogger('GitHelper')
        logger.error(f"Git operation error: {e}")
        return 3

    except GitHubOperationError as e:
        print(f"{Colors.RED}✗ GitHub operation failed: {e}{Colors.END}")
        print(f"{Colors.YELLOW}  Check GitHub CLI authentication: gh auth login{Colors.END}")
        logger = logging.getLogger('GitHelper')
        logger.error(f"GitHub operation error: {e}")
        return 4

    except NetworkError as e:
        print(f"{Colors.RED}✗ Network error: {e}{Colors.END}")
        print(f"{Colors.YELLOW}  Check your internet connection{Colors.END}")
        logger = logging.getLogger('GitHelper')
        logger.error(f"Network error: {e}")
        return 5

    except (SessionError, ConfigurationError) as e:
        print(f"{Colors.RED}✗ Error: {e}{Colors.END}")
        logger = logging.getLogger('GitHelper')
        logger.error(f"Error: {e}")
        return 1

    except Exception as e:
        print(f"{Colors.RED}✗ Unexpected error: {e}{Colors.END}")
        logger = logging.getLogger('GitHelper')
        logger.exception("Unexpected error occurred")
        return 1


if __name__ == '__main__':
    sys.exit(main())
