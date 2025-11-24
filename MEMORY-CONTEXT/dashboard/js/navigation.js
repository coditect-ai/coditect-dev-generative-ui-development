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
            'search': { title: 'Search Results', icon: '🔍' },
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

        // Modal setup
        this.setupModal();

        // Escape key to close modals/filters
        document.addEventListener('keydown', (e) => {
            if (e.key === 'Escape') {
                this.closeModals();
            }
        });
    }

    setupModal() {
        const modal = document.getElementById('file-modal');
        if (!modal) return;

        const closeBtn = document.getElementById('modal-close');
        const overlay = modal.querySelector('.modal-overlay');

        // Close on X button
        if (closeBtn) {
            closeBtn.addEventListener('click', () => this.closeModal());
        }

        // Close on overlay click
        if (overlay) {
            overlay.addEventListener('click', () => this.closeModal());
        }
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

        // Parse hash: #view or #view/id or #view/filter/id
        const parts = hash.split('/');
        const view = parts[0];

        // For checkpoints, second part is the ID (not a filter)
        let filter = null;
        let id = null;

        if (view === 'checkpoints' && parts[1]) {
            id = decodeURIComponent(parts[1]);
        } else {
            filter = parts[1] ? decodeURIComponent(parts[1]) : null;
            id = parts[2] ? decodeURIComponent(parts[2]) : null;
        }

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
            case 'search':
                this.renderSearch(filter);
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

    async renderTimeline() {
        const mainContent = document.querySelector('.main-content');
        mainContent.innerHTML = '<div class="loading">Loading timeline data...</div>';

        try {
            const checkpoints = await window.dashboardData.loadCheckpoints();

            // Extract date from checkpoint ID using regex
            const extractDateFromId = (id) => {
                // Pattern 1: 2025-11-17T20:08:18Z (ISO timestamp)
                const isoMatch = id.match(/(\d{4}-\d{2}-\d{2}T[\d:]+Z)/);
                if (isoMatch) {
                    return new Date(isoMatch[1]);
                }

                // Pattern 2: 2025-11-17 (date only)
                // Use noon UTC to avoid timezone issues causing date to shift
                const dateMatch = id.match(/(\d{4}-\d{2}-\d{2})/);
                if (dateMatch) {
                    return new Date(dateMatch[1] + 'T12:00:00Z');
                }

                // Fallback to current date if no pattern found
                return new Date();
            };

            // Parse dates and sort chronologically
            const timelineData = checkpoints
                .map(c => ({
                    ...c,
                    date: extractDateFromId(c.id),
                    messageCount: c.message_count || 0
                }))
                .filter(c => !isNaN(c.date.getTime()))
                .sort((a, b) => a.date - b.date);

            if (timelineData.length === 0) {
                mainContent.innerHTML = '<div class="card"><p>No timeline data available</p></div>';
                return;
            }

            mainContent.innerHTML = `
                <div class="timeline-view">
                    <div class="section-header">
                        <h1>📅 Activity Timeline</h1>
                        <p class="text-secondary">${timelineData.length} sessions from ${this.formatDate(timelineData[0].date)} to ${this.formatDate(timelineData[timelineData.length - 1].date)}</p>
                    </div>

                    <div class="card" style="margin-bottom: var(--space-6);">
                        <div class="card-content">
                            <div class="flex gap-4" style="flex-wrap: wrap; margin-bottom: var(--space-4);">
                                <div>
                                    <label for="timeline-filter-topic" style="display: block; font-weight: 600; margin-bottom: var(--space-2); color: var(--text-primary);">Filter by Topic:</label>
                                    <select id="timeline-filter-topic" class="form-control" style="min-width: 200px;">
                                        <option value="">All Topics</option>
                                    </select>
                                </div>
                                <div>
                                    <label for="timeline-filter-range" style="display: block; font-weight: 600; margin-bottom: var(--space-2); color: var(--text-primary);">Date Range:</label>
                                    <select id="timeline-filter-range" class="form-control" style="min-width: 200px;">
                                        <option value="all">All Time</option>
                                        <option value="7">Last 7 Days</option>
                                        <option value="30">Last 30 Days</option>
                                        <option value="90">Last 90 Days</option>
                                        <option value="365">Last Year</option>
                                    </select>
                                </div>
                                <div style="display: flex; align-items: flex-end;">
                                    <button id="timeline-reset-btn" class="btn btn-secondary">Reset Filters</button>
                                </div>
                            </div>
                            <div class="flex gap-2" style="margin-bottom: var(--space-4);">
                                <button id="timeline-nav-left" class="btn btn-primary" style="padding: var(--space-2) var(--space-4);">
                                    ◄ Previous
                                </button>
                                <button id="timeline-nav-today" class="btn btn-secondary" style="padding: var(--space-2) var(--space-4);">
                                    Today
                                </button>
                                <button id="timeline-nav-right" class="btn btn-primary" style="padding: var(--space-2) var(--space-4);">
                                    Next ►
                                </button>
                                <div style="flex: 1;"></div>
                                <div>
                                    <label for="timeline-zoom-level" style="display: block; font-weight: 600; margin-bottom: var(--space-2); color: var(--text-primary);">Zoom Level:</label>
                                    <select id="timeline-zoom-level" class="form-control" style="min-width: 150px;">
                                        <option value="month">Monthly View</option>
                                        <option value="week">Weekly View</option>
                                        <option value="day">Daily View</option>
                                    </select>
                                </div>
                            </div>
                            <div id="timeline-period-info" style="padding: var(--space-2); background: var(--primary-100); border-radius: var(--radius-sm); font-size: var(--text-sm); margin-bottom: var(--space-4); font-weight: 600; color: var(--primary-900);"></div>
                            <div style="padding: var(--space-2); background: var(--bg-tertiary); border-radius: var(--radius-sm); font-size: var(--text-sm);">
                                <strong>💡 Tips:</strong> Click sessions for full details • Use arrows to navigate periods • Change zoom level for more separation • Scroll to zoom • Drag to pan
                            </div>
                        </div>
                    </div>

                    <div class="card">
                        <div id="timeline-chart"></div>
                    </div>

                    <div id="timeline-detail-panel" class="card" style="position: fixed; display: none; z-index: 2000; max-width: 800px; max-height: 80vh; overflow-y: auto; box-shadow: var(--shadow-2xl);">
                        <div class="card-header drag-handle" style="display: flex; justify-content: space-between; align-items: center; cursor: move; user-select: none;">
                            <h3 class="card-title" id="timeline-detail-title" style="cursor: move;">📋 Session Details (drag to move)</h3>
                            <button onclick="document.getElementById('timeline-detail-panel').style.display='none'" class="btn btn-sm btn-secondary" style="cursor: pointer;">✕ Close</button>
                        </div>
                        <div class="card-content" id="timeline-detail-content"></div>
                    </div>

                    <div id="timeline-legend" class="card" style="margin-top: var(--space-4);">
                        <div class="card-header">
                            <h3 class="card-title">Legend</h3>
                        </div>
                        <div class="card-content">
                            <div class="flex gap-4" style="flex-wrap: wrap;">
                                <div class="flex items-center gap-2">
                                    <div style="width: 12px; height: 12px; border-radius: 50%; background: var(--primary-500);"></div>
                                    <span>1-50 messages</span>
                                </div>
                                <div class="flex items-center gap-2">
                                    <div style="width: 18px; height: 18px; border-radius: 50%; background: var(--primary-500);"></div>
                                    <span>51-200 messages</span>
                                </div>
                                <div class="flex items-center gap-2">
                                    <div style="width: 24px; height: 24px; border-radius: 50%; background: var(--primary-500);"></div>
                                    <span>201-500 messages</span>
                                </div>
                                <div class="flex items-center gap-2">
                                    <div style="width: 30px; height: 30px; border-radius: 50%; background: var(--primary-500);"></div>
                                    <span>501+ messages</span>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            `;

            // Initialize enhanced D3 timeline
            window.initD3TimelineEnhanced(timelineData, this);

        } catch (error) {
            console.error('Failed to load timeline:', error);
            mainContent.innerHTML = `
                <div class="card">
                    <div class="card-content">
                        <h3 style="color: var(--error-500);">❌ Failed to Load Timeline</h3>
                        <p>${this.escapeHtml(error.message)}</p>
                    </div>
                </div>
            `;
        }
    }

    initD3Timeline(data) {
        // Chart dimensions
        const margin = { top: 40, right: 40, bottom: 60, left: 60 };
        const width = Math.min(1200, document.getElementById('timeline-chart').clientWidth) - margin.left - margin.right;
        const height = 500 - margin.top - margin.bottom;

        // Clear any existing chart
        d3.select('#timeline-chart').selectAll('*').remove();

        // Create SVG
        const svg = d3.select('#timeline-chart')
            .append('svg')
            .attr('width', width + margin.left + margin.right)
            .attr('height', height + margin.top + margin.bottom)
            .append('g')
            .attr('transform', `translate(${margin.left},${margin.top})`);

        // Scales
        const xScale = d3.scaleTime()
            .domain(d3.extent(data, d => d.date))
            .range([0, width]);

        const yScale = d3.scaleLinear()
            .domain([0, d3.max(data, d => d.messageCount)])
            .range([height, 0]);

        const sizeScale = d3.scaleSqrt()
            .domain([0, d3.max(data, d => d.messageCount)])
            .range([6, 30]);

        // Axes
        const xAxis = d3.axisBottom(xScale)
            .ticks(10)
            .tickFormat(d3.timeFormat('%b %d, %Y'));

        const yAxis = d3.axisLeft(yScale)
            .ticks(5)
            .tickFormat(d => d.toLocaleString());

        svg.append('g')
            .attr('class', 'x-axis')
            .attr('transform', `translate(0,${height})`)
            .call(xAxis)
            .selectAll('text')
            .attr('transform', 'rotate(-45)')
            .style('text-anchor', 'end')
            .style('font-size', '12px')
            .style('fill', 'var(--text-secondary)');

        svg.append('g')
            .attr('class', 'y-axis')
            .call(yAxis)
            .selectAll('text')
            .style('font-size', '12px')
            .style('fill', 'var(--text-secondary)');

        // Axis labels
        svg.append('text')
            .attr('transform', `translate(${width / 2},${height + margin.bottom - 10})`)
            .style('text-anchor', 'middle')
            .style('font-size', '14px')
            .style('font-weight', '600')
            .style('fill', 'var(--text-primary)')
            .text('Date');

        svg.append('text')
            .attr('transform', 'rotate(-90)')
            .attr('y', 0 - margin.left)
            .attr('x', 0 - (height / 2))
            .attr('dy', '1em')
            .style('text-anchor', 'middle')
            .style('font-size', '14px')
            .style('font-weight', '600')
            .style('fill', 'var(--text-primary)')
            .text('Messages per Session');

        // Tooltip
        const tooltip = d3.select('body')
            .append('div')
            .attr('class', 'timeline-tooltip')
            .style('position', 'absolute')
            .style('visibility', 'hidden')
            .style('background', 'var(--bg-primary)')
            .style('border', '1px solid var(--border-primary)')
            .style('border-radius', 'var(--radius-md)')
            .style('padding', 'var(--space-3)')
            .style('box-shadow', 'var(--shadow-lg)')
            .style('pointer-events', 'none')
            .style('z-index', '1000')
            .style('font-size', '14px')
            .style('max-width', '300px');

        // Plot sessions as circles
        svg.selectAll('.session-dot')
            .data(data)
            .enter()
            .append('circle')
            .attr('class', 'session-dot')
            .attr('cx', d => xScale(d.date))
            .attr('cy', d => yScale(d.messageCount))
            .attr('r', d => sizeScale(d.messageCount))
            .style('fill', 'var(--primary-500)')
            .style('opacity', 0.7)
            .style('stroke', 'var(--primary-700)')
            .style('stroke-width', '2px')
            .style('cursor', 'pointer')
            .on('mouseover', function(event, d) {
                d3.select(this)
                    .transition()
                    .duration(200)
                    .style('opacity', 1)
                    .attr('r', sizeScale(d.messageCount) * 1.2);

                tooltip
                    .style('visibility', 'visible')
                    .html(`
                        <div style="color: var(--text-primary);">
                            <strong style="display: block; margin-bottom: 8px; font-size: 15px;">${d.title || d.id}</strong>
                            <div style="font-size: 13px; color: var(--text-secondary);">
                                <div style="margin-bottom: 4px;"><strong>Date:</strong> ${d.date.toLocaleDateString()}</div>
                                <div style="margin-bottom: 4px;"><strong>Messages:</strong> ${d.messageCount.toLocaleString()}</div>
                                <div style="margin-bottom: 4px;"><strong>Topics:</strong> ${(d.top_topics || []).slice(0, 3).join(', ') || 'None'}</div>
                                <div style="margin-top: 8px; padding-top: 8px; border-top: 1px solid var(--border-primary); font-size: 12px; color: var(--primary-500);">
                                    Click to view session details →
                                </div>
                            </div>
                        </div>
                    `);
            })
            .on('mousemove', function(event) {
                tooltip
                    .style('top', (event.pageY - 10) + 'px')
                    .style('left', (event.pageX + 10) + 'px');
            })
            .on('mouseout', function(event, d) {
                d3.select(this)
                    .transition()
                    .duration(200)
                    .style('opacity', 0.7)
                    .attr('r', sizeScale(d.messageCount));

                tooltip.style('visibility', 'hidden');
            })
            .on('click', function(event, d) {
                window.location.hash = `#checkpoints/${d.id}`;
            });

        // Zoom behavior
        const zoom = d3.zoom()
            .scaleExtent([0.5, 10])
            .on('zoom', (event) => {
                const newXScale = event.transform.rescaleX(xScale);

                svg.select('.x-axis').call(xAxis.scale(newXScale));

                svg.selectAll('.session-dot')
                    .attr('cx', d => newXScale(d.date));
            });

        d3.select('#timeline-chart svg').call(zoom);

        // Filter handlers
        document.getElementById('timeline-filter-range').addEventListener('change', (e) => {
            this.filterTimeline(data, e.target.value, document.getElementById('timeline-filter-topic').value);
        });

        document.getElementById('timeline-reset-btn').addEventListener('click', () => {
            document.getElementById('timeline-filter-range').value = 'all';
            document.getElementById('timeline-filter-topic').value = '';
            this.initD3Timeline(data);
        });

        // Populate topics filter
        const allTopics = new Set();
        data.forEach(d => {
            if (d.top_topics) {
                d.top_topics.forEach(t => allTopics.add(t));
            }
        });

        const topicSelect = document.getElementById('timeline-filter-topic');
        Array.from(allTopics).sort().forEach(topic => {
            const option = document.createElement('option');
            option.value = topic;
            option.textContent = topic;
            topicSelect.appendChild(option);
        });

        topicSelect.addEventListener('change', (e) => {
            this.filterTimeline(data, document.getElementById('timeline-filter-range').value, e.target.value);
        });
    }

    filterTimeline(allData, dateRange, topic) {
        let filtered = [...allData];

        // Filter by date range
        if (dateRange !== 'all') {
            const days = parseInt(dateRange);
            const cutoffDate = new Date();
            cutoffDate.setDate(cutoffDate.getDate() - days);
            filtered = filtered.filter(d => d.date >= cutoffDate);
        }

        // Filter by topic
        if (topic) {
            filtered = filtered.filter(d => d.top_topics && d.top_topics.includes(topic));
        }

        // Re-render with filtered data
        this.initD3Timeline(filtered);
    }

    async renderTopics(filter) {
        const mainContent = document.querySelector('.main-content');

        if (filter) {
            // Show specific topic with messages
            mainContent.innerHTML = '<div class="loading">Loading messages for topic...</div>';

            try {
                // Load messages for this topic
                const messages = await window.dashboardData.loadMessagesByTopic(filter);

                // Get topic info
                const topics = await window.dashboardData.loadTopics();
                const topicInfo = topics.find(t => t.name === filter);

                mainContent.innerHTML = `
                    <div class="topic-detail-view">
                        <button onclick="window.location.hash='#topics'" class="btn-secondary" style="margin-bottom: var(--space-4);">
                            ← Back to All Topics
                        </button>

                        <div class="card">
                            <div class="card-header">
                                <h2 class="card-title">${this.escapeHtml(topicInfo ? topicInfo.display_name : filter)}</h2>
                                <p class="card-subtitle">${messages.length} messages • ${topicInfo ? topicInfo.percentage + '% of all messages' : ''}</p>
                            </div>
                            <div class="card-content">
                                ${topicInfo ? `
                                    <div class="grid grid-cols-4" style="margin-bottom: var(--space-6);">
                                        <div class="stat-card">
                                            <h4>Messages</h4>
                                            <p class="stat-value">${topicInfo.message_count.toLocaleString()}</p>
                                        </div>
                                        <div class="stat-card">
                                            <h4>Percentage</h4>
                                            <p class="stat-value">${topicInfo.percentage}%</p>
                                        </div>
                                        <div class="stat-card">
                                            <h4>Category</h4>
                                            <p class="stat-value" style="font-size: var(--text-base);">${topicInfo.category}</p>
                                        </div>
                                        <div class="stat-card">
                                            <h4>Color</h4>
                                            <div style="width: 40px; height: 40px; background-color: ${topicInfo.color}; border-radius: var(--radius-full); margin: var(--space-2) auto;"></div>
                                        </div>
                                    </div>
                                ` : ''}

                                <h3 style="margin-top: var(--space-6); margin-bottom: var(--space-4);">Messages (${messages.length})</h3>
                                <div class="grid grid-cols-1" style="gap: var(--space-4);">
                                    ${messages.slice(0, 50).map(msg => `
                                        <div class="card" style="background: var(--bg-tertiary);">
                                            <div class="card-header">
                                                <div style="display: flex; justify-content: space-between; align-items: start;">
                                                    <div>
                                                        <span class="badge badge-${msg.role === 'user' ? 'primary' : 'secondary'}" style="margin-right: var(--space-2);">
                                                            ${msg.role}
                                                        </span>
                                                        ${msg.has_code ? '<span class="badge" style="background: var(--success-500); color: white;">📝 Code</span>' : ''}
                                                    </div>
                                                    <span style="color: var(--text-tertiary); font-size: var(--text-xs);">
                                                        ${new Date(msg.first_seen).toLocaleDateString()}
                                                    </span>
                                                </div>
                                            </div>
                                            <div class="card-content">
                                                <p style="font-family: var(--font-mono); font-size: var(--text-sm); color: var(--text-secondary); white-space: pre-wrap;">
                                                    ${this.escapeHtml(msg.content_preview)}
                                                </p>
                                                <div style="margin-top: var(--space-4); padding-top: var(--space-4); border-top: 1px solid var(--border-primary); display: flex; justify-content: space-between; font-size: var(--text-xs); color: var(--text-tertiary);">
                                                    <span>Words: ${msg.word_count}</span>
                                                    <span>Session: ${this.escapeHtml(msg.checkpoint_id.substring(0, 40))}...</span>
                                                </div>
                                            </div>
                                        </div>
                                    `).join('')}
                                </div>

                                ${messages.length > 50 ? `
                                    <div style="text-align: center; margin-top: var(--space-6); padding: var(--space-4); background: var(--bg-tertiary); border-radius: var(--radius-md);">
                                        <p style="color: var(--text-secondary);">
                                            Showing first 50 of ${messages.length} messages
                                        </p>
                                        <p style="color: var(--text-tertiary); font-size: var(--text-sm); margin-top: var(--space-2);">
                                            Full pagination coming soon
                                        </p>
                                    </div>
                                ` : ''}
                            </div>
                        </div>
                    </div>
                `;
            } catch (error) {
                mainContent.innerHTML = `
                    <div class="card">
                        <div class="card-header">
                            <h2 class="card-title" style="color: var(--error-500);">Failed to Load Topic</h2>
                        </div>
                        <div class="card-content">
                            <p>Error: ${error.message}</p>
                            <button onclick="window.location.hash='#topics'" class="btn-primary" style="margin-top: var(--space-4);">
                                Back to All Topics
                            </button>
                        </div>
                    </div>
                `;
            }
        } else {
            // Show all topics
            mainContent.innerHTML = '<div class="loading">Loading topics...</div>';

            try {
                const topics = await window.dashboardData.loadTopics();

                mainContent.innerHTML = `
                    <div class="topics-view">
                        <h2>🏷️ Topics (${topics.length} total)</h2>

                        <div class="grid grid-cols-3" style="gap: var(--space-4); margin-top: var(--space-6);">
                            ${topics.map(topic => `
                                <div class="card clickable" onclick="window.location.hash='#topics/${encodeURIComponent(topic.name)}'" style="cursor: pointer;">
                                    <div class="card-header">
                                        <h3 class="card-title">${this.escapeHtml(topic.display_name || topic.name)}</h3>
                                        <div class="badge" style="background-color: ${topic.color}; color: white;">
                                            ${topic.category}
                                        </div>
                                    </div>
                                    <div class="card-content">
                                        <p style="font-size: var(--text-3xl); font-weight: var(--font-bold); color: var(--primary-500); text-align: center; margin: var(--space-4) 0;">
                                            ${topic.message_count.toLocaleString()}
                                        </p>
                                        <p style="text-align: center; color: var(--text-tertiary);">
                                            ${topic.percentage}% of all messages
                                        </p>
                                        ${topic.top_files && topic.top_files.length > 0 ? `
                                            <div style="margin-top: var(--space-4); padding-top: var(--space-4); border-top: 1px solid var(--border-primary);">
                                                <p style="font-size: var(--text-sm); font-weight: var(--font-semibold); margin-bottom: var(--space-2);">Top Files:</p>
                                                ${topic.top_files.slice(0, 3).map(f => `
                                                    <div style="font-size: var(--text-xs); color: var(--text-secondary); font-family: monospace; margin: var(--space-1) 0;">
                                                        ${this.escapeHtml(f.file)} (${f.count})
                                                    </div>
                                                `).join('')}
                                            </div>
                                        ` : ''}
                                    </div>
                                </div>
                            `).join('')}
                        </div>
                    </div>
                `;
            } catch (error) {
                mainContent.innerHTML = `
                    <div class="card">
                        <div class="card-header">
                            <h2 class="card-title" style="color: var(--error-500);">Failed to Load Topics</h2>
                        </div>
                        <div class="card-content">
                            <p>Error: ${error.message}</p>
                        </div>
                    </div>
                `;
            }
        }
    }

    async renderFiles(filter) {
        const mainContent = document.querySelector('.main-content');
        mainContent.innerHTML = '<div class="loading">Loading files...</div>';

        try {
            const filesData = await window.dashboardData.loadFiles();

            // Transform and calculate statistics from the actual data structure
            // The JSON has: files array with filepath, reference_count, file_type, etc.
            // And a pre-built file_tree object

            // Filter out invalid entries (URLs, malformed paths, etc.)
            const validFiles = (filesData.files || []).filter(file => {
                return file &&
                       file.filepath &&
                       typeof file.filepath === 'string' &&
                       !file.filepath.startsWith('//') &&  // Skip URLs
                       !file.filepath.startsWith('http') && // Skip HTTP URLs
                       file.filepath.length > 0;
            });

            // Calculate summary statistics
            const totalReferences = validFiles.reduce((sum, f) => sum + (f.reference_count || 0), 0);
            const uniqueFiles = validFiles.length;

            // Get unique file types
            const fileTypes = [...new Set(validFiles.map(f => f.file_type).filter(Boolean))];

            // Sort by reference_count descending for top files
            const topFiles = [...validFiles]
                .sort((a, b) => (b.reference_count || 0) - (a.reference_count || 0))
                .slice(0, 20)
                .map(f => ({
                    path: f.filepath,
                    count: f.reference_count || 0,
                    file_type: f.file_type
                }));

            console.log('📁 Files data loaded:', {
                totalReferences,
                uniqueFiles,
                fileTypesCount: fileTypes.length,
                topFilesLength: topFiles.length,
                hasFileTree: !!filesData.file_tree,
                filter: filter
            });

            // If filter is set, show file detail view
            if (filter) {
                await this.renderFileDetail(filter, filesData);
                return;
            }

            // Use the pre-built file tree if available, otherwise build from files
            const tree = filesData.file_tree || this.buildFileTree(validFiles);

            mainContent.innerHTML = `
                <div class="files-view">
                    <div class="section-header">
                        <h1>📁 Files & Code References</h1>
                        <p class="text-secondary">
                            ${totalReferences.toLocaleString()} file references across ${uniqueFiles.toLocaleString()} unique files
                        </p>
                    </div>

                    <div class="card" style="margin-bottom: var(--space-4);">
                        <div class="grid grid-cols-4">
                            <div class="stat-card">
                                <h4>Total References</h4>
                                <p class="stat-value">${totalReferences.toLocaleString()}</p>
                            </div>
                            <div class="stat-card">
                                <h4>Unique Files</h4>
                                <p class="stat-value">${uniqueFiles.toLocaleString()}</p>
                            </div>
                            <div class="stat-card">
                                <h4>Most Referenced</h4>
                                <p class="stat-value">${topFiles[0]?.count || 0}×</p>
                                <p class="text-xs" style="margin-top: var(--space-1);">${this.getFileName(topFiles[0]?.path || '')}</p>
                            </div>
                            <div class="stat-card">
                                <h4>File Types</h4>
                                <p class="stat-value">${fileTypes.length}</p>
                            </div>
                        </div>
                    </div>

                    <div class="card">
                        <h3 style="margin-bottom: var(--space-4);">Top Referenced Files</h3>
                        <div style="display: grid; gap: var(--space-2);">
                            ${topFiles.slice(0, 10).map(file => `
                                <a href="#files/${encodeURIComponent(file.path)}" class="file-item" style="display: flex; justify-content: space-between; align-items: center; padding: var(--space-3); background: var(--bg-secondary); border-radius: var(--radius-md); transition: all var(--transition-fast); text-decoration: none; color: inherit;">
                                    <div style="flex: 1; min-width: 0;">
                                        <div style="display: flex; align-items: center; gap: var(--space-2);">
                                            <span style="font-size: 1.2em;">${this.getFileIcon(file.path)}</span>
                                            <code style="font-size: var(--text-sm); color: var(--text-primary); word-break: break-all;">${this.escapeHtml(file.path)}</code>
                                        </div>
                                    </div>
                                    <span class="badge" style="margin-left: var(--space-3); white-space: nowrap;">
                                        ${file.count} reference${file.count > 1 ? 's' : ''}
                                    </span>
                                </a>
                            `).join('')}
                        </div>
                    </div>

                    <div class="card" style="margin-top: var(--space-6);">
                        <h3 style="margin-bottom: var(--space-4);">File Tree Browser</h3>
                        <div class="file-tree">
                            ${this.renderFileTree(tree, '')}
                        </div>
                    </div>
                </div>
            `;

            // Add click handlers for collapsible folders
            this.attachFileTreeHandlers();

        } catch (error) {
            console.error('Failed to load files:', error);
            mainContent.innerHTML = `
                <div class="card">
                    <div class="card-header">
                        <h2 class="card-title" style="color: var(--error-500);">Failed to Load Files</h2>
                    </div>
                    <div class="card-content">
                        <p>Error: ${error.message}</p>
                    </div>
                </div>
            `;
        }
    }

    buildFileTree(files) {
        const tree = {};

        if (!files || !Array.isArray(files)) {
            console.warn('buildFileTree: files is not an array', files);
            return tree;
        }

        files.forEach(file => {
            // Support both 'path' (transformed) and 'filepath' (raw JSON) fields
            const filePath = file.path || file.filepath;

            // Skip invalid entries
            if (!file || !filePath || typeof filePath !== 'string') {
                console.warn('buildFileTree: skipping invalid file entry', file);
                return;
            }

            const parts = filePath.split('/');
            let current = tree;

            parts.forEach((part, index) => {
                if (!current[part]) {
                    current[part] = {
                        name: part,
                        path: parts.slice(0, index + 1).join('/'),
                        isFile: index === parts.length - 1,
                        count: 0,
                        children: {}
                    };
                }

                if (index === parts.length - 1) {
                    current[part].count = file.count || file.reference_count || 0;
                }

                current = current[part].children;
            });
        });

        return tree;
    }

    renderFileTree(tree, indent = '', currentPath = '') {
        if (!tree || typeof tree !== 'object') {
            return '';
        }

        const entries = Object.entries(tree).map(([name, data]) => {
            // Handle both pre-built tree structure (type: "file"|"directory")
            // and custom built tree structure (isFile: boolean, children: {})
            const isFile = data.type === 'file' || data.isFile === true;
            const path = currentPath ? `${currentPath}/${name}` : name;

            // Get children - either from 'children' property or from all properties except special ones
            let children = {};
            if (data.children && typeof data.children === 'object') {
                children = data.children;
            } else if (!isFile) {
                // For pre-built tree, children are stored as direct properties
                children = Object.fromEntries(
                    Object.entries(data).filter(([key]) =>
                        key !== 'type' && key !== 'count' && key !== 'name' && key !== 'path'
                    )
                );
            }

            return {
                name,
                path,
                isFile,
                count: data.count || 0,
                children
            };
        });

        // Sort: folders first, then files, alphabetically
        entries.sort((a, b) => {
            if (a.isFile !== b.isFile) {
                return a.isFile ? 1 : -1;
            }
            return a.name.localeCompare(b.name);
        });

        return entries.map(entry => {
            const hasChildren = Object.keys(entry.children).length > 0;
            const icon = entry.isFile ? this.getFileIcon(entry.path) : '📁';

            if (entry.isFile) {
                return `
                    <a href="#files/${encodeURIComponent(entry.path)}" class="file-tree-item file-tree-file" style="padding-left: ${indent}px; text-decoration: none; color: inherit; display: flex;">
                        <span class="file-tree-icon">${icon}</span>
                        <span class="file-tree-name">${this.escapeHtml(entry.name)}</span>
                        ${entry.count > 0 ? `<span class="badge badge-sm">${entry.count}</span>` : ''}
                    </a>
                `;
            } else {
                return `
                    <div class="file-tree-folder" data-path="${this.escapeHtml(entry.path)}">
                        <div class="file-tree-item file-tree-folder-header" style="padding-left: ${indent}px;">
                            <span class="file-tree-collapse-icon">▶</span>
                            <span class="file-tree-icon">${icon}</span>
                            <span class="file-tree-name">${this.escapeHtml(entry.name)}</span>
                            ${hasChildren ? `<span class="badge badge-sm">${Object.keys(entry.children).length}</span>` : ''}
                        </div>
                        <div class="file-tree-children collapsed">
                            ${this.renderFileTree(entry.children, indent + 20, entry.path)}
                        </div>
                    </div>
                `;
            }
        }).join('');
    }

    attachFileTreeHandlers() {
        const folders = document.querySelectorAll('.file-tree-folder-header');
        folders.forEach(folder => {
            folder.addEventListener('click', (e) => {
                e.stopPropagation();
                const parent = folder.parentElement;
                const children = parent.querySelector('.file-tree-children');
                const icon = folder.querySelector('.file-tree-collapse-icon');

                if (children.classList.contains('collapsed')) {
                    children.classList.remove('collapsed');
                    icon.textContent = '▼';
                } else {
                    children.classList.add('collapsed');
                    icon.textContent = '▶';
                }
            });
        });
    }

    getFileIcon(path) {
        const ext = path.split('.').pop().toLowerCase();
        const iconMap = {
            'js': '📜',
            'ts': '📘',
            'tsx': '⚛️',
            'jsx': '⚛️',
            'py': '🐍',
            'rs': '🦀',
            'go': '🔷',
            'java': '☕',
            'cpp': '⚙️',
            'c': '⚙️',
            'h': '📋',
            'json': '📋',
            'yaml': '📋',
            'yml': '📋',
            'md': '📝',
            'txt': '📄',
            'html': '🌐',
            'css': '🎨',
            'scss': '🎨',
            'sql': '🗄️',
            'sh': '🔧',
            'bash': '🔧',
            'dockerfile': '🐳',
            'xml': '📰',
            'svg': '🖼️',
            'png': '🖼️',
            'jpg': '🖼️',
            'gif': '🖼️',
            'pdf': '📕'
        };
        return iconMap[ext] || '📄';
    }

    getFileName(path) {
        return path.split('/').pop();
    }

    async renderFileDetail(filePath, filesData) {
        const mainContent = document.querySelector('.main-content');
        mainContent.innerHTML = '<div class="loading">Loading file details...</div>';

        try {
            // Find the file in the data
            const fileInfo = filesData.files?.find(f => f.path === filePath) ||
                           filesData.top_files?.find(f => f.path === filePath);

            if (!fileInfo) {
                mainContent.innerHTML = `
                    <div class="card">
                        <h2 style="color: var(--error-500);">File Not Found</h2>
                        <p>Could not find information for: <code>${this.escapeHtml(filePath)}</code></p>
                        <button onclick="window.location.hash='#files'" class="btn-secondary">
                            ← Back to Files
                        </button>
                    </div>
                `;
                return;
            }

            // Search for messages that reference this file
            const references = await this.findFileReferences(filePath);

            // Try to load the actual file content
            const fileContent = await this.loadFileContent(filePath);

            mainContent.innerHTML = `
                <div class="file-detail-view">
                    <button onclick="window.location.hash='#files'" class="btn-secondary" style="margin-bottom: var(--space-4);">
                        ← Back to Files
                    </button>

                    <div class="card">
                        <div style="display: flex; align-items: center; gap: var(--space-3); margin-bottom: var(--space-4);">
                            <span style="font-size: 2em;">${this.getFileIcon(filePath)}</span>
                            <div style="flex: 1; min-width: 0;">
                                <h1 style="font-size: var(--text-xl); margin: 0; word-break: break-all;">
                                    ${this.escapeHtml(this.getFileName(filePath))}
                                </h1>
                                <code style="font-size: var(--text-sm); color: var(--text-tertiary); word-break: break-all;">
                                    ${this.escapeHtml(filePath)}
                                </code>
                            </div>
                        </div>

                        <div class="grid grid-cols-3" style="margin-top: var(--space-4);">
                            <div class="stat-card">
                                <h4>References</h4>
                                <p class="stat-value">${fileInfo.count || 0}</p>
                            </div>
                            <div class="stat-card">
                                <h4>Sessions</h4>
                                <p class="stat-value">${references.sessions.size}</p>
                            </div>
                            <div class="stat-card">
                                <h4>File Type</h4>
                                <p class="stat-value">${this.getFileExtension(filePath).toUpperCase()}</p>
                            </div>
                        </div>
                    </div>

                    ${fileContent ? `
                        <div class="card" style="margin-top: var(--space-6);">
                            <h3 style="margin-bottom: var(--space-4);">📄 File Content</h3>
                            <div style="background: var(--bg-tertiary); border-radius: var(--radius-md); padding: var(--space-4); overflow-x: auto;">
                                <pre style="margin: 0; font-family: 'Monaco', 'Menlo', 'Courier New', monospace; font-size: var(--text-sm); line-height: 1.6;"><code>${this.escapeHtml(fileContent)}</code></pre>
                            </div>
                            <p class="text-xs text-tertiary" style="margin-top: var(--space-2);">
                                ${fileContent.split('\n').length} lines • ${(fileContent.length / 1024).toFixed(1)} KB
                            </p>
                        </div>
                    ` : `
                        <div class="card" style="margin-top: var(--space-6); background: var(--bg-tertiary);">
                            <p class="text-center text-tertiary">
                                <strong>Note:</strong> File content not available in this dashboard.
                                This view shows metadata about files referenced in the conversation history.
                            </p>
                        </div>
                    `}

                    <div class="card" style="margin-top: var(--space-6);">
                        <h3 style="margin-bottom: var(--space-4);">💬 References in Conversations</h3>

                        ${references.messages.length === 0 ? `
                            <p class="text-tertiary">No message references found.</p>
                        ` : `
                            <p class="text-secondary" style="margin-bottom: var(--space-4);">
                                This file was referenced in ${references.messages.length} message${references.messages.length !== 1 ? 's' : ''}
                                across ${references.sessions.size} session${references.sessions.size !== 1 ? 's' : ''}.
                            </p>

                            <div style="display: grid; gap: var(--space-3);">
                                ${references.messages.slice(0, 20).map(ref => `
                                    <div class="card" style="background: var(--bg-secondary); padding: var(--space-3);">
                                        <div style="display: flex; justify-content: space-between; align-items: start; margin-bottom: var(--space-2);">
                                            <span class="badge badge-${ref.role}">${ref.role}</span>
                                            <span class="text-xs text-tertiary">${this.formatDate(ref.timestamp)}</span>
                                        </div>
                                        <p style="font-size: var(--text-sm); margin: var(--space-2) 0; line-height: 1.6;">
                                            ${this.escapeHtml(ref.content_preview.substring(0, 500))}${ref.content_preview.length > 500 ? '...' : ''}
                                        </p>
                                        <div style="font-size: var(--text-xs); color: var(--text-tertiary);">
                                            Session: ${this.escapeHtml(ref.checkpoint_id)}
                                        </div>
                                    </div>
                                `).join('')}

                                ${references.messages.length > 20 ? `
                                    <div class="card" style="text-align: center; background: var(--bg-tertiary);">
                                        <p>Showing first 20 of ${references.messages.length} references</p>
                                    </div>
                                ` : ''}
                            </div>
                        `}
                    </div>
                </div>
            `;

        } catch (error) {
            console.error('Failed to load file details:', error);
            mainContent.innerHTML = `
                <div class="card">
                    <div class="card-header">
                        <h2 class="card-title" style="color: var(--error-500);">Failed to Load File Details</h2>
                    </div>
                    <div class="card-content">
                        <p>Error: ${error.message}</p>
                        <button onclick="window.location.hash='#files'" class="btn-secondary" style="margin-top: var(--space-4);">
                            ← Back to Files
                        </button>
                    </div>
                </div>
            `;
        }
    }

    async findFileReferences(filePath) {
        // Search through messages to find references to this file
        const messagesData = await window.dashboardData.loader.load('data/messages.json');
        const messages = messagesData.messages || [];

        const references = {
            messages: [],
            sessions: new Set()
        };

        for (const message of messages) {
            const content = message.content_preview || message.content || '';

            // Check if this message references the file
            if (content.includes(filePath)) {
                references.messages.push(message);
                references.sessions.add(message.checkpoint_id);
            }
        }

        console.log(`Found ${references.messages.length} references to ${filePath}`);

        return references;
    }

    async loadFileContent(filePath) {
        // Try to load the actual file content
        // This may not work if the files aren't served alongside the dashboard
        try {
            // Try relative path from dashboard root
            const response = await fetch(`../../${filePath}`);
            if (response.ok) {
                const content = await response.text();
                console.log(`✓ Loaded file content: ${filePath} (${content.length} bytes)`);
                return content;
            }
        } catch (error) {
            console.log(`Could not load file content for ${filePath}:`, error.message);
        }

        return null;
    }

    getFileExtension(path) {
        const parts = path.split('.');
        return parts.length > 1 ? parts.pop() : 'file';
    }

    extractDateFromId(id) {
        // Extract date from checkpoint ID using regex
        const isoMatch = id.match(/(\d{4}-\d{2}-\d{2}T[\d:]+Z)/);
        if (isoMatch) {
            return new Date(isoMatch[1]);
        }
        // Use noon UTC to avoid timezone issues causing date to shift
        const dateMatch = id.match(/(\d{4}-\d{2}-\d{2})/);
        if (dateMatch) {
            return new Date(dateMatch[1] + 'T12:00:00Z');
        }
        return new Date();
    }

    extractProject(id) {
        const patterns = [
            /CODITECT-([A-Z-]+)/i,
            /PROJECTS\/([^\/]+)/i,
            /submodules\/([^\/]+)/i
        ];
        for (const pattern of patterns) {
            const match = id.match(pattern);
            if (match) return match[1];
        }
        return null;
    }

    extractSubmodule(id) {
        const match = id.match(/submodules\/[^\/]+\/([^\/]+)/i);
        return match ? match[1] : null;
    }

    extractModulesFromFiles(files) {
        const modules = new Set();
        files.forEach(file => {
            const match = file.match(/submodules\/([^\/]+)\/([^\/]+)/i);
            if (match) {
                modules.add(`${match[1]}/${match[2]}`);
            }
        });
        return Array.from(modules);
    }

    async renderCheckpoints(id) {
        const mainContent = document.querySelector('.main-content');

        if (id) {
            // Show specific checkpoint
            mainContent.innerHTML = '<div class="loading">Loading checkpoint details...</div>';

            try {
                const checkpoint = await window.dashboardData.loadCheckpoint(id);

                // Load git data for this checkpoint
                const gitData = await window.dashboardData.loadGitCommitsForCheckpoint(id);

                // Extract metadata
                const dateExtracted = this.extractDateFromId(checkpoint.id);
                const project = this.extractProject(checkpoint.id);
                const submodule = this.extractSubmodule(checkpoint.id);
                const modules = this.extractModulesFromFiles(checkpoint.files_modified || []);

                // GitHub repo URL (generic - can be enhanced based on project)
                const githubBaseUrl = 'https://github.com/coditect-ai/coditect-rollout-master';

                mainContent.innerHTML = `
                    <div class="checkpoint-detail-view">
                        <button onclick="window.location.hash='#checkpoints'" class="btn-secondary" style="margin-bottom: var(--space-4);">
                            ← Back to All Sessions
                        </button>

                        <div class="card">
                            <div class="card-header">
                                <h2 class="card-title">${this.escapeHtml(checkpoint.title)}</h2>
                                <p class="card-subtitle">${checkpoint.summary}</p>
                            </div>
                            <div class="card-content">
                                <!-- Session Metadata -->
                                <div style="background: var(--primary-100); padding: var(--space-4); border-radius: var(--radius-md); margin-bottom: var(--space-6);">
                                    <h3 style="margin-bottom: var(--space-3); color: var(--primary-900);">📋 Session Context</h3>
                                    <div class="grid grid-cols-2" style="gap: var(--space-3);">
                                        <div>
                                            <strong style="color: var(--primary-900);">📅 Date & Time:</strong>
                                            <div style="color: var(--primary-700); font-weight: 600; margin-top: var(--space-1);">
                                                ${dateExtracted.toLocaleDateString()} ${dateExtracted.toLocaleTimeString()}
                                            </div>
                                        </div>
                                        ${project ? `
                                            <div>
                                                <strong style="color: var(--primary-900);">📦 Project:</strong>
                                                <div style="color: var(--primary-700); font-weight: 600; margin-top: var(--space-1);">
                                                    ${this.escapeHtml(project)}
                                                </div>
                                            </div>
                                        ` : ''}
                                        ${submodule ? `
                                            <div>
                                                <strong style="color: var(--primary-900);">📂 Submodule:</strong>
                                                <div style="color: var(--primary-700); font-weight: 600; margin-top: var(--space-1);">
                                                    ${this.escapeHtml(submodule)}
                                                </div>
                                            </div>
                                        ` : ''}
                                        ${modules.length > 0 ? `
                                            <div style="grid-column: 1 / -1;">
                                                <strong style="color: var(--primary-900);">🔧 Modules Worked On (${modules.length}):</strong>
                                                <div style="margin-top: var(--space-2); display: flex; flex-wrap: wrap; gap: var(--space-2);">
                                                    ${modules.map(mod => `
                                                        <span class="badge" style="background: var(--primary-200); color: var(--primary-900);">
                                                            ${this.escapeHtml(mod)}
                                                        </span>
                                                    `).join('')}
                                                </div>
                                            </div>
                                        ` : ''}
                                    </div>
                                </div>

                                <!-- Git Commits Section -->
                                ${gitData && gitData.commits && gitData.commits.length > 0 ? `
                                    <div style="background: var(--bg-tertiary); padding: var(--space-4); border-radius: var(--radius-md); margin-bottom: var(--space-6);">
                                        <h3 style="margin-bottom: var(--space-3); color: var(--text-primary);">🔀 Git Commits (${gitData.commits.length})</h3>

                                        ${gitData.branch ? `
                                            <div style="margin-bottom: var(--space-3); padding: var(--space-2); background: var(--primary-100); border-radius: var(--radius-sm);">
                                                <strong style="color: var(--primary-900);">Branch:</strong>
                                                <code style="color: var(--primary-700); font-weight: 600;">${gitData.branch}</code>
                                            </div>
                                        ` : ''}

                                        ${gitData.file_modified_time || gitData.file_created_time ? `
                                            <div style="margin-bottom: var(--space-3); padding: var(--space-3); background: var(--success-100); border-radius: var(--radius-sm); border: 1px solid var(--success-300);">
                                                <div style="font-size: var(--text-sm); color: var(--text-primary);">
                                                    <strong>📁 File System Timestamps (Accurate)</strong>
                                                </div>
                                                ${gitData.file_modified_time ? `
                                                    <div style="margin-top: var(--space-2); font-size: var(--text-sm); color: var(--text-secondary);">
                                                        <strong>Modified:</strong> ${new Date(gitData.file_modified_time).toLocaleString()}
                                                    </div>
                                                ` : ''}
                                                ${gitData.file_created_time ? `
                                                    <div style="margin-top: var(--space-1); font-size: var(--text-sm); color: var(--text-secondary);">
                                                        <strong>Created:</strong> ${new Date(gitData.file_created_time).toLocaleString()}
                                                    </div>
                                                ` : ''}
                                            </div>
                                        ` : ''}

                                        <div style="max-height: 400px; overflow-y: auto;">
                                            ${gitData.commits.map(commit => `
                                                <div style="padding: var(--space-3); margin-bottom: var(--space-2); background: var(--bg-primary); border-left: 3px solid var(--primary-500); border-radius: var(--radius-sm);">
                                                    <div style="font-family: monospace; font-size: var(--text-sm);">
                                                        <a href="${githubBaseUrl}/commit/${commit.hash}"
                                                           target="_blank"
                                                           rel="noopener noreferrer"
                                                           style="color: var(--primary-600); text-decoration: none; font-weight: 600; font-family: monospace;"
                                                           title="View commit on GitHub">
                                                            📝 ${commit.hash}
                                                        </a>
                                                        <div style="color: var(--text-secondary); margin-top: var(--space-1); word-wrap: break-word; white-space: pre-wrap; overflow-wrap: break-word;">
                                                            ${this.escapeHtml(commit.message)}
                                                        </div>
                                                    </div>
                                                </div>
                                            `).join('')}
                                        </div>

                                        ${gitData.working_dir_status ? `
                                            <div style="margin-top: var(--space-3); padding-top: var(--space-3); border-top: 1px solid var(--border-primary);">
                                                <strong>Working Directory Status:</strong>
                                                <div style="margin-top: var(--space-2); padding: var(--space-2); background: var(--bg-primary); border-radius: var(--radius-sm); font-family: monospace; font-size: var(--text-xs); white-space: pre-wrap; overflow-wrap: break-word;">
                                                    ${this.escapeHtml(gitData.working_dir_status)}
                                                </div>
                                            </div>
                                        ` : ''}

                                        ${gitData.submodules && gitData.submodules.length > 0 ? `
                                            <div style="margin-top: var(--space-3); padding-top: var(--space-3); border-top: 1px solid var(--border-primary);">
                                                <strong>Submodule Updates (${gitData.submodules.length}):</strong>
                                                <div style="margin-top: var(--space-2);">
                                                    ${gitData.submodules.map(sub => `
                                                        <div style="padding: var(--space-2); margin-bottom: var(--space-2); background: var(--bg-primary); border-radius: var(--radius-sm); font-size: var(--text-sm);">
                                                            <div style="font-weight: 600; color: var(--text-primary); margin-bottom: var(--space-1);">
                                                                📦 ${this.escapeHtml(sub.name)}
                                                            </div>
                                                            ${sub.commit ? `
                                                                <div style="font-family: monospace; font-size: var(--text-xs); color: var(--text-tertiary);">
                                                                    Commit: <code>${sub.commit}</code>
                                                                </div>
                                                            ` : ''}
                                                            ${sub.latest_hash && sub.latest_message ? `
                                                                <div style="font-family: monospace; font-size: var(--text-xs); color: var(--text-secondary); margin-top: var(--space-1);">
                                                                    Latest: ${sub.latest_hash} ${this.escapeHtml(sub.latest_message)}
                                                                </div>
                                                            ` : ''}
                                                        </div>
                                                    `).join('')}
                                                </div>
                                            </div>
                                        ` : ''}
                                    </div>
                                ` : ''}

                                <div class="grid grid-cols-4" style="margin-bottom: var(--space-6);">
                                    <div class="stat-card">
                                        <h3>Total Messages</h3>
                                        <p class="stat-value">${checkpoint.message_count}</p>
                                    </div>
                                    <div class="stat-card">
                                        <h3>User Messages</h3>
                                        <p class="stat-value">${checkpoint.user_messages}</p>
                                    </div>
                                    <div class="stat-card">
                                        <h3>Assistant Messages</h3>
                                        <p class="stat-value">${checkpoint.assistant_messages}</p>
                                    </div>
                                    <div class="stat-card">
                                        <h3>Commands</h3>
                                        <p class="stat-value">${checkpoint.commands_executed}</p>
                                    </div>
                                </div>

                                <h3 style="margin-top: var(--space-6);">Top Topics</h3>
                                <div class="grid grid-cols-3">
                                    ${checkpoint.top_topics.map(topic => `
                                        <div class="badge badge-primary" style="margin: var(--space-2);">
                                            ${this.escapeHtml(topic)}
                                        </div>
                                    `).join('')}
                                </div>

                                ${checkpoint.files_modified && checkpoint.files_modified.length > 0 ? `
                                    <h3 style="margin-top: var(--space-6);">Files Modified (click to view)</h3>
                                    <div class="grid grid-cols-1" style="gap: var(--space-2);">
                                        ${checkpoint.files_modified.slice(0, 20).map(file => `
                                            <button
                                                onclick="window.navigationController.openFileModal('${this.escapeHtml(file).replace(/'/g, "\\'")}')"
                                                class="file-reference-btn"
                                                style="
                                                    padding: var(--space-3);
                                                    background: var(--bg-tertiary);
                                                    border: 1px solid var(--border-primary);
                                                    border-radius: var(--radius-md);
                                                    font-family: monospace;
                                                    font-size: var(--text-sm);
                                                    cursor: pointer;
                                                    transition: all var(--transition-fast);
                                                    text-align: left;
                                                    width: 100%;
                                                    display: flex;
                                                    align-items: center;
                                                    gap: var(--space-2);
                                                    color: var(--text-primary);
                                                "
                                                onmouseover="this.style.background='var(--bg-elevated)'; this.style.borderColor='var(--primary-500)'; this.style.transform='translateX(4px)';"
                                                onmouseout="this.style.background='var(--bg-tertiary)'; this.style.borderColor='var(--border-primary)'; this.style.transform='translateX(0)';"
                                            >
                                                <span style="color: var(--primary-500);">📄</span>
                                                <span style="flex: 1; word-break: break-all;">${this.escapeHtml(file)}</span>
                                                <span style="color: var(--text-tertiary); font-size: 0.9em;">→</span>
                                            </button>
                                        `).join('')}
                                        ${checkpoint.files_modified.length > 20 ? `
                                            <p class="text-sm text-tertiary">... and ${checkpoint.files_modified.length - 20} more files</p>
                                        ` : ''}
                                    </div>
                                ` : ''}
                            </div>
                        </div>
                    </div>
                `;
            } catch (error) {
                mainContent.innerHTML = `
                    <div class="card">
                        <div class="card-header">
                            <h2 class="card-title" style="color: var(--error-500);">Checkpoint Not Found</h2>
                        </div>
                        <div class="card-content">
                            <p>Could not find checkpoint: ${this.escapeHtml(id)}</p>
                            <button onclick="window.location.hash='#checkpoints'" class="btn-primary" style="margin-top: var(--space-4);">
                                View All Sessions
                            </button>
                        </div>
                    </div>
                `;
            }
        } else {
            // Show all checkpoints
            mainContent.innerHTML = '<div class="loading">Loading sessions...</div>';

            try {
                const checkpoints = await window.dashboardData.loadCheckpoints();

                mainContent.innerHTML = `
                    <div class="checkpoints-view">
                        <h2>💬 Conversation Sessions (${checkpoints.length} total)</h2>

                        <div class="grid grid-cols-1" style="gap: var(--space-4); margin-top: var(--space-6);">
                            ${checkpoints.map(checkpoint => {
                                const date = this.extractDateFromId(checkpoint.id);
                                const project = this.extractProject(checkpoint.id);
                                const submodule = this.extractSubmodule(checkpoint.id);
                                const modules = this.extractModulesFromFiles(checkpoint.files_modified || []);

                                return `
                                    <div class="card card-collapsible collapsed" onclick="this.classList.toggle('collapsed')">
                                        <div class="card-header" style="cursor: pointer;">
                                            <div style="flex: 1;">
                                                <h3 class="card-title">${this.escapeHtml(checkpoint.title)}</h3>
                                                <p class="card-subtitle">
                                                    📅 ${date.toLocaleDateString()} ${date.toLocaleTimeString()} •
                                                    💬 ${checkpoint.message_count} messages •
                                                    ⚡ ${checkpoint.commands_executed} commands
                                                    ${project ? ` • 📦 ${project}` : ''}
                                                    ${submodule ? ` • 📂 ${submodule}` : ''}
                                                </p>
                                            </div>
                                            <span class="card-collapse-icon">▼</span>
                                        </div>
                                        <div class="card-content">
                                            <p><strong>Summary:</strong> ${checkpoint.summary}</p>
                                            <p style="margin-top: var(--space-2);"><strong>Topics:</strong> ${checkpoint.top_topics.slice(0, 3).join(', ')}</p>
                                            ${modules.length > 0 ? `
                                                <p style="margin-top: var(--space-2);">
                                                    <strong>Modules (${modules.length}):</strong>
                                                    ${modules.slice(0, 3).map(m => `<span class="badge" style="margin-left: var(--space-1);">${this.escapeHtml(m)}</span>`).join('')}
                                                    ${modules.length > 3 ? `<span class="text-tertiary"> +${modules.length - 3} more</span>` : ''}
                                                </p>
                                            ` : ''}
                                            <button onclick="event.stopPropagation(); window.location.hash='#checkpoints/${encodeURIComponent(checkpoint.id)}'"
                                                    class="btn-primary" style="margin-top: var(--space-4);">
                                                View Full Details
                                            </button>
                                        </div>
                                    </div>
                                `;
                            }).join('')}
                        </div>
                    </div>
                `;
            } catch (error) {
                mainContent.innerHTML = `
                    <div class="card">
                        <div class="card-header">
                            <h2 class="card-title" style="color: var(--error-500);">Failed to Load Sessions</h2>
                        </div>
                        <div class="card-content">
                            <p>Error: ${error.message}</p>
                        </div>
                    </div>
                `;
            }
        }
    }

    async renderCommands(filter) {
        const mainContent = document.querySelector('.main-content');
        mainContent.innerHTML = '<div class="loading">Loading commands...</div>';

        try {
            const commands = await window.dashboardData.loadCommands();

            // Group by command type
            const grouped = {};
            commands.forEach(cmd => {
                if (!grouped[cmd.command_type]) {
                    grouped[cmd.command_type] = [];
                }
                grouped[cmd.command_type].push(cmd);
            });

            mainContent.innerHTML = `
                <div class="commands-view">
                    <h2>⚡ Commands (${commands.length} total)</h2>

                    <div class="grid grid-cols-1" style="gap: var(--space-4); margin-top: var(--space-6);">
                        ${Object.entries(grouped).map(([type, cmds]) => `
                            <div class="card card-collapsible collapsed" onclick="this.classList.toggle('collapsed')">
                                <div class="card-header" style="cursor: pointer;">
                                    <div>
                                        <h3 class="card-title">${type.toUpperCase()} Commands</h3>
                                        <p class="card-subtitle">${cmds.length} commands executed</p>
                                    </div>
                                    <span class="card-collapse-icon">▼</span>
                                </div>
                                <div class="card-content">
                                    <div style="max-height: 600px; overflow-y: auto;">
                                        ${cmds.slice(0, 50).map(cmd => `
                                            <div style="padding: var(--space-3); margin: var(--space-2) 0; background: var(--bg-tertiary); border-radius: var(--radius-md); font-family: monospace; font-size: var(--text-sm); border-left: 3px solid var(--primary-500);">
                                                <div style="color: var(--primary-600); font-weight: var(--font-semibold); margin-bottom: var(--space-2); word-wrap: break-word; white-space: pre-wrap; overflow-wrap: break-word;">
                                                    ${this.escapeHtml(cmd.command_text)}
                                                </div>
                                                <div style="color: var(--text-tertiary); font-size: var(--text-xs); word-wrap: break-word; overflow-wrap: break-word;">
                                                    📅 ${new Date(cmd.timestamp).toLocaleString()}
                                                </div>
                                                <div style="color: var(--text-tertiary); font-size: var(--text-xs); margin-top: var(--space-1); word-wrap: break-word; overflow-wrap: break-word;">
                                                    📂 Session: ${this.escapeHtml(cmd.checkpoint_id)}
                                                </div>
                                            </div>
                                        `).join('')}
                                        ${cmds.length > 50 ? `
                                            <p class="text-sm text-tertiary" style="text-align: center; margin-top: var(--space-4);">
                                                ... and ${cmds.length - 50} more ${type} commands
                                            </p>
                                        ` : ''}
                                    </div>
                                </div>
                            </div>
                        `).join('')}
                    </div>

                    <div class="card" style="margin-top: var(--space-6);">
                        <div class="card-header">
                            <h3 class="card-title">Command Statistics</h3>
                        </div>
                        <div class="card-content">
                            <div class="grid grid-cols-4">
                                ${Object.entries(grouped).map(([type, cmds]) => `
                                    <div class="stat-card">
                                        <h4>${type}</h4>
                                        <p class="stat-value">${cmds.length}</p>
                                    </div>
                                `).join('')}
                            </div>
                        </div>
                    </div>
                </div>
            `;
        } catch (error) {
            mainContent.innerHTML = `
                <div class="card">
                    <div class="card-header">
                        <h2 class="card-title" style="color: var(--error-500);">Failed to Load Commands</h2>
                    </div>
                    <div class="card-content">
                        <p>Error: ${error.message}</p>
                    </div>
                </div>
            `;
        }
    }

    handleSearch(e) {
        this.searchQuery = e.target.value.trim();

        // Auto-search when query is empty (clear results)
        if (this.searchQuery === '') {
            // Don't automatically navigate, just clear the stored query
            return;
        }

        // Debounce search - wait for user to stop typing
        clearTimeout(this.searchTimeout);
        this.searchTimeout = setTimeout(() => {
            if (this.searchQuery.length >= 2) {
                this.executeSearch();
            }
        }, 500); // 500ms debounce
    }

    async executeSearch() {
        if (!this.searchQuery || this.searchQuery.length < 2) {
            return;
        }

        console.log('🔍 Executing search:', this.searchQuery);

        // Navigate to search results view
        window.location.hash = `#search/${encodeURIComponent(this.searchQuery)}`;
    }

    async renderSearch(query) {
        const mainContent = document.querySelector('.main-content');

        if (!query || query.length < 2) {
            mainContent.innerHTML = `
                <div class="search-view">
                    <h1>🔍 Search Messages</h1>
                    <p class="text-secondary">Enter at least 2 characters to search across 10,206 messages</p>
                </div>
            `;
            return;
        }

        mainContent.innerHTML = '<div class="loading">Searching messages...</div>';

        try {
            const results = await this.searchMessages(query);

            mainContent.innerHTML = `
                <div class="search-view">
                    <div class="section-header">
                        <h1>🔍 Search Results</h1>
                        <p class="text-secondary">
                            Found ${results.length} message${results.length !== 1 ? 's' : ''} matching "${this.escapeHtml(query)}"
                        </p>
                    </div>

                    ${results.length === 0 ? `
                        <div class="card">
                            <h3>No results found</h3>
                            <p>Try different keywords or check your spelling</p>
                            <p class="text-sm text-tertiary" style="margin-top: var(--space-4);">
                                Search tips:
                                <ul style="margin-top: var(--space-2); margin-left: var(--space-6);">
                                    <li>Use specific technical terms</li>
                                    <li>Try partial words (e.g., "auth" finds "authentication")</li>
                                    <li>Search is case-insensitive</li>
                                </ul>
                            </p>
                        </div>
                    ` : `
                        <div class="search-results">
                            ${results.slice(0, 50).map(result => {
                                const isCheckpointResult = result.message.role === 'checkpoint';
                                const checkpointLink = isCheckpointResult ? `#checkpoints/${encodeURIComponent(result.message.checkpoint_id)}` : '';

                                return `
                                <${isCheckpointResult ? 'a href="' + checkpointLink + '" style="text-decoration: none; color: inherit;"' : 'div'} class="card message-result" style="margin-bottom: var(--space-4); ${isCheckpointResult ? 'cursor: pointer; transition: all var(--transition-fast);' : ''}" ${isCheckpointResult ? 'onmouseover="this.style.transform=\'translateX(4px)\'; this.style.boxShadow=\'var(--shadow-lg)\';" onmouseout="this.style.transform=\'\'; this.style.boxShadow=\'var(--shadow-md)\';"' : ''}>
                                    <div style="display: flex; justify-content: space-between; align-items: start; margin-bottom: var(--space-2);">
                                        <div style="display: flex; gap: var(--space-2); align-items: center;">
                                            <span class="badge badge-${result.message.role}">${result.message.role}</span>
                                            ${result.message.has_code ? '<span class="badge">📝 Code</span>' : ''}
                                            ${isCheckpointResult ? '<span class="badge" style="background: var(--primary-500); color: white;">Click to View →</span>' : ''}
                                        </div>
                                        <span class="text-xs text-tertiary">${this.formatDate(result.message.first_seen || result.message.timestamp)}</span>
                                    </div>

                                    <div class="search-match-preview" style="margin: var(--space-3) 0; white-space: pre-wrap;">
                                        ${this.highlightSearchTerms(result.preview, query)}
                                    </div>

                                    <div style="display: flex; gap: var(--space-4); font-size: var(--text-xs); color: var(--text-tertiary); flex-wrap: wrap;">
                                        <span>${isCheckpointResult ? 'Messages' : 'Words'}: ${result.message.word_count}</span>
                                        <span style="max-width: 300px; overflow: hidden; text-overflow: ellipsis; white-space: nowrap;">Session: ${this.escapeHtml(result.message.checkpoint_id)}</span>
                                        <span>Match score: ${result.score.toFixed(2)}</span>
                                    </div>
                                </${isCheckpointResult ? 'a' : 'div'}>
                            `}).join('')}

                            ${results.length > 50 ? `
                                <div class="card" style="text-align: center; background: var(--bg-tertiary);">
                                    <p>Showing first 50 of ${results.length} results</p>
                                    <p class="text-sm text-tertiary">Refine your search for more specific results</p>
                                </div>
                            ` : ''}
                        </div>
                    `}
                </div>
            `;

        } catch (error) {
            console.error('Search failed:', error);
            mainContent.innerHTML = `
                <div class="card">
                    <div class="card-header">
                        <h2 class="card-title" style="color: var(--error-500);">Search Failed</h2>
                    </div>
                    <div class="card-content">
                        <p>Error: ${error.message}</p>
                    </div>
                </div>
            `;
        }
    }

    async searchMessages(query) {
        console.log(`🔍 Searching for: "${query}"`);

        // Load all messages (this searches across all pages)
        const messagesData = await window.dashboardData.loadOverviewData();
        const allMessages = messagesData.stats ? await this.loadAllMessages() : [];

        // Also load checkpoints for checkpoint-specific searches
        const checkpoints = await window.dashboardData.loadCheckpoints();

        const queryLower = query.toLowerCase();

        // Detect if this looks like a checkpoint ID search
        const looksLikeCheckpointId = /export|checkpoint|session/i.test(query) || query.includes('-');

        // Detect and normalize date queries
        const dateFormats = this.detectDateQuery(query);
        const isDateQuery = dateFormats.length > 0;

        if (isDateQuery) {
            console.log('📅 Detected date query, searching dates:', dateFormats);
        }

        if (looksLikeCheckpointId) {
            console.log('💬 Detected checkpoint ID search pattern');
        }

        // Split query into words
        // For checkpoint IDs, don't split on hyphens; for regular text, split on both spaces and hyphens
        const queryWords = looksLikeCheckpointId
            ? queryLower.split(/\s+/).filter(w => w.length > 0)  // Keep hyphens intact for checkpoint IDs
            : queryLower.split(/[\s\-]+/).filter(w => w.length > 0); // Split on hyphens for regular search

        // Search and score results
        const results = [];

        // First, search checkpoints directly if query looks like checkpoint ID
        if (looksLikeCheckpointId) {
            for (const checkpoint of checkpoints) {
                const checkpointIdLower = (checkpoint.id || '').toLowerCase();
                const checkpointTitleLower = (checkpoint.title || '').toLowerCase();

                // Check if checkpoint ID or title contains the full query or significant parts
                if (checkpointIdLower.includes(queryLower) || checkpointTitleLower.includes(queryLower)) {
                    // Add a synthetic result representing this checkpoint
                    results.push({
                        message: {
                            role: 'checkpoint',
                            checkpoint_id: checkpoint.id,
                            content_preview: `Session: ${checkpoint.title}\nMessages: ${checkpoint.message_count} (${checkpoint.user_messages} user, ${checkpoint.assistant_messages} assistant)\nTop topics: ${(checkpoint.top_topics || []).slice(0, 3).join(', ')}`,
                            first_seen: checkpoint.date,
                            word_count: checkpoint.message_count,
                            has_code: false
                        },
                        score: 100, // High score for direct checkpoint match
                        matchedWords: queryWords.length,
                        preview: `🎯 Checkpoint Match: ${checkpoint.title}\n\n${checkpoint.summary || ''}\n\nMessages: ${checkpoint.message_count} | Date: ${checkpoint.date}`
                    });
                    continue; // Don't also search individual messages from this checkpoint
                }

                // Also check if multiple query words match the checkpoint ID
                let checkpointWordMatches = 0;
                for (const word of queryWords) {
                    if (word.length > 2 && checkpointIdLower.includes(word)) {
                        checkpointWordMatches++;
                    }
                }

                // If most query words match, add this checkpoint
                if (checkpointWordMatches >= Math.min(3, queryWords.length * 0.6)) {
                    results.push({
                        message: {
                            role: 'checkpoint',
                            checkpoint_id: checkpoint.id,
                            content_preview: `Session: ${checkpoint.title}\nMessages: ${checkpoint.message_count}`,
                            first_seen: checkpoint.date,
                            word_count: checkpoint.message_count,
                            has_code: false
                        },
                        score: 50 + checkpointWordMatches * 5,
                        matchedWords: checkpointWordMatches,
                        preview: `💬 Checkpoint: ${checkpoint.title}\n\n${checkpoint.summary || ''}\n\nMessages: ${checkpoint.message_count} | Top topics: ${(checkpoint.top_topics || []).slice(0, 3).join(', ')}`
                    });
                }
            }
        }

        for (const message of allMessages) {
            const contentLower = (message.content_preview || message.content || '').toLowerCase();
            const checkpointLower = (message.checkpoint_id || '').toLowerCase();
            const firstSeen = message.first_seen || '';

            let score = 0;
            let matchedWords = 0;
            let matchedInDate = false;

            // Check date fields if this is a date query
            if (isDateQuery) {
                for (const dateStr of dateFormats) {
                    if (firstSeen.includes(dateStr) || checkpointLower.includes(dateStr)) {
                        score += 10; // High score for date matches
                        matchedInDate = true;
                        matchedWords = queryWords.length; // Count as matching all words
                        break;
                    }
                }
            }

            // Search content
            queryWords.forEach(word => {
                // Check content
                if (contentLower.includes(word)) {
                    matchedWords++;
                    const wordRegex = new RegExp(`\\b${word}\\b`, 'gi');
                    const exactMatches = (contentLower.match(wordRegex) || []).length;
                    score += exactMatches * 2;

                    const partialMatches = (contentLower.match(new RegExp(word, 'gi')) || []).length;
                    score += partialMatches;
                }

                // Also check checkpoint ID for keywords
                if (checkpointLower.includes(word)) {
                    matchedWords++;
                    score += 1;
                }
            });

            // Only include if at least one word matched
            if (matchedWords > 0) {
                // Find the best preview snippet with the match
                let preview;
                if (matchedInDate) {
                    // Show date info in preview for date matches
                    preview = `Date: ${this.formatDate(firstSeen)} | Session: ${message.checkpoint_id}\n\n${message.content_preview || ''}`;
                } else {
                    preview = this.extractSearchPreview(message.content_preview || message.content || '', query, queryWords);
                }

                results.push({
                    message: message,
                    score: score,
                    matchedWords: matchedWords,
                    preview: preview.substring(0, 500)
                });
            }
        }

        // Sort by score (highest first)
        results.sort((a, b) => b.score - a.score);

        console.log(`✓ Found ${results.length} matching messages`);

        return results;
    }

    detectDateQuery(query) {
        const dateFormats = [];

        // Detect MM/DD/YYYY or M/D/YYYY format
        const slashDateRegex = /(\d{1,2})\/(\d{1,2})\/(\d{4})/g;
        let match;
        while ((match = slashDateRegex.exec(query)) !== null) {
            const month = match[1].padStart(2, '0');
            const day = match[2].padStart(2, '0');
            const year = match[3];
            // Convert to ISO format YYYY-MM-DD
            dateFormats.push(`${year}-${month}-${day}`);
        }

        // Detect YYYY-MM-DD format (ISO)
        const isoDateRegex = /(\d{4})-(\d{2})-(\d{2})/g;
        while ((match = isoDateRegex.exec(query)) !== null) {
            dateFormats.push(match[0]);
        }

        // Detect YYYY/MM/DD format
        const yearFirstRegex = /(\d{4})\/(\d{1,2})\/(\d{1,2})/g;
        while ((match = yearFirstRegex.exec(query)) !== null) {
            const year = match[1];
            const month = match[2].padStart(2, '0');
            const day = match[3].padStart(2, '0');
            dateFormats.push(`${year}-${month}-${day}`);
        }

        return [...new Set(dateFormats)]; // Remove duplicates
    }

    async loadAllMessages() {
        // For now, just load from the overview data
        // In a real implementation, we'd load all message pages
        const messagesData = await window.dashboardData.loader.load('data/messages.json');
        return messagesData.messages || [];
    }

    extractSearchPreview(content, originalQuery, queryWords) {
        // Find the first occurrence of any query word
        const contentLower = content.toLowerCase();
        let bestIndex = -1;

        for (const word of queryWords) {
            const index = contentLower.indexOf(word);
            if (index !== -1 && (bestIndex === -1 || index < bestIndex)) {
                bestIndex = index;
            }
        }

        if (bestIndex === -1) {
            return content.substring(0, 400) + (content.length > 400 ? '...' : '');
        }

        // Extract context around the match (250 chars before and after)
        const contextSize = 250;
        const start = Math.max(0, bestIndex - contextSize);
        const end = Math.min(content.length, bestIndex + contextSize);

        let preview = content.substring(start, end);

        if (start > 0) preview = '...' + preview;
        if (end < content.length) preview = preview + '...';

        return preview;
    }

    highlightSearchTerms(text, query) {
        if (!text || !query) return this.escapeHtml(text);

        const escaped = this.escapeHtml(text);
        const queryWords = query.toLowerCase().split(/\s+/).filter(w => w.length > 0);

        let highlighted = escaped;

        queryWords.forEach(word => {
            // Escape special regex characters
            const escapedWord = word.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
            const regex = new RegExp(`(${escapedWord})`, 'gi');
            highlighted = highlighted.replace(regex, '<mark style="background-color: var(--primary-100); color: var(--primary-900); padding: 2px 4px; border-radius: 2px;">$1</mark>');
        });

        return highlighted;
    }

    closeModals() {
        // Close file modal
        this.closeModal();
    }

    openFileModal(filePath) {
        const modal = document.getElementById('file-modal');
        const titleEl = document.getElementById('modal-file-title');
        const contentEl = document.getElementById('modal-file-content');

        console.log('📄 Opening file modal:', filePath);

        // Show modal
        modal.classList.add('active');
        document.body.style.overflow = 'hidden'; // Prevent background scroll

        // Set title
        titleEl.textContent = this.getFileName(filePath);

        // Load file content
        contentEl.innerHTML = '<div class="loading">Loading file...</div>';

        this.loadFileContentForModal(filePath).then(content => {
            if (content) {
                // Check if this is an external file indicator
                if (typeof content === 'object' && content.external) {
                    contentEl.innerHTML = `
                        <div style="padding: var(--space-8); text-align: center;">
                            <div style="font-size: 3em; margin-bottom: var(--space-4);">📍</div>
                            <h3 style="color: var(--text-primary); margin-bottom: var(--space-4);">External File</h3>
                            <p style="color: var(--text-secondary); margin-bottom: var(--space-6); max-width: 600px; margin-left: auto; margin-right: auto;">
                                ${this.escapeHtml(content.message)}
                            </p>
                            <div style="background: var(--bg-tertiary); border-radius: var(--radius-md); padding: var(--space-4); margin-bottom: var(--space-6);">
                                <div style="color: var(--text-tertiary); font-size: var(--text-sm); margin-bottom: var(--space-2);">File Location:</div>
                                <code style="color: var(--primary-500); font-size: var(--text-base); word-break: break-all; display: block; text-align: left;">
                                    ${this.escapeHtml(content.path)}
                                </code>
                            </div>
                            <div style="color: var(--text-tertiary); font-size: var(--text-sm);">
                                <p>This file is from a different project or directory outside the MEMORY-CONTEXT folder.</p>
                                <p style="margin-top: var(--space-2);">To view it, please open the file directly in your editor or file manager.</p>
                            </div>
                        </div>
                    `;
                } else {
                    // Convert markdown to HTML (basic conversion)
                    const html = this.markdownToHtml(content);
                    contentEl.innerHTML = html;
                }
            } else {
                contentEl.innerHTML = `
                    <div style="text-align: center; padding: var(--space-8); color: var(--text-tertiary);">
                        <p>Could not load file content.</p>
                        <p class="text-sm" style="margin-top: var(--space-4);">
                            File path: <code>${this.escapeHtml(filePath)}</code>
                        </p>
                    </div>
                `;
            }
        });
    }

    closeModal() {
        const modal = document.getElementById('file-modal');
        if (modal) {
            modal.classList.remove('active');
            document.body.style.overflow = ''; // Restore scroll
        }
    }

    async loadFileContentForModal(filePath) {
        try {
            // Clean up the path
            let cleanPath = filePath;

            // Check if this is an absolute path outside MEMORY-CONTEXT
            const isExternalPath = cleanPath.startsWith('/') && !cleanPath.startsWith('/MEMORY-CONTEXT');

            // Remove leading slashes and fix malformed paths
            cleanPath = cleanPath.replace(/^\/+/, '');

            // Skip if path looks invalid
            if (cleanPath.startsWith('-') || cleanPath.length === 0) {
                console.warn(`Invalid file path: ${filePath}`);
                return null;
            }

            // If it's an external path, return a special indicator
            if (isExternalPath) {
                console.log(`📍 External file (outside MEMORY-CONTEXT): ${filePath}`);
                return {
                    external: true,
                    path: filePath,
                    message: 'This file is located outside the MEMORY-CONTEXT directory and cannot be previewed in the dashboard.'
                };
            }

            // Normalize directory names (case-insensitive for known directories)
            // CHECKPOINTS -> checkpoints, SESSIONS -> sessions, etc.
            cleanPath = cleanPath.replace(/^CHECKPOINTS\//i, 'checkpoints/')
                                 .replace(/^SESSIONS\//i, 'sessions/')
                                 .replace(/^EXPORTS\//i, 'exports/')
                                 .replace(/^DOCS\//i, 'docs/');

            // Try multiple possible paths relative to dashboard location
            const paths = [
                `../${cleanPath}`,              // Up from dashboard to MEMORY-CONTEXT/
                `../../${cleanPath}`,           // Up to project root
                `../../../${cleanPath}`,        // Up even further if needed
                cleanPath                       // Try as-is
            ];

            console.log(`Trying to load: ${filePath}`);
            console.log(`Normalized path: ${cleanPath}`);

            for (const path of paths) {
                try {
                    console.log(`  Trying: ${path}`);
                    const response = await fetch(path);
                    if (response.ok) {
                        const content = await response.text();
                        console.log(`✓ Loaded file from: ${path}`);
                        return content;
                    }
                } catch (e) {
                    // Try next path
                }
            }

            console.warn(`Could not load file after trying all paths: ${filePath}`);
            return null;
        } catch (error) {
            console.error('Error loading file:', error);
            return null;
        }
    }

    markdownToHtml(markdown) {
        // Basic markdown to HTML conversion
        let html = this.escapeHtml(markdown);

        // Headers
        html = html.replace(/^### (.*$)/gim, '<h3>$1</h3>');
        html = html.replace(/^## (.*$)/gim, '<h2>$1</h2>');
        html = html.replace(/^# (.*$)/gim, '<h1>$1</h1>');

        // Bold
        html = html.replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>');
        html = html.replace(/__(.*?)__/g, '<strong>$1</strong>');

        // Italic
        html = html.replace(/\*(.*?)\*/g, '<em>$1</em>');
        html = html.replace(/_(.*?)_/g, '<em>$1</em>');

        // Code blocks
        html = html.replace(/```(\w+)?\n([\s\S]*?)```/g, (match, lang, code) => {
            return `<pre><code class="language-${lang || 'text'}">${code.trim()}</code></pre>`;
        });

        // Inline code
        html = html.replace(/`([^`]+)`/g, '<code>$1</code>');

        // Links
        html = html.replace(/\[([^\]]+)\]\(([^)]+)\)/g, '<a href="$2" target="_blank">$1</a>');

        // Lists
        html = html.replace(/^\* (.*$)/gim, '<li>$1</li>');
        html = html.replace(/^\- (.*$)/gim, '<li>$1</li>');
        html = html.replace(/(<li>.*<\/li>)/s, '<ul>$1</ul>');

        // Line breaks
        html = html.replace(/\n\n/g, '</p><p>');
        html = '<p>' + html + '</p>';

        // Clean up empty paragraphs
        html = html.replace(/<p>\s*<\/p>/g, '');
        html = html.replace(/<p>\s*(<h[1-6])/g, '$1');
        html = html.replace(/(<\/h[1-6]>)\s*<\/p>/g, '$1');
        html = html.replace(/<p>\s*(<pre>)/g, '$1');
        html = html.replace(/(<\/pre>)\s*<\/p>/g, '$1');
        html = html.replace(/<p>\s*(<ul>)/g, '$1');
        html = html.replace(/(<\/ul>)\s*<\/p>/g, '$1');

        return html;
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
