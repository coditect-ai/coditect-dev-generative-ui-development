# CODITECT Rollout Restructure - First Revision Proposal

## Current State: 29 Submodules

### Rollout-Ready (Keep & Rename)

| Current | Proposed Name | Notes |
|---------|---------------|-------|
| **CORE** | | |
| coditect-project-dot-claude | coditect-core | The brain - agents, skills, commands |
| coditect-framework | coditect-core-framework | Framework utilities |
| coditect-distributed-architecture | coditect-core-architecture | Architecture docs |
| **CLOUD PLATFORM** | | |
| coditect-cloud-backend | coditect-cloud-backend | API server |
| coditect-cloud-frontend | coditect-cloud-frontend | Web UI |
| coditect-infrastructure | coditect-cloud-infra | Terraform, K8s |
| **DEVELOPER TOOLS** | | |
| coditect-cli | coditect-dev-cli | CLI tools |
| coditect-automation | coditect-dev-automation | Automation scripts |
| coditect-analytics | coditect-dev-analytics | Usage analytics |
| coditect-context-api | coditect-dev-context | Context management |
| coditect-project-intelligence | coditect-dev-intelligence | Project analysis |
| **MARKETPLACE** | | |
| coditect-agent-marketplace | coditect-market-agents | Agent store |
| coditect-activity-data-model-ui | coditect-market-activity | Activity tracking UI |
| **DOCUMENTATION** | | |
| coditect-docs | coditect-docs-main | User documentation |
| coditect-legal | coditect-docs-legal | Terms, privacy, licenses |
| coditect-blog-application | coditect-docs-blog | Blog/marketing content |
| **OPERATIONS** | | |
| coditect-rollout-master | coditect-ops-master | This repo (orchestration) |
| coditect (halcasteel) | coditect-ops-distribution | Install/update scripts |
| coditect-installer | **MERGE** | Merge into ops-distribution |
| coditect-license-manager | coditect-ops-license | License management |
| coditect-license-server | **MERGE** | Merge into ops-license |
| **GO-TO-MARKET** | | |
| communications | coditect-gtm-comms | Internal/external comms |
| coditect-competition | coditect-gtm-competition | Competitive analysis |
| az1.ai-CODITECT.AI-GTM | coditect-gtm-strategy | GTM strategy |
| az1.ai-CODITECT-ERP-CRM | coditect-gtm-crm | CRM/ERP planning |
| **CLOUD PLATFORM** (continued) | | |
| Coditect-v5-multiple-LLM-IDE | coditect-cloud-ide | The CODITECT IDE (deployed) |
| **LABS/R&D** | | |
| NESTED-LEARNING-GOOGLE | coditect-labs-learning | Learning system R&D |
| az1.ai-coditect-agent-new-standard-development | coditect-labs-agent-standards | Agent dev standards |
| az1.ai-coditect-ai-screenshot-automator | coditect-labs-screenshot | Screenshot automation |
| coditect-interactive-workflow-analyzer | coditect-labs-workflow | Workflow analysis |

---

## Recommended Additions from Other Repos

### ADD ALL NOW - Organize First, Refine Later

| Repo | Add As | Category | Notes |
|------|--------|----------|-------|
| **coditect-pdf-convertor** | coditect-dev-pdf | dev | Utility tool |
| **coditect-foundation-db** (az1-ai) | coditect-cloud-foundationdb | cloud | DEPLOYED |
| **coditect-enterprise-agents** (az1-ai) | coditect-market-enterprise | market | Agent archetypes |
| **agents-research-plan-code** | coditect-labs-agents-research | labs | Active R&D |
| **az1.ai-coditect-ai-syllubus-curriculum-course-material** | coditect-docs-training | docs | Training (WIP) |
| **coditect-gcp-migration** (az1-ai) | coditect-cloud-migration | cloud | GCP migration |
| **az1.ai-coditect-AI-IDE-competitive-market-research** | coditect-gtm-research | gtm | Market research |
| **claude-code-functionality-tools-research** | coditect-labs-claude-research | labs | Claude research |
| **coditect-projects** | coditect-ops-projects | ops | WIP/customers/templates |
| **az1.ai-coditect-audio2text-workflow** | coditect-dev-audio2text | dev | Audio transcription |
| **az1.ai-coditect-contact-qr-code-generator** | coditect-dev-qrcode | dev | QR generator |
| **az1.ai-coditect-first-principles-analysis** | coditect-labs-first-principles | labs | Analysis methodology |
| **coditect-persona-customer-questions** | coditect-gtm-personas | gtm | Customer research |
| **coditect-customer-clipora-ravi-mehta** | coditect-gtm-customer-clipora | gtm | Customer project |
| **CODITECTv4** | coditect-labs-v4-archive | labs | Historical reference |
| **Coditect-MCP-RAG-Claude-Code-AUTH** | coditect-labs-mcp-auth | labs | MCP integration |
| **Coditect-Multi-Agent-RAG-Pipeline** | coditect-labs-multi-agent-rag | labs | RAG pipeline |
| **claude-cli-web-architecture** | coditect-labs-cli-web-arch | labs | Architecture research |
| **coditect-claude-code-initial-setup** | coditect-docs-setup | docs | Setup guides |
| **product-legitimacy-enterprise-software** | coditect-gtm-legitimacy | gtm | Enterprise positioning |

---

## Consolidation Recommendations

### Merge These Repos

| Merge From | Into | Reason |
|------------|------|--------|
| coditect-installer | coditect-ops-distribution | Same purpose |
| coditect-license-server | coditect-ops-license | Related functionality |
| az1.ai-coditect-AI-IDE-competitive-market-research | coditect-gtm-competition | Same domain |
| Coditect-MCP-RAG-Claude-Code-AUTH | coditect-core | MCP integration |
| Coditect-Multi-Agent-RAG-Pipeline | coditect-labs-agents-research | R&D |

### Remove from Rollout (Keep as Standalone)

| Repo | Reason |
|------|--------|
| None recommended | All current submodules have rollout value |

---

## First Revision Structure

### Proposed: 32 Submodules (was 29)

```
coditect-ops-master/
├── submodules/
│   ├── core/                    # Foundation (3)
│   │   ├── coditect-core
│   │   ├── coditect-core-framework
│   │   └── coditect-core-architecture
│   │
│   ├── cloud/                   # Platform (5)
│   │   ├── coditect-cloud-backend
│   │   ├── coditect-cloud-frontend
│   │   ├── coditect-cloud-ide            # THE IDE
│   │   ├── coditect-cloud-infra
│   │   └── coditect-cloud-foundationdb   # NEW
│   │
│   ├── dev/                     # Tools (6)
│   │   ├── coditect-dev-cli
│   │   ├── coditect-dev-automation
│   │   ├── coditect-dev-analytics
│   │   ├── coditect-dev-context
│   │   ├── coditect-dev-intelligence
│   │   └── coditect-dev-pdf              # NEW
│   │
│   ├── market/                  # Products (3)
│   │   ├── coditect-market-agents
│   │   ├── coditect-market-activity
│   │   └── coditect-market-enterprise    # NEW
│   │
│   ├── docs/                    # Content (4)
│   │   ├── coditect-docs-main
│   │   ├── coditect-docs-legal
│   │   ├── coditect-docs-blog
│   │   └── coditect-docs-training        # NEW
│   │
│   ├── ops/                     # Operations (2)
│   │   ├── coditect-ops-distribution     # MERGED
│   │   └── coditect-ops-license          # MERGED
│   │
│   ├── gtm/                     # Business (4)
│   │   ├── coditect-gtm-comms
│   │   ├── coditect-gtm-competition
│   │   ├── coditect-gtm-strategy
│   │   └── coditect-gtm-crm
│   │
│   └── labs/                    # R&D (6)
│       ├── coditect-labs-multi-llm
│       ├── coditect-labs-learning
│       ├── coditect-labs-agent-standards
│       ├── coditect-labs-screenshot
│       ├── coditect-labs-workflow
│       └── coditect-labs-agents-research # NEW
```

---

## Action Plan for First Revision

### Phase 1: Consolidations (Day 1-2)

1. **Merge coditect-installer → coditect (halcasteel)**
   ```bash
   # Copy installer content into distribution repo
   # Update to single coditect-ops-distribution
   ```

2. **Merge coditect-license-server → coditect-license-manager**
   ```bash
   # Combine license repos
   # Rename to coditect-ops-license
   ```

3. **Merge competitive research repos → coditect-competition**
   ```bash
   # Add IDE research to competition repo
   # Rename to coditect-gtm-competition
   ```

### Phase 2: Renames (Day 3-4)

Execute all renames on GitHub:

```bash
# Core
gh repo rename coditect-ai/coditect-project-dot-claude coditect-core
gh repo rename coditect-ai/coditect-framework coditect-core-framework
gh repo rename coditect-ai/coditect-distributed-architecture coditect-core-architecture

# Cloud
gh repo rename coditect-ai/coditect-infrastructure coditect-cloud-infra

# Dev tools
gh repo rename coditect-ai/coditect-context-api coditect-dev-context
gh repo rename coditect-ai/coditect-project-intelligence coditect-dev-intelligence

# Market
gh repo rename coditect-ai/coditect-agent-marketplace coditect-market-agents
gh repo rename coditect-ai/coditect-activity-data-model-ui coditect-market-activity

# Docs
gh repo rename coditect-ai/coditect-docs coditect-docs-main

# GTM
gh repo rename coditect-ai/coditect-communications coditect-gtm-comms
gh repo rename coditect-ai/az1.ai-CODITECT.AI-GTM coditect-gtm-strategy
gh repo rename coditect-ai/az1.ai-CODITECT-ERP-CRM coditect-gtm-crm

# Labs
gh repo rename coditect-ai/Coditect-v5-multiple-LLM-IDE coditect-labs-multi-llm
gh repo rename coditect-ai/NESTED-LEARNING-GOOGLE coditect-labs-learning
gh repo rename coditect-ai/az1.ai-coditect-agent-new-standard-development coditect-labs-agent-standards
gh repo rename coditect-ai/az1.ai-coditect-ai-screenshot-automator coditect-labs-screenshot
gh repo rename coditect-ai/coditect-interactive-workflow-analyzer coditect-labs-workflow
```

### Phase 3: Transfers (Day 3-4)

Transfer halcasteel repos to coditect-ai:

```bash
gh repo transfer halcasteel/coditect coditect-ai
gh repo transfer halcasteel/coditect-competition coditect-ai
```

Then rename:
```bash
gh repo rename coditect-ai/coditect coditect-ops-distribution
gh repo rename coditect-ai/coditect-competition coditect-gtm-competition
```

### Phase 4: Add New Submodules (Day 4-5)

```bash
# Add valuable repos to rollout
git submodule add https://github.com/coditect-ai/coditect-cloud-foundationdb submodules/cloud/coditect-cloud-foundationdb
git submodule add https://github.com/coditect-ai/coditect-dev-pdf submodules/dev/coditect-dev-pdf
git submodule add https://github.com/coditect-ai/coditect-market-enterprise submodules/market/coditect-market-enterprise
git submodule add https://github.com/coditect-ai/coditect-docs-training submodules/docs/coditect-docs-training
git submodule add https://github.com/coditect-ai/coditect-labs-agents-research submodules/labs/coditect-labs-agents-research
```

### Phase 5: Update References (Day 5-6)

1. Update .gitmodules with new URLs
2. Update install.sh/update.sh GitHub URLs
3. Update CLAUDE.md references
4. Update README.md links
5. Update CI/CD workflows

### Phase 6: Organize Subfolders (Day 6-7)

Restructure submodules/ into categorical folders:
```
submodules/
├── core/
├── cloud/
├── dev/
├── market/
├── docs/
├── ops/
├── gtm/
└── labs/
```

---

## Expected Outcome

| Metric | Before | After |
|--------|--------|-------|
| Submodules | 29 | 32 |
| Naming patterns | 5+ | 1 |
| Categories | Unclear | 8 clear |
| Finding repos | Hard | Instant |
| Onboarding time | Hours | Minutes |

---

## Questions for Review

1. **Subfolders**: Do you want submodules organized in category folders (core/, cloud/, etc.) or flat?

2. **Training content**: Is az1.ai-coditect-ai-syllubus-curriculum-course-material ready to add, or in progress?

3. **Foundation DB**: Is coditect-foundation-db ready for rollout, or still R&D?

4. **Enterprise agents**: What's in coditect-enterprise-agents - ready for market?

5. **The "coditect-projects" repo**: What is its purpose vs rollout-master?

---

## Approval Checklist

- [ ] Naming convention approved
- [ ] Consolidations approved
- [ ] New additions approved
- [ ] Subfolder structure approved
- [ ] Ready to execute Phase 1

---

*Proposal Version: 1.0*
*Date: 2025-11-19*
*Author: Claude Code*
