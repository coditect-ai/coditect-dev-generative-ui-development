# GDPval: Technical Formulations

## 1. Speed & Cost Analysis Framework

### Variable Definitions

| Symbol | Definition | Gold Subset Average |
|--------|------------|---------------------|
| H_T | Human expert completion time | 404 minutes |
| H_C | Human expert completion cost | $361 |
| R_T | Human review time (for model output) | 109 minutes |
| R_C | Human review cost | $86 |
| M_T | Model completion time | Varies by model |
| M_C | Model completion cost | Varies by model |
| w | Model win rate | Varies by model |
| w_i | Win rate for task i | Task-specific |

### Cost Calculation

```
H_C = Completion Hours × Median Hourly Wage (OEWS)
R_C = Review Hours × Median Hourly Wage (OEWS)
```

---

### Scenario 1: Naive Ratio

Simple comparison ignoring quality differences:

```
Speed Ratio = H_T / M_T
Cost Ratio  = H_C / M_C
```

**Example (GPT-5)**:
- Speed: 90x faster than human
- Cost: 474x cheaper than human

> Not practically meaningful—ignores that model output may need fixing.

---

### Scenario 2: Try Once, Then Fix If Needed

Expert tries model once, reviews, then completes manually if unsatisfactory.

#### Expected Time

```
E[T₁,ᵢ] = M_T,ᵢ + R_T,ᵢ + (1 - wᵢ) × H_T,ᵢ
```

#### Expected Cost

```
E[C₁,ᵢ] = M_C,ᵢ + R_C,ᵢ + (1 - wᵢ) × H_C,ᵢ
```

#### Improvement Ratios

```
Speed Improvement = H_T / T̂₁
Cost Improvement  = H_C / Ĉ₁
```

Where T̂₁, Ĉ₁ are empirical means across all tasks.

---

### Scenario 3: Try n Times, Then Fix If Needed

Expert resamples up to n times before manual completion.

#### Expected Time (Derivation)

```
E[Tₙ,ᵢ] = Σₖ₌₁ⁿ [(1 - wᵢ)^(k-1) × (M_T,ᵢ + R_T,ᵢ)] + (1 - wᵢ)ⁿ × H_T,ᵢ
```

Simplified using geometric series:

```
E[Tₙ,ᵢ] = (M_T,ᵢ + R_T,ᵢ) × [1 - (1 - wᵢ)ⁿ] / wᵢ + (1 - wᵢ)ⁿ × H_T,ᵢ
```

#### Expected Cost

```
E[Cₙ,ᵢ] = (M_C,ᵢ + R_C,ᵢ) × [1 - (1 - wᵢ)ⁿ] / wᵢ + (1 - wᵢ)ⁿ × H_C,ᵢ
```

#### Limiting Behavior (n → ∞)

As n approaches infinity with w > 0:

```
Speed Improvement → H_T / [(M_T + R_T) / w]
Cost Improvement  → H_C / [(M_C + R_C) / w]
```

> Higher win rate = greater benefit from resampling strategy.

---

### Scenario Comparison (GPT-5)

| Scenario | Speed Improvement | Cost Improvement |
|----------|-------------------|------------------|
| Naive | 90x | 474x |
| Try 1x | 1.12x | 1.18x |
| Try nx | 1.39x | 1.63x |

---

## 2. Grader Agreement Metrics

### Human-Automated Grader Agreement

For sample s with human score H and automated score A in {0, 0.5, 1}:

```
A^HA_s = E[1 - |H - A|]
```

Model-level agreement = mean of A^HA_s across all samples.

### Human Inter-Rater Agreement

For sample s with two random human ratings H₁, H₂:

```
A^HH_s = E[1 - |H₁ - H₂|]
```

Estimated by empirical mean over all rating pairs for each sample.

### Interpretation

| Agreement Value | Meaning |
|-----------------|---------|
| 1.0 | Perfect agreement |
| 0.5 | One rating differs by 0.5 (e.g., win vs tie) |
| 0.0 | Complete disagreement (win vs loss) |

### Results

| Metric | Value | 95% CI Method |
|--------|-------|---------------|
| Automated-Human | 65.7% | Bootstrap resampling |
| Human-Human | 70.8% | Bootstrap resampling |

---

## 3. Digital Task Classification

### Per-Task Adjusted Score

For each (occupation, task) pair:

```
Adjusted_Score = (Frequency/7 + Importance/5 + Relevance/100) / 3
```

Where:
- Frequency: 1-7 scale
- Importance: 1-5 scale
- Relevance: 0-100 scale

### Missing Value Imputation

If rating missing for a task, impute with mean of that rating across all tasks in same occupation.

### SOC-4 Aggregation

For 4-digit SOC occupations composed of multiple 6-digit occupations:

```
SOC4_Score(task) = Σ SOC6_Scores(task)
```

### Weighted Task Share

```
Weighted_Share(task) = Adjusted_Score(task) / Σ Adjusted_Scores(all tasks)
```

Sum of all Weighted_Shares for an occupation = 1.0

### Digital Classification Threshold

```
If Σ(Weighted_Share × Is_Digital) ≥ 0.60:
    Occupation = "Digital/Knowledge Work"
```

---

## 4. Task Dollar Value Calculation

### Formula

```
Dollar_Value = Estimated_Hours × Median_Hourly_Wage
```

### Hourly Wage Source

- OEWS May 2024 national employment and wage estimates
- Annual salary jobs: Reported annual / 2080 hours
- Hourly jobs: Direct hourly rate

> 2080 hours = BLS "typical work year" (40 hours × 52 weeks)

### Limitations

- Self-reported time estimates
- Median wage may underestimate highly-experienced expert cost

---

## 5. Win Rate Confidence Intervals

### Bootstrap Method

For each model:

1. Resample with replacement: available scores per sample
2. Compute mean per sample
3. Average across all samples (or specified model subset)
4. Repeat 1000+ times
5. Report 2.5th and 97.5th percentiles as 95% CI

### Visualization

Error bars in figures represent 95% bootstrap confidence intervals.

---

## 6. Total Wages Calculation

For occupation ranking:

```
Total_Wages = Total_Employment × Mean_Annual_Salary
```

Or for hourly-only occupations:

```
Total_Wages = Total_Employment × Hourly_Rate × 2080
```

### Data Sources

- Employment: O*NET May 2024
- Wages: OEWS May 2024
- Sector mapping: BLS 2023 National Employment Matrix

---

## 7. Task Content Validation (Acemoglu & Autor Framework)

### Five Task Content Scores

| Score | O*NET Components |
|-------|------------------|
| Non-routine Cognitive: Analytical | Analyzing data + Thinking creatively + Interpreting information |
| Non-routine Cognitive: Interpersonal | (Specific work activity composites) |
| Routine Cognitive | (Specific work activity composites) |
| Routine Manual | (Specific work activity composites) |
| Non-routine Manual Physical | (Specific work activity composites) |

### Validation Result

Digital task share correlations:
- **Positive** with Non-routine Cognitive (both types)
- **Negative** with Routine Cognitive
- **Negative** with Routine Manual
- **Negative** with Non-routine Manual Physical

> Confirms alignment with established labor economics measures.
