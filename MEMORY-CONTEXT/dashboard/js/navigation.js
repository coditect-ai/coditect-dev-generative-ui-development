// CODITECT Dashboard - Navigation System
// Handles tab switching, URL routing, sidebar navigation, and search

console.log('✓ Navigation system loading...');

/**
 * Navigation Controller
 * Manages application state, routing, and view rendering
 */
class NavigationController {
    constructor() {
        this.currentView = 'overview';
        this.currentFilter = null;
        this.searchQuery = '';
        this.data = null;

        // View definitions
        this.views = {
            'overview': { title: 'Overview', icon: '📊' },
            'timeline': { title: 'Timeline', icon: '📅' },
            'topics': { title: 'Topics', icon: '🏷️' },
            'files': { title: 'Files', icon: '📁' },
            'checkpoints': { title: 'Sessions', icon: '💬' },
            'commands': { title: 'Commands', icon: '⚡' }
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

        // Mobile menu toggle
        const menuToggle = document.getElementById('menu-toggle');
        if (menuToggle) {
            menuToggle.addEventListener('click', () => this.toggleSidebar());
        }

        // Global search
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

        // Render view
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
            default:
                this.renderOverview();
        }
    }

    renderOverview() {
        const mainContent = document.querySelector('.main-content');

        // Keep existing overview content (generated by Python)
        // Just add interactive elements
        mainContent.innerHTML = `
            <div class="dashboard-overview">
                <section class="quick-stats">
                    <div class="stat-card" onclick="window.location.hash='#checkpoints'">
                        <h3>Total Messages</h3>
                        <p class="stat-value" id="stat-messages">Loading...</p>
                        <p class="stat-label">Click to view all sessions</p>
                    </div>
                    <div class="stat-card" onclick="window.location.hash='#checkpoints'">
                        <h3>Checkpoints</h3>
                        <p class="stat-value" id="stat-checkpoints">Loading...</p>
                        <p class="stat-label">Conversation sessions</p>
                    </div>
                    <div class="stat-card" onclick="window.location.hash='#files'">
                        <h3>Files Referenced</h3>
                        <p class="stat-value" id="stat-files">Loading...</p>
                        <p class="stat-label">Click to browse files</p>
                    </div>
                    <div class="stat-card" onclick="window.location.hash='#commands'">
                        <h3>Commands Executed</h3>
                        <p class="stat-value" id="stat-commands">Loading...</p>
                        <p class="stat-label">Click to view history</p>
                    </div>
                </section>

                <section class="welcome-section">
                    <h2>Welcome to CODITECT Knowledge Base</h2>
                    <p>
                        This dashboard provides interactive access to your entire conversation history.
                        Navigate using the sidebar or use the search bar above.
                    </p>

                    <div class="quick-actions">
                        <h3>Quick Actions</h3>
                        <button onclick="window.location.hash='#timeline'" class="action-btn">
                            📅 View Activity Timeline
                        </button>
                        <button onclick="window.location.hash='#topics'" class="action-btn">
                            🏷️ Browse Topics
                        </button>
                        <button onclick="window.location.hash='#checkpoints'" class="action-btn">
                            💬 View All Sessions
                        </button>
                        <button onclick="document.getElementById('global-search').focus()" class="action-btn">
                            🔍 Search Messages
                        </button>
                    </div>
                </section>

                <section class="recent-activity">
                    <h2>Recent Sessions</h2>
                    <div id="recent-sessions-list">Loading recent sessions...</div>
                </section>

                <section class="top-topics-section">
                    <h2>Top Topics</h2>
                    <div id="top-topics-list">Loading topics...</div>
                </section>
            </div>
        `;

        // Load and display stats
        this.loadOverviewData();
    }

    async loadOverviewData() {
        try {
            // Load stats from JSON files
            const [messages, topics, checkpoints, commands] = await Promise.all([
                fetch('data/messages.json').then(r => r.json()),
                fetch('data/topics.json').then(r => r.json()),
                fetch('data/checkpoints.json').then(r => r.json()),
                fetch('data/commands.json').then(r => r.json())
            ]);

            // Update stats
            document.getElementById('stat-messages').textContent =
                messages.total_messages.toLocaleString();
            document.getElementById('stat-checkpoints').textContent =
                checkpoints.checkpoints.length.toLocaleString();
            document.getElementById('stat-files').textContent =
                '4,060'; // From export summary
            document.getElementById('stat-commands').textContent =
                commands.commands.length.toLocaleString();

            // Render recent sessions (top 5)
            this.renderRecentSessions(checkpoints.checkpoints.slice(0, 5));

            // Render top topics (top 6)
            this.renderTopTopics(topics.topics.slice(0, 6));

        } catch (error) {
            console.error('Failed to load overview data:', error);
        }
    }

    renderRecentSessions(sessions) {
        const container = document.getElementById('recent-sessions-list');
        if (!container) return;

        container.innerHTML = sessions.map(session => `
            <div class="session-card" onclick="window.location.hash='#checkpoints/${session.id}'">
                <div class="session-header">
                    <h4>${session.title || session.id}</h4>
                    <span class="session-date">${this.formatDate(session.date)}</span>
                </div>
                <div class="session-stats">
                    <span class="stat">💬 ${session.message_count} messages</span>
                    <span class="stat">👤 ${session.user_messages} user</span>
                    <span class="stat">🤖 ${session.assistant_messages} assistant</span>
                </div>
                <div class="session-topics">
                    ${(session.top_topics || []).slice(0, 3).map(topic =>
                        `<span class="tag">${topic.split(':')[1]}</span>`
                    ).join('')}
                </div>
            </div>
        `).join('');
    }

    renderTopTopics(topics) {
        const container = document.getElementById('top-topics-list');
        if (!container) return;

        container.innerHTML = topics.map(topic => `
            <div class="topic-card" onclick="window.location.hash='#topics/${topic.name}'">
                <div class="topic-header">
                    <h4>${topic.display_name}</h4>
                    <span class="topic-count">${topic.message_count} messages</span>
                </div>
                <div class="topic-bar">
                    <div class="topic-bar-fill" style="width: ${topic.percentage}%; background-color: ${topic.color}"></div>
                </div>
                <div class="topic-percentage">${topic.percentage}%</div>
            </div>
        `).join('');
    }

    renderTimeline() {
        const mainContent = document.querySelector('.main-content');
        mainContent.innerHTML = `
            <div class="timeline-view">
                <h2>📅 Activity Timeline</h2>
                <p>Timeline visualization coming in Week 2 (D3.js implementation)</p>
                <div id="timeline-placeholder" style="background: #f5f5f5; padding: 2rem; border-radius: 8px; text-align: center;">
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
                    <p>Topic detail view with filtered messages coming in Task 1.5</p>
                </div>
            `;
        } else {
            // Show all topics
            mainContent.innerHTML = `
                <div class="topics-view">
                    <h2>🏷️ Topics</h2>
                    <div id="topics-grid">Loading topics...</div>
                </div>
            `;

            this.loadTopics();
        }
    }

    async loadTopics() {
        try {
            const response = await fetch('data/topics.json');
            const data = await response.json();

            const container = document.getElementById('topics-grid');
            container.innerHTML = data.topics.map(topic => `
                <div class="topic-card clickable" onclick="window.location.hash='#topics/${topic.name}'">
                    <div class="topic-header">
                        <h3>${topic.display_name}</h3>
                        <span class="badge" style="background-color: ${topic.color}">${topic.category}</span>
                    </div>
                    <div class="topic-stats">
                        <div class="stat-large">${topic.message_count.toLocaleString()}</div>
                        <div class="stat-label">messages (${topic.percentage}%)</div>
                    </div>
                    <div class="topic-files">
                        <strong>Top files:</strong>
                        ${topic.top_files.slice(0, 3).map(f =>
                            `<div class="file-ref">${f.file} (${f.count})</div>`
                        ).join('')}
                    </div>
                </div>
            `).join('');
        } catch (error) {
            console.error('Failed to load topics:', error);
        }
    }

    renderFiles(filter) {
        const mainContent = document.querySelector('.main-content');
        mainContent.innerHTML = `
            <div class="files-view">
                <h2>📁 Files</h2>
                <p>File tree browser coming in Task 2.4 (Day 9)</p>
                <div id="files-placeholder" style="background: #f5f5f5; padding: 2rem; border-radius: 8px;">
                    <h3>File Tree</h3>
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
                    <div id="checkpoint-content">Loading session...</div>
                </div>
            `;

            this.loadCheckpointDetail(id);
        } else {
            // Show all checkpoints
            mainContent.innerHTML = `
                <div class="checkpoints-view">
                    <h2>💬 Conversation Sessions</h2>
                    <div class="filters">
                        <input type="search" id="checkpoint-search" placeholder="Search sessions..." />
                        <select id="checkpoint-sort">
                            <option value="date-desc">Newest First</option>
                            <option value="date-asc">Oldest First</option>
                            <option value="messages-desc">Most Messages</option>
                        </select>
                    </div>
                    <div id="checkpoints-list">Loading sessions...</div>
                </div>
            `;

            this.loadCheckpoints();
        }
    }

    async loadCheckpoints() {
        try {
            const response = await fetch('data/checkpoints.json');
            const data = await response.json();

            const container = document.getElementById('checkpoints-list');
            container.innerHTML = data.checkpoints.map(checkpoint => `
                <div class="checkpoint-card clickable" onclick="window.location.hash='#checkpoints/${checkpoint.id}'">
                    <div class="checkpoint-header">
                        <h3>${checkpoint.title || checkpoint.id}</h3>
                        <span class="checkpoint-date">${this.formatDate(checkpoint.date)}</span>
                    </div>
                    <div class="checkpoint-summary">${checkpoint.summary}</div>
                    <div class="checkpoint-stats">
                        <span class="stat">💬 ${checkpoint.message_count} messages</span>
                        <span class="stat">👤 ${checkpoint.user_messages} user</span>
                        <span class="stat">🤖 ${checkpoint.assistant_messages} assistant</span>
                        <span class="stat">⚡ ${checkpoint.commands_executed} commands</span>
                    </div>
                    <div class="checkpoint-topics">
                        ${(checkpoint.top_topics || []).map(topic =>
                            `<span class="tag">${topic.split(':')[1]}</span>`
                        ).join('')}
                    </div>
                    ${checkpoint.files_modified.length > 0 ? `
                        <div class="checkpoint-files">
                            <strong>Files modified:</strong> ${checkpoint.files_modified.slice(0, 3).join(', ')}
                            ${checkpoint.files_modified.length > 3 ? ` +${checkpoint.files_modified.length - 3} more` : ''}
                        </div>
                    ` : ''}
                </div>
            `).join('');

            // Setup search and sort
            this.setupCheckpointFilters(data.checkpoints);
        } catch (error) {
            console.error('Failed to load checkpoints:', error);
        }
    }

    async loadCheckpointDetail(id) {
        const container = document.getElementById('checkpoint-content');
        container.innerHTML = '<div class="loading">Loading session details...</div>';

        try {
            const response = await fetch('data/checkpoints.json');
            const data = await response.json();
            const checkpoint = data.checkpoints.find(c => c.id === id);

            if (!checkpoint) {
                container.innerHTML = '<div class="error">Session not found</div>';
                return;
            }

            container.innerHTML = `
                <div class="checkpoint-detail">
                    <div class="detail-header">
                        <h3>${checkpoint.title || checkpoint.id}</h3>
                        <div class="detail-meta">
                            <span>📅 ${this.formatDate(checkpoint.date)}</span>
                            <span>💬 ${checkpoint.message_count} messages</span>
                        </div>
                    </div>

                    <div class="detail-summary">
                        <h4>Summary</h4>
                        <p>${checkpoint.summary}</p>
                    </div>

                    <div class="detail-stats-grid">
                        <div class="stat-box">
                            <div class="stat-value">${checkpoint.user_messages}</div>
                            <div class="stat-label">User Messages</div>
                        </div>
                        <div class="stat-box">
                            <div class="stat-value">${checkpoint.assistant_messages}</div>
                            <div class="stat-label">Assistant Messages</div>
                        </div>
                        <div class="stat-box">
                            <div class="stat-value">${checkpoint.commands_executed}</div>
                            <div class="stat-label">Commands</div>
                        </div>
                        <div class="stat-box">
                            <div class="stat-value">${checkpoint.files_modified.length}</div>
                            <div class="stat-label">Files Modified</div>
                        </div>
                    </div>

                    ${checkpoint.top_topics.length > 0 ? `
                        <div class="detail-section">
                            <h4>Topics Discussed</h4>
                            <div class="tags-list">
                                ${checkpoint.top_topics.map(topic =>
                                    `<span class="tag">${topic.split(':')[1]}</span>`
                                ).join('')}
                            </div>
                        </div>
                    ` : ''}

                    ${checkpoint.files_modified.length > 0 ? `
                        <div class="detail-section">
                            <h4>Files Modified</h4>
                            <ul class="files-list">
                                ${checkpoint.files_modified.map(file =>
                                    `<li>${file}</li>`
                                ).join('')}
                            </ul>
                        </div>
                    ` : ''}

                    <div class="detail-actions">
                        <button onclick="alert('Full conversation view coming in Task 1.5')" class="btn-primary">
                            View Full Conversation
                        </button>
                        <button onclick="window.history.back()" class="btn-secondary">
                            Back to Sessions
                        </button>
                    </div>
                </div>
            `;
        } catch (error) {
            console.error('Failed to load checkpoint detail:', error);
            container.innerHTML = '<div class="error">Failed to load session</div>';
        }
    }

    setupCheckpointFilters(checkpoints) {
        const searchInput = document.getElementById('checkpoint-search');
        const sortSelect = document.getElementById('checkpoint-sort');

        if (searchInput) {
            searchInput.addEventListener('input', (e) => {
                this.filterCheckpoints(checkpoints, e.target.value, sortSelect.value);
            });
        }

        if (sortSelect) {
            sortSelect.addEventListener('change', (e) => {
                this.filterCheckpoints(checkpoints, searchInput.value, e.target.value);
            });
        }
    }

    filterCheckpoints(checkpoints, searchTerm, sortBy) {
        let filtered = checkpoints;

        // Filter by search term
        if (searchTerm) {
            const term = searchTerm.toLowerCase();
            filtered = filtered.filter(c =>
                (c.title || '').toLowerCase().includes(term) ||
                c.id.toLowerCase().includes(term) ||
                c.summary.toLowerCase().includes(term)
            );
        }

        // Sort
        filtered = [...filtered].sort((a, b) => {
            switch (sortBy) {
                case 'date-desc':
                    return (b.date || '').localeCompare(a.date || '');
                case 'date-asc':
                    return (a.date || '').localeCompare(b.date || '');
                case 'messages-desc':
                    return b.message_count - a.message_count;
                default:
                    return 0;
            }
        });

        // Re-render
        const container = document.getElementById('checkpoints-list');
        container.innerHTML = filtered.map(checkpoint => `
            <div class="checkpoint-card clickable" onclick="window.location.hash='#checkpoints/${checkpoint.id}'">
                <div class="checkpoint-header">
                    <h3>${checkpoint.title || checkpoint.id}</h3>
                    <span class="checkpoint-date">${this.formatDate(checkpoint.date)}</span>
                </div>
                <div class="checkpoint-summary">${checkpoint.summary}</div>
                <div class="checkpoint-stats">
                    <span class="stat">💬 ${checkpoint.message_count} messages</span>
                    <span class="stat">👤 ${checkpoint.user_messages} user</span>
                    <span class="stat">🤖 ${checkpoint.assistant_messages} assistant</span>
                </div>
            </div>
        `).join('');
    }

    renderCommands(filter) {
        const mainContent = document.querySelector('.main-content');
        mainContent.innerHTML = `
            <div class="commands-view">
                <h2>⚡ Command History</h2>
                <p>Command history browser coming in Task 2.5 (Day 9)</p>
                <div id="commands-placeholder" style="background: #f5f5f5; padding: 2rem; border-radius: 8px;">
                    <h3>Command Table</h3>
                    <p>Sortable table showing all 1,732 executed commands</p>
                    <p>Filter by type (git, bash, python, docker, gcloud)</p>
                </div>
            </div>
        `;
    }

    handleSearch(e) {
        this.searchQuery = e.target.value;
        // Debounced search will be implemented in Task 1.4
        console.log('Search query:', this.searchQuery);
    }

    executeSearch() {
        if (!this.searchQuery) return;

        console.log('Executing search:', this.searchQuery);
        alert(`Full-text search coming in Task 1.4\nQuery: "${this.searchQuery}"`);
    }

    toggleSidebar() {
        const sidebar = document.querySelector('.sidebar');
        if (sidebar) {
            sidebar.classList.toggle('collapsed');
        }
    }

    closeModals() {
        // Close any open modals (to be implemented)
        console.log('Closing modals...');
    }

    formatDate(dateStr) {
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
        window.nav = new NavigationController();
    });
} else {
    window.nav = new NavigationController();
}

console.log('✓ Navigation system loaded');
