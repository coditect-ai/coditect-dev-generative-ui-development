# Message Query Reference Guide

**Quick lookup for common queries on organized messages**

---

## Quick Reference Table

| Use Case | Command | Output |
|----------|---------|--------|
| **List all projects** | `ls by-checkpoint/*.jsonl` | All checkpoint files |
| **Count messages in project** | `wc -l by-checkpoint/2025-11-19-CODITECT-*.jsonl` | Message count |
| **Get project timeline** | `jq -s 'sort_by(.first_seen)' by-checkpoint/2025-11-19-*.jsonl` | Chronological messages |
| **Find messages by date** | `grep "2025-11-18" by-checkpoint/*.jsonl` | All Nov 18 messages |
| **Find messages by keyword** | `grep -l "authentication" by-checkpoint/*.jsonl` | Files with keyword |
| **Extract message content** | `jq -r '.message.content' by-checkpoint/*.jsonl` | Just the text |
| **Get metadata only** | `jq '{time: .first_seen, checkpoint: .checkpoint}' by-checkpoint/*.jsonl` | Metadata without content |

---

## Command Patterns

### Get All Messages for a Project

```bash
# Find the exact checkpoint file name
ls MEMORY-CONTEXT/messages/by-checkpoint/ | grep -i "project-name"

# Get all messages from that project
cat MEMORY-CONTEXT/messages/by-checkpoint/2025-11-19-CODITECT-Brain.jsonl

# Count messages
wc -l MEMORY-CONTEXT/messages/by-checkpoint/2025-11-19-CODITECT-Brain.jsonl

# View first 10 messages with timestamps
jq '.first_seen' MEMORY-CONTEXT/messages/by-checkpoint/2025-11-19-CODITECT-Brain.jsonl | head -10
```

### Get All Messages from a Date

```bash
# Get all messages from Nov 18
grep "2025-11-18" MEMORY-CONTEXT/messages/by-checkpoint/*.jsonl

# Count messages per project on that date
grep "2025-11-18" MEMORY-CONTEXT/messages/by-checkpoint/*.jsonl | \
  cut -d: -f1 | sort | uniq -c

# Get unique projects worked on that day
grep "2025-11-18" MEMORY-CONTEXT/messages/by-checkpoint/*.jsonl | \
  jq -r '.checkpoint' | sort -u
```

### Get Chronological Timeline

```bash
# Single project timeline (sorted by timestamp)
jq -s 'sort_by(.first_seen) | .[] | {time: .first_seen, msg: .message.content}' \
  MEMORY-CONTEXT/messages/by-checkpoint/2025-11-19-CODITECT-Brain.jsonl

# All projects on a date (chronological)
for f in MEMORY-CONTEXT/messages/by-checkpoint/*.jsonl; do
  jq 'select(.first_seen | startswith("2025-11-18"))' "$f"
done | jq -s 'sort_by(.first_seen)'

# Day-by-day summary
for day in 2025-11-{15..22}; do
  echo "=== $day ==="
  for f in MEMORY-CONTEXT/messages/by-checkpoint/*.jsonl; do
    count=$(grep -c "$day" "$f" 2>/dev/null || echo 0)
    if [ "$count" -gt 0 ]; then
      checkpoint=$(jq -r '.checkpoint' "$f" | head -1)
      echo "  $checkpoint: $count messages"
    fi
  done
done
```

### Search for Specific Content

```bash
# Find files mentioning "database"
grep -l "database" MEMORY-CONTEXT/messages/by-checkpoint/*.jsonl

# Find files mentioning "authentication" and show checkpoint name
for f in MEMORY-CONTEXT/messages/by-checkpoint/*.jsonl; do
  if grep -q "authentication" "$f"; then
    checkpoint=$(jq -r '.checkpoint' "$f" | head -1)
    echo "$checkpoint"
  fi
done

# Find all messages containing keyword and show time + content
grep "deployment" MEMORY-CONTEXT/messages/by-checkpoint/*.jsonl | \
  jq -r '.first_seen, .message.content' | paste - -
```

### Get Statistics

```bash
# Total messages across all checkpoints
find MEMORY-CONTEXT/messages/by-checkpoint -name "*.jsonl" -type f | \
  xargs wc -l | tail -1

# Messages per checkpoint
find MEMORY-CONTEXT/messages/by-checkpoint -name "*.jsonl" -type f | \
  xargs wc -l | sort -rn | head -20

# Date range of all messages
jq -r '.first_seen' MEMORY-CONTEXT/messages/by-checkpoint/*.jsonl | \
  cut -d'T' -f1 | sort -u

# Working hours analysis
jq -r '.first_seen' MEMORY-CONTEXT/messages/by-checkpoint/*.jsonl | \
  cut -d'T' -f2 | cut -d':' -f1 | sort | uniq -c | sort -rn
```

### Compare Across Sessions

```bash
# Find related work across different checkpoints
# (All messages about "cloud-backend" across all sessions)

echo "Sessions discussing cloud-backend:"
for f in MEMORY-CONTEXT/messages/by-checkpoint/*.jsonl; do
  if grep -q "cloud-backend" "$f"; then
    checkpoint=$(jq -r '.checkpoint' "$f" | head -1)
    date=$(jq -r '.first_seen' "$f" | head -1 | cut -d'T' -f1)
    count=$(grep -c "cloud-backend" "$f")
    echo "  [$date] $checkpoint ($count mentions)"
  fi
done
```

---

## JSON Query Patterns (jq)

### Basic Selection

```bash
# Get just the message content
jq '.message.content' file.jsonl

# Get just the timestamp
jq '.first_seen' file.jsonl

# Get just the checkpoint
jq '.checkpoint' file.jsonl

# Get hash for verification
jq '.hash' file.jsonl
```

### Filtering

```bash
# Messages from a specific date
jq 'select(.first_seen | startswith("2025-11-18"))' file.jsonl

# Messages from a specific project
jq 'select(.checkpoint | contains("CODITECT"))' file.jsonl

# Messages containing specific text
jq 'select(.message.content | contains("database"))' file.jsonl

# Messages from a time range
jq 'select(.first_seen >= "2025-11-18T00:00:00Z" and .first_seen <= "2025-11-18T23:59:59Z")' file.jsonl
```

### Sorting & Grouping

```bash
# Sort messages by timestamp
jq -s 'sort_by(.first_seen)' file.jsonl

# Sort reverse chronological (newest first)
jq -s 'sort_by(.first_seen) | reverse' file.jsonl

# Group by checkpoint
jq -s 'group_by(.checkpoint) | map({checkpoint: .[0].checkpoint, count: length})' file.jsonl

# Group by date
jq -s 'map(.first_seen | split("T")[0]) | group_by(.) | map({date: .[0], count: length})' file.jsonl
```

### Custom Output

```bash
# Timeline format: time → checkpoint → summary of content
jq '{
  time: .first_seen,
  checkpoint: .checkpoint,
  summary: .message.content | .[0:100]
}' file.jsonl

# Analysis format: what, when, where
jq '{
  what: .message.content,
  when: .first_seen | split("T")[0],
  where: .checkpoint,
  hash: .hash
}' file.jsonl

# Metadata only (no content, useful for large files)
jq '{
  time: .first_seen,
  checkpoint: .checkpoint,
  type: .message.role,
  hash: .hash
}' file.jsonl
```

---

## Python Examples

### Read All Messages from Project

```python
import json
from pathlib import Path

checkpoint_file = Path("MEMORY-CONTEXT/messages/by-checkpoint/2025-11-19-CODITECT-Brain.jsonl")

messages = []
with open(checkpoint_file) as f:
    for line in f:
        if line.strip():
            messages.append(json.loads(line))

print(f"Loaded {len(messages)} messages")

# Print timeline
for msg in sorted(messages, key=lambda m: m['first_seen']):
    print(f"{msg['first_seen']}: {msg['message']['content'][:80]}")
```

### Search Across All Checkpoints

```python
import json
from pathlib import Path

search_term = "authentication"
checkpoint_dir = Path("MEMORY-CONTEXT/messages/by-checkpoint")

results = {}
for checkpoint_file in checkpoint_dir.glob("*.jsonl"):
    matches = []
    with open(checkpoint_file) as f:
        for line in f:
            if line.strip():
                msg = json.loads(line)
                if search_term.lower() in msg['message']['content'].lower():
                    matches.append({
                        'time': msg['first_seen'],
                        'content': msg['message']['content'][:100]
                    })

    if matches:
        results[checkpoint_file.name] = matches

# Print results
for checkpoint, messages in sorted(results.items()):
    print(f"\n{checkpoint}: {len(messages)} matches")
    for msg in messages[:3]:  # Show first 3
        print(f"  {msg['time']}: {msg['content']}")
```

### Analyze Message Distribution

```python
import json
from pathlib import Path
from collections import defaultdict

checkpoint_dir = Path("MEMORY-CONTEXT/messages/by-checkpoint")

# Count messages per checkpoint
stats = {}
for checkpoint_file in checkpoint_dir.glob("*.jsonl"):
    count = sum(1 for line in open(checkpoint_file) if line.strip())
    stats[checkpoint_file.name] = count

# Print statistics
print("Top 10 projects by message count:")
for name, count in sorted(stats.items(), key=lambda x: -x[1])[:10]:
    print(f"  {name}: {count}")

print(f"\nTotal: {sum(stats.values())} messages")
print(f"Projects: {len(stats)}")
```

### Timeline Reconstruction

```python
import json
from pathlib import Path
from datetime import datetime

checkpoint_dir = Path("MEMORY-CONTEXT/messages/by-checkpoint")

# Load all messages with timeline
all_messages = []
for checkpoint_file in checkpoint_dir.glob("*.jsonl"):
    with open(checkpoint_file) as f:
        for line in f:
            if line.strip():
                msg = json.loads(line)
                all_messages.append(msg)

# Sort chronologically
all_messages.sort(key=lambda m: m['first_seen'])

# Group by day
by_day = defaultdict(list)
for msg in all_messages:
    day = msg['first_seen'].split('T')[0]
    by_day[day].append(msg)

# Print daily summary
for day in sorted(by_day.keys()):
    messages = by_day[day]
    checkpoints = set(m['checkpoint'] for m in messages)
    print(f"{day}: {len(messages)} messages across {len(checkpoints)} projects")
    for cp in sorted(checkpoints):
        cp_count = sum(1 for m in messages if m['checkpoint'] == cp)
        print(f"  - {cp}: {cp_count}")
```

---

## Manifest Queries

### List All Available Checkpoints

```bash
# Get checkpoint names and message counts from manifest
jq '.by_checkpoint | keys' MEMORY-CONTEXT/messages/MANIFEST.json

# Get checkpoint with message counts
jq '.by_checkpoint | to_entries | map({name: .key, count: .value.count})' \
  MEMORY-CONTEXT/messages/MANIFEST.json | jq -s 'sort_by(.count) | reverse'
```

### Find Checkpoints by Date Range

```bash
# Find all checkpoints from November 2025
jq '.by_checkpoint | keys[] | select(startswith("2025-11"))' \
  MEMORY-CONTEXT/messages/MANIFEST.json

# With counts
jq '.by_checkpoint | to_entries | map(select(.key | startswith("2025-11"))) |
    map({name: .key, count: .value.count})' \
  MEMORY-CONTEXT/messages/MANIFEST.json
```

### Get Manifest Statistics

```bash
# Total messages across all checkpoints
jq '.by_checkpoint | [.[].count] | add' MEMORY-CONTEXT/messages/MANIFEST.json

# Number of checkpoints
jq '.by_checkpoint | length' MEMORY-CONTEXT/messages/MANIFEST.json

# Average messages per checkpoint
jq '.by_checkpoint | [.[].count] | (add / length)' MEMORY-CONTEXT/messages/MANIFEST.json
```

---

## Performance Tips

### For Large Files (212K+ messages)

```bash
# Don't load entire file into memory
# Use grep first to filter, then parse JSON

# ❌ Slow - loads entire file
jq 'select(.checkpoint | contains("old"))' by-date-fallback/2025-01-01-uncategorized.jsonl

# ✅ Fast - filters first, then parses
grep "old" by-date-fallback/2025-01-01-uncategorized.jsonl | jq '...'
```

### For Multiple Files

```bash
# ❌ Slow - opens each file separately
for f in *.jsonl; do jq '.first_seen' "$f"; done

# ✅ Fast - single jq process
jq -r '.first_seen' *.jsonl

# ✅✅ Fastest - parallel processing
jq -r '.first_seen' *.jsonl | parallel process_chunk
```

---

## Troubleshooting

### Message Not Found

```bash
# Search across ALL files
grep -r "search term" MEMORY-CONTEXT/messages/

# Search in content only (faster)
grep "search term" MEMORY-CONTEXT/messages/by-checkpoint/*.jsonl

# Search specific date
grep "2025-11-19" MEMORY-CONTEXT/messages/by-checkpoint/*.jsonl
```

### Verify Message Integrity

```bash
# Check for missing required fields
jq 'if (.hash and .first_seen and .checkpoint) then . else empty end' file.jsonl | wc -l

# Check for invalid JSON
jq empty file.jsonl 2>&1 | grep error

# Verify hashes are unique
jq -r '.hash' file.jsonl | sort | uniq -d
```

### Performance Issues

```bash
# Check file sizes
ls -lh MEMORY-CONTEXT/messages/by-checkpoint/ | sort -k5 -h

# Count messages per file
wc -l MEMORY-CONTEXT/messages/by-checkpoint/*.jsonl | sort -rn

# Find largest messages (for streaming optimization)
jq 'length' MEMORY-CONTEXT/messages/by-checkpoint/*.jsonl | sort -rn
```

---

## Real-World Examples

### Example 1: "What did I build on Nov 19?"

```bash
# Find Nov 19 checkpoints
ls MEMORY-CONTEXT/messages/by-checkpoint/2025-11-19*.jsonl | xargs -I {} basename {} .jsonl

# Get summary of work that day
for f in MEMORY-CONTEXT/messages/by-checkpoint/2025-11-19*.jsonl; do
  checkpoint=$(basename "$f" .jsonl)
  count=$(wc -l < "$f")
  first_time=$(jq -r '.first_seen' "$f" | head -1)
  last_time=$(jq -r '.first_seen' "$f" | tail -1)
  echo "$checkpoint: $count messages ($first_time to $last_time)"
done
```

### Example 2: "How long did CODITECT-Brain take?"

```bash
# Find CODITECT-Brain checkpoint
f="MEMORY-CONTEXT/messages/by-checkpoint/2025-11-19-CODITECT-Distributed-Brain.jsonl"

# Get start and end times
start=$(jq -r '.first_seen' "$f" | head -1)
end=$(jq -r '.first_seen' "$f" | tail -1)
duration=$(($(date -d "$end" +%s) - $(date -d "$start" +%s)))

echo "Start: $start"
echo "End: $end"
echo "Duration: $((duration / 3600)) hours $((($duration % 3600) / 60)) minutes"
```

### Example 3: "All work related to authentication"

```bash
echo "=== Messages about authentication ==="

for f in MEMORY-CONTEXT/messages/by-checkpoint/*.jsonl; do
  matches=$(grep -c "authentication" "$f" 2>/dev/null || echo 0)
  if [ "$matches" -gt 0 ]; then
    checkpoint=$(jq -r '.checkpoint' "$f" | head -1)
    date=$(jq -r '.first_seen' "$f" | head -1 | cut -d'T' -f1)
    echo "[$date] $checkpoint: $matches mentions"

    # Show snippets
    grep "authentication" "$f" | jq -r '.message.content' | head -2 | sed 's/^/  /'
  fi
done
```

