# GDPval: Executive Summary

## Overview

**GDPval** is a benchmark evaluating AI model capabilities on real-world economically valuable tasks, introduced by OpenAI researchers in October 2025.

## Key Statistics

| Metric | Value |
|--------|-------|
| Total Tasks (Full Set) | 1,320 |
| Gold Subset (Open-Sourced) | 220 |
| Occupations Covered | 44 |
| GDP Sectors | 9 (top contributors to US GDP) |
| Annual Earnings of Covered Occupations | $3 Trillion |
| Average Expert Experience | 14 years |
| Average Task Completion Time | 7 hours |

## Primary Evaluation Metric

**Head-to-head human expert comparison** using blinded pairwise comparisons where experts rank model outputs against human expert deliverables.

## Headline Finding

> Frontier model performance on GDPval is improving roughly linearly over time, and current best frontier models are approaching industry experts in deliverable quality.

**Best Performer**: Claude Opus 4.1 achieved **47.6% win+tie rate** vs human experts (highest among tested models).

## Why GDPval Matters

### Advantages Over Existing Benchmarks

1. **Realism**: Tasks based on actual work product from industry experts with 14+ years average experience
2. **Representative Breadth**: Covers majority of O*NET Work Activities across 44 occupations
3. **Computer Use & Multi-modality**: Tasks require CAD files, photos, video, audio, spreadsheets, slide decks
4. **Subjectivity**: Evaluates structure, style, format, aesthetics—not just correctness
5. **No Upper Limit**: Win rate metric allows continuous evaluation as models improve
6. **Long-horizon Difficulty**: Average 7 hours per task; some span multiple weeks

## Models Evaluated

- GPT-4o
- o4-mini (high)
- o3 (high)
- GPT-5 (high)
- Claude Opus 4.1
- Gemini 2.5 Pro
- Grok 4

## Open-Source Availability

- 220 gold subset tasks available at **evals.openai.com**
- Experimental automated grader provided (66% agreement with human experts)
- Human expert inter-rater agreement: 71%

## Economic Implications

The benchmark enables assessment of AI's potential economic impact **ahead of widespread adoption**, serving as a leading indicator rather than lagging one (like adoption rates or GDP growth attribution).
