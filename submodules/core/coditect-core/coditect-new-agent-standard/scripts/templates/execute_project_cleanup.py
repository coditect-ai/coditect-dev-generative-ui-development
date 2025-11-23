#!/usr/bin/env python3
"""
Execute Project Cleanup - Direct Task Tool Execution
Calls the project-organizer agent to autonomously organize the current directory.
"""

import os
import sys
from datetime import datetime

def execute_project_organizer(dry_run=True):
    """
    Execute project-organizer agent using the correct Task Tool Proxy Pattern
    This function demonstrates the proper way to call agents from the 47-agent framework
    """
    
    current_dir = os.getcwd()
    project_name = os.path.basename(current_dir)
    
    print(f"🎭 Calling project-organizer agent for: {project_name}")
    print(f"📁 Working directory: {current_dir}")
    print(f"🔧 Mode: {'DRY RUN (analysis only)' if dry_run else 'LIVE EXECUTION (with user permission)'}")
    print("=" * 70)
    
    # Build the comprehensive task prompt
    task_prompt = f"""Use project-organizer subagent to conduct autonomous directory organization and cleanup for {project_name}.

PROJECT LOCATION: {current_dir}

AUTONOMOUS CLEANUP REQUIREMENTS:

1. DIRECTORY ANALYSIS:
   - Scan root directory for misplaced files and organizational issues
   - Identify files that belong in subdirectories (docs/, .session/, scripts/, etc.)
   - Categorize files by type, purpose, and proper location
   - Map current structure against production standards
   - Check for cluttered root directory with non-essential files

2. PERMISSION PROTOCOL - CRITICAL:
   - ⚠️ NEVER delete any files without explicit user permission
   - ⚠️ ALWAYS ask before moving important configuration files
   - ⚠️ ALWAYS use 'git mv' to preserve file history when moving files
   - ⚠️ ASK permission before creating new directories
   - ⚠️ Present clear organization plan before executing any moves
   - ⚠️ Request confirmation for each major organizational change

3. ORGANIZATION STANDARDS:
   - Follow project-organizer agent's production directory structure specifications
   - Move session exports to .session/conversations/ directory
   - Move research documents to docs/research/ or appropriate subdirectories  
   - Move project management files to docs/management/ or similar
   - Keep only essential files in root: README.md, CLAUDE.md, package.json, .gitignore, etc.
   - Organize documentation by topic, type, and date
   - Maintain clear separation between development artifacts and documentation

4. SAFETY REQUIREMENTS:
   - Check for file references and imports before moving any files
   - Update any broken links or references after moves
   - Create atomic git commits for each organizational change
   - Never overwrite existing files - ask for resolution strategy
   - Preserve all file permissions and timestamps
   - Verify git status before and after each change

5. EXECUTION MODE:
   - {'DRY RUN MODE: Analyze and show what would be done, but make no actual changes' if dry_run else 'LIVE MODE: Execute approved changes with git operations and user confirmation'}

6. SKILLS TO UTILIZE:
   - Use git-workflow-automation skill for safe file moves with history preservation
   - Use cross-file-documentation-update skill for updating file references
   - Use internal-comms skill for generating clear organization reports
   - Use communication-protocols skill for coordinating permission requests

7. EXPECTED DELIVERABLES:
   - Complete directory analysis with misplaced files identified
   - Detailed organization plan with specific move operations
   - Clear permission requests for any deletions or major restructuring
   - Step-by-step implementation commands using 'git mv' for file moves
   - Verification steps to ensure organization success
   - Summary report of organizational improvements

Please execute this autonomous organization task following all safety protocols and permission requirements."""

    print("📋 Task Prompt Prepared - Executing via Task Tool...")
    print("\n" + "🎯" + " TASK EXECUTION " + "🎯".center(50, "="))
    
    # This is where Claude Code will execute the Task tool call
    print(f"\nExecuting: Task(subagent_type='general-purpose', prompt='Use project-organizer subagent to...')")
    print(f"Expected Result: Project-organizer agent will autonomously analyze and organize the directory")
    print(f"Permission Level: Agent will request permission before any file operations")
    
    return {
        "task_type": "project_organization",
        "subagent_type": "general-purpose", 
        "prompt": task_prompt,
        "project_name": project_name,
        "working_directory": current_dir,
        "dry_run": dry_run,
        "timestamp": datetime.now().isoformat(),
        "expected_behavior": "Agent will analyze directory structure and request permission for organizational changes"
    }

def main():
    """Main execution function"""
    
    # Check command line arguments
    dry_run = True
    if len(sys.argv) > 1:
        if sys.argv[1].lower() in ['live', 'execute', 'run']:
            dry_run = False
            print("⚠️  LIVE EXECUTION MODE - Agent will request permission for actual file operations")
        elif sys.argv[1].lower() in ['dry', 'dryrun', 'preview']:
            dry_run = True
            print("🔍 DRY RUN MODE - Agent will analyze only, no file operations")
        else:
            print("Usage: python execute_project_cleanup.py [dry|live]")
            print("  dry  - Analysis only (default)")
            print("  live - Execute with user permission")
            return
    else:
        print("🔍 DRY RUN MODE (default) - Use 'live' argument for actual execution")
    
    # Execute the project organization
    result = execute_project_organizer(dry_run)
    
    print(f"\n✅ Task prepared for execution")
    print(f"📊 Project: {result['project_name']}")
    print(f"🔧 Mode: {'DRY RUN' if dry_run else 'LIVE EXECUTION'}")
    print(f"⏰ Timestamp: {result['timestamp']}")
    
    print("\n" + "=" * 70)
    print("📝 NEXT STEPS:")
    print("1. The project-organizer agent will analyze the directory structure")
    print("2. It will identify misplaced files and organizational opportunities") 
    print("3. It will request permission before making any changes")
    print("4. All file moves will use 'git mv' to preserve history")
    print("5. Results will be committed with descriptive messages")
    print("\n🎯 Ready for agent execution!")

if __name__ == "__main__":
    main()