// CODITECT Dashboard - Navigation System (Task 1.3)
// Handles tab switching, URL routing, sidebar navigation
// NOTE: Data loading moved to data-loader.js (Task 1.4)

console.log('✓ Navigation system loading...');

/**
 * Navigation Controller
 * Manages application state, routing, and view rendering (structure only)
 */
class NavigationController {
    constructor() {
        this.currentView = 'overview';
        this.currentFilter = null;
        this.searchQuery = '';

        // View definitions
        this.views = {
            'overview': { title: 'Overview', icon: '📊' },
            'timeline': { title: 'Timeline', icon: '📅' },
            'topics': { title: 'Topics', icon: '🏷️' },
            'files': { title: 'Files', icon: '📁' },
            'checkpoints': { title: 'Sessions', icon: '💬' },
            'commands': { title: 'Commands', icon: '⚡' },
            'about': { title: 'About MEMORY-CONTEXT', icon: 'ℹ️' },
            'help': { title: 'Help', icon: '❓' }
        };

        // Initialize
        this.init();
    }

    init() {
        console.log('Initializing navigation...');

        // Set up event listeners
        this.setupEventListeners();

        // Handle initial route
        this.handleRoute();

        // Listen for URL changes
        window.addEventListener('hashchange', () => this.handleRoute());

        console.log('✓ Navigation initialized');
    }

    setupEventListeners() {
        // Sidebar navigation links
        const sidebarLinks = document.querySelectorAll('.sidebar a');
        sidebarLinks.forEach(link => {
            link.addEventListener('click', (e) => this.handleNavClick(e));
        });

        // Global search input
        const searchInput = document.getElementById('global-search');
        if (searchInput) {
            searchInput.addEventListener('input', (e) => this.handleSearch(e));
            searchInput.addEventListener('keypress', (e) => {
                if (e.key === 'Enter') {
                    this.executeSearch();
                }
            });
        }

        // Escape key to close modals/filters
        document.addEventListener('keydown', (e) => {
            if (e.key === 'Escape') {
                this.closeModals();
            }
        });
    }

    handleNavClick(e) {
        e.preventDefault();
        const href = e.currentTarget.getAttribute('href');

        if (href && href.startsWith('#')) {
            // Update URL hash
            window.location.hash = href;
        }
    }

    handleRoute() {
        // Parse URL hash
        const hash = window.location.hash.slice(1); // Remove '#'

        if (!hash) {
            // Default to overview
            this.navigateTo('overview');
            return;
        }

        // Parse hash: #view or #view/filter or #view/filter/id
        const parts = hash.split('/');
        const view = parts[0];
        const filter = parts[1] || null;
        const id = parts[2] || null;

        // Validate view
        if (this.views[view]) {
            this.navigateTo(view, filter, id);
        } else {
            console.warn(`Unknown view: ${view}`);
            this.navigateTo('overview');
        }
    }

    navigateTo(view, filter = null, id = null) {
        console.log(`Navigating to: ${view}`, { filter, id });

        // Update state
        this.currentView = view;
        this.currentFilter = filter;

        // Update active states in sidebar
        this.updateSidebarActive(view);

        // Update page title
        document.title = `${this.views[view].title} - CODITECT Knowledge Base`;

        // Render view (structure only - data loading in Task 1.4)
        this.renderView(view, filter, id);
    }

    updateSidebarActive(view) {
        // Remove all active states
        const sidebarLinks = document.querySelectorAll('.sidebar a');
        sidebarLinks.forEach(link => {
            link.classList.remove('active');
        });

        // Add active state to current view
        const activeLink = document.querySelector(`.sidebar a[href="#${view}"]`);
        if (activeLink) {
            activeLink.classList.add('active');
        }
    }

    renderView(view, filter, id) {
        const mainContent = document.querySelector('.main-content');
        if (!mainContent) return;

        // Show loading state
        mainContent.innerHTML = '<div class="loading">Loading...</div>';

        // Render based on view
        switch (view) {
            case 'overview':
                this.renderOverview();
                break;
            case 'timeline':
                this.renderTimeline();
                break;
            case 'topics':
                this.renderTopics(filter);
                break;
            case 'files':
                this.renderFiles(filter);
                break;
            case 'checkpoints':
                this.renderCheckpoints(id);
                break;
            case 'commands':
                this.renderCommands(filter);
                break;
            case 'about':
                this.renderAbout();
                break;
            case 'help':
                this.renderHelp();
                break;
            default:
                this.renderOverview();
        }
    }

    async renderOverview() {
        const mainContent = document.querySelector('.main-content');

        // Show loading state
        mainContent.innerHTML = '<div class="loading">Loading overview data...</div>';

        try {
            // Load overview data using data loader
            const data = await window.dashboardData.loadOverviewData();

            mainContent.innerHTML = `
                <div class="dashboard-overview">
                    <section class="quick-stats">
                        <div class="stat-card clickable" onclick="window.location.hash='#checkpoints'">
                            <h3>Total Messages</h3>
                            <p class="stat-value">${data.stats.totalMessages.toLocaleString()}</p>
                            <p class="stat-label">Click to view all sessions</p>
                        </div>
                        <div class="stat-card clickable" onclick="window.location.hash='#checkpoints'">
                            <h3>Checkpoints</h3>
                            <p class="stat-value">${data.stats.totalCheckpoints.toLocaleString()}</p>
                            <p class="stat-label">Conversation sessions</p>
                        </div>
                        <div class="stat-card clickable" onclick="window.location.hash='#files'">
                            <h3>Files Referenced</h3>
                            <p class="stat-value">${data.stats.totalFiles.toLocaleString()}</p>
                            <p class="stat-label">Click to browse files</p>
                        </div>
                        <div class="stat-card clickable" onclick="window.location.hash='#commands'">
                            <h3>Commands Executed</h3>
                            <p class="stat-value">${data.stats.totalCommands.toLocaleString()}</p>
                            <p class="stat-label">Click to view history</p>
                        </div>
                    </section>

                    <section class="section">
                        <div class="card">
                            <div class="card-header">
                                <h2 class="card-title">Welcome to CODITECT Knowledge Base</h2>
                                <p class="card-subtitle">Interactive dashboard for exploring ${data.stats.totalMessages.toLocaleString()} conversation messages</p>
                            </div>
                            <div class="card-content">
                                <p>
                                    This dashboard provides comprehensive access to your entire CODITECT conversation history.
                                    Navigate using the sidebar or search above to find specific conversations, topics, files, or commands.
                                </p>

                                <div class="flex gap-2" style="margin-top: var(--space-4); flex-wrap: wrap;">
                                    <button onclick="window.location.hash='#timeline'" class="btn btn-primary">
                                        📅 View Timeline
                                    </button>
                                    <button onclick="window.location.hash='#topics'" class="btn btn-secondary">
                                        🏷️ Browse Topics
                                    </button>
                                    <button onclick="window.location.hash='#checkpoints'" class="btn btn-secondary">
                                        💬 All Sessions
                                    </button>
                                    <button onclick="window.location.hash='#about'" class="btn btn-secondary">
                                        ℹ️ What is MEMORY-CONTEXT?
                                    </button>
                                </div>
                            </div>
                        </div>
                    </section>

                    <section class="section">
                        <h2 class="section-title">Recent Sessions</h2>
                        <div class="grid">
                            ${data.recentSessions.map(session => `
                                <div class="card card-collapsible collapsed" onclick="this.classList.toggle('collapsed')">
                                    <div class="card-header">
                                        <div>
                                            <h3 class="card-title">${this.escapeHtml(session.title || session.id)}</h3>
                                            <p class="card-subtitle">${session.message_count} messages • ${this.formatDate(session.timestamp)}</p>
                                        </div>
                                        <span class="card-collapse-icon">▼</span>
                                    </div>
                                    <div class="card-content">
                                        <p><strong>Topics:</strong> ${session.top_topics.slice(0, 3).join(', ') || 'None'}</p>
                                        <p><strong>Files:</strong> ${session.files_modified || 0} modified</p>
                                        <p><strong>Commands:</strong> ${session.commands_executed || 0} executed</p>
                                        <a href="#checkpoints/${session.id}" class="btn btn-sm btn-primary" style="margin-top: var(--space-2);">
                                            View Full Session →
                                        </a>
                                    </div>
                                </div>
                            `).join('')}
                        </div>
                    </section>

                    <section class="section">
                        <h2 class="section-title">Top Topics</h2>
                        <div class="grid grid-cols-2">
                            ${data.topTopics.map(topic => `
                                <div class="card clickable" onclick="window.location.hash='#topics/${topic.name}'">
                                    <h3 class="card-title">${this.escapeHtml(topic.display_name || topic.name)}</h3>
                                    <p style="font-size: var(--text-2xl); font-weight: var(--font-bold); color: var(--primary-500); margin: var(--space-2) 0;">
                                        ${topic.message_count.toLocaleString()}
                                    </p>
                                    <p class="text-sm" style="color: var(--text-tertiary);">
                                        ${topic.percentage}% of all messages
                                    </p>
                                </div>
                            `).join('')}
                        </div>
                    </section>
                </div>
            `;
        } catch (error) {
            console.error('Failed to load overview data:', error);
            mainContent.innerHTML = `
                <div class="card">
                    <div class="card-header">
                        <h2 class="card-title" style="color: var(--error-500);">Failed to Load Data</h2>
                    </div>
                    <div class="card-content">
                        <p>Could not load overview data. Please ensure:</p>
                        <ol style="margin-left: var(--space-6); margin-top: var(--space-2);">
                            <li>You are running an HTTP server (not file://)</li>
                            <li>The data files exist in the <code>data/</code> directory</li>
                        </ol>
                        <p style="margin-top: var(--space-4);">
                            <strong>To start HTTP server:</strong><br>
                            <code>cd dashboard && python3 -m http.server 8080</code><br>
                            Then open <code>http://localhost:8080</code>
                        </p>
                        <p style="margin-top: var(--space-4); font-size: var(--text-sm); color: var(--text-tertiary);">
                            Error: ${error.message}
                        </p>
                    </div>
                </div>
            `;
        }
    }

    escapeHtml(text) {
        const div = document.createElement('div');
        div.textContent = text;
        return div.innerHTML;
    }

    renderTimeline() {
        const mainContent = document.querySelector('.main-content');
        mainContent.innerHTML = `
            <div class="timeline-view">
                <h2>📅 Activity Timeline</h2>
                <p>Timeline visualization coming in Week 2 (D3.js implementation)</p>
                <div style="background: #f5f5f5; padding: 2rem; border-radius: 8px; text-align: center; margin-top: 2rem;">
                    <h3>Timeline Chart</h3>
                    <p>Interactive D3.js timeline will be implemented in Task 2.1</p>
                    <p>Will show message distribution by date with zoom/pan controls</p>
                </div>
            </div>
        `;
    }

    renderTopics(filter) {
        const mainContent = document.querySelector('.main-content');

        if (filter) {
            // Show specific topic
            mainContent.innerHTML = `
                <div class="topic-detail-view">
                    <h2>Topic: ${filter}</h2>
                    <div style="padding: 2rem; background: #f9f9f9; border-radius: 8px; text-align: center; margin-top: 2rem;">
                        <p><strong>Task 1.5: Message Rendering</strong></p>
                        <p>Topic-filtered message list will be implemented next</p>
                        <p>Shows all messages tagged with topic "${filter}"</p>
                    </div>
                </div>
            `;
        } else {
            // Show all topics
            mainContent.innerHTML = `
                <div class="topics-view">
                    <h2>🏷️ Topics</h2>
                    <div id="topics-grid" style="padding: 2rem; background: #f9f9f9; border-radius: 8px; text-align: center; margin-top: 2rem;">
                        <p><strong>Task 1.4: Data Loading</strong></p>
                        <p>Dynamic topic grid will be loaded next</p>
                        <p>Will display all 14 topics with statistics</p>
                    </div>
                </div>
            `;
        }
    }

    renderFiles(filter) {
        const mainContent = document.querySelector('.main-content');
        mainContent.innerHTML = `
            <div class="files-view">
                <h2>📁 Files (4,060 references)</h2>
                <div style="padding: 2rem; background: #f9f9f9; border-radius: 8px; text-align: center; margin-top: 2rem;">
                    <h3>File Tree Browser</h3>
                    <p><strong>Task 2.4 (Week 2)</strong></p>
                    <p>Hierarchical file browser will show all 4,060 referenced files</p>
                    <p>Collapsible folders, reference counts, click to view history</p>
                </div>
            </div>
        `;
    }

    renderCheckpoints(id) {
        const mainContent = document.querySelector('.main-content');

        if (id) {
            // Show specific checkpoint
            mainContent.innerHTML = `
                <div class="checkpoint-detail-view">
                    <h2>Session: ${id}</h2>
                    <div id="checkpoint-content" style="padding: 2rem; background: #f9f9f9; border-radius: 8px; text-align: center; margin-top: 2rem;">
                        <p><strong>Task 1.4: Data Loading</strong></p>
                        <p>Session details will be loaded dynamically</p>
                        <p>Will display full metadata, topics, files, and commands</p>
                    </div>
                </div>
            `;
        } else {
            // Show all checkpoints
            mainContent.innerHTML = `
                <div class="checkpoints-view">
                    <h2>💬 Conversation Sessions (124 total)</h2>
                    <div class="filters">
                        <input type="search" id="checkpoint-search" placeholder="Search sessions..." disabled />
                        <select id="checkpoint-sort" disabled>
                            <option value="date-desc">Newest First</option>
                            <option value="date-asc">Oldest First</option>
                            <option value="messages-desc">Most Messages</option>
                        </select>
                    </div>
                    <div id="checkpoints-list" style="padding: 2rem; background: #f9f9f9; border-radius: 8px; text-align: center; margin-top: 2rem;">
                        <p><strong>Task 1.4: Data Loading</strong></p>
                        <p>Session list with search and sort will be implemented next</p>
                        <p>Will display all 124 sessions with metadata</p>
                    </div>
                </div>
            `;
        }
    }

    renderCommands(filter) {
        const mainContent = document.querySelector('.main-content');
        mainContent.innerHTML = `
            <div class="commands-view">
                <h2>⚡ Commands (1,732 total)</h2>
                <div style="padding: 2rem; background: #f9f9f9; border-radius: 8px; text-align: center; margin-top: 2rem;">
                    <p><strong>Task 1.4: Data Loading</strong></p>
                    <p>Command history with filtering will be implemented next</p>
                    <p>Will display all 1,732 executed commands with timestamps</p>
                </div>
            </div>
        `;
    }

    handleSearch(e) {
        this.searchQuery = e.target.value;
        console.log('Search query:', this.searchQuery);
        // Search implementation in Task 1.4
    }

    executeSearch() {
        if (!this.searchQuery) return;
        console.log('Executing search:', this.searchQuery);
        // Search execution in Task 1.4
        alert('Search functionality will be implemented in Task 1.4 - Data Loading System');
    }

    closeModals() {
        // Modal close logic for Task 1.5
    }

    renderAbout() {
        const mainContent = document.querySelector('.main-content');
        mainContent.innerHTML = `
            <div class="dashboard-overview">
                <section class="section">
                    <div class="card">
                        <div class="card-header">
                            <h1 class="card-title">What is MEMORY-CONTEXT?</h1>
                            <p class="card-subtitle">Understanding CODITECT's Conversation Intelligence System</p>
                        </div>
                        <div class="card-content">
                            <h3>Overview</h3>
                            <p>
                                <strong>MEMORY-CONTEXT</strong> is CODITECT's comprehensive conversation intelligence system that captures,
                                indexes, and makes searchable your entire Claude Code conversation history. Think of it as your project's
                                permanent memory - every decision, implementation detail, and problem-solving session preserved and accessible.
                            </p>

                            <h3 style="margin-top: var(--space-6);">Key Features</h3>
                            <div class="grid grid-cols-2" style="margin-top: var(--space-4);">
                                <div class="card" style="background-color: var(--bg-tertiary);">
                                    <h4>📊 Complete History</h4>
                                    <p class="text-sm">
                                        ${(10206).toLocaleString()} conversation messages from ${(124).toLocaleString()} sessions,
                                        giving you complete visibility into your project's evolution.
                                    </p>
                                </div>
                                <div class="card" style="background-color: var(--bg-tertiary);">
                                    <h4>🔍 Smart Search</h4>
                                    <p class="text-sm">
                                        Find any conversation, decision, or code snippet instantly with full-text search
                                        powered by SQLite FTS5.
                                    </p>
                                </div>
                                <div class="card" style="background-color: var(--bg-tertiary);">
                                    <h4>🏷️ Topic Organization</h4>
                                    <p class="text-sm">
                                        Conversations automatically categorized into 14 topics including Documentation,
                                        Testing, Agents, and more.
                                    </p>
                                </div>
                                <div class="card" style="background-color: var(--bg-tertiary);">
                                    <h4>📁 File Tracking</h4>
                                    <p class="text-sm">
                                        ${(4060).toLocaleString()} file references tracked across all sessions, showing
                                        what was read, written, or edited.
                                    </p>
                                </div>
                            </div>

                            <h3 style="margin-top: var(--space-6);">How It Works</h3>
                            <ol style="margin-left: var(--space-6); margin-top: var(--space-2);">
                                <li><strong>Automatic Export</strong> - After each Claude Code session, conversations are automatically exported to JSON format.</li>
                                <li><strong>Intelligent Deduplication</strong> - Content-based hashing removes duplicate messages while preserving unique context.</li>
                                <li><strong>Database Indexing</strong> - Messages are indexed into SQLite with full-text search capabilities.</li>
                                <li><strong>Dashboard Generation</strong> - This web dashboard is generated from the indexed data for easy browsing.</li>
                            </ol>

                            <h3 style="margin-top: var(--space-6);">Use Cases</h3>
                            <ul style="margin-left: var(--space-6); margin-top: var(--space-2);">
                                <li><strong>Onboarding</strong> - New team members can review the complete project history to get up to speed.</li>
                                <li><strong>Decision Auditing</strong> - Review why certain architectural choices were made and when.</li>
                                <li><strong>Knowledge Retrieval</strong> - Find solutions to problems you've already solved in past sessions.</li>
                                <li><strong>Progress Tracking</strong> - See the evolution of your project over time with timeline visualizations.</li>
                                <li><strong>Documentation</strong> - Generate project documentation from actual implementation conversations.</li>
                            </ul>

                            <h3 style="margin-top: var(--space-6);">Technical Stack</h3>
                            <div class="grid grid-cols-3" style="margin-top: var(--space-4);">
                                <div>
                                    <h4 class="text-sm font-semibold">Backend</h4>
                                    <ul class="text-sm" style="list-style: none; padding: 0; color: var(--text-secondary);">
                                        <li>Python 3.10+</li>
                                        <li>SQLite + FTS5</li>
                                        <li>Jinja2 Templates</li>
                                    </ul>
                                </div>
                                <div>
                                    <h4 class="text-sm font-semibold">Frontend</h4>
                                    <ul class="text-sm" style="list-style: none; padding: 0; color: var(--text-secondary);">
                                        <li>Vanilla JavaScript</li>
                                        <li>CSS Grid Layout</li>
                                        <li>Zero dependencies</li>
                                    </ul>
                                </div>
                                <div>
                                    <h4 class="text-sm font-semibold">Data Format</h4>
                                    <ul class="text-sm" style="list-style: none; padding: 0; color: var(--text-secondary);">
                                        <li>JSON exports</li>
                                        <li>Paginated files</li>
                                        <li>Gzip compression</li>
                                    </ul>
                                </div>
                            </div>

                            <div style="margin-top: var(--space-8); padding: var(--space-4); background-color: var(--primary-50); border-left: 4px solid var(--primary-500); border-radius: var(--radius-md);">
                                <p class="font-semibold" style="color: var(--primary-700);">
                                    💡 Pro Tip
                                </p>
                                <p class="text-sm" style="margin-top: var(--space-2); color: var(--text-secondary);">
                                    Use the <a href="#checkpoints" style="color: var(--primary-600);">Sessions view</a> to browse all conversations,
                                    or try the <a href="#topics" style="color: var(--primary-600);">Topics view</a> to find conversations by category.
                                    The search bar above works across all ${(10206).toLocaleString()} messages!
                                </p>
                            </div>
                        </div>
                    </div>
                </section>
            </div>
        `;
    }

    renderHelp() {
        const mainContent = document.querySelector('.main-content');
        mainContent.innerHTML = `
            <div class="dashboard-overview">
                <section class="section">
                    <div class="card">
                        <div class="card-header">
                            <h1 class="card-title">Help & User Guide</h1>
                            <p class="card-subtitle">Learn how to navigate and use the CODITECT Knowledge Base Dashboard</p>
                        </div>
                        <div class="card-content">
                            <h3>Getting Started</h3>
                            <div class="card" style="background-color: var(--warning-50); border-left: 4px solid var(--warning-500); margin-top: var(--space-2);">
                                <p class="font-semibold" style="color: var(--warning-700);">⚠️ HTTP Server Required</p>
                                <p class="text-sm" style="margin-top: var(--space-2); color: var(--text-secondary);">
                                    This dashboard requires an HTTP server to load data (browser security blocks fetch() on file://).
                                </p>
                                <pre style="margin-top: var(--space-2); padding: var(--space-2); background-color: var(--bg-tertiary); border-radius: var(--radius-sm); font-size: var(--text-sm);">cd dashboard
python3 -m http.server 8080</pre>
                                <p class="text-sm" style="margin-top: var(--space-2); color: var(--text-secondary);">
                                    Then open <code>http://localhost:8080</code> in your browser.
                                </p>
                            </div>

                            <h3 style="margin-top: var(--space-6);">Navigation</h3>
                            <div class="grid" style="margin-top: var(--space-4);">
                                <div class="card card-collapsible collapsed" onclick="this.classList.toggle('collapsed')">
                                    <div class="card-header">
                                        <h4 class="card-title">📊 Overview</h4>
                                        <span class="card-collapse-icon">▼</span>
                                    </div>
                                    <div class="card-content">
                                        <p class="text-sm">
                                            Dashboard home with quick stats, recent sessions, and top topics.
                                            Click stat cards to jump to detailed views.
                                        </p>
                                    </div>
                                </div>

                                <div class="card card-collapsible collapsed" onclick="this.classList.toggle('collapsed')">
                                    <div class="card-header">
                                        <h4 class="card-title">📅 Timeline</h4>
                                        <span class="card-collapse-icon">▼</span>
                                    </div>
                                    <div class="card-content">
                                        <p class="text-sm">
                                            Chronological view of all conversation sessions with D3.js visualization
                                            (coming in Week 2 implementation).
                                        </p>
                                    </div>
                                </div>

                                <div class="card card-collapsible collapsed" onclick="this.classList.toggle('collapsed')">
                                    <div class="card-header">
                                        <h4 class="card-title">🏷️ Topics</h4>
                                        <span class="card-collapse-icon">▼</span>
                                    </div>
                                    <div class="card-content">
                                        <p class="text-sm">
                                            Browse all 14 conversation topics. Click a topic to see all messages in that category.
                                            Topics include Documentation, Testing, Agents, Python-Code, and more.
                                        </p>
                                    </div>
                                </div>

                                <div class="card card-collapsible collapsed" onclick="this.classList.toggle('collapsed')">
                                    <div class="card-header">
                                        <h4 class="card-title">📁 Files</h4>
                                        <span class="card-collapse-icon">▼</span>
                                    </div>
                                    <div class="card-content">
                                        <p class="text-sm">
                                            Hierarchical file browser showing all ${(4060).toLocaleString()} referenced files.
                                            See which files were read, written, or edited across all sessions.
                                        </p>
                                    </div>
                                </div>

                                <div class="card card-collapsible collapsed" onclick="this.classList.toggle('collapsed')">
                                    <div class="card-header">
                                        <h4 class="card-title">💬 Sessions</h4>
                                        <span class="card-collapse-icon">▼</span>
                                    </div>
                                    <div class="card-content">
                                        <p class="text-sm">
                                            Browse all ${(124).toLocaleString()} conversation sessions. Search by title, filter by date,
                                            sort by message count. Click a session to see full details, topics, files, and commands.
                                        </p>
                                    </div>
                                </div>

                                <div class="card card-collapsible collapsed" onclick="this.classList.toggle('collapsed')">
                                    <div class="card-header">
                                        <h4 class="card-title">⚡ Commands</h4>
                                        <span class="card-collapse-icon">▼</span>
                                    </div>
                                    <div class="card-content">
                                        <p class="text-sm">
                                            View all ${(1732).toLocaleString()} executed commands. Filter by type (git, bash, python, docker, gcloud).
                                            See command history with timestamps and session context.
                                        </p>
                                    </div>
                                </div>
                            </div>

                            <h3 style="margin-top: var(--space-6);">Features</h3>
                            <div class="grid grid-cols-2" style="margin-top: var(--space-4);">
                                <div>
                                    <h4>🔍 Global Search</h4>
                                    <p class="text-sm" style="color: var(--text-secondary);">
                                        Use the search bar at the top to search across all ${(10206).toLocaleString()} messages.
                                        Results show matching messages with context and links to full sessions.
                                    </p>
                                </div>
                                <div>
                                    <h4>🌙 Dark Mode</h4>
                                    <p class="text-sm" style="color: var(--text-secondary);">
                                        Click the moon/sun icon in the header to toggle between light and dark themes.
                                        Your preference is saved to localStorage.
                                    </p>
                                </div>
                                <div>
                                    <h4>📋 Collapsible Cards</h4>
                                    <p class="text-sm" style="color: var(--text-secondary);">
                                        Click card headers to expand/collapse content. Keeps the interface compact
                                        while giving you access to detailed information when needed.
                                    </p>
                                </div>
                                <div>
                                    <h4>🔗 Deep Linking</h4>
                                    <p class="text-sm" style="color: var(--text-secondary);">
                                        URLs update as you navigate. Share direct links to sessions, topics, or specific views.
                                        Browser back/forward buttons work as expected.
                                    </p>
                                </div>
                            </div>

                            <h3 style="margin-top: var(--space-6);">Keyboard Shortcuts</h3>
                            <div style="margin-top: var(--space-4);">
                                <table style="width: 100%; border-collapse: collapse;">
                                    <thead>
                                        <tr style="border-bottom: 2px solid var(--border-primary);">
                                            <th style="text-align: left; padding: var(--space-2); font-weight: var(--font-semibold);">Shortcut</th>
                                            <th style="text-align: left; padding: var(--space-2); font-weight: var(--font-semibold);">Action</th>
                                        </tr>
                                    </thead>
                                    <tbody>
                                        <tr style="border-bottom: 1px solid var(--border-primary);">
                                            <td style="padding: var(--space-2);"><code>/</code></td>
                                            <td style="padding: var(--space-2); color: var(--text-secondary);">Focus search bar</td>
                                        </tr>
                                        <tr style="border-bottom: 1px solid var(--border-primary);">
                                            <td style="padding: var(--space-2);"><code>Esc</code></td>
                                            <td style="padding: var(--space-2); color: var(--text-secondary);">Close modals and dialogs</td>
                                        </tr>
                                        <tr>
                                            <td style="padding: var(--space-2);"><code>← →</code></td>
                                            <td style="padding: var(--space-2); color: var(--text-secondary);">Navigate browser history (back/forward)</td>
                                        </tr>
                                    </tbody>
                                </table>
                            </div>

                            <h3 style="margin-top: var(--space-6);">Troubleshooting</h3>
                            <div class="grid" style="margin-top: var(--space-4);">
                                <div class="card" style="background-color: var(--bg-tertiary);">
                                    <h4 class="text-sm font-semibold">Data not loading?</h4>
                                    <p class="text-xs" style="margin-top: var(--space-2); color: var(--text-secondary);">
                                        Make sure you're running an HTTP server (<code>python3 -m http.server 8080</code>).
                                        The dashboard won't work with the file:// protocol due to browser security.
                                    </p>
                                </div>
                                <div class="card" style="background-color: var(--bg-tertiary);">
                                    <h4 class="text-sm font-semibold">Search not working?</h4>
                                    <p class="text-xs" style="margin-top: var(--space-2); color: var(--text-secondary);">
                                        Full-text search requires the SQLite FTS5 extension. Make sure you've run the indexing
                                        script: <code>python3 scripts/index-messages.py</code>
                                    </p>
                                </div>
                                <div class="card" style="background-color: var(--bg-tertiary);">
                                    <h4 class="text-sm font-semibold">Outdated data?</h4>
                                    <p class="text-xs" style="margin-top: var(--space-2); color: var(--text-secondary);">
                                        Regenerate the dashboard after new sessions: <code>python3 scripts/generate-dashboard.py</code>.
                                        This updates all JSON files with the latest conversation data.
                                    </p>
                                </div>
                            </div>

                            <div style="margin-top: var(--space-8); padding: var(--space-4); background-color: var(--info-50); border-left: 4px solid var(--info-500); border-radius: var(--radius-md);">
                                <p class="font-semibold" style="color: var(--info-700);">
                                    📚 Need More Help?
                                </p>
                                <p class="text-sm" style="margin-top: var(--space-2); color: var(--text-secondary);">
                                    Check the <a href="#about" style="color: var(--info-600);">About MEMORY-CONTEXT</a> page to understand
                                    how the system works, or visit the
                                    <a href="https://github.com/coditect-ai" target="_blank" rel="noopener" style="color: var(--info-600);">
                                        CODITECT GitHub repository
                                    </a> for technical documentation.
                                </p>
                            </div>
                        </div>
                    </div>
                </section>
            </div>
        `;
    }

    formatDate(dateStr) {
        // Date formatting helper for Task 1.4
        if (!dateStr) return 'Unknown date';

        try {
            const date = new Date(dateStr);
            const now = new Date();
            const diffDays = Math.floor((now - date) / (1000 * 60 * 60 * 24));

            if (diffDays === 0) return 'Today';
            if (diffDays === 1) return 'Yesterday';
            if (diffDays < 7) return `${diffDays} days ago`;
            if (diffDays < 30) return `${Math.floor(diffDays / 7)} weeks ago`;
            if (diffDays < 365) return `${Math.floor(diffDays / 30)} months ago`;

            return date.toLocaleDateString('en-US', {
                year: 'numeric',
                month: 'short',
                day: 'numeric'
            });
        } catch (error) {
            return dateStr;
        }
    }
}

// Initialize navigation when DOM is ready
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', () => {
        window.navigationController = new NavigationController();
    });
} else {
    window.navigationController = new NavigationController();
}

console.log('✓ Navigation module loaded');
