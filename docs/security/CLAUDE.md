# Security Documentation - Claude Code Configuration

## Directory Purpose

Security advisories, compliance documentation, and GCP security notifications for CODITECT platform.

## Essential Reading

**READ FIRST:**
1. container-contract.html - GCP Cloud Run security requirements
2. Recent security advisories in coditect-google-security-advisories/
3. ../adrs/ADR-007 (GCP deployment), ADR-008 (RBAC), ADR-004 (multi-tenancy)

## Security Context

**Cloud Provider:** Google Cloud Platform (GCP)
**Deployment Model:** Cloud Run containers (ADR-007)
**Security Model:** RBAC + Multi-tenant schema isolation
**Monitored Assets:** Cloud Run services, Cloud SQL, Artifact Registry

## Key Security Files

### Container Security Contract
- **File:** coditect-google-security-advisories/container-contract.html
- **Purpose:** GCP Cloud Run container security requirements
- **Size:** 300KB
- **Content:** Image requirements, vulnerability scanning, runtime constraints

### Security Advisories
- **Directory:** coditect-google-security-advisories/
- **Count:** 1 tracked advisory
- **Format:** HTML exports from GCP Security Command Center
- **Latest:** November 21, 2025

## Security Best Practices

### Container Security
- Scan images before deployment (Artifact Registry)
- Use minimal base images (distroless, Alpine)
- Run as non-root user
- Read-only filesystems
- Never hardcode secrets

### Cloud Run Security
- Enable binary authorization
- IAM least privilege
- VPC egress controls
- Audit logging enabled
- Cloud Armor for DDoS

### Application Security
- JWT validation on all endpoints (ADR-008)
- SQL parameterized queries (ADR-002)
- Schema-based tenant isolation (ADR-004)
- Input validation and sanitization
- CSRF protection

### Secrets Management
- Use Google Secret Manager
- Never commit secrets to Git
- Rotate credentials regularly
- Audit secret access

## Common Operations

### Review Security Advisories
```bash
# List recent advisories
ls -lt coditect-google-security-advisories/

# View latest notification
open coditect-google-security-advisories/*.html

# Check metadata
cat coditect-google-security-advisories/attachment.csv
```

### Container Compliance Check
```bash
# Review contract
open coditect-google-security-advisories/container-contract.html

# Validate deployment meets requirements
```

### Scan Dependencies
```bash
# Python
pip install safety
safety check

# Node.js
npm audit
```

## Project-Specific Instructions

### Before Deployment
1. Scan container images (Artifact Registry)
2. Validate against container-contract.html
3. Check no hardcoded secrets
4. Review IAM permissions
5. Enable audit logging

### After Security Advisory
1. Export notification from GCP Console
2. Save HTML to coditect-google-security-advisories/
3. Assess impact on CODITECT components
4. Create remediation tasks in ../project-management/TASKLIST.md
5. Document fix in MEMORY-CONTEXT checkpoint

### Code Review Security Checks
1. No credentials in code
2. JWT validation on protected endpoints
3. SQL queries use parameters (no string concat)
4. Schema filtering for multi-tenancy
5. RBAC checks before data access
6. Input validation on all endpoints
7. Error messages don't leak sensitive data

### Security Incident Response
1. Export GCP notification to HTML
2. Document in coditect-google-security-advisories/
3. Create tasks in TASKLIST.md
4. Implement remediation
5. Validate fix
6. Update compliance reports

## Cross-References

**Architecture:**
- ../adrs/ADR-007 - GCP Cloud Run deployment
- ../adrs/ADR-008 - RBAC permissions
- ../adrs/ADR-004 - Multi-tenant isolation
- ../adrs/ADR-002 - Database security

**Implementation:**
- submodules/cloud/coditect-cloud-backend/ - Apply security practices
- submodules/dev/ - Security scanning tools

**Planning:**
- ../project-management/TASKLIST.md - Track security tasks

## Important Constraints

### Never Commit
- API keys, tokens, credentials
- .env files with secrets
- SSL certificates or private keys
- Database passwords
- JWT signing keys

### Always Use
- Google Secret Manager for credentials
- Environment variables for config
- IAM service accounts (no user credentials)
- Encrypted connections (TLS/SSL)
- Audit logging

### Multi-Tenancy (ADR-004)
- All queries MUST filter by tenant schema
- Never cross-tenant data access
- Validate tenant context on every request

### Access Control (ADR-008)
- Check JWT token validity
- Validate user permissions
- Enforce RBAC at API layer
- Audit all permission changes

## Quality Gates

**Before Code Merge:**
- [ ] No credentials in code
- [ ] Security best practices followed
- [ ] Dependencies scanned
- [ ] RBAC implemented correctly

**Before Deployment:**
- [ ] Container image scanned
- [ ] Secrets in Secret Manager
- [ ] IAM permissions reviewed
- [ ] Audit logging enabled
- [ ] Container contract validated

**Monthly Security Review:**
- [ ] Check new GCP advisories
- [ ] Scan all dependencies
- [ ] Review IAM permissions
- [ ] Validate RBAC enforcement
- [ ] Audit log analysis

## Security Monitoring

### GCP Resources
- Security Command Center
- Cloud Armor
- Artifact Registry scanning
- Cloud Audit Logs
- VPC Flow Logs

### Application Monitoring
- Failed authentication attempts
- Permission denied events
- Unusual data access patterns
- API rate limit violations

## Incident Contacts

**Security Lead:** Hal Casteel, CTO
**Email:** security@az1.ai
**GCP Console:** Security Command Center
**Response Time:** Critical < 4hrs, High < 24hrs

---

**Status:** ✅ Production Ready
**Last Updated:** 2025-11-22
**Review Frequency:** Weekly during active development, monthly in maintenance
