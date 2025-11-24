# GDPval: Experimental Results

## 1. Headline Model Performance

### Pairwise Expert Preferences (Gold Subset)

| Model | Wins Only | Wins + Ties | Notes |
|-------|-----------|-------------|-------|
| **Claude Opus 4.1** | 34.1% | **47.6%** | Best overall; excels on aesthetics |
| GPT-5 high | 27.9% | 38.8% | Best on accuracy; excels on pure text |
| o3 high | 25.5% | 34.1% | - |
| o4-mini high | 24.3% | 27.9% | - |
| Gemini 2.5 Pro | - | 25.5% | - |
| Grok 4 | - | 24.3% | - |
| GPT-4o | - | 12.4% | Baseline |

> **Parity threshold**: 50% (model deliverable = human deliverable quality)
> 
> Best models approaching but not yet reaching parity with 14-year average experience industry experts.

### Performance Trajectory (OpenAI Models)

Model performance increased **roughly linearly over time**:
- GPT-4o (May 2024): ~20% win rate
- o3 high (Dec 2024): ~35% win rate
- GPT-5 high (Sep 2025): ~39% win rate

---

## 2. Speed and Cost Analysis

### Methodology

Three scenarios analyzed for AI assistance to expert workflows:

1. **Naive Ratio**: Raw speed/cost comparison (no quality adjustment)
2. **Try 1x, Fix If Needed**: Expert samples model → reviews → redoes if unsatisfactory
3. **Try nx, Fix If Needed**: Expert resamples up to n times before manual completion

### Results Summary

| Model | Win Rate | Speed (Naive) | Speed (Try 1x) | Speed (Try nx) | Cost (Naive) | Cost (Try 1x) | Cost (Try nx) |
|-------|----------|---------------|----------------|----------------|--------------|---------------|---------------|
| GPT-4o | 12.5% | 327x | 0.87x | 0.46x | 5172x | 0.90x | 0.53x |
| o4-mini | 29.1% | 186x | 1.02x | 1.06x | 1265x | 1.06x | 1.22x |
| o3 | 35.2% | 161x | 1.08x | 1.28x | 480x | 1.13x | 1.47x |
| GPT-5 | 39.0% | 90x | 1.12x | 1.39x | 474x | 1.18x | 1.63x |

### Key Insight

> With "Try n times" workflow, **GPT-5 high** achieves:
> - **1.5x speed improvement** over unassisted expert
> - **1.5x cost improvement** over unassisted expert
> - Positioned in upper-right quadrant (better on both dimensions)

### Baseline Statistics (Gold Subset)

| Metric | Average | Description |
|--------|---------|-------------|
| Human completion time (HT) | 404 min | Expert time to complete task |
| Human completion cost (HC) | $361 | Time × median hourly wage |
| Review time (RT) | 109 min | Time to assess model output |
| Review cost (RC) | $86 | Review time × median wage |

---

## 3. Model Strengths & Weaknesses

### Failure Mode Analysis

| Failure Type | Claude Opus 4.1 | GPT-5 high | Grok 4 | Gemini 2.5 Pro |
|--------------|-----------------|------------|--------|----------------|
| Instruction Following | 14% | 9% | 35% | 40% |
| Formatting | 5% | 10% | 5% | 6% |
| Accuracy | 6% | 5% | 13% | 7% |

### Key Observations

**Claude Opus 4.1**:
- Best on aesthetics (document formatting, slide layout)
- Better on visual file types (.pdf, .xlsx, .pptx)
- Lower instruction-following failures

**GPT-5 high**:
- Best on accuracy (following instructions, correct calculations)
- Best on pure text outputs
- Most formatting errors

**Grok 4 & Gemini 2.5 Pro**:
- Frequent instruction-following failures
- Often promised but failed to provide deliverables
- Ignored reference data or used wrong format

---

## 4. Performance by Dimension

### By Deliverable File Type

| File Type | % of Tasks | GPT-4o | o4-mini | o3 | GPT-5 | Claude |
|-----------|------------|--------|---------|-----|-------|--------|
| Pure Text | 9.9% | 15% | 22% | 23% | **30%** | 25% |
| PDF | 31.3% | 5% | 18% | 26% | 35% | **45%** |
| XLSX | 23.1% | 9% | 12% | 27% | 27% | **35%** |
| PPTX | 5.6% | 5% | 11% | 25% | 27% | **45%** |
| Other | 30.1% | 14% | 15% | 25% | 34% | **46%** |

> Claude excels on all visual/formatted deliverables; GPT-5 leads only on pure text.

### By Time to Complete

| Task Duration | GPT-4o | o4-mini | o3 | GPT-5 | Claude |
|---------------|--------|---------|-----|-------|--------|
| 0-2 hours | 19% | 38% | 45% | 48% | **56%** |
| 2-4 hours | 7% | 25% | 28% | 33% | **44%** |
| 4-8 hours | 8% | 23% | 23% | 29% | **42%** |
| 8+ hours | 9% | 19% | 25% | 30% | **37%** |

> Win rates decline steadily with task complexity—models perform best on shorter tasks.

### By Sector (Selected)

**Highest Model Performance**:
- Government: ~55% (Claude)
- Retail Trade: ~55% (Claude)
- Wholesale Trade: ~60% (Claude)

**Lowest Model Performance**:
- Manufacturing: ~35% (Claude)
- Information: ~35% (Claude)
- Health Care: ~40% (Claude)

---

## 5. GPT-5 Failure Severity Analysis

When GPT-5 lost to human expert, failures were categorized:

| Severity | % of Failures | Description |
|----------|---------------|-------------|
| Acceptable but Subpar | 47.7% | Usable but human was stronger |
| Model Better (Grader Disagreement) | 22.9% | Second grader preferred model |
| Bad | 26.7% | Not fit for use, but not dangerous |
| Catastrophic | 2.7% | Harmful or dangerously wrong |

> ~3% catastrophic failure rate includes: insulting customers, wrong diagnoses, recommending fraud, suggesting physically harmful actions.

---

## 6. Reasoning Effort Experiment

### Impact of Reasoning Level

| Model | Reasoning | Win Rate (Wins Only) | Win Rate (Wins + Ties) |
|-------|-----------|----------------------|------------------------|
| o3 | Low | 29.8% | - |
| o3 | Medium | 30.8% | - |
| o3 | **High** | **34.1%** | - |
| GPT-5 | Low | 32.7% | - |
| GPT-5 | Medium | 35.5% | - |
| GPT-5 | **High** | **38.8%** | - |

> Additional reasoning effort **consistently improves performance**.

### Prompt Tuning Experiment

Targeted prompting improvements:
1. Rigorous deliverable checking for correctness
2. Render files as images to check layouts
3. Avoid nonstandard Unicode characters
4. Reduce excess verbosity

**Results**:
- Black-square PDF artifacts: 50%+ → **0%** (eliminated)
- Egregious PPTX formatting errors: 86% → **64%**
- Agents inspecting deliverables visually: 15% → **97%**
- Win rate improvement: **+5 percentage points**

---

## 7. Under-Contextualized Experiment

### Setup

Created modified prompts with 42% less context:
- Omitted file location details
- Omitted approach guidance
- Omitted detailed formatting expectations

### Results

| Condition | Win Rate (Wins + Ties) |
|-----------|------------------------|
| Full Context | 47.7% |
| Under-specified (42% shorter) | 44.3% |

> Models struggle when required to "figure out" context—performance degrades with ambiguity.
