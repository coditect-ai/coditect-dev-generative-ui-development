# Infrastructure Analysis: GKE Integration vs. Separation

**Date:** 2025-11-17
**Decision:** Week 1 PostgreSQL Deployment Strategy
**Status:** Analysis Complete - Awaiting Decision

---

## Executive Summary

**Recommendation:** **CREATE NEW PROJECT** with separate GKE cluster for CODITECT Week 1 deployment.

**Confidence:** 90% - Clear separation of concerns outweighs integration benefits for pilot phase.

**Key Rationale:**
1. **Blast radius containment** - Week 1 is experimental pilot
2. **Clean accounting** - Separate billing tracking for CODITECT platform
3. **Independent scaling** - Different resource profiles (POC vs. production SaaS)
4. **Easier rollback** - Can delete entire project if Week 1 fails

---

## Existing Infrastructure Analysis

### Current GKE Cluster: `codi-poc-e2-cluster`

**Project:** serene-voltage-464305-n2
**Purpose:** CODITECT v5 IDE POC (Proof of Concept)

| Attribute | Value | Implications |
|-----------|-------|-------------|
| **Location** | us-central1-a | Single-zone (lower cost, lower availability) |
| **Node Count** | 4 (2-10 autoscaling) | Medium utilization capacity |
| **Machine Type** | e2-standard-4 | 4 vCPU, 16 GB RAM per node |
| **Total Capacity** | 16 vCPU, 64 GB RAM | Currently allocated to POC workload |
| **Network** | default VPC | Shared network namespace |
| **Workload Label** | codi-poc | Tagged as proof-of-concept |
| **Release Channel** | REGULAR | Moderate update cadence |
| **Created** | 2025-09-05 | 2.5 months old |

**Current Resource Allocation:**
- **Unknown workload utilization** (kubectl access blocked)
- **Assumption:** POC workload is using significant portion of cluster
- **Risk:** Resource contention if we add Week 1 workload

---

## Option 1: Integrate with Existing GKE Cluster

### Approach
Deploy Cloud SQL + FastAPI backend to existing `codi-poc-e2-cluster`.

### Pros ✅

1. **Cost Savings ($150-200/month)**
   - Reuse existing cluster infrastructure
   - No additional control plane costs
   - Share node pool across workloads

2. **Faster Setup (2-3 hours)**
   - Cluster already provisioned
   - Network already configured
   - No IAM/firewall setup needed

3. **Resource Efficiency**
   - Utilize spare capacity on existing nodes
   - Better bin-packing of workloads
   - Kubernetes autoscaling handles both workloads

4. **Simplified Networking**
   - Both workloads in same VPC
   - No VPC peering needed
   - Easier service-to-service communication

### Cons ❌

1. **Blast Radius Risk (HIGH)**
   - Week 1 experiment could impact POC workload
   - POC workload could impact Week 1 pilot
   - Shared failure modes (node crashes, network issues)

2. **Resource Contention (MEDIUM)**
   - Unknown POC resource usage
   - Potential CPU/memory conflicts
   - Risk of OOM kills or throttling

3. **Namespace Complexity (LOW)**
   - Need strict RBAC boundaries
   - Separate secrets/configmaps
   - Risk of accidental cross-namespace operations

4. **Billing Confusion (MEDIUM)**
   - Cannot isolate CODITECT platform costs
   - POC costs mixed with Week 1 costs
   - Harder to justify ROI to stakeholders

5. **Cleanup Complexity (HIGH)**
   - Cannot delete everything if Week 1 fails
   - Must manually remove deployments, services, PVCs
   - Risk of orphaned resources

6. **Different Lifecycle (HIGH)**
   - POC is experimental, Week 1 is path-to-production
   - Different update cadences
   - Different monitoring/alerting requirements

---

## Option 2: Separate GKE Cluster (NEW PROJECT)

### Approach
Create new GCP project `coditect-week1-pilot` with dedicated GKE cluster.

### Pros ✅

1. **Clean Separation (CRITICAL)**
   - Zero blast radius to existing POC
   - Independent scaling and resource allocation
   - No contention or interference

2. **Clear Accounting (HIGH VALUE)**
   - Dedicated billing for CODITECT platform
   - Easy ROI calculation for Week 1
   - Clean P&L tracking for stakeholders

3. **Independent Lifecycle (HIGH VALUE)**
   - Can upgrade/downgrade independently
   - Different SLAs (POC vs. pilot)
   - Can delete entire project if pilot fails

4. **Production-Ready Path (STRATEGIC)**
   - Week 1 → Week 10 → Production in same project
   - No migration needed from POC to production
   - Cleaner promotion path

5. **Better Security Boundaries (MEDIUM)**
   - Separate IAM policies
   - Different service accounts
   - No cross-project IAM conflicts

6. **Easier Rollback (HIGH)**
   - Single command: `gcloud projects delete coditect-week1-pilot`
   - No risk of deleting POC resources
   - Clean slate if needed

### Cons ❌

1. **Higher Cost ($150-200/month)**
   - Additional GKE control plane: ~$75/month
   - Additional nodes: ~$75-125/month
   - Total: ~$150-200/month additional

2. **Slower Setup (4-6 hours)**
   - Create new project
   - Provision GKE cluster
   - Configure networking
   - Setup IAM/RBAC

3. **Network Complexity (LOW)**
   - Need VPC peering if POC/Week1 must communicate
   - Separate firewall rules
   - More complex DNS setup

4. **Operational Overhead (LOW)**
   - Two clusters to monitor
   - Two clusters to upgrade
   - Separate dashboards

---

## Decision Matrix

| Criteria | Weight | Integrate | Separate | Winner |
|----------|--------|-----------|----------|--------|
| **Blast Radius** | 25% | 3/10 | 10/10 | **Separate** |
| **Cost** | 15% | 10/10 | 6/10 | Integrate |
| **Speed to Deploy** | 10% | 9/10 | 6/10 | Integrate |
| **Billing Clarity** | 20% | 4/10 | 10/10 | **Separate** |
| **Production Path** | 20% | 5/10 | 10/10 | **Separate** |
| **Rollback Ease** | 10% | 4/10 | 10/10 | **Separate** |
| **Total Score** | 100% | **5.5/10** | **9.0/10** | **🏆 Separate** |

**Winner:** **Separate GKE Cluster** (9.0/10 vs. 5.5/10)

---

## Recommended Architecture

### New Project Configuration

**Project ID:** `coditect-week1-pilot` (or `coditect-platform-dev`)
**Billing Account:** Same as `serene-voltage-464305-n2`
**Organization:** Same (1015420128875)
**Region:** us-central1 (same as existing)

### GKE Cluster Specification

**Cluster Name:** `coditect-platform-cluster`
**Zone:** us-central1-a (or multi-zone: us-central1-a,b,c)

**Node Pool:**
- **Machine Type:** e2-standard-2 (2 vCPU, 8 GB RAM) - smaller for pilot
- **Node Count:** 2-6 (autoscaling)
- **Disk:** 50 GB SSD per node
- **Network:** VPC auto-mode (isolated from POC)

**Features:**
- Workload Identity: Enabled
- Managed Prometheus: Enabled
- Release Channel: REGULAR
- Auto-upgrade: Enabled
- Auto-repair: Enabled

### Cloud SQL Configuration

**Instance Name:** `coditect-platform-db`
**Version:** PostgreSQL 15
**Tier:** db-f1-micro (for pilot, upgradeable)
**Region:** us-central1
**HA:** Disabled (single-zone for pilot)
**Backup:** Daily (7-day retention)
**Network:** Private IP (VPC peering with GKE)

### Cost Estimate (Week 1 Pilot)

| Resource | Quantity | Unit Cost | Monthly Cost |
|----------|----------|-----------|--------------|
| GKE Control Plane | 1 | $75/mo | $75 |
| e2-standard-2 Nodes | 2-3 avg | $25/mo each | $60 |
| Cloud SQL (db-f1-micro) | 1 | $8/mo | $8 |
| Storage (100 GB) | 100 GB | $0.17/GB | $17 |
| Network Egress | ~10 GB | $0.12/GB | $1 |
| **Total** | | | **~$161/month** |

**Annual Cost (if scaled to production):** ~$2,000-3,500/year

---

## Migration Path (Week 1 → Production)

### Phase 1: Week 1 Pilot (Current)
- Project: `coditect-week1-pilot`
- Cluster: `coditect-platform-cluster` (dev tier)
- Cloud SQL: `db-f1-micro`
- Users: Internal testing only

### Phase 2: Week 10 Pilot Launch
- **Same project, same cluster**
- Upgrade Cloud SQL: `db-f1-micro` → `db-g1-small`
- Add HA: Enable multi-zone
- Scale nodes: 3-8 autoscaling
- Users: 50-100 pilot users

### Phase 3: Production (3-6 months)
- **Same project, same cluster**
- Upgrade Cloud SQL: `db-g1-small` → `db-custom-4-16384` (4 vCPU, 16 GB)
- Multi-region setup (GKE + Cloud SQL)
- Scale nodes: 5-15 autoscaling
- Users: 500+ production users

**Benefit:** No project migration, just in-place upgrades. Clean lineage from Week 1 → Production.

---

## Risk Analysis

### Risk: Higher Cost

**Probability:** 100% (certain)
**Impact:** LOW ($161/month = $5.37/day)
**Mitigation:**
- Budget approved in Week 1 plan ($17,500 total, infrastructure ~$500)
- Cost is <1% of Week 1 budget
- Clean accounting justifies ROI

**Status:** ACCEPTED RISK ✅

### Risk: Slower Setup

**Probability:** 100% (certain)
**Impact:** LOW (4-6 hours one-time delay)
**Mitigation:**
- Use automated Terraform scripts
- GKE provisioning is parallelizable with backend development
- Can start backend implementation while cluster provisions

**Status:** ACCEPTED RISK ✅

### Risk: Network Complexity

**Probability:** 50% (if POC/Week1 need to communicate)
**Impact:** MEDIUM (VPC peering setup)
**Mitigation:**
- Week 1 is standalone, no POC dependency
- If needed, VPC peering is 30-minute setup
- Cloud DNS handles cross-VPC resolution

**Status:** LOW RISK (unlikely need) ✅

---

## Recommendation

### ✅ CREATE NEW PROJECT: `coditect-week1-pilot`

**Justification:**
1. **Week 1 is a pilot** - Experimental, may fail, needs clean rollback
2. **Billing clarity** - Stakeholders need clear ROI data
3. **Blast radius** - Zero impact to existing POC workload
4. **Production path** - Same project can scale to production
5. **Cost acceptable** - $161/month is <1% of Week 1 budget

**Next Steps:**
1. Create new GCP project with same billing account
2. Provision GKE cluster (e2-standard-2, 2-6 nodes)
3. Deploy Cloud SQL (db-f1-micro, PostgreSQL 15)
4. Apply database schema + RLS policies
5. Deploy FastAPI backend
6. Run integration tests

---

## Alternative: Hybrid Approach (NOT RECOMMENDED)

**Scenario:** Use existing GKE for backend, separate Cloud SQL.

**Why NOT Recommended:**
- Worst of both worlds: resource contention + split costs
- Database is isolated but compute is shared
- Still risky blast radius to POC
- Cleanup complexity remains

**Decision:** REJECTED ❌

---

## Billing Account Selection

### Available Billing Accounts

| Account ID | Display Name | Status | Current Usage |
|-----------|--------------|--------|---------------|
| 013AA8-3BF2B2-DD428A | My Billing Account | Open | Unknown |
| 018452-0097F3-759E3B | My Billing Account | Open | Unknown |
| **01C53B-47A12B-A7F32D** | **My Billing Account** | **Open** | **serene-voltage-464305-n2** |

### ✅ Selected Billing Account

**Account ID:** `01C53B-47A12B-A7F32D`
**Display Name:** My Billing Account
**Status:** Open (Active)

### Rationale for Selection

**Primary Reason:** **Consistency with existing CODITECT infrastructure**

1. **Same as serene-voltage-464305-n2**
   - Existing CODITECT POC project uses this billing account
   - Keeps all CODITECT-related charges in one place
   - Easier consolidated billing reports

2. **Unified Cost Tracking**
   - All CODITECT costs (POC + Week 1 + future) on single account
   - Simplified accounting for stakeholders
   - Single invoice for all CODITECT infrastructure

3. **Simplified Budgeting**
   - Can set budget alerts at billing account level
   - Track total CODITECT platform spend across all projects
   - Easier variance analysis (planned vs. actual)

4. **Organizational Consistency**
   - Both projects under same organization (1015420128875)
   - Same billing account = administrative consistency
   - Reduces IAM complexity

### Alternative Billing Accounts (Not Selected)

**013AA8-3BF2B2-DD428A:**
- **Reason Not Selected:** No existing CODITECT usage
- **Potential Use:** Future production workload separation (if needed)

**018452-0097F3-759E3B:**
- **Reason Not Selected:** No existing CODITECT usage
- **Potential Use:** Reserved for non-CODITECT projects

### Billing Account Validation

```bash
# Verify existing project billing
$ gcloud beta billing projects describe serene-voltage-464305-n2 \
    --format="value(billingAccountName)"
billingAccounts/01C53B-47A12B-A7F32D  ✅

# Confirm account is active
$ gcloud beta billing accounts list --filter="name:01C53B-47A12B-A7F32D"
ACCOUNT_ID            NAME                OPEN
01C53B-47A12B-A7F32D  My Billing Account  True  ✅
```

**Status:** VERIFIED ✅

### Cost Projection (Billing Account Level)

| Project | Monthly Cost | Annual Cost | Purpose |
|---------|--------------|-------------|---------|
| serene-voltage-464305-n2 | ~$200-300 | ~$2,400-3,600 | CODITECT v5 IDE POC |
| **coditect-week1-pilot** | **~$161** | **~$1,932** | **Week 1 Pilot** |
| **Total (Billing Account)** | **~$361-461** | **~$4,332-5,532** | **Combined** |

**Budget Impact:** Within acceptable range for dual-project CODITECT infrastructure.

---

## Implementation Plan

### Step 1: Create New GCP Project (10 minutes)

```bash
# Create project
gcloud projects create coditect-week1-pilot \
  --organization=1015420128875 \
  --name="CODITECT Week 1 Pilot"

# Link billing (SAME account as serene-voltage-464305-n2)
gcloud billing projects link coditect-week1-pilot \
  --billing-account=01C53B-47A12B-A7F32D

# Verify billing link
gcloud beta billing projects describe coditect-week1-pilot \
  --format="value(billingAccountName)"
# Should output: billingAccounts/01C53B-47A12B-A7F32D ✅

# Set as active project
gcloud config set project coditect-week1-pilot
```

### Step 2: Enable APIs (5 minutes)

```bash
gcloud services enable \
  container.googleapis.com \
  sqladmin.googleapis.com \
  compute.googleapis.com \
  servicenetworking.googleapis.com \
  secretmanager.googleapis.com
```

### Step 3: Provision GKE Cluster (15-20 minutes)

```bash
gcloud container clusters create coditect-platform-cluster \
  --zone=us-central1-a \
  --machine-type=e2-standard-2 \
  --num-nodes=2 \
  --enable-autoscaling \
  --min-nodes=2 \
  --max-nodes=6 \
  --enable-workload-identity \
  --enable-cloud-monitoring \
  --enable-cloud-logging \
  --release-channel=regular \
  --disk-size=50 \
  --disk-type=pd-standard \
  --labels=environment=pilot,project=coditect-week1
```

### Step 4: Deploy Cloud SQL (15-20 minutes)

```bash
# Deploy using automated script (created by devops-engineer)
cd /Users/halcasteel/PROJECTS/coditect-rollout-master/submodules/coditect-cloud-backend
./deployment/deploy-cloud-sql.sh
```

### Step 5: Apply Schema + RLS (5 minutes)

```bash
# Apply schema
psql -h <cloud-sql-ip> -U coditect_app -d coditect_dev \
  -f database/migrations/001_initial_schema.sql

# Apply RLS policies
psql -h <cloud-sql-ip> -U coditect_app -d coditect_dev \
  -f database/rls_policies.sql

# Optionally apply seed data
psql -h <cloud-sql-ip> -U coditect_app -d coditect_dev \
  -f database/seeds/dev_seed_data.sql
```

### Step 6: Deploy Backend (Phase 2.2)

*Backend implementation pending*

**Total Setup Time:** 50-60 minutes (mostly automated, mostly waiting)

---

## Cost-Benefit Analysis

### Option 1: Integrate (Existing Cluster)
**Monthly Cost:** $0 (using existing resources)
**Risk Cost:** HIGH (blast radius, cleanup complexity, billing confusion)
**Total Cost:** HIGH RISK (unknown failure cost)

### Option 2: Separate (New Project)
**Monthly Cost:** $161/month
**Risk Cost:** LOW (isolated, easy rollback, clean accounting)
**Total Cost:** LOW RISK + predictable cost

**ROI:**
- Week 1 budget: $17,500
- Infrastructure cost: $161/month × 1 month = $161
- Infrastructure % of budget: 0.9%
- **Conclusion:** Negligible cost for massive risk reduction ✅

---

## Final Recommendation

### ✅ APPROVED: Create New Project `coditect-week1-pilot`

**Rationale Summary:**
1. **Isolation:** Zero blast radius to existing POC
2. **Accounting:** Clean billing for CODITECT platform
3. **Rollback:** Single command to delete if Week 1 fails
4. **Production Path:** Same project scales to production
5. **Cost:** $161/month is negligible (0.9% of Week 1 budget)

**Confidence:** 90%

**Risk Level:** LOW ✅

**Next Action:** Execute Step 1 (Create new GCP project)

---

**Prepared by:** Claude (autonomous infrastructure analysis)
**Date:** 2025-11-17
**Status:** READY FOR APPROVAL
**Awaiting:** Executive decision to proceed

