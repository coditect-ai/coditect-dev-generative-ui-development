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
            default:
                this.renderOverview();
        }
    }

    renderOverview() {
        const mainContent = document.querySelector('.main-content');

        mainContent.innerHTML = `
            <div class="dashboard-overview">
                <section class="quick-stats">
                    <div class="stat-card clickable" onclick="window.location.hash='#checkpoints'">
                        <h3>Total Messages</h3>
                        <p class="stat-value">10,206</p>
                        <p class="stat-label">Click to view all sessions</p>
                    </div>
                    <div class="stat-card clickable" onclick="window.location.hash='#checkpoints'">
                        <h3>Checkpoints</h3>
                        <p class="stat-value">124</p>
                        <p class="stat-label">Conversation sessions</p>
                    </div>
                    <div class="stat-card clickable" onclick="window.location.hash='#files'">
                        <h3>Files Referenced</h3>
                        <p class="stat-value">4,060</p>
                        <p class="stat-label">Click to browse files</p>
                    </div>
                    <div class="stat-card clickable" onclick="window.location.hash='#commands'">
                        <h3>Commands Executed</h3>
                        <p class="stat-value">1,732</p>
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
                    <div id="recent-sessions-list" style="padding: 2rem; background: #f9f9f9; border-radius: 8px; text-align: center;">
                        <p><strong>Task 1.4: Data Loading</strong></p>
                        <p>Dynamic data loading will be implemented next</p>
                        <p>This will fetch and display the 5 most recent sessions</p>
                    </div>
                </section>

                <section class="top-topics-section">
                    <h2>Top Topics</h2>
                    <div id="top-topics-list" style="padding: 2rem; background: #f9f9f9; border-radius: 8px; text-align: center;">
                        <p><strong>Task 1.4: Data Loading</strong></p>
                        <p>Dynamic data loading will be implemented next</p>
                        <p>This will display top 6 topics with progress bars</p>
                    </div>
                </section>
            </div>
        `;
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
