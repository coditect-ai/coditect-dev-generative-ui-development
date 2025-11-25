# Navigation Links - Quick Fix Reference
**3 Critical Bugs to Fix Immediately**

---

## Bug 1: Recent Sessions Link (navigation.js:293)

**Location**: Overview page recent sessions
**Impact**: HIGH - Breaks all session detail navigation from overview
**Current Code**:
```javascript
<a href="#checkpoints/${session.id}" class="btn btn-sm btn-primary" style="margin-top: var(--space-2);">
    View Full Session →
</a>
```

**Fixed Code**:
```javascript
<a href="#checkpoints/${encodeURIComponent(session.id)}" class="btn btn-sm btn-primary" style="margin-top: var(--space-2);">
    View Full Session →
</a>
```

---

## Bug 2: Timeline Session Click (navigation.js:706)

**Location**: Timeline chart session click handler
**Impact**: HIGH - Breaks all timeline-to-detail navigation
**Current Code**:
```javascript
window.location.hash = `#checkpoints/${d.id}`;
```

**Fixed Code**:
```javascript
window.location.hash = `#checkpoints/${encodeURIComponent(d.id)}`;
```

---

## Bug 3: Topic Card Link (navigation.js:306)

**Location**: Overview page top topics
**Impact**: MEDIUM - Breaks topic filtering for topics with special chars
**Current Code**:
```javascript
<div class="card clickable" onclick="window.location.hash='#topics/${topic.name}'">
```

**Fixed Code**:
```javascript
<div class="card clickable" onclick="window.location.hash='#topics/${encodeURIComponent(topic.name)}'">
```

---

## Why These Bugs Occur

**Session IDs contain special characters**:
```
2025-11-17T20:08:18Z
CODITECT-ROLLOUT-MASTER/submodules/core/coditect-core/2025-11-17
```

**Without encoding**:
- `#checkpoints/2025-11-17T20:08:18Z` → Browser parses `T20:08:18Z` as separate segment
- `#checkpoints/path/with/slashes` → Browser treats each `/` as route separator
- Handler receives truncated or malformed ID → Detail view fails to load

**With encoding**:
- `#checkpoints/2025-11-17T20%3A08%3A18Z` → Correctly preserved
- `#checkpoints/path%2Fwith%2Fslashes` → Correctly preserved
- Handler decodes properly → Detail view loads successfully

---

## Testing After Fix

1. **Navigate to Overview** → Click any recent session → Should show detail view
2. **Navigate to Timeline** → Click session bubble → Click "View Details →" → Should navigate to detail
3. **Navigate to Overview** → Click any topic card → Should filter messages by topic

---

## File to Edit

**Single file**: `/MEMORY-CONTEXT/dashboard/js/navigation.js`

Search for line numbers:
- Line 293 (recent sessions)
- Line 706 (timeline click)
- Line 306 (topic cards)

Add `encodeURIComponent()` wrapper around:
- `${session.id}` → `${encodeURIComponent(session.id)}`
- `${d.id}` → `${encodeURIComponent(d.id)}`
- `${topic.name}` → `${encodeURIComponent(topic.name)}`

---

**Estimated Fix Time**: 5 minutes
**Testing Time**: 10 minutes
**Total**: 15 minutes to resolve all critical navigation bugs
