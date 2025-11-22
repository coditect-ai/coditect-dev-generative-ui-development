# New Project Creation Workflow

This command orchestrates a complete new project creation workflow that guides users from initial idea through discovery, planning, and structure creation to have a production-ready project ready for development. The workflow is designed for CODITECT internal teams, enterprise customers, and end-users, with different guidance styles adapted to each audience.

The workflow progresses through five integrated phases with specialized agents handling each responsibility:
1. **Project Discovery** - Interactive interview to gather requirements and create project brief
2. **Submodule Creation** - Automated git repository setup with CODITECT distributed intelligence
3. **Project Planning** - Comprehensive specification generation (PROJECT-PLAN.md, TASKLIST.md)
4. **Structure Optimization** - Production-ready directory structure and starter templates
5. **Quality Assurance** - Verification that everything is in place and ready for development

## Steps to follow:

### Step 1: Initiate Project Discovery

Launch the interactive discovery phase with the `project-discovery-specialist` agent to gather comprehensive project requirements.

**Action:** Invoke the discovery specialist agent to conduct an interactive discovery interview.

```
Task(
    subagent_type="orchestrator",
    prompt="""Use project-discovery-specialist subagent to conduct a comprehensive interactive discovery interview for a new project.

The discovery process should:
1. Ask adaptive questions based on initial project description
2. Gather functional and non-functional requirements
3. Assess team, timeline, and resource constraints
4. Identify risks and mitigation strategies
5. Document business case and success criteria
6. Generate a complete project brief in JSON format

Output the project brief and be prepared to pass it to the planning phase."""
)
```

**Success Criteria:**
- Project brief created with all required sections
- User confirms understanding of scope and requirements
- Risk assessment complete with mitigation strategies
- Business case documented with success metrics
- Tech stack recommendations provided
- No major ambiguities or conflicting requirements remain

**Common Issues & Solutions:**
- User uncertain about scope → Ask clarifying questions until scope is clear
- Conflicting requirements → Surface conflicts and guide user to prioritization
- Unrealistic timeline → Discuss scope/team tradeoffs
- Risk level too high → Explore risk mitigation strategies

### Step 2: Create Submodule Repository

Create the git repository and submodule infrastructure using the `submodule-orchestrator` agent.

**Action:** Invoke the submodule orchestrator to set up git repository structure.

```
Task(
    subagent_type="orchestrator",
    prompt="""Use submodule-orchestrator subagent to create a new CODITECT submodule for the project.

The submodule creation should:
1. Determine appropriate category (cloud, dev, ops, etc.) based on project type
2. Create git repository with proper CODITECT naming convention (coditect-{category}-{name})
3. Create all required directories and symlinks (.coditect, .claude)
4. Initialize git with first commit
5. Create GitHub repository
6. Register as submodule with parent repository
7. Verify all components are in place

Use the project brief from Step 1 to guide decisions about naming and structure."""
)
```

**Success Criteria:**
- Git repository created with correct naming convention
- Symlink chains established (.coditect → ../../../.coditect, .claude → .coditect)
- GitHub repository created and configured
- Submodule registered with parent repository
- Initial commit created and pushed
- All verification checks pass

**Important Notes:**
- Use REPO-NAMING-CONVENTION.md to determine correct category
- Repository name must follow `coditect-{category}-{name}` format
- Symlinks are critical for distributed intelligence architecture
- Verify symlink accessibility after creation

### Step 3: Generate Project Plan

Create comprehensive project specification using the `software-design-document-specialist` agent.

**Action:** Invoke the design specialist to create detailed project plan.

```
Task(
    subagent_type="orchestrator",
    prompt="""Use software-design-document-specialist subagent to create a comprehensive PROJECT-PLAN.md for the project.

The project plan should include:
1. Executive summary of project scope and goals
2. System architecture and design (C4 if applicable)
3. Detailed requirements breakdown (functional and non-functional)
4. Technology stack rationale
5. Implementation roadmap with phases
6. Risk assessment and mitigation strategies
7. Success metrics and quality gates
8. Dependencies and integration points
9. Team structure and roles
10. Budget and resource requirements

Also generate TASKLIST.md with checkbox-based tracking of:
- Phase-based task breakdown
- Dependencies between tasks
- Acceptance criteria for each task
- Estimated effort for planning purposes

Use the project brief from Step 1 as comprehensive input."""
)
```

**Success Criteria:**
- PROJECT-PLAN.md complete with all sections filled in
- TASKLIST.md created with 50+ tasks broken down by phase
- Architecture diagrams included (if applicable)
- Implementation roadmap with realistic timeline
- Risk assessment documented with mitigation plans
- All checkboxes ready for progress tracking
- Documentation is clear enough for development team to start immediately

**Important Notes:**
- Plan must be comprehensive enough to guide development without further discovery
- Include clear acceptance criteria for each phase
- Document all assumptions and constraints
- Provide architecture diagrams when applicable
- Break down into phases with clear deliverables

### Step 4: Optimize Project Structure

Create production-ready directory structure using the `project-structure-optimizer` agent.

**Action:** Invoke the structure optimizer to generate project directory hierarchy.

```
Task(
    subagent_type="orchestrator",
    prompt="""Use project-structure-optimizer subagent to create a production-ready project structure.

The structure optimization should:
1. Analyze project type and tech stack from project brief
2. Create optimal directory hierarchy following CODITECT standards
3. Generate starter code templates for primary components
4. Create example implementations showing best practices
5. Generate configuration templates (dev, staging, prod)
6. Create GitHub Actions CI/CD templates
7. Generate Dockerfile and docker-compose.yml for local development
8. Create comprehensive documentation (README, CONTRIBUTING, DEVELOPMENT, ARCHITECTURE)
9. Set up testing structure with example tests
10. Create Makefile or equivalent for common tasks

The structure should be completely production-ready so developers can:
- Clone the repository
- Install dependencies
- Run the application
- Start development with confidence

Use the project brief and plan from previous steps as input."""
)
```

**Success Criteria:**
- Directory structure matches CODITECT production standards
- All starter code is production-quality
- Configuration templates provided for all environments
- CI/CD workflows set up and ready to use
- Documentation is comprehensive and clear
- Developers can run `make dev` or equivalent and start coding
- No manual setup or file reorganization needed
- Testing structure in place with examples

**Important Notes:**
- Structure should support growth from MVP to enterprise scale
- Include security best practices in templates
- Provide performance optimization patterns
- Support team collaboration patterns
- Include monitoring and observability hooks from the start

### Step 5: Quality Assurance Verification

Run comprehensive verification to ensure all phases completed successfully.

**Action:** Execute verification checks to validate the complete setup.

```
Task(
    subagent_type="orchestrator",
    prompt="""Use submodule-orchestrator subagent to run comprehensive QA verification for the new project.

The verification should check:
1. Git repository exists and is properly configured
2. Symlinks are properly established and accessible
3. PROJECT-PLAN.md is complete with all sections
4. TASKLIST.md has all tasks with checkboxes
5. Directory structure matches expected patterns
6. All starter files are in place and syntactically correct
7. Configuration files (env templates, docker, CI/CD) are complete
8. Documentation is complete and accurate
9. No broken references or missing files
10. Project is ready for team onboarding

Generate a QA report showing:
- All checks passed (green ✓)
- Any issues found (red ✗)
- Remediation steps for any failures
- Next steps for beginning development
- Team onboarding checklist"""
)
```

**Success Criteria:**
- All verification checks pass (100% green)
- QA report generated and reviewed
- Any issues immediately remediated
- Project is production-ready
- Team can begin development immediately
- Clear next steps documented

**Important Notes:**
- Don't skip verification even if previous steps appeared successful
- Fix any issues immediately before declaring complete
- Generate team onboarding checklist
- Provide clear documentation on how to get started

## Important notes:

- **Adaptive to audience:** Tailor guidance, terminology, and process based on whether this is for CODITECT internal teams (full control), enterprise customers (guided + compliance), or end-users (simplified + smart defaults)

- **Seamless integration:** Each phase builds on the previous one, with artifacts from each phase feeding into the next. The orchestrator agent coordinates all five agents to ensure smooth handoff.

- **Complete by end:** After all five phases complete successfully, the project is production-ready. Developers should be able to clone, setup, and start coding immediately.

- **Risk-aware:** Identify risks early (during discovery) so they can be addressed during planning. Escalate high-risk projects to human review before proceeding.

- **Documentation complete:** All documentation generated during the workflow (PROJECT-PLAN.md, TASKLIST.md, architecture docs, API docs, deployment guides) is ready for the team.

- **No manual work required:** The workflow is fully automated. No manual file creation, folder organization, or configuration needed after the workflow completes.

- **Verification mandatory:** Always run QA verification before considering the project complete. Don't assume previous steps were successful.

- **Extensible design:** The modular architecture allows for future enhancements (add templates, customize structures, add compliance checks) without disrupting the core workflow.

- **Team collaboration ready:** Generated structure and documentation support team collaboration patterns. Git workflow, code review processes, and CI/CD are all pre-configured.

- **Monitoring from day one:** All starter code includes observability hooks. Developers don't need to retrofit monitoring; it's built in from the beginning.
