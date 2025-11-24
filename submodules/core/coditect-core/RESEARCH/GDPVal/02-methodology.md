# GDPval: Methodology

## 1. Occupation Prioritization

### Selection Criteria

1. **Sector Selection**: Sectors contributing >5% to US GDP (Q2 2024 Value Added by Industry)
2. **Occupation Selection**: Top 5 occupations per sector by total wages/compensation
3. **Digital Classification**: ≥60% of O*NET tasks classified as "digital" (weighted by relevance, importance, frequency)

### The 9 Sectors Covered

| Sector | % GDP | Example Occupations |
|--------|-------|---------------------|
| Real Estate & Rental/Leasing | 13.8% | Property Managers, Real Estate Agents, Concierges |
| Government | 11.3% | Compliance Officers, Social Workers, Recreation Workers |
| Manufacturing | 10.0% | Industrial Engineers, Mechanical Engineers, Buyers/Purchasing Agents |
| Professional/Scientific/Technical | 8.1% | Software Developers, Lawyers, Accountants, Project Managers |
| Health Care & Social Assistance | 7.6% | Registered Nurses, Nurse Practitioners, Medical/Health Services Managers |
| Finance & Insurance | 7.4% | Financial Managers, Customer Service Reps, Financial Analysts |
| Retail Trade | 6.3% | General/Operations Managers, Pharmacists, Private Detectives |
| Wholesale Trade | 5.8% | Sales Managers, Sales Representatives, Order Clerks |
| Information | 5.4% | Producers/Directors, Editors, Journalists, Film/Video Editors |

### Digital Task Classification Method

```
For each occupation:
  1. Identify all tasks from O*NET database
  2. GPT-4o classifies each task as digital/non-digital
  3. Weight tasks by: relevance × importance × frequency
  4. If weighted digital share ≥ 60% → classify as "predominantly digital"
```

**Validation**: Correlated against Acemoglu & Autor (2011) task-content framework—digital tasks increase with non-routine cognitive content, decrease with routine/manual content.

---

## 2. Expert Recruitment

### Requirements

- **Minimum 4 years** professional experience in occupation
- Strong resume with professional recognition, promotion, management responsibilities
- Video interview + background check + training + quiz
- **Average experience: 14 years**

### Expert Sources (Partial List)

Fortune 500 companies, major consulting firms, government agencies:
- Tech: Google, Apple, Microsoft, Meta, IBM, Oracle
- Finance: Goldman Sachs, JPMorgan Chase, Morgan Stanley, Wells Fargo
- Healthcare: Massachusetts General Hospital, Johnson & Johnson, CVS
- Law: Paul Weiss, White & Case, Kirkland & Ellis
- Government: DOJ, FTC, DOD, CDC, US Postal Service

---

## 3. Task Creation

### Task Structure

Each task consists of:
1. **Request**: Task prompt (often with reference files)
2. **Deliverable**: Expert-created work product (ground truth)

### Reference File Complexity

| Metric | Gold Subset | Full Set |
|--------|-------------|----------|
| Max reference files per task | 17 | 38 |
| Mean reference files | 1.92 | - |
| Tasks with ≥1 reference file | 67.7% | - |

### File Types Required

- Documents: DOCX, PDF, PPTX, XLSX
- Media: Photos, Video, Audio
- Technical: CAD design files, Diagrams
- Communication: Social media posts, Customer support conversations

### Task Characteristics (Gold Subset)

| Metric | Mean | Std | Min | Max |
|--------|------|-----|-----|-----|
| Overall Quality (1-5) | 4.47 | 0.32 | 3.18 | 5.00 |
| Difficulty (1-5) | 3.32 | 0.95 | 1.00 | 5.00 |
| Representativeness (1-5) | 4.50 | 0.74 | 2.00 | 5.00 |
| Time to Complete (hrs) | 9.49 | 13.75 | 0.50 | 100.00 |
| Dollar Value | $398 | $599 | $12.59 | $4,114 |

### Dollar Value Calculation

```
Task Value = Estimated Completion Time × Median Hourly Wage (from OEWS data)
```

---

## 4. Task Quality Control Pipeline

### Multi-Stage Review Process

```
┌─────────────────────────────────────────────────────────────────────────┐
│ Stage 1: General Task Guidance                                          │
│ ┌──────────────┐    ┌──────────────┐    ┌──────────────┐               │
│ │ Task Created │ →  │ Automated    │ →  │ Generalist   │               │
│ │ by Expert    │    │ Screening    │    │ Review       │               │
│ └──────────────┘    └──────────────┘    └──────────────┘               │
└─────────────────────────────────────────────────────────────────────────┘
                                ↓
┌─────────────────────────────────────────────────────────────────────────┐
│ Stage 2: Occupation-Specific Guidance                                   │
│ ┌──────────────────────────────────────────────────────────────────┐   │
│ │ Occupational expert reviews → Author revises → Expert re-reviews │   │
│ │ (Iterative loop until quality standards met)                     │   │
│ └──────────────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────────────┘
                                ↓
┌─────────────────────────────────────────────────────────────────────────┐
│ Stage 3: Final Review                                                   │
│ ┌──────────────────────────────────────────────────────────────────┐   │
│ │ Lead reviewer provides final guidance → Sign-off or iteration   │   │
│ └──────────────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────────────┘
```

### Review Statistics

- **Average reviews per task**: 5
- **Minimum reviews per task**: 3
- **Task specification quality**: 89% rated "well-specified"

### Automated Screening Criteria

Model-based screening flags:
- Task relevance to selected O*NET occupation
- Whether task is computer-based
- Task complexity (filtering trivial tasks)
- Missing deliverable/reference files

---

## 5. O*NET Coverage

### Representativeness Metrics

| Category | Unique in O*NET | Covered in Gold Set | Coverage % |
|----------|-----------------|---------------------|------------|
| Skills | 35 | 25 | 71.4% |
| Work Activities | 41 | 26 | 63.4% |
| Tasks | 1,470 | 208 | 14.15% |

Most GDPval tasks involve **multiple O*NET tasks, skills, and work activities** simultaneously.
