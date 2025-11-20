# Repository Audit - 2025-11-19

## Summary

| Organization | Count | Primary Purpose |
|-------------|-------|-----------------|
| **coditect-ai** | 51 | CODITECT product repos |
| **halcasteel** | 46 | Personal projects, legacy tools |
| **az1-ai** | 76 | Company R&D, TELLER, experiments |
| **Total** | **173** | |

---

## Recommended Actions

### 1. KEEP & RENAME (Core CODITECT Product) - 35 repos

These are the active CODITECT product repos that should follow the new naming convention.

#### coditect-ai org (migrate to naming convention)

| Current Name | Proposed Name | Category |
|-------------|---------------|----------|
| coditect-project-dot-claude | coditect-core-framework | core |
| coditect-framework | coditect-core-agents | core |
| coditect-distributed-architecture | coditect-core-architecture | core |
| coditect-cloud-backend | coditect-cloud-backend | cloud |
| coditect-cloud-frontend | coditect-cloud-frontend | cloud |
| coditect-infrastructure | coditect-cloud-infrastructure | cloud |
| coditect-cli | coditect-dev-cli | dev |
| coditect-automation | coditect-dev-automation | dev |
| coditect-analytics | coditect-dev-analytics | dev |
| coditect-context-api | coditect-dev-context-api | dev |
| coditect-project-intelligence | coditect-dev-intelligence | dev |
| coditect-agent-marketplace | coditect-market-agents | market |
| coditect-activity-data-model-ui | coditect-market-activity-ui | market |
| coditect-docs | coditect-docs-main | docs |
| coditect-legal | coditect-docs-legal | docs |
| coditect-blog-application | coditect-docs-blog | docs |
| coditect-rollout-master | coditect-ops-rollout | ops |
| coditect-installer | coditect-ops-installer | ops |
| coditect-license-manager | coditect-ops-license | ops |
| coditect-license-server | coditect-ops-license-server | ops |
| coditect-communications | coditect-gtm-communications | gtm |
| az1.ai-CODITECT.AI-GTM | coditect-gtm-strategy | gtm |
| coditect-interactive-workflow-analyzer | coditect-labs-workflow-analyzer | labs |
| Coditect-v5-multiple-LLM-IDE | coditect-labs-multi-llm-ide | labs |
| NESTED-LEARNING-GOOGLE | coditect-labs-nested-learning | labs |
| az1.ai-coditect-agent-new-standard-development | coditect-labs-agent-standards | labs |
| CODITECTv4 | coditect-labs-v4-archive | labs |

#### halcasteel account (transfer to coditect-ai)

| Current Name | Proposed Name | Category |
|-------------|---------------|----------|
| coditect | coditect-ops-distribution | ops |
| coditect-competition | coditect-gtm-competition | gtm |
| coditect-core-1.0 | (merge or archive) | - |

---

### 2. ARCHIVE (Stale/Superseded) - ~60 repos

These repos haven't been updated in 6+ months or are superseded.

#### halcasteel (mostly 2023-2024 personal tools)

| Repo | Last Updated | Reason |
|------|-------------|--------|
| PDF2TXT2HTML | 2023-12 | Superseded by coditect-pdf-convertor |
| MHTML | 2023-12 | Legacy utility |
| HTML2TEXT | 2023-12 | Legacy utility |
| PRETTY2HTML | 2023-12 | Legacy utility |
| chatgpt_frontend | 2023-12 | Obsolete |
| PDFConvertorTokenCounter | 2024-01 | Superseded |
| my_audio_transcription_project | 2024-01 | Superseded |
| Scrapy_NewProject | 2024-01 | Experiment |
| SaveImagesFromURL | 2024-01 | Simple utility |
| SPIDER_URLS | 2024-01 | Experiment |
| BuildBibliography | 2024-01 | Legacy |
| FilesReName | 2024-01 | Simple script |
| GoogleAppScripts | 2024-01 | Scripts collection |
| googleappscript_format_doc | 2024-01 | Legacy |
| convertMD2TXT2HTML | 2024-01 | Superseded |
| dlYT_downloader | 2024-02 | Utility |
| md2md | 2024-03 | Legacy |
| convertPDF2TXT2MD2HTML | 2024-07 | Superseded |
| prettifier | 2024-07 | Legacy |
| google_doc_prettifier_v1 | 2024-07 | Legacy |
| p1 | 2024-09 | Unknown/temp |
| convert_json2csv_txt | 2024-10 | Simple utility |
| graphrag-app | 2024-10 | Superseded |
| graphrag-app-claude-analysis | 2024-11 | Superseded |
| GraphRAG_PROJECT_FUTURE_UPDATES_THOUGHTS | 2024-10 | Planning doc |
| CALENDAR_PROJECT_WIP | 2024-10 | Superseded |
| AI_BOOK_FRAMEWORK_APP | 2024-10 | Superseded |
| 000_AI_DOCUMENT_MANAGEMENT_SYSTEM | 2024-11 | Superseded |
| enhanced_git_init_python_app | 2024-11 | Simple utility |
| git_init_python_script | 2024-11 | Simple utility |
| generate_git_status_report | 2024-10 | Simple utility |
| python_file_copier | 2024-10 | Simple utility |
| formatGdoc | 2024-11 | Superseded |
| hybridagi-analysis-initial | 2024-11 | Research complete |
| formatGDOC.3.0 | 2024-12 | Superseded |
| JSON-File-Manager-Navigator-MongoDB | 2024-12 | Experiment |

#### az1-ai (old projects and experiments)

| Repo | Last Updated | Reason |
|------|-------------|--------|
| TELLER-v2 | 2025-05 | Old product |
| TELLER-NEW | 2025-06 | Old product |
| TELLER-GCP-PHASE1-PHASE2 | 2025-07 | Old product |
| TELLER-DIALOGS-* | 2025-07 | Old product |
| runway-calculator-rust-wasm | 2025-03 | Learning project |
| yew-wasm-starter-runway-calculator | 2025-03 | Learning project |
| os-marketplace | 2025-03 | Early concept |
| llm-aider-ide | 2025-03 | Early concept |
| new-front-end-az1.ai-workbench | 2025-03 | Superseded |
| agentic-system-evaluation | 2025-04 | Research complete |
| local-markdown-graphrag | 2025-04 | Experiment |
| markdown-local-markdown-search | 2025-04 | Experiment |
| neo-graph-rag-search | 2025-04 | Experiment |
| scraper2-cli-docker | 2025-04 | Utility |
| backup-google-cloud-storage | 2025-05 | Simple utility |
| gc-backup-buckets | 2025-05 | Simple utility |
| wasm-rust-webscraper | 2025-05 | Experiment |
| z-webscraper | 2025-05 | Experiment |
| whitepaper-generation-mcp | 2025-05 | Experiment |
| master-prompt-json-to-arangodb | 2025-05 | Experiment |
| process-manager | 2025-05 | Experiment |
| AGENTIC-SYSTEM-UI | 2025-05 | Superseded |
| AZ1-AI_AI-CODING-FRAMEWORK | 2025-05 | Superseded by CODITECT |
| 0000-MULTI-AGENT-AGENTIC-SYSTEM-A2A | 2025-05 | Superseded |
| AZ1-AI-MULTI-AGENT-PLATFORM-HUGGIN-A2A | 2025-06 | Superseded |
| life-sciences-regulatory-compliance-* | 2025-05 | Client project complete |
| academic-scraper | 2025-06 | Utility |
| web-scraper-latest | 2025-06 | Utility |
| 00-CORE-AZ1 | 2025-06 | Superseded |
| CORE-AZ1-0001 | 2025-06 | Superseded |
| bookmark-manager | 2025-06 | Simple utility |
| manafold-analysis | 2025-06 | Research complete |
| CLAUDIA-ANALYSIS | 2025-06 | Research complete |
| CODITECT.AI | 2025-06 | Superseded |
| coditect-0000 | 2025-06 | Early version |
| coditect-0001 | 2025-06 | Early version |
| CLAUDE-CODE-CORE-MASTER-PROMPTS | 2025-06 | Merged into framework |
| neo4j-graph-rag-prompt-management-0000 | 2025-07 | Experiment |
| coditect-ide-ai | 2025-07 | Superseded |
| cap-table-enterprise | 2025-07 | Side project |
| death-by-dinner | 2025-07 | Side project |
| elevate-packaging-matias | 2025-07 | Client project |
| autonomous-adr-submodule | 2025-07 | Merged |
| AZ1-CODITECT-INITIAL-PROJECT-SETUP-HOW-TO | 2025-07 | Outdated docs |
| utf-8-google-app-script-gdocs-fix | 2025-07 | Utility |
| vertex-ai-workshop | 2025-07 | Learning |

---

### 3. KEEP AS-IS (Non-CODITECT) - ~25 repos

These serve specific purposes outside CODITECT.

#### halcasteel (public utilities)

| Repo | Purpose | Action |
|------|---------|--------|
| Markdown-to-PDF-CONVERTOR | Public tool | Keep |
| backup2usb-chromeos | Public tool | Keep |
| chrome-bookmark-organizer | Public tool | Keep |
| google-tir-judge-research | Research | Keep |
| sustainability-application | Project | Keep |
| desktop-tutorial | GitHub template | Keep or delete |

#### az1-ai (business & infrastructure)

| Repo | Purpose | Action |
|------|---------|--------|
| AZ1.AI-INVESTMENT-BRIEFINGS | Business docs | Keep (rename az1-docs-investment) |
| az1-business-foundation-documentation | Business docs | Keep (rename az1-docs-foundation) |
| az1.ai-legal-foundation-document-drafts | Legal | Keep (rename az1-docs-legal) |
| business_master_documents | Business | Keep (merge with above) |
| hal-mac-air-m4-16gb | Personal setup | Keep |
| amd395-ai-max-plus-linux-setup | Hardware setup | Keep |
| amd395-ai-max-plus-windows-linux-vm-setup | Hardware setup | Keep |
| mac-os-systemd-brew-update-controls | System config | Keep |
| docker-debian-windows-how-to | DevOps docs | Keep |
| gitea-gcp-github-mirroring | Infrastructure | Keep |
| ibm-ai-thought-leadership | Research | Keep |

---

### 4. CONSOLIDATE (Duplicate/Related) - ~15 repos

These can be merged into single repos.

| Current Repos | Merge Into |
|--------------|------------|
| coditect-license-manager + coditect-license-server | coditect-ops-licensing |
| az1.ai-coditect-audio2text-workflow + my_audio_transcription_project | Archive both (use existing tools) |
| Multiple PDF converters (6+ repos) | Archive all (use existing tools) |
| Multiple web scrapers (5+ repos) | Archive all (use existing tools) |
| calendar-scheduling-with-survey-form + AZ1.AI-CODITECT-CALENDAR-SCHEDULING-APPLICATION-SaaS + CALENDAR_PROJECT_WIP | coditect-market-calendar |
| coditect-installer + coditect (halcasteel) | coditect-ops-distribution |
| Format/prettifier repos (5+ repos) | Archive all |

---

### 5. INVESTIGATE (Unclear Purpose) - ~10 repos

| Repo | Notes |
|------|-------|
| agents-research-plan-code | Active (Nov 19) - what is this? |
| coditect-projects | Active (Nov 19) - vs rollout-master? |
| claude-code-functionality-tools-research | Active - keep as labs? |
| claude-cli-web-architecture | What is this? |
| coditect-claude-code-initial-setup | Outdated setup guide? |
| product-legitimacy-enterprise-software | Research? |
| find-me-a-mechanic | Side project? |
| hookup-app-2025-10-09 | Side project? |
| coditect-customer-clipora-ravi-mehta | Customer project? |
| coditect-persona-customer-questions | Research? |
| az1.ai-coditect-norcal-eco-divers-Naniloa | Side project? |
| az1.ai-coditect-contact-qr-code-generator | Utility? |
| az1.ai-coditect-first-principles-analysis | Research? |
| scientific-business-analysis-process-application | Research? |
| stochastic-computing-with-semantic-programming-using-llms | Research? |
| autonomous-software-analysis-competitive-landscape-BLITZY | Research? |
| claude-state-management | Merged into framework? |
| coditect-foundation-db | Active development? |
| coditect-gcp-migration | Active? |
| coditect-enterprise-agents | Active? |
| linux-process-manager-dashboard | Utility? |
| weather-app | Learning project? |

---

## Proposed Naming Convention

### Categories

| Prefix | Purpose | Example |
|--------|---------|---------|
| `coditect-core-` | Foundation, framework, architecture | coditect-core-framework |
| `coditect-cloud-` | Cloud platform services | coditect-cloud-backend |
| `coditect-dev-` | Developer tools | coditect-dev-cli |
| `coditect-market-` | Marketplace & products | coditect-market-agents |
| `coditect-docs-` | Documentation | coditect-docs-main |
| `coditect-ops-` | Operations, DevOps | coditect-ops-distribution |
| `coditect-gtm-` | Go-to-market | coditect-gtm-strategy |
| `coditect-labs-` | Research & experiments | coditect-labs-v4-archive |

### Non-CODITECT repos

| Prefix | Purpose | Example |
|--------|---------|---------|
| `az1-docs-` | AZ1.AI company documents | az1-docs-legal |
| `az1-infra-` | AZ1.AI infrastructure | az1-infra-gcp |
| `az1-client-` | Client projects | az1-client-clipora |

---

## Migration Plan

### Phase 1: Clean Up (Week 1)
- [ ] Archive 60 stale repos
- [ ] Delete test/temp repos
- [ ] Consolidate duplicates

### Phase 2: Organize (Week 2)
- [ ] Transfer halcasteel CODITECT repos to coditect-ai org
- [ ] Apply naming convention to core 35 repos
- [ ] Update all .gitmodules

### Phase 3: Document (Week 3)
- [ ] Update all READMEs with new repo names
- [ ] Update CI/CD workflows
- [ ] Update install.sh/update.sh URLs
- [ ] Create master repo index

### Phase 4: Communicate (Week 4)
- [ ] Update internal documentation
- [ ] Notify team of new structure
- [ ] Create onboarding guide

---

## Expected Outcome

**Before:** 173 repos scattered across 3 accounts with inconsistent naming

**After:** ~50 active repos in coditect-ai org with clear naming convention

| Metric | Before | After |
|--------|--------|-------|
| Total repos | 173 | ~50 |
| Organizations | 3 | 1 (coditect-ai) |
| Naming patterns | 10+ | 1 |
| Finding a repo | Minutes | Seconds |

---

## Next Steps

1. **Review this audit** - Correct any miscategorizations
2. **Decide on archives** - Confirm repos to archive
3. **Clarify unknowns** - Explain purpose of "investigate" repos
4. **Approve naming convention** - Finalize category prefixes
5. **Begin Phase 1** - Start archiving

---

*Generated: 2025-11-19*
*Author: Claude Code*
