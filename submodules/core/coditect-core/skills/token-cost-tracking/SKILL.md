---
name: token-cost-tracking
description: Token usage and cost tracking with model-specific pricing for monitoring and optimizing AI token consumption. Use when tracking sessions, calculating costs, analyzing efficiency, or budget planning.
license: MIT
allowed-tools: [Bash, Read, Write]
metadata:
  token-efficiency: "Cost visibility enables 20-30% token optimization through informed decisions"
  integration: "All workflows + Orchestrator phase-level tracking"
  tech-stack: "Python, JSON Lines, CSV export, Multi-model pricing"
  production-usage: "Monitor 200K token sessions, track multi-model costs"
tags: [monitoring, cost-optimization, analytics, tokens]
version: 2.0.0
status: production
---

# Token Cost Tracking Skill

Track token usage and costs across different LLM models to optimize AI operations and budget planning.

## When to Use This Skill

✅ **Use this skill when:**
- Starting/ending a session (log token usage)
- Comparing efficiency of different approaches (skill vs manual)
- Monthly cost reporting for AI operations
- Identifying token-heavy operations for optimization
- Validating skill vs manual workflow savings
- Budget planning for multi-model AI usage
- Proven need: Monitor 200K token sessions

❌ **Don't use this skill when:**
- Using free local models only (LM Studio - no cost tracking needed)
- Session < 10K tokens (overhead not worth tracking)
- One-off experiments (not enough data for trends)
- Token cost not a concern for the project

## What It Provides

**Token Tracking:**
- Input tokens (prompt + context)
- Output tokens (generated responses)
- Total tokens per session/task
- Model-specific pricing

**Cost Calculation:**
```
Claude Sonnet 4: $3/1M input, $15/1M output
Claude Opus: $15/1M input, $75/1M output
GPT-4 Turbo: $10/1M input, $30/1M output
GPT-4o: $5/1M input, $15/1M output
Gemini 1.5 Pro: $1.25/1M input, $5/1M output
```

**Reporting:**
- Per-session costs
- Daily/weekly/monthly summaries
- Model usage breakdown
- Cost trends over time

## Usage

### Log Session Usage

```bash
cd .claude/skills/token-cost-tracking

# Log current session
./core/track-tokens.py log \
  --session "Sprint 2 Build #19" \
  --model "claude-sonnet-4" \
  --input-tokens 50000 \
  --output-tokens 15000 \
  --notes "Build + deploy + documentation"
```

### Generate Cost Report

```bash
# Today's usage
./core/track-tokens.py report --period today

# This week
./core/track-tokens.py report --period week

# This month
./core/track-tokens.py report --period month

# Specific model
./core/track-tokens.py report --model claude-sonnet-4 --period month
```

### Compare Approaches

```bash
# Skill vs manual
./core/track-tokens.py compare \
  --approach-1 "Manual git commit" \
  --tokens-1 10000 \
  --approach-2 "git-workflow-automation skill" \
  --tokens-2 2500
```

### Export Data

```bash
# Export to CSV
./core/track-tokens.py export --output token-usage-october.csv

# View summary
./core/track-tokens.py summary
```

## Model Pricing (as of Oct 2025)

| Model | Input ($/1M) | Output ($/1M) | Use Case |
|-------|--------------|---------------|----------|
| Claude Sonnet 4.5 | $3 | $15 | Production (balanced) |
| Claude Opus 3.5 | $15 | $75 | Complex reasoning |
| GPT-4 Turbo | $10 | $30 | General purpose |
| GPT-4o | $5 | $15 | Cost-effective |
| Gemini 1.5 Pro | $1.25 | $5 | High volume |
| LM Studio (local) | $0 | $0 | Free (hardware cost only) |

## Data Storage

**Log File**: `.coditect/token-usage.jsonl` (JSON Lines format)

**Example entry:**
```json
{
  "timestamp": "2025-10-19T20:30:00Z",
  "session": "Sprint 2 Build #19",
  "model": "claude-sonnet-4",
  "input_tokens": 50000,
  "output_tokens": 15000,
  "total_tokens": 65000,
  "cost_usd": 0.375,
  "notes": "Build + deploy + documentation"
}
```

## Cost Calculation Formula

```python
input_cost = (input_tokens / 1_000_000) * input_price_per_million
output_cost = (output_tokens / 1_000_000) * output_price_per_million
total_cost = input_cost + output_cost
```

## Example Workflows

### Session Logging
```bash
# At end of session
python3 ./core/track-tokens.py log \
  --session "Feature implementation" \
  --model claude-sonnet-4 \
  --input-tokens 120000 \
  --output-tokens 35000 \
  --notes "User profile editing + tests"

# Output:
# ✓ Logged session: Feature implementation
# Total tokens: 155,000
# Cost: $0.885 USD
```

### Monthly Report
```bash
python3 ./core/track-tokens.py report --period month

# Output:
# Token Usage Report - October 2025
#
# Total sessions: 45
# Total tokens: 3,250,000
# Total cost: $18.75 USD
#
# By model:
#   Claude Sonnet 4: 2,500,000 tokens ($14.25)
#   Claude Opus: 500,000 tokens ($3.75)
#   GPT-4o: 250,000 tokens ($0.75)
#
# Top sessions:
#   1. Sprint 2 deployment (155K tokens, $0.885)
#   2. Architecture research (98K tokens, $0.564)
```

### Skill Efficiency Analysis
```bash
# Compare manual vs skill approach
python3 ./core/track-tokens.py compare \
  --approach-1 "Manual deployment" \
  --tokens-1 45000 \
  --approach-2 "build-deploy-workflow skill" \
  --tokens-2 5000

# Output:
# Comparison Report
#
# Manual deployment:
#   Tokens: 45,000
#   Cost: $0.270 USD
#
# build-deploy-workflow skill:
#   Tokens: 5,000
#   Cost: $0.030 USD
#
# Savings: 40,000 tokens (89%), $0.240 USD (89%)
```

## Integration with Skills

**Track skill usage automatically:**

```bash
# Before using skill
START_TOKENS=$(get current token count)

# Use skill
./core/deploy.sh --build-num=20 --changes="Feature X"

# After using skill
END_TOKENS=$(get current token count)
USED_TOKENS=$((END_TOKENS - START_TOKENS))

# Log usage
./token-cost-tracking/core/track-tokens.py log \
  --session "Build #20" \
  --model claude-sonnet-4 \
  --input-tokens $USED_TOKENS \
  --notes "build-deploy-workflow skill"
```

## Metrics Tracked

1. **Token Metrics:**
   - Total tokens used
   - Input vs output ratio
   - Tokens per session
   - Tokens per task type

2. **Cost Metrics:**
   - Total spend (daily/weekly/monthly)
   - Cost per session
   - Cost per model
   - Cost trends over time

3. **Efficiency Metrics:**
   - Skill usage vs manual (token savings)
   - Model selection efficiency
   - Token waste identification

## Safety & Privacy

**Data stored locally only:**
- No external API calls
- No cloud storage
- Privacy-preserving (session names, notes are user-controlled)
- Can be git-ignored if sensitive

## Troubleshooting

**Error: "Log file not found"**
- Fix: File created automatically on first use
- Location: `.coditect/token-usage.jsonl`

**Error: "Invalid model"**
- Check: Model name matches pricing table
- Supported: claude-sonnet-4, claude-opus, gpt-4-turbo, gpt-4o, gemini-1.5-pro

**Cost seems wrong**
- Verify: Token counts are accurate
- Check: Using correct model pricing
- Update: Prices change periodically, update script

## See Also

- **multi-agent-workflow** - Token budget management for complex workflows
- **evaluation-framework** - LLM-as-judge cost tracking
- **Anthropic Pricing**: https://www.anthropic.com/pricing
- **OpenAI Pricing**: https://openai.com/api/pricing
