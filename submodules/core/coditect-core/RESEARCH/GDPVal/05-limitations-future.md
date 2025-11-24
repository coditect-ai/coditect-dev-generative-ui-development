# GDPval: Limitations & Future Directions

## 1. Current Limitations

### Dataset Size

| Constraint | Current State |
|------------|---------------|
| Occupations | Only 44 (of 761 detailed OEWS occupations) |
| Tasks per occupation | ~30 |
| Coverage | Limited initial cut, not comprehensive |

> The team is actively expanding dataset size.

---

### Focus on Self-Contained Knowledge Work

**In Scope**:
- Digital deliverables
- Computer-based tasks
- Self-contained work products

**Out of Scope**:

| Excluded Category | Reason |
|-------------------|--------|
| Manual labor / physical tasks | Cannot be performed digitally |
| Extensive tacit knowledge | Requires organizational context |
| PII access | Privacy and legal constraints |
| Proprietary software tools | Licensing and availability |
| Inter-person communication | Cannot be simulated authentically |

---

### Task Specification Issues

**Current State**: Tasks are precisely-specified and one-shot

| Real-World Aspect | GDPval Limitation |
|-------------------|-------------------|
| Figuring out context | Full context provided in prompt |
| Iterative refinement | Single-shot evaluation |
| Clarifying ambiguity | No interactive back-and-forth |
| Understanding requirements | Requirements fully specified |

**Evidence of Impact**:
Under-contextualized experiment showed **3.4 percentage point drop** in win rate with 42% shorter prompts.

> Future versions will incorporate more interactivity and contextual realism.

---

### Grader Performance

| Limitation | Impact |
|------------|--------|
| Self-preference bias | GPT-5 grader may favor OpenAI outputs |
| Agreement gap | 5% below human inter-rater agreement |
| Container constraints | Python-only, no internet, limited fonts |
| File type limitations | Some deliverables ungradable |

**12 tasks excluded** from automated grading due to technical limitations.

---

### Cost

| Factor | Implication |
|--------|-------------|
| Expert recruitment | High bar (4+ years, video interview, background check) |
| Task creation | Multiple review rounds, 5+ reviews per task |
| Human grading | >1 hour per comparison at expert wages |
| Evaluation runs | 9 comparisons per task per model |

> Automated grader provided as proxy, but not considered full substitute.

---

## 2. Methodological Caveats

### Speed/Cost Analysis Limitations

The analysis does **not** account for:

1. **Human self-review time** (professionals typically review own work)
2. **Supervisor review time** (common in real workflows)
3. **Possibility that human deliverable is also unsatisfactory**
4. **Cost of catastrophic mistakes** (disproportionately expensive in some domains)
5. **Improving win rate with prompt iteration** (analysis assumes fixed win rate)

### Self-Reported Time Estimates

- Expert completion times are **self-reported**
- Possible under/over-estimation
- Multiple reviewers validated, but not directly measured

### Wage Estimation

- Used median O*NET wages
- Experts recruited for high experience → likely **underestimates true market cost**

---

## 3. Content Disclosures

### AI Usage in Paper Creation

- AI models used for literature review
- AI used for language tweaking
- AI coding assistants used in engineering workflows

### Sensitive Content

Some tasks include NSFW themes reflecting real occupational content:
- Sex, alcohol, vulgar language
- Political content

> Retained for realism in film, literature, law, politics occupations. No endorsement implied.

### Third-Party References

- Limited brand/trademark references for research purposes only
- No affiliation or endorsement implied
- Some AI-generated individuals and permitted real people appear
- Fictitious names used; any resemblance coincidental

---

## 4. Future Directions

### Planned Improvements

| Area | Enhancement |
|------|-------------|
| **Breadth** | Expand beyond 44 occupations |
| **Realism** | Add interactive, multi-turn tasks |
| **Context** | Reduce prompt over-specification |
| **Interactivity** | Allow clarifying questions |
| **Tools** | Expand grader container capabilities |
| **Baseline** | Replace human baseline with strong models over time |

### Continuous Evaluation Design

The win-rate metric enables **indefinite evaluation**:

```
Current:  Model vs. Human Expert (14 years avg)
Future:   Model vs. Best Previous Model
          Model vs. Model (Elo-style ratings)
```

No theoretical upper limit—benchmark won't saturate as models improve.

---

## 5. Open Questions

### Representativeness

- How well do 30 tasks per occupation represent the full scope of work?
- Are digital tasks representative of total occupational value?
- Does the 60% digital threshold appropriately classify "knowledge work"?

### Generalization

- Do results on US occupations transfer to other economies?
- Are O*NET task classifications universally applicable?
- How do cultural factors affect deliverable quality assessment?

### Economic Interpretation

- What win rate threshold indicates meaningful economic impact?
- How do speed/cost improvements translate to productivity gains?
- What is the relationship between benchmark performance and real-world adoption?

---

## 6. Comparison to Existing Benchmarks

### GDPval vs. Academic Benchmarks

| Aspect | GDPval | MMLU/GPQA/HLE |
|--------|--------|---------------|
| Task source | Real work products | Academic tests |
| Evaluation | Pairwise expert comparison | Correctness scoring |
| Saturation risk | Low (win rate metric) | High |
| Multimodal | Yes (CAD, video, audio) | Mostly text |
| Subjectivity | Yes (style, aesthetics) | No |

### GDPval vs. Domain-Specific Evals (e.g., SWE-Lancer)

| Aspect | GDPval | SWE-Lancer |
|--------|--------|------------|
| Scope | 44 occupations | Software engineering only |
| Coverage | Broad but shallow | Deep in domain |
| Task origin | Expert-created | Freelance platform |
| File diversity | High | Code-focused |
