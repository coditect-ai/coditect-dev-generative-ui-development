# GDPval Paper Analysis - Index

## Paper Citation

> **GDPval: Evaluating AI Model Performance on Real-World Economically Valuable Tasks**  
> Patwardhan, Dias, Proehl, Kim, Wang, Watkins, et al.  
> OpenAI, October 2025  
> arXiv:2510.04374v1

---

## Analysis Documents

| # | Document | Description |
|---|----------|-------------|
| 01 | [Executive Summary](./01-executive-summary.md) | High-level overview, key statistics, headline findings |
| 02 | [Methodology](./02-methodology.md) | Occupation selection, expert recruitment, task creation pipeline |
| 03 | [Experimental Results](./03-experimental-results.md) | Model performance, speed/cost analysis, failure modes |
| 04 | [Grading Methodology](./04-grading-methodology.md) | Human expert grading, automated grader, agreement metrics |
| 05 | [Limitations & Future](./05-limitations-future.md) | Current constraints, methodological caveats, roadmap |
| 06 | [Technical Formulations](./06-technical-formulations.md) | Mathematical definitions, cost calculations, metrics |
| 07 | [Key Takeaways](./07-key-takeaways.md) | Implications for developers, users, researchers, policymakers |

---

## Quick Reference

### Top-Line Results

| Model | Win+Tie Rate | Best At |
|-------|--------------|---------|
| Claude Opus 4.1 | **47.6%** | Aesthetics, visual files |
| GPT-5 high | 38.8% | Accuracy, pure text |
| o3 high | 34.1% | - |
| o4-mini high | 27.9% | - |
| Gemini 2.5 Pro | 25.5% | - |
| Grok 4 | 24.3% | - |
| GPT-4o | 12.4% | (baseline) |

### Key Numbers

- **44** occupations across **9** GDP sectors
- **1,320** tasks (full set) / **220** tasks (gold subset)
- **$3 trillion** annual earnings of covered occupations
- **14 years** average expert experience
- **7 hours** average task completion time
- **71%** human inter-rater agreement
- **66%** automated grader agreement
- **3%** catastrophic failure rate in model losses

### Speed/Cost with GPT-5 (Try n Times)

- **1.39x** faster than unassisted expert
- **1.63x** cheaper than unassisted expert

---

## Benchmark Access

- **Tasks**: [evals.openai.com](https://evals.openai.com)
- **Automated Grader**: Available at same URL
- **Gold Subset Size**: 220 tasks (5 per occupation)

---

## Key Implications

1. **Frontier models approaching expert parity** (linear improvement trajectory)
2. **Claude excels on aesthetics, GPT-5 on accuracy** (use case dependent)
3. **Instruction following is #1 failure mode** (room for improvement)
4. **"Try n times" workflow optimal** for economic value capture
5. **Human oversight still essential** (3% catastrophic failure rate)
6. **Prompt tuning yields +5pp improvement** (low-hanging optimization)
