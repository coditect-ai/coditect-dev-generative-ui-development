# Knowledge Navigation System - Phase 2 Architecture
## Web Dashboard Static Site Generator

**Version**: 1.0
**Date**: 2025-11-24
**Status**: Architecture Design Complete
**Phase**: 2.1 - Dashboard Foundation

---

## Executive Summary

This document defines the complete architecture for the Knowledge Navigation Web Dashboard, a static HTML application that visualizes 10,206 conversation messages through interactive charts, timelines, and search interfaces.

**Architecture Philosophy**:
- **Local-First**: Zero cloud dependencies, works via file:// protocol
- **Zero-Build**: No webpack, babel, or npm - pure HTML/CSS/JS
- **Static Generation**: Python script generates HTML from SQLite database
- **Progressive Enhancement**: Core functionality works without JavaScript
- **Portable**: Zip and run anywhere

**Key Components**:
1. **Static Site Generator** (Python) - Exports SQLite → JSON + HTML
2. **Web Dashboard** (HTML/CSS/JS) - Client-side application
3. **Visualization Library** (D3.js, Chart.js) - Interactive charts
4. **Client-Side Search** (Lunr.js) - Fast full-text search
5. **Report Generator** (JS) - Export to MD/HTML/PDF

---

## 1. System Architecture

### 1.1 C4 Context Diagram

```
┌─────────────────────────────────────────────────────────────────┐
│                    Knowledge Navigation System                   │
│                           (Phase 2)                              │
└─────────────────────────────────────────────────────────────────┘
                                  │
                    ┌─────────────┴──────────────┐
                    │                            │
           ┌────────▼────────┐          ┌───────▼────────┐
           │  Team Members   │          │   Stakeholders  │
           │  (Primary Users)│          │  (Reports Only) │
           └────────┬────────┘          └────────┬────────┘
                    │                            │
           ┌────────▼────────────────────────────▼────────┐
           │                                               │
           │         Web Dashboard (Browser)               │
           │                                               │
           │  • Message Search & Navigation                │
           │  • Interactive Visualizations                 │
           │  • Report Generation                          │
           │                                               │
           └────────┬─────────────────────────┬────────────┘
                    │                         │
           ┌────────▼────────┐       ┌────────▼────────────┐
           │  JSON Data Files │       │  Static HTML/CSS/JS │
           │  (Generated)     │       │  (Generated)        │
           └────────┬─────────┘       └─────────────────────┘
                    │
           ┌────────▼────────┐
           │  SQLite Database│
           │  (knowledge.db) │
           │  [Phase 1]      │
           └─────────────────┘
```

### 1.2 C4 Container Diagram

```
┌───────────────────────────────────────────────────────────────────────┐
│                        Web Dashboard Application                       │
└───────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────────┐
│                          Static Site Generator                          │
│                         (Python 3.10+, Jinja2)                         │
│                                                                          │
│  ┌──────────────┐    ┌──────────────┐    ┌──────────────┐             │
│  │   SQLite     │───▶│  Data Export │───▶│  JSON Files  │             │
│  │   Reader     │    │   Pipeline   │    │  Generator   │             │
│  └──────────────┘    └──────────────┘    └──────┬───────┘             │
│                                                   │                     │
│  ┌──────────────┐    ┌──────────────┐           │                     │
│  │   Jinja2     │───▶│  HTML        │◀──────────┘                     │
│  │   Templates  │    │  Generator   │                                 │
│  └──────────────┘    └──────┬───────┘                                 │
│                              │                                          │
│                              ▼                                          │
│                     ┌──────────────┐                                   │
│                     │  Asset       │                                   │
│                     │  Copier      │                                   │
│                     └──────┬───────┘                                   │
└────────────────────────────┼────────────────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────────────┐
│                           Dashboard Directory                           │
│                                                                          │
│  ┌──────────────────────┐  ┌──────────────────────┐                   │
│  │   index.html         │  │   data/              │                   │
│  │   (Main Dashboard)   │  │   • messages.json    │                   │
│  └──────────────────────┘  │   • topics.json      │                   │
│                             │   • files.json       │                   │
│  ┌──────────────────────┐  │   • checkpoints.json │                   │
│  │   css/               │  │   • commands.json    │                   │
│  │   • main.css         │  └──────────────────────┘                   │
│  │   • layout.css       │                                              │
│  │   • print.css        │  ┌──────────────────────┐                   │
│  └──────────────────────┘  │   templates/         │                   │
│                             │   • base.html        │                   │
│  ┌──────────────────────┐  │   • report-*.html    │                   │
│  │   js/                │  └──────────────────────┘                   │
│  │   • navigation.js    │                                              │
│  │   • data-loader.js   │  ┌──────────────────────┐                   │
│  │   • timeline.js      │  │   assets/            │                   │
│  │   • charts.js        │  │   • logo.png         │                   │
│  │   • report-gen.js    │  │   • favicon.ico      │                   │
│  └──────────────────────┘  └──────────────────────┘                   │
└─────────────────────────────────────────────────────────────────────────┘
                             │
                             ▼
                    ┌──────────────────┐
                    │   Web Browser    │
                    │   (file:// URL)  │
                    │                  │
                    │  • Chrome 90+    │
                    │  • Firefox 88+   │
                    │  • Safari 14+    │
                    │  • Edge 90+      │
                    └──────────────────┘
```

---

## 2. Data Export Schema

### 2.1 JSON File Structure

The static site generator exports 5 primary JSON files:

#### messages.json
```json
{
  "version": "1.0",
  "generated_at": "2025-11-24T12:00:00Z",
  "total_messages": 10206,
  "messages": [
    {
      "hash": "a1b2c3d4e5f6...",
      "role": "user",
      "content": "Message text...",
      "content_preview": "First 200 chars...",
      "checkpoint_id": "2025-11-20-EXPORT-...",
      "checkpoint_title": "Session Title",
      "first_seen": "2025-11-20T10:30:00Z",
      "tags": ["topic:agents", "action:shell-command"],
      "file_references": [
        {"filepath": "README.md", "operation": "read"}
      ],
      "commands": [
        {"type": "git", "text": "git status"}
      ],
      "word_count": 145,
      "has_code": true
    }
  ],
  "pagination": {
    "page_size": 100,
    "total_pages": 103,
    "index_by_hash": true
  }
}
```

**Design Rationale**:
- `content_preview` reduces initial load size (200 char preview vs full message)
- `pagination` enables lazy loading (100 messages per page = 103 pages)
- `index_by_hash` allows O(1) lookup for message details
- Embedded checkpoint/file/command data avoids JOIN queries

#### topics.json
```json
{
  "version": "1.0",
  "generated_at": "2025-11-24T12:00:00Z",
  "topics": [
    {
      "name": "topic:documentation",
      "display_name": "Documentation",
      "category": "topic",
      "message_count": 1994,
      "percentage": 19.5,
      "color": "#3498db",
      "description": "README, CLAUDE.md, architecture docs",
      "top_files": [
        {"file": "README.md", "count": 363},
        {"file": "CLAUDE.md", "count": 306}
      ],
      "recent_messages": [
        {"hash": "abc123...", "date": "2025-11-20"}
      ],
      "activity_by_month": {
        "2025-11": 1456,
        "2025-10": 312
      }
    }
  ],
  "topic_hierarchy": {
    "topics": ["documentation", "submodules", "agents", "testing", "deployment", "security"],
    "actions": ["read-file", "write-file", "edit-file", "shell-command", "task-invocation"],
    "artifacts": ["documentation", "python-code", "shell-script", "config-file"]
  }
}
```

**Design Rationale**:
- Pre-computed `message_count` and `percentage` for fast rendering
- `color` for consistent visual identity across charts
- `activity_by_month` enables timeline visualization
- `topic_hierarchy` defines tag taxonomy

#### files.json
```json
{
  "version": "1.0",
  "generated_at": "2025-11-24T12:00:00Z",
  "files": [
    {
      "filepath": "README.md",
      "reference_count": 363,
      "operations": {
        "read": 226,
        "write": 94,
        "edit": 43
      },
      "first_reference": "2024-11-18T10:00:00Z",
      "last_reference": "2025-11-24T11:00:00Z",
      "file_type": "markdown",
      "related_topics": ["topic:documentation"],
      "related_checkpoints": ["2025-11-20-EXPORT-..."],
      "message_hashes": ["abc123...", "def456..."]
    }
  ],
  "file_tree": {
    "": {
      "README.md": {"count": 363, "type": "file"},
      "docs": {
        "project-management": {
          "PROJECT-PLAN.md": {"count": 184, "type": "file"}
        }
      }
    }
  }
}
```

**Design Rationale**:
- `file_tree` enables hierarchical navigation
- `operations` breakdown shows read vs write activity
- `message_hashes` links to full conversation context
- `file_type` for syntax highlighting

#### checkpoints.json
```json
{
  "version": "1.0",
  "generated_at": "2025-11-24T12:00:00Z",
  "checkpoints": [
    {
      "id": "2025-11-20-EXPORT-SUBMODULE-UPDATES",
      "title": "Submodule Updates",
      "date": "2025-11-20",
      "message_count": 88,
      "user_messages": 42,
      "assistant_messages": 46,
      "duration_minutes": 120,
      "top_topics": ["topic:submodules", "topic:documentation"],
      "files_modified": ["README.md", "PROJECT-PLAN.md"],
      "commands_executed": 23,
      "summary": "Synced all submodules to latest, updated documentation",
      "message_hashes": ["abc123...", "def456..."],
      "previous_checkpoint": "2025-11-19-...",
      "next_checkpoint": "2025-11-21-..."
    }
  ],
  "timeline": [
    {
      "date": "2025-11-20",
      "checkpoints": ["2025-11-20-EXPORT-..."],
      "message_count": 234
    }
  ]
}
```

**Design Rationale**:
- `timeline` aggregates daily activity for D3.js timeline
- `duration_minutes` calculated from first/last message timestamps
- `summary` provides quick context (AI-generated in future)
- `previous_checkpoint` and `next_checkpoint` enable session navigation

#### commands.json
```json
{
  "version": "1.0",
  "generated_at": "2025-11-24T12:00:00Z",
  "commands": [
    {
      "id": 1,
      "command_type": "git",
      "command_text": "git commit -m \"feat: Add feature\"",
      "message_hash": "abc123...",
      "checkpoint_id": "2025-11-20-...",
      "timestamp": "2025-11-20T10:30:00Z",
      "exit_code": 0,
      "output_preview": "First 200 chars of output..."
    }
  ],
  "command_stats": {
    "git": 429,
    "bash": 1215,
    "python": 72,
    "docker": 3,
    "gcloud": 13
  }
}
```

**Design Rationale**:
- `command_type` enables filtering by language/tool
- `exit_code` shows success/failure (if available)
- `command_stats` for pie chart visualization

### 2.2 Data Export Pipeline

```
┌─────────────────────────────────────────────────────────────────┐
│                    Data Export Pipeline                          │
└─────────────────────────────────────────────────────────────────┘

Step 1: Read SQLite Database
    ├─ Connect to knowledge.db
    ├─ Query all messages with tags
    ├─ Query all checkpoints
    ├─ Query file_references
    └─ Query commands

Step 2: Transform Data
    ├─ Aggregate by topic (message counts)
    ├─ Build file tree hierarchy
    ├─ Compute checkpoint summaries
    ├─ Generate timeline data (daily counts)
    └─ Create content previews (200 chars)

Step 3: Paginate Messages
    ├─ Split into 100-message chunks
    ├─ Create message index (hash → page)
    └─ Generate page manifests

Step 4: Write JSON Files
    ├─ messages.json (paginated)
    ├─ topics.json
    ├─ files.json
    ├─ checkpoints.json
    └─ commands.json

Step 5: Validate Output
    ├─ Check JSON syntax
    ├─ Verify message counts
    ├─ Validate relationships
    └─ Test file tree structure
```

**Performance Targets**:
- Export time: < 30 seconds
- Total JSON size: < 15 MB (compressed: < 3 MB)
- Message pagination: 100/page = 103 pages
- File tree depth: Max 10 levels

---

## 3. HTML Template Hierarchy

### 3.1 Template Structure

```
templates/
├── base.html               # Master template (layout, navigation)
│   ├─ header
│   ├─ sidebar (navigation)
│   ├─ main content area (blocks)
│   └─ footer
│
├── index.html              # Dashboard home (extends base)
│   ├─ Overview tab
│   ├─ Quick stats
│   ├─ Recent activity
│   └─ Search bar
│
├── topic.html              # Topic detail view (extends base)
│   ├─ Topic header
│   ├─ Message list (filtered)
│   ├─ Topic cloud
│   └─ Related topics
│
├── file.html               # File history view (extends base)
│   ├─ File header
│   ├─ Operation timeline
│   ├─ Message list (referencing file)
│   └─ Related files
│
├── checkpoint.html         # Session view (extends base)
│   ├─ Session header
│   ├─ Full conversation
│   ├─ Stats sidebar
│   └─ Navigation (prev/next)
│
├── report-executive.html   # Executive summary report
│   ├─ High-level stats
│   ├─ Key insights
│   ├─ Top topics
│   └─ Activity trends
│
├── report-activity.html    # Activity report
│   ├─ Timeline chart
│   ├─ Message breakdown
│   ├─ Command history
│   └─ File changes
│
└── report-topic.html       # Topic analysis report
    ├─ Topic breakdown
    ├─ Trend analysis
    ├─ Key discussions
    └─ Recommendations
```

### 3.2 Template Inheritance

**base.html** (Master Template):
```jinja2
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{% block title %}CODITECT Knowledge Base{% endblock %}</title>

    <!-- CSS -->
    <link rel="stylesheet" href="css/main.css">
    <link rel="stylesheet" href="css/layout.css">
    {% block extra_css %}{% endblock %}

    <!-- External Libraries (CDN) -->
    <script src="https://cdn.jsdelivr.net/npm/d3@7"></script>
    <script src="https://cdn.jsdelivr.net/npm/chart.js@4"></script>
    <script src="https://unpkg.com/lunr@2"></script>
</head>
<body>
    <div class="app-container">
        <!-- Header -->
        <header class="app-header">
            {% block header %}
            <div class="logo">
                <img src="assets/logo.png" alt="CODITECT">
                <h1>Knowledge Base</h1>
            </div>
            <div class="global-search">
                <input type="search" id="global-search" placeholder="Search messages...">
            </div>
            {% endblock %}
        </header>

        <!-- Sidebar Navigation -->
        <aside class="sidebar">
            {% block sidebar %}
            <nav>
                <ul>
                    <li><a href="#/overview">📊 Overview</a></li>
                    <li><a href="#/timeline">📅 Timeline</a></li>
                    <li><a href="#/topics">🏷️ Topics</a></li>
                    <li><a href="#/files">📁 Files</a></li>
                    <li><a href="#/checkpoints">💬 Sessions</a></li>
                    <li><a href="#/commands">⚡ Commands</a></li>
                </ul>
            </nav>
            {% endblock %}
        </aside>

        <!-- Main Content Area -->
        <main class="main-content">
            {% block content %}
            <!-- Child templates override this block -->
            {% endblock %}
        </main>

        <!-- Footer -->
        <footer class="app-footer">
            {% block footer %}
            <p>CODITECT Knowledge Base • Generated {{ generated_at }} • {{ total_messages }} messages</p>
            {% endblock %}
        </footer>
    </div>

    <!-- JavaScript -->
    <script src="js/navigation.js"></script>
    <script src="js/data-loader.js"></script>
    {% block extra_js %}{% endblock %}
</body>
</html>
```

**index.html** (Dashboard Home):
```jinja2
{% extends "base.html" %}

{% block title %}Dashboard - CODITECT Knowledge Base{% endblock %}

{% block content %}
<div class="dashboard-overview">
    <!-- Quick Stats Panel -->
    <section class="quick-stats">
        <div class="stat-card">
            <h3>Total Messages</h3>
            <p class="stat-value">{{ total_messages }}</p>
        </div>
        <div class="stat-card">
            <h3>Checkpoints</h3>
            <p class="stat-value">{{ checkpoint_count }}</p>
        </div>
        <div class="stat-card">
            <h3>Files Referenced</h3>
            <p class="stat-value">{{ file_count }}</p>
        </div>
        <div class="stat-card">
            <h3>Commands Executed</h3>
            <p class="stat-value">{{ command_count }}</p>
        </div>
    </section>

    <!-- Recent Activity -->
    <section class="recent-activity">
        <h2>Recent Activity</h2>
        <div id="activity-timeline"></div>
    </section>

    <!-- Top Topics -->
    <section class="top-topics">
        <h2>Top Topics</h2>
        <div id="topic-cloud"></div>
    </section>
</div>
{% endblock %}

{% block extra_js %}
<script src="js/timeline.js"></script>
<script src="js/topic-cloud.js"></script>
<script>
    // Initialize dashboard visualizations
    renderActivityTimeline('#activity-timeline');
    renderTopicCloud('#topic-cloud');
</script>
{% endblock %}
```

---

## 4. File Organization

### 4.1 Directory Structure

```
MEMORY-CONTEXT/
├── knowledge.db                           # Phase 1 SQLite database
│
├── scripts/
│   ├── index-messages.py                  # Phase 1: Indexing
│   ├── knowledge-cli.py                   # Phase 1: CLI
│   └── generate-dashboard.py              # Phase 2: Generator ⭐
│
├── dashboard/                             # Phase 2: Web UI ⭐
│   ├── index.html                         # Main entry point
│   │
│   ├── css/
│   │   ├── main.css                       # Global styles, variables
│   │   ├── layout.css                     # Grid layout, responsive
│   │   ├── components.css                 # Component styles (cards, buttons)
│   │   └── print.css                      # Print-specific styles
│   │
│   ├── js/
│   │   ├── navigation.js                  # Sidebar, tabs, routing
│   │   ├── data-loader.js                 # JSON loading, caching
│   │   ├── message-renderer.js            # Message list, pagination
│   │   ├── search.js                      # Client-side search (Lunr.js)
│   │   ├── timeline.js                    # D3.js timeline visualization
│   │   ├── topic-cloud.js                 # D3.js word cloud
│   │   ├── charts.js                      # Chart.js bar/pie charts
│   │   ├── file-tree.js                   # File browser component
│   │   ├── command-history.js             # Command table component
│   │   └── report-generator.js            # Export to MD/HTML/PDF
│   │
│   ├── data/                              # Generated JSON files
│   │   ├── messages.json                  # All messages (paginated)
│   │   ├── messages-page-001.json         # Page 1 (messages 1-100)
│   │   ├── messages-page-002.json         # Page 2 (messages 101-200)
│   │   ├── ...                            # ... (103 pages total)
│   │   ├── topics.json                    # Topic metadata
│   │   ├── files.json                     # File references + tree
│   │   ├── checkpoints.json               # Session metadata
│   │   └── commands.json                  # Command history
│   │
│   ├── templates/                         # Jinja2 templates (source)
│   │   ├── base.html                      # Master template
│   │   ├── index.html                     # Dashboard home
│   │   ├── topic.html                     # Topic detail
│   │   ├── file.html                      # File history
│   │   ├── checkpoint.html                # Session view
│   │   ├── report-executive.html          # Executive report
│   │   ├── report-activity.html           # Activity report
│   │   └── report-topic.html              # Topic report
│   │
│   └── assets/
│       ├── logo.png                       # CODITECT logo
│       ├── favicon.ico                    # Browser favicon
│       └── images/                        # Additional images
│
└── docs/
    ├── PHASE-2-ARCHITECTURE.md            # This file
    └── PHASE-2-USER-GUIDE.md              # User documentation
```

### 4.2 File Size Estimates

| File/Directory | Size | Description |
|----------------|------|-------------|
| **knowledge.db** | 12 MB | SQLite database (Phase 1) |
| **dashboard/data/** | 10-15 MB | JSON exports (paginated) |
| ├─ messages.json | 8 MB | Index + metadata |
| ├─ messages-page-*.json | 5 MB | 103 pages × ~50 KB |
| ├─ topics.json | 50 KB | Topic metadata |
| ├─ files.json | 200 KB | File references |
| ├─ checkpoints.json | 1 MB | Session metadata |
| └─ commands.json | 500 KB | Command history |
| **dashboard/css/** | 100 KB | 4 CSS files |
| **dashboard/js/** | 150 KB | 9 JS modules |
| **dashboard/templates/** | 50 KB | 8 HTML templates |
| **dashboard/assets/** | 100 KB | Logo, favicon |
| **TOTAL** | ~25 MB | Complete dashboard |

**Optimization Strategy**:
- Gzip compression: 25 MB → ~6 MB (75% reduction)
- Lazy load message pages: Load 1 page at a time (50 KB each)
- CDN libraries: D3.js, Chart.js not included in size
- Image optimization: PNG → WebP (50% smaller)

---

## 5. Data Loading Strategy

### 5.1 Loading Patterns

#### Pattern 1: Initial Page Load (Fast Path)

```
User opens dashboard (index.html)
    ↓
1. Load critical data only:
   ├─ messages.json (index + metadata, 200 KB)
   ├─ topics.json (50 KB)
   ├─ checkpoints.json (1 MB)
   └─ TOTAL: ~1.3 MB
    ↓
2. Parse JSON → Store in memory
    ↓
3. Render UI skeleton (< 100ms)
    ↓
4. Render overview stats (< 200ms)
    ↓
Dashboard interactive in < 2 seconds ✅
```

**Performance Target**: < 2 seconds to interactive

#### Pattern 2: Lazy Load Message Content (On-Demand)

```
User clicks "View Messages" or scrolls to page 5
    ↓
1. Check cache: Is page 5 already loaded?
   ├─ YES → Render from cache (< 50ms)
   └─ NO → Continue
    ↓
2. Fetch messages-page-005.json (50 KB)
    ↓
3. Parse JSON → Add to cache
    ↓
4. Render 100 messages (< 100ms)
    ↓
Messages visible in < 200ms ✅
```

**Performance Target**: < 200ms per page

#### Pattern 3: Search Index (Precomputed)

```
User types "git submodule" in search bar
    ↓
1. Check if Lunr.js index built:
   ├─ YES → Search immediately
   └─ NO → Build index (one-time, 2-3 seconds)
    ↓
2. Query Lunr.js index
    ↓
3. Get matching message hashes
    ↓
4. Fetch message content (lazy load pages if needed)
    ↓
5. Render search results (< 200ms)
    ↓
Search results displayed in < 500ms ✅
```

**Performance Target**: < 500ms search (after index built)

### 5.2 Caching Strategy

#### In-Memory Cache (JavaScript)

```javascript
const DataCache = {
    messages: {
        index: null,        // messages.json (index)
        pages: new Map(),   // page number → messages
        byHash: new Map()   // message hash → full message
    },
    topics: null,
    files: null,
    checkpoints: null,
    commands: null,
    searchIndex: null       // Lunr.js index (built on demand)
};
```

**Cache Policy**:
- **Immutable Data**: Once loaded, never refetch (static files)
- **Page Cache**: Keep last 10 pages in memory (LRU eviction)
- **Prefetch**: Load adjacent pages (page N → prefetch N+1, N-1)
- **Index Once**: Build Lunr.js search index once, reuse

#### Browser Storage (IndexedDB)

```javascript
// Optional: Store in IndexedDB for offline access
IndexedDB Schema:
    - Store: "messages" → Key: hash, Value: message object
    - Store: "topics" → Key: name, Value: topic object
    - Store: "files" → Key: filepath, Value: file object
    - Store: "cache_meta" → Key: "last_updated", Value: timestamp
```

**Usage**:
- First visit: Populate IndexedDB from JSON files
- Subsequent visits: Check IndexedDB first, fall back to JSON
- **Benefit**: Instant load after first visit

### 5.3 Performance Optimization

#### Virtual Scrolling (Message List)

```javascript
// Only render visible messages (100 visible, 10,206 total)
const VirtualScroll = {
    viewportHeight: 800,     // px
    rowHeight: 120,          // px per message card
    visibleRows: 7,          // 800 / 120 ≈ 7
    bufferRows: 5,           // Extra rows above/below
    renderWindow: 17,        // 7 + (5×2) = 17 total rendered

    onScroll: () => {
        const scrollTop = window.scrollY;
        const firstVisible = Math.floor(scrollTop / rowHeight);
        const lastVisible = firstVisible + renderWindow;

        // Render only messages [firstVisible, lastVisible]
        renderMessages(messages.slice(firstVisible, lastVisible));
    }
};
```

**Benefit**: Render 17 messages instead of 10,206 = 600x faster

#### Progressive Enhancement

```html
<!-- Works without JavaScript (basic functionality) -->
<noscript>
    <p>For the best experience, enable JavaScript.</p>
    <p>You can still browse via CLI: <code>python3 knowledge-cli.py</code></p>
</noscript>

<!-- Core content accessible without JS -->
<div class="message-list">
    {% for message in messages[:100] %}
    <article class="message-card">
        <p>{{ message.content }}</p>
    </article>
    {% endfor %}
</div>

<!-- Enhanced with JS -->
<script>
    // Add interactivity (pagination, search, charts)
    initializeDashboard();
</script>
```

---

## 6. Security Considerations

### 6.1 Threat Model

**Attack Surface**:
- ✅ **No Server**: Static files = no server-side vulnerabilities
- ✅ **Local-First**: No network requests = no MITM attacks
- ⚠️ **XSS Risk**: User content (messages) could contain malicious scripts

**Primary Threat**: XSS (Cross-Site Scripting) via message content

### 6.2 XSS Prevention

#### HTML Sanitization

```javascript
// Sanitize all user-generated content before rendering
function sanitizeHTML(content) {
    const div = document.createElement('div');
    div.textContent = content;  // textContent auto-escapes HTML
    return div.innerHTML;
}

// Safe message rendering
function renderMessage(message) {
    const card = document.createElement('article');
    card.className = 'message-card';

    // SAFE: textContent escapes HTML
    card.textContent = message.content;

    // UNSAFE: innerHTML would execute scripts
    // card.innerHTML = message.content;  ❌ NEVER DO THIS

    return card;
}
```

#### Content Security Policy (CSP)

```html
<meta http-equiv="Content-Security-Policy" content="
    default-src 'self';
    script-src 'self' https://cdn.jsdelivr.net https://unpkg.com;
    style-src 'self' 'unsafe-inline';
    img-src 'self' data:;
    connect-src 'none';
">
```

**Policy Explanation**:
- `default-src 'self'`: Only load resources from same origin
- `script-src`: Allow JS from CDNs (D3.js, Chart.js, Lunr.js)
- `style-src 'unsafe-inline'`: Allow inline CSS (for dynamic styles)
- `img-src 'self' data:`: Allow local images and data URIs
- `connect-src 'none'`: No AJAX requests (static files only)

### 6.3 Code Injection Prevention

#### Safe JSON Loading

```javascript
// Load and parse JSON safely
async function loadData(url) {
    try {
        const response = await fetch(url);
        if (!response.ok) throw new Error(`HTTP ${response.status}`);

        // JSON.parse is safe (doesn't execute code)
        const data = await response.json();

        // Validate structure
        if (!validateSchema(data)) {
            throw new Error('Invalid data schema');
        }

        return data;
    } catch (error) {
        console.error('Failed to load data:', error);
        throw error;
    }
}
```

#### Command Display Safety

```javascript
// Display commands without executing them
function renderCommand(command) {
    const pre = document.createElement('pre');
    const code = document.createElement('code');

    // Safe: textContent prevents execution
    code.textContent = command.text;
    code.className = `language-${command.type}`;

    pre.appendChild(code);
    return pre;
}
```

---

## 7. Browser Compatibility

### 7.1 Target Browsers

| Browser | Minimum Version | Market Share | Notes |
|---------|----------------|--------------|-------|
| **Chrome** | 90+ (Apr 2021) | 65% | Full ES6+, CSS Grid support |
| **Firefox** | 88+ (Apr 2021) | 8% | Full ES6+, CSS Grid support |
| **Safari** | 14+ (Sep 2020) | 19% | ES6+ (partial), CSS Grid OK |
| **Edge** | 90+ (Apr 2021) | 5% | Chromium-based, same as Chrome |

**Total Coverage**: 97%+ of desktop users

### 7.2 Feature Support Matrix

| Feature | Chrome 90+ | Firefox 88+ | Safari 14+ | Edge 90+ | Fallback |
|---------|-----------|------------|-----------|---------|----------|
| **ES6+ (arrow fns, async/await)** | ✅ | ✅ | ✅ | ✅ | N/A (required) |
| **CSS Grid** | ✅ | ✅ | ✅ | ✅ | Flexbox |
| **CSS Variables** | ✅ | ✅ | ✅ | ✅ | N/A (required) |
| **Fetch API** | ✅ | ✅ | ✅ | ✅ | N/A (required) |
| **IndexedDB** | ✅ | ✅ | ✅ | ✅ | localStorage |
| **D3.js v7** | ✅ | ✅ | ⚠️ (partial) | ✅ | Degrade gracefully |
| **Chart.js v4** | ✅ | ✅ | ✅ | ✅ | Show data tables |
| **Lunr.js v2** | ✅ | ✅ | ✅ | ✅ | Server search |
| **Print CSS (@page)** | ✅ | ⚠️ (limited) | ✅ | ✅ | Browser defaults |

**Fallback Strategy**:
- **No JavaScript**: Show static HTML (first 100 messages)
- **Old Browsers**: Show warning, provide CLI alternative
- **Failed Charts**: Display data tables instead

### 7.3 Progressive Enhancement Checklist

- [x] Core content accessible without JavaScript
- [x] Navigation works with browser back/forward
- [x] Links use standard URLs (#/topics/agents)
- [x] Print CSS for report generation
- [x] Keyboard navigation (Tab, Enter, Esc)
- [x] ARIA labels for screen readers
- [x] High contrast mode support
- [x] Responsive design (mobile, tablet, desktop)

---

## 8. Implementation Checklist

### Phase 2.1: Dashboard Foundation (Week 1)

#### Day 1-2: Static Site Generator
- [ ] Design JSON export schema (this section ✅)
- [ ] Implement `generate-dashboard.py` script
  - [ ] SQLite reader (connect to knowledge.db)
  - [ ] Data transformer (messages → JSON)
  - [ ] Pagination engine (100 msgs/page)
  - [ ] Topic aggregation
  - [ ] File tree builder
  - [ ] Checkpoint summarizer
  - [ ] JSON writer (5 files)
- [ ] Create Jinja2 templates (base, index, topic, file, checkpoint)
- [ ] Implement asset copier (CSS, JS, images)
- [ ] Test generator: `python3 generate-dashboard.py`

#### Day 3-4: Dashboard Layout
- [ ] Create CSS Grid layout (responsive)
- [ ] Build sidebar navigation
- [ ] Implement tab system
- [ ] Add global search bar
- [ ] Style message cards
- [ ] Test responsive design (mobile, tablet, desktop)

#### Day 5: Data Loading & Rendering
- [ ] Implement `data-loader.js` (fetch, cache, paginate)
- [ ] Build `message-renderer.js` (virtual scroll, cards)
- [ ] Add syntax highlighting (Prism.js or highlight.js)
- [ ] Create pagination controls
- [ ] Test performance: Render 100 messages in < 100ms

### Phase 2.2: Visualizations (Week 2)

#### Day 6-7: Timeline
- [ ] Integrate D3.js timeline
- [ ] Implement zoom/pan controls
- [ ] Add click-to-filter interaction
- [ ] Create activity heatmap view
- [ ] Test timeline with 10,206 messages

#### Day 8: Topic Cloud & Charts
- [ ] Build D3.js word cloud
- [ ] Create Chart.js bar chart (topics)
- [ ] Add pie chart (user vs assistant)
- [ ] Implement horizontal bar (top files)
- [ ] Test interactions (click to filter)

#### Day 9: File Tree & Commands
- [ ] Build hierarchical file tree
- [ ] Add expand/collapse controls
- [ ] Create command history table
- [ ] Add filtering by command type
- [ ] Test navigation and sorting

#### Day 10: Report Generation
- [ ] Design report templates
- [ ] Implement Markdown export
- [ ] Add HTML export (self-contained)
- [ ] Create PDF export (print CSS)
- [ ] Test all 3 formats

---

## 9. Success Criteria

### Technical Success
- [x] Architecture document complete (this file)
- [ ] Static site generator produces working HTML
- [ ] Dashboard loads in < 2 seconds
- [ ] Search results in < 500ms
- [ ] All visualizations interactive
- [ ] Works in 4 browsers (Chrome, Firefox, Safari, Edge)
- [ ] No console errors
- [ ] Responsive design (mobile, tablet, desktop)

### User Experience Success
- [ ] Team members prefer dashboard over CLI
- [ ] Non-technical users can navigate easily
- [ ] Reports generated and used in meetings
- [ ] Daily active usage > 5 team members
- [ ] Average session duration > 10 minutes

### Business Success
- [ ] Onboarding time reduced by 50%
- [ ] Knowledge retrieval 5x faster
- [ ] Developer satisfaction 8/10+
- [ ] Stakeholder reports generated monthly

---

## 10. Next Steps

### Immediate (Today)
1. ✅ Review this architecture document
2. ⏸️ Approve design decisions
3. ⏸️ Begin implementation: `generate-dashboard.py` script

### Week 1 (Days 1-5)
1. ⏸️ Build static site generator
2. ⏸️ Create dashboard layout
3. ⏸️ Implement data loading
4. ⏸️ Test with full dataset (10,206 messages)

### Week 2 (Days 6-10)
1. ⏸️ Add visualizations (timeline, charts, topic cloud)
2. ⏸️ Build file tree and command history
3. ⏸️ Implement report generation
4. ⏸️ Final testing and polish

---

## Appendix: Technology Stack

### Core Technologies
- **HTML5**: Semantic markup, accessibility
- **CSS3**: Grid layout, Flexbox, variables
- **JavaScript ES6+**: Modules, async/await, arrow functions

### External Libraries (CDN)
- **D3.js v7**: Data visualization, charts, timeline
- **Chart.js v4**: Bar charts, pie charts, line charts
- **Lunr.js v2**: Client-side full-text search
- **Prism.js** (optional): Syntax highlighting for code blocks

### Python Stack
- **Python 3.10+**: Static site generator
- **Jinja2**: HTML templating
- **SQLite3**: Database access (stdlib)
- **JSON**: Data serialization (stdlib)

### Development Tools
- **VS Code**: Primary IDE
- **Chrome DevTools**: Debugging, performance profiling
- **Firefox Developer Tools**: Cross-browser testing
- **Git**: Version control

---

**Architecture Status**: Complete ✅
**Next Task**: Implement Static Site Generator (Task 1.2)
**Estimated Time**: 8 hours
**Assignee**: frontend-react-typescript-expert

**Last Updated**: 2025-11-24
