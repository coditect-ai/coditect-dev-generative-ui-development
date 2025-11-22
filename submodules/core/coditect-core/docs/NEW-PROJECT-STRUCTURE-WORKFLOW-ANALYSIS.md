# New Project Structure Creation Workflow - Comprehensive Analysis

**Analysis Date:** November 22, 2025
**Status:** ✅ Complete
**Scope:** Evaluating optimal workflow for new project discovery, planning, and structure creation
**Audience:** CODITECT Internal Teams, Enterprise Customers, End Users

---

## Executive Summary

CODITECT **ALREADY HAS** a sophisticated agentic system for project planning and structure creation, but it operates in **TWO SEPARATE PHASES** rather than as an integrated workflow. This analysis identifies the current architecture, gaps, and proposes an enhanced unified workflow.

### Current State: Two-Phase Approach

**Phase 1: Submodule Creation** (Automated)
- `setup-new-submodule.py` - Creates git repos, symlinks, templates
- Output: Empty project structure with templates
- Duration: 2-3 minutes
- Fully automated, zero input required

**Phase 2: Project Planning** (Semi-Automated)
- `/generate-project-plan` command - Creates detailed specifications
- Agents: orchestrator, software-design-document-specialist
- Output: PROJECT-PLAN.md, TASKLIST.md
- Duration: 10-30 minutes
- Requires user context/input

### Recommendation: **INTEGRATE INTO SINGLE WORKFLOW**

Create a new **Project Discovery → Planning → Structure** unified workflow that:
1. Guides users through project discovery (What? Why? How?)
2. Automatically generates project specifications
3. Creates optimized project structure
4. Sets up multi-agent orchestration ready for execution

---

## Part 1: Current Agentic System Analysis

### Architecture: What CODITECT Has TODAY

#### **1. Submodule Orchestrator Agent** ✅
- **File:** `.coditect/agents/submodule-orchestrator.md`
- **Purpose:** Master coordinator for submodule lifecycle
- **Capabilities:**
  - Directory structure creation
  - Symlink chain establishment
  - GitHub repository setup
  - Git initialization and first commit
  - Parent registration

#### **2. Project Organizer Agent** ✅
- **File:** `.coditect/agents/project-organizer.md`
- **Purpose:** Directory structure and file organization
- **Capabilities:**
  - Analyze current structure
  - Identify misplaced files
  - Reorganize to production standards
  - Smart automation features

#### **3. Software Design Document Specialist Agent** ✅
- **File:** `.coditect/agents/software-design-document-specialist.md`
- **Purpose:** Enterprise architecture documentation
- **Capabilities:**
  - System architecture documentation
  - Technical requirements specification
  - API design and documentation
  - Database schema design
  - Implementation guidance

#### **4. Orchestrator Agent** ✅
- **File:** `.coditect/agents/orchestrator.md`
- **Purpose:** Multi-agent workflow coordination
- **Capabilities:**
  - Workflow pattern recognition
  - Intelligent agent selection
  - Parallel execution management
  - Progress orchestration
  - Quality gate enforcement

### Skills Available

| Skill | Purpose | Automation Level |
|-------|---------|------------------|
| **framework-patterns** | Event-driven, FSM, C4 modeling | High |
| **rust-backend-patterns** | Backend architecture patterns | High |
| **production-patterns** | Circuit breakers, error handling | High |
| **evaluation-framework** | LLM-as-judge, quality assessment | High |

### Commands Available

| Command | Purpose | User Input |
|---------|---------|-----------|
| **`/generate-project-plan`** | Create project specs + tasklist | High (context-dependent) |
| **`/setup-submodule`** | Interactive submodule setup | Medium (5-6 prompts) |
| **`/agent-dispatcher`** | Agent selection guidance | Low (natural language) |

### Scripts Available

| Script | Purpose | Automation |
|--------|---------|-----------|
| **setup-new-submodule.py** | Automated submodule creation | 100% |
| **coditect-router** | AI command selection | 100% |

---

## Part 2: Gap Analysis - What's Missing

### Gap 1: No Unified "New Project" Workflow

**Current State:**
```
User wants to create new project
         ↓
    Two separate steps:
    Step 1: /setup-submodule (Creates git repo)
    Step 2: /generate-project-plan (Creates specs)

Problem: User must understand and trigger both separately
```

**Desired State:**
```
User wants to create new project
         ↓
    Single unified command:
    /new-project (Combines discovery + submodule + planning)
         ↓
    Integrated workflow:
    - Discovery (interview project)
    - Submodule creation (git repo)
    - Planning (specifications)
    - Structure optimization (organize files)
    - Quality assurance (verify against standards)
```

### Gap 2: No Project Discovery Phase

**Missing:**
- Structured project discovery process
- Requirement gathering for new projects
- Problem/solution definition
- Success criteria collection
- Tech stack recommendations

**Current Behavior:**
- `/generate-project-plan` assumes basic context exists
- No guidance on WHAT to define before planning
- Users must self-discover project intent

### Gap 3: No Input Validation for Project Intent

**Missing:**
- Validation that user understands project scope
- Risk detection (conflicting requirements, unclear goals)
- Guided questions to clarify intent
- Confidence scoring on project definition

### Gap 4: No Integration Between Phases

**Current:**
- Submodule structure created (generic templates)
- Project plan created (generic structure)
- No automatic optimization based on project type

**Needed:**
- Structure customized by project type (backend vs frontend vs full-stack)
- Initial file organization based on project plan
- Sample code or starter templates by tech stack

### Gap 5: No Multi-Tenant User Guidance

**Current System Works For:**
- ✅ CODITECT internal teams (know the system)
- ⚠️ Enterprise customers (need more guidance)
- ❌ End users of customers (need even more guidance)

**Missing:**
- Progressive disclosure (basic → advanced)
- Customization by user experience level
- Default templates for common project types

---

## Part 3: Recommended Architecture

### Option 1: Monolithic Approach (Simple)

**Single New Agent:**
- `project-lifecycle-orchestrator` - Handles discovery, planning, structure

**Pros:**
- Simple to use (one command)
- Single point of coordination
- Unified error handling

**Cons:**
- Agent becomes large and complex
- Harder to test individual phases
- Harder to reuse for specialized use cases

### Option 2: Modular Approach (Recommended) ⭐

**Three Specialized Agents:**

1. **`project-discovery-specialist`** (NEW)
   - Interactive project discovery
   - Requirement gathering
   - Risk assessment
   - Output: Project brief JSON

2. **`project-orchestrator`** (ENHANCED)
   - Coordinates discovery → planning → structure
   - Calls submodule-orchestrator for git setup
   - Calls project-discovery-specialist for requirements
   - Calls software-design-document-specialist for planning
   - Output: Complete project ready for development

3. **`project-structure-optimizer`** (NEW)
   - Customizes structure by project type
   - Organizes initial files
   - Creates starter templates
   - Output: Production-ready project structure

**Pros:**
- Clear separation of concerns
- Reusable for other workflows
- Easier to test and maintain
- Composable with other tools

**Cons:**
- Requires coordination between agents
- User must understand phases (mitigated with CLI wrapper)

### Option 3: Hybrid Approach

**Combine with Enhanced Command:**
- Keep modular agents (Option 2)
- Create new slash command: `/new-project`
- Wraps all three agents in seamless workflow
- Progressive disclosure based on user experience

**Recommended: Option 2 + Option 3 (Modular + CLI Wrapper)**

---

## Part 4: Detailed Workflow Design

### Unified Workflow: `/new-project`

```
/new-project
    ↓
[1. Project Discovery] - 10-15 min
    ├─ User provides: Name, category, purpose
    ├─ Agent gathers: Tech stack, team size, timeline
    ├─ Agent identifies: Risks, blockers, success metrics
    └─ Output: Project Brief (JSON)

    ↓
[2. Submodule Creation] - 2-3 min
    ├─ Creates git repo in proper category
    ├─ Sets up symlinks (.coditect, .claude)
    ├─ Configures GitHub repository
    └─ Output: Empty project directory

    ↓
[3. Project Planning] - 10-15 min
    ├─ Uses Project Brief from Step 1
    ├─ Generates PROJECT-PLAN.md
    ├─ Generates TASKLIST.md
    ├─ Creates architecture documentation
    └─ Output: Complete specifications

    ↓
[4. Structure Optimization] - 5-10 min
    ├─ Customizes directory structure
    ├─ Creates starter templates
    ├─ Organizes files by project type
    ├─ Adds sample code if requested
    └─ Output: Production-ready structure

    ↓
[5. Quality Assurance] - 2-3 min
    ├─ Validates project plan completeness
    ├─ Verifies structure against standards
    ├─ Checks documentation quality
    └─ Output: Quality report + next steps

    ↓
COMPLETE: Project ready for development! 🎉
```

**Total Time: 30-45 minutes (fully automated after initial input)**

---

## Part 5: Recommended Implementation

### Phase 1: Create Discovery Agent

**File:** `.coditect/agents/project-discovery-specialist.md`

**Responsibilities:**
```yaml
core_responsibilities:
  1. Interactive Project Discovery
     - Name and category validation
     - Purpose and business case definition
     - Technical stack selection
     - Team composition and size
     - Timeline and milestones

  2. Requirement Gathering
     - Feature list and priorities
     - Integration requirements
     - Performance and scale requirements
     - Security and compliance needs

  3. Risk Assessment
     - Technical complexity evaluation
     - Dependency analysis
     - Timeline feasibility check
     - Resource availability check

  4. Output Generation
     - Structured project brief (JSON/YAML)
     - Recommendation summary
     - Next steps guidance
```

**Key Features:**
- Context-aware discovery (e.g., different questions for backend vs frontend)
- Smart defaults based on category and purpose
- Validation that requirements are clear
- Risk scoring and mitigation suggestions

### Phase 2: Create Project Orchestrator Command

**File:** `.coditect/commands/new-project.md`

**Purpose:** Unified entry point for project creation

**Steps:**
1. Verify current directory is rollout-master
2. Invoke project-discovery-specialist
3. Invoke submodule-orchestrator
4. Invoke project-planning workflow
5. Invoke structure optimization
6. Summarize and provide next steps

### Phase 3: Create Structure Optimizer Agent

**File:** `.coditect/agents/project-structure-optimizer.md`

**Purpose:** Customize structure based on project type

**Specializations:**
- Backend services (API servers)
- Frontend applications (Web/Mobile UI)
- Full-stack projects
- Monorepos
- Libraries/SDKs
- Data/ML projects

---

## Part 6: Multi-Tenant Considerations

### For CODITECT Internal Teams

**Workflow:**
```
/new-project
  → Advanced mode (all options available)
  → Full control over all aspects
  → Direct agent orchestration access
```

**Features:**
- Detailed project briefing
- Custom tech stack selection
- Advanced configuration options

### For Enterprise Customers

**Workflow:**
```
/new-project --guided
  → Step-by-step guidance
  → Recommended defaults
  → Best practices enforcement
```

**Features:**
- Limited choices (curated tech stacks)
- Automatic compliance templates
- Enterprise standards applied

### For End Users (Customer's Customers)

**Workflow:**
```
/new-project --simple
  → Minimal questions
  → Smart defaults
  → Guided through complex decisions
```

**Features:**
- 5-10 simple questions only
- AI recommends tech stack
- Pre-built templates by use case

---

## Part 7: Integration Points

### With Existing Systems

```
/new-project
    ├─ Uses: orchestrator (workflow coordination)
    ├─ Uses: software-design-document-specialist (docs)
    ├─ Uses: submodule-orchestrator (git setup)
    ├─ Uses: project-organizer (structure)
    └─ Generates: Projects compatible with all existing agents
```

### With CI/CD

```
New project created
    ↓
Auto-generated PROJECT-PLAN.md
    ↓
CI/CD pipeline checks compliance
    ↓
GitHub Actions triggered
    ↓
Development environment ready
```

### With Training/Onboarding

```
Project created
    ↓
README.md auto-generated with setup instructions
    ↓
TASKLIST.md ready for team
    ↓
Documentation auto-linked
    ↓
Training materials available
```

---

## Part 8: Success Criteria

### Phase 1 (Discovery)
- ✅ Project brief created with all required fields
- ✅ Risk assessment completed
- ✅ Team understands scope and success criteria
- ✅ Tech stack documented

### Phase 2 (Planning)
- ✅ PROJECT-PLAN.md complete and valid
- ✅ TASKLIST.md with checkboxes ready
- ✅ Architecture documentation drafted
- ✅ Implementation roadmap defined

### Phase 3 (Structure)
- ✅ Directory structure follows CODITECT standards
- ✅ Initial files organized properly
- ✅ Starter templates available
- ✅ Git repo ready for development

### Overall
- ✅ New project usable in < 1 hour
- ✅ Team can immediately start development
- ✅ All agents have project context
- ✅ Monitoring and observability ready

---

## Part 9: Implementation Checklist

### Immediate Actions (Week 1)

- [ ] Create `project-discovery-specialist.md` agent
- [ ] Create `/new-project` command wrapper
- [ ] Create discovery interview questionnaire
- [ ] Implement project brief JSON schema
- [ ] Test with 3 different project types

### Short Term (Week 2-3)

- [ ] Create `project-structure-optimizer.md` agent
- [ ] Implement structure customization by type
- [ ] Create starter templates for common stacks
- [ ] Add risk assessment scoring
- [ ] Document best practices

### Medium Term (Week 4-6)

- [ ] Create guided/simple modes for different users
- [ ] Implement compliance templates for enterprises
- [ ] Add integration with CI/CD systems
- [ ] Create onboarding documentation
- [ ] Train teams on new workflow

### Long Term (Month 2-3)

- [ ] Gather customer feedback
- [ ] Optimize discovery questions
- [ ] Expand starter templates
- [ ] Create advanced customization options
- [ ] Build analytics dashboard

---

## Part 10: Competitive Analysis

### How Other Platforms Handle This

**Rails (Rails Generate)**
```bash
rails new myapp
  → Creates basic structure
  → Minimal guidance
  → User customizes manually
```

**Next.js (Create Next App)**
```bash
npx create-next-app@latest
  → Guided setup (TypeScript? Tailwind? etc)
  → Generates working app
  → Ready to run: npm run dev
```

**Django (Django Admin)**
```bash
django-admin startproject myproject
  → Creates structure
  → Some configuration
  → Ready for development
```

**AWS SAM (Serverless)**
```bash
sam init
  → Guided questions
  → Selects runtime, project type
  → Generates full scaffold
```

**CODITECT Will Be:**
```bash
coditect new-project
  ↓ (Discovery)
  → Interactive project discovery
  → Risk assessment
  ↓ (Planning)
  → Generates complete specifications
  → Multi-agent ready
  ↓ (Structure)
  → Production-ready project structure
  → Custom by project type
  → Ready for development + CI/CD
```

**Key Difference:** CODITECT provides full specification + structure + multi-agent coordination, not just boilerplate

---

## Part 11: Recommendations Summary

### ✅ RECOMMENDED APPROACH

**Modular Architecture (Option 2) + CLI Wrapper (Option 3)**

**Create:**
1. `project-discovery-specialist.md` - New agent for discovery
2. `project-structure-optimizer.md` - New agent for structure
3. `/new-project` command - Unified entry point
4. Discovery interview questionnaire
5. Project brief JSON schema

**Integrate:**
- Orchestrator for workflow coordination
- Software design specialist for planning
- Submodule orchestrator for git setup
- Project organizer for structure cleanup

**Benefit:**
- Simple for users (one command)
- Modular for developers (reusable agents)
- Extensible for future enhancements
- Works for internal + external + end users

### Timeline

- **Week 1:** Discovery agent + command wrapper (MVP)
- **Week 2:** Structure optimizer + customization
- **Week 3-4:** Testing, customer feedback, refinement
- **Month 2:** Advanced features, guided modes, templates

### Success Metrics

- New projects created in < 1 hour (currently 30-45 min manual)
- Zero ambiguity about project scope
- 100% compliance with CODITECT standards
- All teams can immediately start development
- Suitable for CODITECT internal + enterprise customers + end users

---

## Conclusion

**CODITECT ALREADY HAS** all the necessary agents and infrastructure for sophisticated project creation. The gap is not in the components, but in the **integration and guidance**.

**Recommended Next Step:** Implement unified workflow with project discovery specialist agent, creating seamless experience from "I want to start a project" to "Ready to start development" in under 1 hour.

This solution will serve:
- ✅ CODITECT internal teams (full control)
- ✅ Enterprise customers (guided + compliance)
- ✅ End users (simplified + smart defaults)
- ✅ Future customers (scalable + extensible)

---

**Analysis Complete: Ready for Implementation**

