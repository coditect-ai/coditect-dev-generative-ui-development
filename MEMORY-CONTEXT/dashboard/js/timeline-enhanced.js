// Enhanced Timeline Functions - to be merged into navigation.js

// Timeline state
let timelineState = {
    allData: [],
    currentPeriodStart: null,
    currentPeriodEnd: null,
    zoomLevel: 'month', // month, week, day
    currentTopic: '',
    currentProject: ''
};

// Constrain element position to viewport bounds
function constrainToViewport(x, y, element) {
    // Force layout to get accurate dimensions
    element.offsetWidth; // Trigger reflow

    const rect = element.getBoundingClientRect();
    const viewportWidth = window.innerWidth;
    const viewportHeight = window.innerHeight;

    // Get actual dimensions, fallback if not yet rendered
    let width = rect.width;
    let height = rect.height;

    // If dimensions are 0 (element not rendered), use computed style or fallback
    if (width === 0 || height === 0) {
        const computed = window.getComputedStyle(element);
        width = parseInt(computed.width) || 400;
        height = parseInt(computed.height) || 300;
    }

    // Add padding for safe margins
    const padding = 10;

    // Ensure element stays within viewport with padding
    const constrainedX = Math.max(padding, Math.min(x, viewportWidth - width - padding));
    const constrainedY = Math.max(padding, Math.min(y, viewportHeight - height - padding));

    return { x: constrainedX, y: constrainedY };
}

// Make element draggable
function makeDraggable(element) {
    let isDragging = false;
    let dragOffset = { x: 0, y: 0 };

    element.style.cursor = 'move';

    element.addEventListener('mousedown', function(event) {
        if (event.button === 0 && event.target === this || event.target.closest('.drag-handle')) {
            event.preventDefault();
            event.stopPropagation();
            isDragging = true;
            const rect = this.getBoundingClientRect();
            dragOffset = {
                x: event.clientX - rect.left,
                y: event.clientY - rect.top
            };
            this.style.cursor = 'grabbing';
        }
    });

    document.addEventListener('mousemove', function(event) {
        if (isDragging) {
            const x = event.clientX - dragOffset.x;
            const y = event.clientY - dragOffset.y;
            const constrained = constrainToViewport(x, y, element);
            element.style.left = constrained.x + 'px';
            element.style.top = constrained.y + 'px';
        }
    });

    document.addEventListener('mouseup', function() {
        if (isDragging) {
            isDragging = false;
            element.style.cursor = 'move';
        }
    });
}

function initD3TimelineEnhanced(data, nav) {
    timelineState.allData = data;

    // Initialize period to show latest data
    if (!timelineState.currentPeriodStart) {
        const latestDate = d3.max(data, d => d.date);
        timelineState.currentPeriodEnd = latestDate;
        timelineState.currentPeriodStart = calculatePeriodStart(latestDate, timelineState.zoomLevel);
    }

    // Filter data to current period
    const periodData = data.filter(d =>
        d.date >= timelineState.currentPeriodStart &&
        d.date <= timelineState.currentPeriodEnd
    );

    // Update period info
    updatePeriodInfo();

    // Chart dimensions
    const margin = { top: 40, right: 40, bottom: 80, left: 70 };
    const width = Math.min(1400, document.getElementById('timeline-chart').clientWidth) - margin.left - margin.right;
    const height = 600 - margin.top - margin.bottom;

    // Clear any existing chart and tooltips
    d3.select('#timeline-chart').selectAll('*').remove();
    d3.selectAll('.timeline-tooltip').remove();

    // Create SVG
    const svg = d3.select('#timeline-chart')
        .append('svg')
        .attr('width', width + margin.left + margin.right)
        .attr('height', height + margin.top + margin.bottom)
        .append('g')
        .attr('transform', `translate(${margin.left},${margin.top})`);

    // Scales - adjusted for zoom level spacing
    const xScale = d3.scaleTime()
        .domain([timelineState.currentPeriodStart, timelineState.currentPeriodEnd])
        .range([0, width]);

    const yScale = d3.scaleLinear()
        .domain([0, d3.max(periodData, d => d.messageCount) * 1.1])
        .range([height, 0]);

    const sizeScale = d3.scaleSqrt()
        .domain([0, d3.max(data, d => d.messageCount)])
        .range([8, 40]);

    // Axes with zoom-level-specific formatting
    const timeFormat = getTimeFormat(timelineState.zoomLevel);
    const xAxis = d3.axisBottom(xScale)
        .ticks(getTickCount(timelineState.zoomLevel))
        .tickFormat(d3.timeFormat(timeFormat));

    const yAxis = d3.axisLeft(yScale)
        .ticks(6)
        .tickFormat(d => d.toLocaleString());

    svg.append('g')
        .attr('class', 'x-axis')
        .attr('transform', `translate(0,${height})`)
        .call(xAxis)
        .selectAll('text')
        .attr('transform', 'rotate(-45)')
        .style('text-anchor', 'end')
        .style('font-size', '11px')
        .style('fill', 'var(--text-secondary)');

    svg.append('g')
        .attr('class', 'y-axis')
        .call(yAxis)
        .selectAll('text')
        .style('font-size', '12px')
        .style('fill', 'var(--text-secondary)');

    // Grid lines
    svg.append('g')
        .attr('class', 'grid')
        .attr('opacity', 0.1)
        .call(d3.axisLeft(yScale)
            .ticks(6)
            .tickSize(-width)
            .tickFormat(''));

    // Axis labels
    svg.append('text')
        .attr('transform', `translate(${width / 2},${height + margin.bottom - 20})`)
        .style('text-anchor', 'middle')
        .style('font-size', '14px')
        .style('font-weight', '600')
        .style('fill', 'var(--text-primary)')
        .text('Date');

    svg.append('text')
        .attr('transform', 'rotate(-90)')
        .attr('y', 0 - margin.left + 10)
        .attr('x', 0 - (height / 2))
        .style('text-anchor', 'middle')
        .style('font-size', '14px')
        .style('font-weight', '600')
        .style('fill', 'var(--text-primary)')
        .text('Messages per Session');

    // Tooltip with drag functionality
    const tooltip = d3.select('body')
        .append('div')
        .attr('class', 'timeline-tooltip')
        .style('position', 'fixed')
        .style('visibility', 'hidden')
        .style('background', 'var(--bg-primary)')
        .style('border', '2px solid var(--primary-500)')
        .style('border-radius', 'var(--radius-md)')
        .style('padding', 'var(--space-4)')
        .style('box-shadow', 'var(--shadow-xl)')
        .style('pointer-events', 'auto')
        .style('cursor', 'move')
        .style('z-index', '3000')
        .style('font-size', '13px')
        .style('max-width', '400px');

    // Make tooltip draggable
    let isDraggingTooltip = false;
    let tooltipDragOffset = { x: 0, y: 0 };

    tooltip.on('mousedown', function(event) {
        if (event.button === 0) { // Left click only
            event.preventDefault();
            event.stopPropagation();
            isDraggingTooltip = true;
            const rect = this.getBoundingClientRect();
            tooltipDragOffset = {
                x: event.clientX - rect.left,
                y: event.clientY - rect.top
            };
            d3.select(this).style('cursor', 'grabbing');
        }
    });

    d3.select('body').on('mousemove.tooltip-drag', function(event) {
        if (isDraggingTooltip) {
            const tooltipNode = tooltip.node();
            const x = event.clientX - tooltipDragOffset.x;
            const y = event.clientY - tooltipDragOffset.y;
            const constrained = constrainToViewport(x, y, tooltipNode);
            tooltip
                .style('left', constrained.x + 'px')
                .style('top', constrained.y + 'px');
        }
    });

    d3.select('body').on('mouseup.tooltip-drag', function() {
        if (isDraggingTooltip) {
            isDraggingTooltip = false;
            tooltip.style('cursor', 'move');
        }
    });

    // Click to dismiss (only if not dragging)
    let tooltipMouseDownTime = 0;
    tooltip.on('mousedown.dismiss', function() {
        tooltipMouseDownTime = Date.now();
    });

    tooltip.on('click', function(event) {
        if (Date.now() - tooltipMouseDownTime < 200) { // Quick click (not drag)
            event.stopPropagation();
            tooltip.style('visibility', 'hidden');
        }
    });

    // ESC key to dismiss tooltip
    d3.select('body').on('keydown', function(event) {
        if (event.key === 'Escape') {
            tooltip.style('visibility', 'hidden');
        }
    });

    // Plot sessions as circles
    svg.selectAll('.session-dot')
        .data(periodData)
        .enter()
        .append('circle')
        .attr('class', 'session-dot')
        .attr('cx', d => xScale(d.date))
        .attr('cy', d => yScale(d.messageCount))
        .attr('r', d => sizeScale(d.messageCount))
        .style('fill', 'var(--primary-500)')
        .style('opacity', 0.75)
        .style('stroke', 'var(--primary-700)')
        .style('stroke-width', '2.5px')
        .style('cursor', 'pointer')
        .on('mouseover', function(event, d) {
            d3.select(this)
                .transition()
                .duration(150)
                .style('opacity', 1)
                .attr('r', sizeScale(d.messageCount) * 1.3);

            const project = extractProject(d.id);
            const submodule = extractSubmodule(d.id);

            tooltip
                .html(`
                    <div style="color: var(--text-primary);">
                        <strong style="display: block; margin-bottom: 10px; font-size: 15px; color: var(--primary-600);">${nav.escapeHtml(d.title || d.id).substring(0, 80)}${d.title?.length > 80 ? '...' : ''}</strong>
                        <div style="font-size: 13px; line-height: 1.6;">
                            <div style="margin-bottom: 6px;"><strong>📅 Date:</strong> ${d.date.toLocaleString()}</div>
                            <div style="margin-bottom: 6px;"><strong>💬 Messages:</strong> ${d.messageCount.toLocaleString()} (${d.user_messages} user, ${d.assistant_messages} assistant)</div>
                            ${project ? `<div style="margin-bottom: 6px;"><strong>📦 Project:</strong> ${project}</div>` : ''}
                            ${submodule ? `<div style="margin-bottom: 6px;"><strong>📂 Submodule:</strong> ${submodule}</div>` : ''}
                            <div style="margin-bottom: 6px;"><strong>🏷️ Topics:</strong> ${(d.top_topics || []).slice(0, 5).join(', ') || 'None'}</div>
                            <div style="margin-bottom: 6px;"><strong>📄 Files:</strong> ${(d.files_modified || []).length || 0}</div>
                            <div style="margin-bottom: 6px;"><strong>⚡ Commands:</strong> ${d.commands_executed || 0}</div>
                            <div style="margin-top: 10px; padding-top: 10px; border-top: 2px solid var(--border-primary); font-size: 12px; color: var(--primary-600); font-weight: 600;">
                                🔍 Click for full details →
                            </div>
                        </div>
                    </div>
                `);

            // Set initial position constrained to viewport BEFORE making visible
            const tooltipNode = tooltip.node();
            const x = event.clientX + 20;
            const y = event.clientY - 10;
            const constrained = constrainToViewport(x, y, tooltipNode);
            tooltip
                .style('left', constrained.x + 'px')
                .style('top', constrained.y + 'px')
                .style('visibility', 'visible');
        })
        .on('mousemove', function(event) {
            if (!isDraggingTooltip) { // Only update position if not being dragged
                const tooltipNode = tooltip.node();
                const x = event.clientX + 20;
                const y = event.clientY - 10;
                const constrained = constrainToViewport(x, y, tooltipNode);
                tooltip
                    .style('left', constrained.x + 'px')
                    .style('top', constrained.y + 'px');
            }
        })
        .on('mouseout', function(event, d) {
            d3.select(this)
                .transition()
                .duration(150)
                .style('opacity', 0.75)
                .attr('r', sizeScale(d.messageCount));

            tooltip.style('visibility', 'hidden');
        })
        .on('click', function(event, d) {
            event.stopPropagation();
            // Hide tooltip when session is clicked
            tooltip.style('visibility', 'hidden');
            // Show detail panel
            showDetailPanel(d, nav);
        });

    // Setup navigation handlers
    setupNavigationHandlers(nav);

    // Setup zoom level handler
    document.getElementById('timeline-zoom-level').onchange = (e) => {
        timelineState.zoomLevel = e.target.value;
        // Recalculate period based on new zoom level
        timelineState.currentPeriodStart = calculatePeriodStart(timelineState.currentPeriodEnd, timelineState.zoomLevel);
        initD3TimelineEnhanced(data, nav);
    };
}

function calculatePeriodStart(endDate, zoomLevel) {
    const start = new Date(endDate);
    switch (zoomLevel) {
        case 'day':
            start.setDate(start.getDate() - 1);
            break;
        case 'week':
            start.setDate(start.getDate() - 7);
            break;
        case 'month':
        default:
            start.setMonth(start.getMonth() - 1);
            break;
    }
    return start;
}

function getTimeFormat(zoomLevel) {
    switch (zoomLevel) {
        case 'day':
            return '%I:%M %p';
        case 'week':
            return '%b %d';
        case 'month':
        default:
            return '%b %d';
    }
}

function getTickCount(zoomLevel) {
    switch (zoomLevel) {
        case 'day':
            return 24;
        case 'week':
            return 7;
        case 'month':
        default:
            return 30;
    }
}

function updatePeriodInfo() {
    const info = document.getElementById('timeline-period-info');
    if (info) {
        const zoomLabel = {
            'day': 'Daily',
            'week': 'Weekly',
            'month': 'Monthly'
        }[timelineState.zoomLevel];

        info.textContent = `📍 Viewing ${zoomLabel}: ${timelineState.currentPeriodStart.toLocaleDateString()} - ${timelineState.currentPeriodEnd.toLocaleDateString()}`;
    }
}

function setupNavigationHandlers(nav) {
    // Remove existing handlers
    const leftBtn = document.getElementById('timeline-nav-left');
    const rightBtn = document.getElementById('timeline-nav-right');
    const todayBtn = document.getElementById('timeline-nav-today');

    leftBtn.onclick = () => navigatePeriod(-1, nav);
    rightBtn.onclick = () => navigatePeriod(1, nav);
    todayBtn.onclick = () => navigateToToday(nav);
}

function navigatePeriod(direction, nav) {
    const periodLength = timelineState.currentPeriodEnd - timelineState.currentPeriodStart;

    timelineState.currentPeriodStart = new Date(timelineState.currentPeriodStart.getTime() + (direction * periodLength));
    timelineState.currentPeriodEnd = new Date(timelineState.currentPeriodEnd.getTime() + (direction * periodLength));

    initD3TimelineEnhanced(timelineState.allData, nav);
}

function navigateToToday(nav) {
    const now = new Date();
    timelineState.currentPeriodEnd = now;
    timelineState.currentPeriodStart = calculatePeriodStart(now, timelineState.zoomLevel);
    initD3TimelineEnhanced(timelineState.allData, nav);
}

function extractProject(id) {
    // Extract project name from checkpoint ID
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

function extractSubmodule(id) {
    const match = id.match(/submodules\/[^\/]+\/([^\/]+)/i);
    return match ? match[1] : null;
}

function showDetailPanel(checkpoint, nav) {
    const panel = document.getElementById('timeline-detail-panel');
    const title = document.getElementById('timeline-detail-title');
    const content = document.getElementById('timeline-detail-content');

    const project = extractProject(checkpoint.id);
    const submodule = extractSubmodule(checkpoint.id);

    title.textContent = checkpoint.title || checkpoint.id;

    content.innerHTML = `
        <div class="grid grid-cols-2" style="gap: var(--space-4); margin-bottom: var(--space-6);">
            <div class="stat-card">
                <h4>Total Messages</h4>
                <p class="stat-value">${checkpoint.message_count.toLocaleString()}</p>
                <p class="text-xs text-tertiary">${checkpoint.user_messages} user, ${checkpoint.assistant_messages} assistant</p>
            </div>
            <div class="stat-card">
                <h4>Date</h4>
                <p class="stat-value">${checkpoint.date.toLocaleDateString()}</p>
                <p class="text-xs text-tertiary">${checkpoint.date.toLocaleTimeString()}</p>
            </div>
            <div class="stat-card">
                <h4>Files Modified</h4>
                <p class="stat-value">${(checkpoint.files_modified || []).length}</p>
            </div>
            <div class="stat-card">
                <h4>Commands</h4>
                <p class="stat-value">${checkpoint.commands_executed || 0}</p>
            </div>
        </div>

        ${project ? `
            <div style="margin-bottom: var(--space-4); padding: var(--space-3); background: var(--primary-100); border-radius: var(--radius-md);">
                <strong style="color: var(--primary-900);">📦 Project:</strong> <span style="color: var(--primary-700); font-weight: 600;">${nav.escapeHtml(project)}</span>
                ${submodule ? `<br><strong style="color: var(--primary-900);">📂 Submodule:</strong> <span style="color: var(--primary-700); font-weight: 600;">${nav.escapeHtml(submodule)}</span>` : ''}
            </div>
        ` : ''}

        <div style="margin-bottom: var(--space-4);">
            <h4 style="margin-bottom: var(--space-2); color: var(--text-primary);">Summary</h4>
            <p style="color: var(--text-secondary);">${nav.escapeHtml(checkpoint.summary || 'No summary available')}</p>
        </div>

        <div style="margin-bottom: var(--space-4);">
            <h4 style="margin-bottom: var(--space-2); color: var(--text-primary);">Top Topics (${(checkpoint.top_topics || []).length})</h4>
            <div class="flex gap-2" style="flex-wrap: wrap;">
                ${(checkpoint.top_topics || []).map(topic => `
                    <span class="badge" style="background: var(--primary-100); color: var(--primary-900);">${nav.escapeHtml(topic)}</span>
                `).join('')}
            </div>
        </div>

        ${checkpoint.files_modified && checkpoint.files_modified.length > 0 ? `
            <div style="margin-bottom: var(--space-4);">
                <h4 style="margin-bottom: var(--space-2); color: var(--text-primary);">Files Modified (${checkpoint.files_modified.length})</h4>
                <div style="max-height: 200px; overflow-y: auto; background: var(--bg-tertiary); padding: var(--space-3); border-radius: var(--radius-sm);">
                    ${checkpoint.files_modified.slice(0, 20).map(file => `
                        <div style="margin-bottom: var(--space-1); font-family: monospace; font-size: 12px; color: var(--text-secondary);">
                            📄 ${nav.escapeHtml(file)}
                        </div>
                    `).join('')}
                    ${checkpoint.files_modified.length > 20 ? `<div style="margin-top: var(--space-2); font-style: italic; color: var(--text-tertiary);">...and ${checkpoint.files_modified.length - 20} more</div>` : ''}
                </div>
            </div>
        ` : ''}

        <div style="margin-top: var(--space-6); padding-top: var(--space-4); border-top: 1px solid var(--border-primary);">
            <a href="#checkpoints/${checkpoint.id}" class="btn btn-primary">
                View Full Session Details →
            </a>
        </div>
    `;

    panel.style.display = 'block';

    // Center panel in viewport initially
    const panelWidth = 800; // max-width from CSS
    const panelHeight = Math.min(window.innerHeight * 0.8, panel.scrollHeight);
    const centerX = (window.innerWidth - panelWidth) / 2;
    const centerY = (window.innerHeight - panelHeight) / 4; // Slight bias toward top

    const constrained = constrainToViewport(centerX, centerY, panel);
    panel.style.left = constrained.x + 'px';
    panel.style.top = constrained.y + 'px';

    // Make panel draggable (only needs to be done once)
    if (!panel.dataset.draggable) {
        makeDraggable(panel);
        panel.dataset.draggable = 'true';
    }
}

// Export for use in navigation.js
if (typeof window !== 'undefined') {
    window.initD3TimelineEnhanced = initD3TimelineEnhanced;
}
