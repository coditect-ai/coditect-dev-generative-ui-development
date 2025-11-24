// Enhanced Timeline Functions - to be merged into navigation.js

// Timeline state
let timelineState = {
    allData: [],
    allCommits: [],
    currentPeriodStart: null,
    currentPeriodEnd: null,
    zoomLevel: 'month', // month, week, day
    currentTopic: '',
    currentProject: '',
    showSessions: true,
    showCommits: true,
    customRangeMode: false, // When true, use custom start/end dates
    isPanning: false, // For CMD+Click drag navigation
    panStartX: 0,
    panStartDate: null
};

// Smart tooltip positioning that ALWAYS maintains complete separation from mouse cursor
// Intelligently selects quadrant with most space and ensures 250px+ separation
function positionTooltipAwayFromCursor(mouseX, mouseY, element) {
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

    const padding = 30;
    const minSeparation = 250; // Minimum 250px separation from cursor

    // Calculate available space in each quadrant
    const spaceLeft = mouseX - padding;
    const spaceRight = viewportWidth - mouseX - padding;
    const spaceTop = mouseY - padding;
    const spaceBottom = viewportHeight - mouseY - padding;

    let x, y;

    // Priority: Try to place in quadrant with most horizontal space
    // 1. Try LEFT and UP (best for keeping cursor visible)
    if (spaceLeft >= width + minSeparation && spaceTop >= height) {
        x = mouseX - minSeparation - width;
        y = Math.max(padding, mouseY - height - 50);
    }
    // 2. Try LEFT and DOWN
    else if (spaceLeft >= width + minSeparation && spaceBottom >= height) {
        x = mouseX - minSeparation - width;
        y = Math.min(viewportHeight - height - padding, mouseY + 50);
    }
    // 3. Try RIGHT and UP
    else if (spaceRight >= width + minSeparation && spaceTop >= height) {
        x = mouseX + minSeparation;
        y = Math.max(padding, mouseY - height - 50);
    }
    // 4. Try RIGHT and DOWN
    else if (spaceRight >= width + minSeparation && spaceBottom >= height) {
        x = mouseX + minSeparation;
        y = Math.min(viewportHeight - height - padding, mouseY + 50);
    }
    // 5. Emergency fallback - place in largest quadrant, maximize separation
    else {
        if (spaceLeft > spaceRight) {
            x = Math.max(padding, mouseX - width - 100);
        } else {
            x = Math.min(viewportWidth - width - padding, mouseX + 100);
        }

        if (spaceTop > spaceBottom) {
            y = Math.max(padding, mouseY - height - 100);
        } else {
            y = Math.min(viewportHeight - height - padding, mouseY + 100);
        }
    }

    // Final safety constraint - ensure within viewport
    x = Math.max(padding, Math.min(x, viewportWidth - width - padding));
    y = Math.max(padding, Math.min(y, viewportHeight - height - padding));

    return { x, y };
}

// Simple viewport constraint for centered panels (not tooltips)
function constrainToViewport(x, y, element) {
    element.offsetWidth; // Trigger reflow

    const rect = element.getBoundingClientRect();
    const viewportWidth = window.innerWidth;
    const viewportHeight = window.innerHeight;

    let width = rect.width;
    let height = rect.height;

    if (width === 0 || height === 0) {
        const computed = window.getComputedStyle(element);
        width = parseInt(computed.width) || 400;
        height = parseInt(computed.height) || 300;
    }

    const padding = 30;

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

// Show date range selection modal
function showDateRangeModal(nav) {
    // Create modal if it doesn't exist
    let modal = document.getElementById('timeline-date-range-modal');
    if (!modal) {
        modal = document.createElement('div');
        modal.id = 'timeline-date-range-modal';
        modal.style.cssText = `
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: rgba(0, 0, 0, 0.6);
            backdrop-filter: blur(4px);
            z-index: 5000;
            display: flex;
            align-items: center;
            justify-content: center;
        `;

        // Get earliest and latest dates from all data
        const allDates = [...timelineState.allData.map(d => d.date), ...timelineState.allCommits.map(d => d.date)];
        const minDate = d3.min(allDates);
        const maxDate = d3.max(allDates);

        // Format dates for input fields (YYYY-MM-DD)
        const formatDate = (date) => {
            const year = date.getFullYear();
            const month = String(date.getMonth() + 1).padStart(2, '0');
            const day = String(date.getDate()).padStart(2, '0');
            return `${year}-${month}-${day}`;
        };

        // Default to last 30 days
        const defaultEnd = new Date();
        const defaultStart = new Date();
        defaultStart.setDate(defaultStart.getDate() - 30);

        modal.innerHTML = `
            <div style="background: var(--bg-primary); border-radius: var(--radius-lg); padding: var(--space-6); max-width: 500px; width: 90%; box-shadow: var(--shadow-2xl); border: 2px solid var(--primary-500);">
                <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: var(--space-4);">
                    <h3 style="margin: 0; color: var(--text-primary); font-size: 20px; font-weight: 600;">📅 Select Date Range</h3>
                    <button onclick="document.getElementById('timeline-date-range-modal').style.display='none'" style="background: none; border: none; font-size: 24px; cursor: pointer; color: var(--text-secondary); padding: 0; width: 32px; height: 32px; display: flex; align-items: center; justify-content: center; border-radius: 4px; transition: all 0.2s;" onmouseover="this.style.background='var(--bg-tertiary)'" onmouseout="this.style.background='none'">×</button>
                </div>

                <div style="margin-bottom: var(--space-6);">
                    <p style="color: var(--text-secondary); font-size: 14px; margin-bottom: var(--space-4);">
                        Available data range: <strong>${minDate.toLocaleDateString()}</strong> to <strong>${maxDate.toLocaleDateString()}</strong>
                    </p>

                    <div style="display: grid; gap: var(--space-4);">
                        <div>
                            <label for="timeline-start-date" style="display: block; font-weight: 600; margin-bottom: var(--space-2); color: var(--text-primary);">Start Date:</label>
                            <input type="date" id="timeline-start-date" class="form-control"
                                   min="${formatDate(minDate)}"
                                   max="${formatDate(maxDate)}"
                                   value="${formatDate(defaultStart)}"
                                   style="width: 100%; padding: var(--space-2); border: 2px solid var(--border-primary); border-radius: var(--radius-sm); font-size: 14px;">
                        </div>

                        <div>
                            <label for="timeline-end-date" style="display: block; font-weight: 600; margin-bottom: var(--space-2); color: var(--text-primary);">End Date:</label>
                            <input type="date" id="timeline-end-date" class="form-control"
                                   min="${formatDate(minDate)}"
                                   max="${formatDate(maxDate)}"
                                   value="${formatDate(defaultEnd)}"
                                   style="width: 100%; padding: var(--space-2); border: 2px solid var(--border-primary); border-radius: var(--radius-sm); font-size: 14px;">
                        </div>
                    </div>
                </div>

                <div style="margin-bottom: var(--space-6);">
                    <h4 style="margin-bottom: var(--space-3); color: var(--text-primary); font-size: 14px; font-weight: 600;">Quick Presets:</h4>
                    <div style="display: grid; grid-template-columns: repeat(2, 1fr); gap: var(--space-2);">
                        <button class="btn btn-secondary" onclick="window.setDateRangePreset('today')" style="font-size: 13px; padding: var(--space-2);">📍 Today</button>
                        <button class="btn btn-secondary" onclick="window.setDateRangePreset('week')" style="font-size: 13px; padding: var(--space-2);">📅 This Week</button>
                        <button class="btn btn-secondary" onclick="window.setDateRangePreset('month')" style="font-size: 13px; padding: var(--space-2);">🗓️ This Month</button>
                        <button class="btn btn-secondary" onclick="window.setDateRangePreset('all')" style="font-size: 13px; padding: var(--space-2);">🌐 All Data</button>
                    </div>
                </div>

                <div style="display: flex; gap: var(--space-3); justify-content: flex-end;">
                    <button onclick="document.getElementById('timeline-date-range-modal').style.display='none'" class="btn btn-secondary" style="padding: var(--space-3) var(--space-4);">
                        Cancel
                    </button>
                    <button onclick="window.applyDateRange()" class="btn btn-primary" style="padding: var(--space-3) var(--space-4);">
                        ✓ Apply Range
                    </button>
                </div>
            </div>
        `;

        document.body.appendChild(modal);

        // Close modal on escape key
        document.addEventListener('keydown', (e) => {
            if (e.key === 'Escape' && modal.style.display !== 'none') {
                modal.style.display = 'none';
            }
        });

        // Close modal on background click
        modal.addEventListener('click', (e) => {
            if (e.target === modal) {
                modal.style.display = 'none';
            }
        });
    }

    modal.style.display = 'flex';
}

// Set date range presets
window.setDateRangePreset = function(preset) {
    const allDates = [...timelineState.allData.map(d => d.date), ...timelineState.allCommits.map(d => d.date)];
    const minDate = d3.min(allDates);
    const maxDate = d3.max(allDates);

    const formatDate = (date) => {
        const year = date.getFullYear();
        const month = String(date.getMonth() + 1).padStart(2, '0');
        const day = String(date.getDate()).padStart(2, '0');
        return `${year}-${month}-${day}`;
    };

    let startDate, endDate;
    const now = new Date();

    switch (preset) {
        case 'today':
            startDate = new Date(now);
            startDate.setHours(0, 0, 0, 0);
            endDate = new Date(now);
            endDate.setHours(23, 59, 59, 999);
            break;
        case 'week':
            endDate = new Date(now);
            startDate = new Date(now);
            startDate.setDate(startDate.getDate() - 7);
            break;
        case 'month':
            endDate = new Date(now);
            startDate = new Date(now);
            startDate.setMonth(startDate.getMonth() - 1);
            break;
        case 'all':
            startDate = minDate;
            endDate = maxDate;
            break;
    }

    document.getElementById('timeline-start-date').value = formatDate(startDate);
    document.getElementById('timeline-end-date').value = formatDate(endDate);
};

// Apply custom date range
window.applyDateRange = function() {
    const startInput = document.getElementById('timeline-start-date').value;
    const endInput = document.getElementById('timeline-end-date').value;

    if (!startInput || !endInput) {
        alert('Please select both start and end dates');
        return;
    }

    const startDate = new Date(startInput);
    const endDate = new Date(endInput);

    // Set time to beginning/end of day
    startDate.setHours(0, 0, 0, 0);
    endDate.setHours(23, 59, 59, 999);

    if (startDate > endDate) {
        alert('Start date must be before end date');
        return;
    }

    // Update timeline state
    timelineState.customRangeMode = true;
    timelineState.currentPeriodStart = startDate;
    timelineState.currentPeriodEnd = endDate;

    // Hide modal and refresh timeline
    document.getElementById('timeline-date-range-modal').style.display = 'none';

    // Get nav object from window
    if (window.currentNav) {
        initD3TimelineEnhanced(timelineState.allData, window.currentNav);
    }
};

async function initD3TimelineEnhanced(data, nav) {
    // Store nav reference globally for modal callbacks
    window.currentNav = nav;
    timelineState.allData = data;

    // Load git commits
    try {
        const gitData = await window.dashboardData.loadGitCommits();
        timelineState.allCommits = gitData.commits.map(commit => ({
            ...commit,
            date: new Date(commit.date),
            type: 'commit'
        }));
        console.log(`✓ Loaded ${timelineState.allCommits.length} git commits`);
    } catch (error) {
        console.warn('⚠️  Could not load git commits:', error);
        timelineState.allCommits = [];
    }

    // Initialize period to show latest data
    if (!timelineState.currentPeriodStart) {
        const latestDate = d3.max(data, d => d.date);
        timelineState.currentPeriodEnd = latestDate;
        timelineState.currentPeriodStart = calculatePeriodStart(latestDate, timelineState.zoomLevel);
    }

    // Filter data to current period
    const periodData = data.filter(d =>
        d.date >= timelineState.currentPeriodStart &&
        d.date <= timelineState.currentPeriodEnd &&
        timelineState.showSessions
    );

    const periodCommits = timelineState.allCommits.filter(d =>
        d.date >= timelineState.currentPeriodStart &&
        d.date <= timelineState.currentPeriodEnd &&
        timelineState.showCommits
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

    // Create SVG with CMD+Click drag panning
    const svgContainer = d3.select('#timeline-chart')
        .append('svg')
        .attr('width', width + margin.left + margin.right)
        .attr('height', height + margin.top + margin.bottom);

    // Add panning rectangle for CMD+Click drag
    svgContainer.append('rect')
        .attr('class', 'pan-background')
        .attr('width', width + margin.left + margin.right)
        .attr('height', height + margin.top + margin.bottom)
        .style('fill', 'transparent')
        .style('cursor', 'default')
        .on('mousedown', function(event) {
            // Check for CMD (Mac) or Ctrl (Windows/Linux) key
            if (event.metaKey || event.ctrlKey) {
                event.preventDefault();
                timelineState.isPanning = true;
                timelineState.panStartX = event.clientX;
                timelineState.panStartDate = new Date(timelineState.currentPeriodEnd);
                d3.select(this).style('cursor', 'grabbing');
            }
        });

    const svg = svgContainer
        .append('g')
        .attr('transform', `translate(${margin.left},${margin.top})`);

    // Add "Git Commits:" label to main SVG (before transformation)
    if (periodCommits.length > 0) {
        svgContainer.append('text')
            .attr('x', 5)
            .attr('y', 0)
            .style('font-size', '20px')
            .style('font-weight', '700')
            .style('fill', 'var(--text-primary)')
            .style('text-anchor', 'start')
            .style('dominant-baseline', 'hanging')
            .text('Git Commits:');
    }

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
        .style('pointer-events', 'none')
        .style('cursor', 'move')
        .style('z-index', '9999')
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
            tooltip
                .style('visibility', 'hidden')
                .style('pointer-events', 'none');
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

            // Set initial position using smart positioning to ALWAYS maintain complete separation from cursor
            // Intelligently selects best quadrant and ensures 250px+ separation in all directions
            const tooltipNode = tooltip.node();
            const position = positionTooltipAwayFromCursor(event.clientX, event.clientY, tooltipNode);
            tooltip
                .style('left', position.x + 'px')
                .style('top', position.y + 'px')
                .style('visibility', 'visible');

            // Enable pointer events after a short delay to allow dragging
            setTimeout(() => {
                if (tooltip.style('visibility') === 'visible') {
                    tooltip.style('pointer-events', 'auto');
                }
            }, 100);
        })
        .on('mousemove', function(event) {
            // Disable position updates on mousemove to prevent shaking
            // Tooltip position is set once on mouseover
        })
        .on('mouseout', function(event, d) {
            d3.select(this)
                .transition()
                .duration(150)
                .style('opacity', 0.75)
                .attr('r', sizeScale(d.messageCount));

            tooltip
                .style('visibility', 'hidden')
                .style('pointer-events', 'none');
        })
        .on('click', function(event, d) {
            console.log('Session bubble clicked!', d);
            event.stopPropagation();
            event.preventDefault();

            // Hide tooltip when session is clicked
            tooltip
                .style('visibility', 'hidden')
                .style('pointer-events', 'none');

            // Show detail panel
            console.log('Calling showDetailPanel...');
            showDetailPanel(d, nav);
        })
        .style('cursor', 'pointer');

    // Plot git commits as squares (separate row above sessions)
    const commitYPosition = -40; // Positioned above the chart area (negative y = above)

    // Group commits by date to add horizontal offset for same-day commits
    const commitsByDate = d3.group(periodCommits, d => d.date.toDateString());
    let commitIndex = 0;

    svg.selectAll('.commit-marker')
        .data(periodCommits)
        .enter()
        .append('path')
        .attr('class', 'commit-marker')
        .attr('d', d3.symbol().type(d3.symbolSquare).size(1024)) // Increased to 1024 (32x32 pixels)
        .attr('transform', d => {
            // Add small horizontal offset for commits on same day
            const sameDayCommits = commitsByDate.get(d.date.toDateString());
            const indexInDay = sameDayCommits.indexOf(d);
            const offset = (indexInDay - (sameDayCommits.length - 1) / 2) * 8; // 8px spacing for larger squares
            return `translate(${xScale(d.date) + offset},${commitYPosition})`;
        })
        .style('fill', (d, i) => {
            // Alternate between blue and green for easy differentiation
            return i % 2 === 0 ? '#3b82f6' : '#22c55e'; // Blue (#3b82f6) and Green (#22c55e)
        })
        .style('opacity', 0.85)
        .style('stroke', '#fff')
        .style('stroke-width', '3px')
        .style('cursor', 'pointer')
        .attr('data-commit-index', (d, i) => i)
        .on('mouseover', function(event, d) {
            d3.select(this)
                .transition()
                .duration(150)
                .style('opacity', 1)
                .attr('d', d3.symbol().type(d3.symbolSquare).size(1600)); // Increased to 1600 (40x40 pixels on hover)

            tooltip
                .html(`
                    <div style="color: var(--text-primary);">
                        <strong style="display: block; margin-bottom: 10px; font-size: 15px; color: #22c55e;">
                            🔧 ${nav.escapeHtml(d.subject).substring(0, 80)}${d.subject?.length > 80 ? '...' : ''}
                        </strong>
                        <div style="font-size: 13px; line-height: 1.6;">
                            <div style="margin-bottom: 6px;"><strong>📅 Date:</strong> ${d.date.toLocaleString()}</div>
                            <div style="margin-bottom: 6px;"><strong>👤 Author:</strong> ${d.author}</div>
                            <div style="margin-bottom: 6px;"><strong>🏷️ Type:</strong> ${d.type}</div>
                            <div style="margin-bottom: 6px;"><strong>🔗 Commit:</strong> <code>${d.short_hash}</code></div>
                            ${d.body ? `<div style="margin-top: 8px; padding: 8px; background: var(--bg-secondary); border-radius: 4px; max-height: 150px; overflow-y: auto;">${nav.escapeHtml(d.body).substring(0, 300)}${d.body.length > 300 ? '...' : ''}</div>` : ''}
                            ${d.github_url ? `<div style="margin-top: 10px; padding-top: 10px; border-top: 2px solid var(--border-primary); font-size: 12px; color: #22c55e; font-weight: 600;">
                                🔗 Click to view on GitHub →
                            </div>` : ''}
                        </div>
                    </div>
                `);

            // Use smart positioning to ALWAYS maintain complete separation from cursor
            // Intelligently selects best quadrant and ensures 250px+ separation in all directions
            const tooltipNode = tooltip.node();
            const position = positionTooltipAwayFromCursor(event.clientX, event.clientY, tooltipNode);
            tooltip
                .style('left', position.x + 'px')
                .style('top', position.y + 'px')
                .style('visibility', 'visible');

            // Enable pointer events after a short delay to allow dragging
            setTimeout(() => {
                if (tooltip.style('visibility') === 'visible') {
                    tooltip.style('pointer-events', 'auto');
                }
            }, 100);
        })
        .on('mousemove', function(event) {
            // Disable position updates on mousemove to prevent shaking
            // Tooltip position is set once on mouseover
        })
        .on('mouseout', function(event, d) {
            d3.select(this)
                .transition()
                .duration(150)
                .style('opacity', 0.85)
                .attr('d', d3.symbol().type(d3.symbolSquare).size(1024)); // Restore to 32x32 default size

            tooltip
                .style('visibility', 'hidden')
                .style('pointer-events', 'none');
        })
        .on('click', function(event, d) {
            console.log('Commit square clicked!', d);
            event.stopPropagation();
            event.preventDefault();

            tooltip
                .style('visibility', 'hidden')
                .style('pointer-events', 'none');

            // Show commit detail panel
            console.log('Calling showCommitDetailPanel...');
            showCommitDetailPanel(d, nav);
        })
        .style('cursor', 'pointer');

    // Setup navigation handlers
    setupNavigationHandlers(nav);

    // Setup zoom level handler
    document.getElementById('timeline-zoom-level').onchange = (e) => {
        timelineState.zoomLevel = e.target.value;
        // Recalculate period based on new zoom level
        timelineState.currentPeriodStart = calculatePeriodStart(timelineState.currentPeriodEnd, timelineState.zoomLevel);
        initD3TimelineEnhanced(data, nav);
    };

    // Setup filter handlers
    document.getElementById('timeline-show-sessions').onchange = (e) => {
        timelineState.showSessions = e.target.checked;
        initD3TimelineEnhanced(data, nav);
    };

    document.getElementById('timeline-show-commits').onchange = (e) => {
        timelineState.showCommits = e.target.checked;
        initD3TimelineEnhanced(data, nav);
    };

    // Setup CMD+Click drag panning handlers (document-level for smooth panning)
    document.addEventListener('mousemove', (event) => {
        if (timelineState.isPanning) {
            const panRect = d3.select('.pan-background').node();
            if (panRect) {
                panRect.style.cursor = 'grabbing';
            }

            // Calculate drag distance
            const dragDistance = event.clientX - timelineState.panStartX;

            // Convert drag distance to time shift (pixels to milliseconds)
            // More sensitive panning: 1 pixel = portion of visible range
            const visibleRange = timelineState.currentPeriodEnd - timelineState.currentPeriodStart;
            const chartWidth = width; // Use actual chart width
            const timePerPixel = visibleRange / chartWidth;
            const timeShift = -dragDistance * timePerPixel; // Negative for natural drag direction

            // Calculate new period dates
            const newEnd = new Date(timelineState.panStartDate.getTime() + timeShift);
            const newStart = new Date(newEnd.getTime() - visibleRange);

            // Update timeline state
            timelineState.currentPeriodEnd = newEnd;
            timelineState.currentPeriodStart = newStart;
            timelineState.customRangeMode = true; // Enable custom mode when panning

            // Refresh timeline (debounce for performance)
            if (!timelineState.panDebounceTimer) {
                timelineState.panDebounceTimer = setTimeout(() => {
                    initD3TimelineEnhanced(data, nav);
                    timelineState.panDebounceTimer = null;
                }, 50); // 50ms debounce
            }
        }
    });

    document.addEventListener('mouseup', () => {
        if (timelineState.isPanning) {
            timelineState.isPanning = false;
            const panRect = d3.select('.pan-background').node();
            if (panRect) {
                panRect.style.cursor = 'default';
            }
            // Final refresh after panning completes
            if (timelineState.panDebounceTimer) {
                clearTimeout(timelineState.panDebounceTimer);
                timelineState.panDebounceTimer = null;
            }
            initD3TimelineEnhanced(data, nav);
        }
    });

    // Update cursor when CMD/Ctrl key is held over chart
    document.addEventListener('keydown', (event) => {
        if ((event.metaKey || event.ctrlKey) && !timelineState.isPanning) {
            const panRect = d3.select('.pan-background').node();
            if (panRect) {
                panRect.style.cursor = 'grab';
            }
        }
    });

    document.addEventListener('keyup', (event) => {
        if (!event.metaKey && !event.ctrlKey && !timelineState.isPanning) {
            const panRect = d3.select('.pan-background').node();
            if (panRect) {
                panRect.style.cursor = 'default';
            }
        }
    });
}

function calculatePeriodStart(endDate, zoomLevel) {
    const start = new Date(endDate);
    switch (zoomLevel) {
        case 'hour':
            start.setHours(start.getHours() - 1);
            break;
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
        case 'hour':
            return '%I:%M %p'; // 12-hour format with AM/PM (e.g., 02:35 PM)
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
        case 'hour':
            return 12; // 5-minute intervals: 0, 5, 10, 15, 20, 25, 30, 35, 40, 45, 50, 55 minutes
        case 'day':
            return 24;
        case 'week':
            return 7;
        case 'month':
        default:
            return 30;
    }
}

function getCommitColor(commitType) {
    const colors = {
        feat: '#22c55e',      // Green
        fix: '#ef4444',       // Red
        docs: '#3b82f6',      // Blue
        refactor: '#a855f7',  // Purple
        test: '#f59e0b',      // Orange
        chore: '#6b7280',     // Gray
        ci: '#8b5cf6',        // Violet
        style: '#ec4899',     // Pink
        perf: '#10b981',      // Emerald
        other: '#64748b'      // Slate
    };
    return colors[commitType] || colors.other;
}

function updatePeriodInfo() {
    const info = document.getElementById('timeline-period-info');
    if (info) {
        const zoomLabel = {
            'hour': 'Hourly (5min intervals)',
            'day': 'Daily',
            'week': 'Weekly',
            'month': 'Monthly'
        }[timelineState.zoomLevel];

        // For hourly view, show time; for others, show date
        let periodText;
        if (timelineState.zoomLevel === 'hour') {
            periodText = `${timelineState.currentPeriodStart.toLocaleString()} - ${timelineState.currentPeriodEnd.toLocaleString()}`;
        } else {
            periodText = `${timelineState.currentPeriodStart.toLocaleDateString()} - ${timelineState.currentPeriodEnd.toLocaleDateString()}`;
        }

        info.textContent = `📍 Viewing ${zoomLabel}: ${periodText}`;
    }
}

function setupNavigationHandlers(nav) {
    // Remove existing handlers
    const leftBtn = document.getElementById('timeline-nav-left');
    const rightBtn = document.getElementById('timeline-nav-right');
    const todayBtn = document.getElementById('timeline-nav-today');
    const customRangeBtn = document.getElementById('timeline-custom-range-btn');

    leftBtn.onclick = () => navigatePeriod(-1, nav);
    rightBtn.onclick = () => navigatePeriod(1, nav);
    todayBtn.onclick = () => navigateToToday(nav);

    if (customRangeBtn) {
        customRangeBtn.onclick = () => showDateRangeModal(nav);
    }
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

function showCommitDetailPanel(commit, nav) {
    const panel = document.getElementById('timeline-detail-panel');
    const title = document.getElementById('timeline-detail-title');
    const content = document.getElementById('timeline-detail-content');

    // Set title with commit type badge
    const typeColor = getCommitColor(commit.type);
    title.innerHTML = `
        <span style="display: inline-block; padding: 4px 12px; background: ${typeColor}; color: white; border-radius: 4px; font-size: 12px; font-weight: 600; margin-right: 10px;">
            ${commit.type.toUpperCase()}
        </span>
        <span>${nav.escapeHtml(commit.subject)}</span>
    `;

    content.innerHTML = `
        <div class="grid grid-cols-2" style="gap: var(--space-4); margin-bottom: var(--space-4);">
            <div class="stat-card">
                <h4>📅 Commit Date</h4>
                <p class="stat-value">${commit.date.toLocaleDateString()}</p>
                <p class="text-xs text-tertiary">${commit.date.toLocaleTimeString()}</p>
            </div>
            <div class="stat-card">
                <h4>👤 Author</h4>
                <p class="stat-value" style="font-size: 16px;">${nav.escapeHtml(commit.author)}</p>
            </div>
            <div class="stat-card">
                <h4>🔗 Commit Hash</h4>
                <p class="stat-value" style="font-family: monospace; font-size: 14px;">${commit.short_hash}</p>
                <p class="text-xs text-tertiary">${commit.hash ? commit.hash.substring(0, 16) + '...' : ''}</p>
            </div>
            <div class="stat-card">
                <h4>🏷️ Type</h4>
                <p class="stat-value">
                    <span style="display: inline-block; padding: 4px 12px; background: ${typeColor}; color: white; border-radius: 4px; font-size: 14px;">
                        ${commit.type}
                    </span>
                </p>
            </div>
        </div>

        ${commit.github_url ? `
            <div style="margin-bottom: var(--space-4);">
                <a href="${commit.github_url}" target="_blank" rel="noopener noreferrer"
                   style="display: inline-flex; align-items: center; justify-content: center; gap: 8px;
                          background: #0969da; color: #ffffff; font-weight: 600; font-size: 14px;
                          padding: 10px 16px; border-radius: 6px; text-decoration: none;
                          border: 2px solid #0969da; min-height: 44px; min-width: 44px;
                          transition: all 0.2s ease;"
                   onmouseover="this.style.background='#0550ae'; this.style.borderColor='#0550ae';"
                   onmouseout="this.style.background='#0969da'; this.style.borderColor='#0969da';"
                   onfocus="this.style.outline='3px solid #0969da'; this.style.outlineOffset='2px';"
                   onblur="this.style.outline='none';">
                    <svg style="width: 20px; height: 20px; fill: #ffffff;" viewBox="0 0 24 24" aria-hidden="true">
                        <path d="M12 0c-6.626 0-12 5.373-12 12 0 5.302 3.438 9.8 8.207 11.387.599.111.793-.261.793-.577v-2.234c-3.338.726-4.033-1.416-4.033-1.416-.546-1.387-1.333-1.756-1.333-1.756-1.089-.745.083-.729.083-.729 1.205.084 1.839 1.237 1.839 1.237 1.07 1.834 2.807 1.304 3.492.997.107-.775.418-1.305.762-1.604-2.665-.305-5.467-1.334-5.467-5.931 0-1.311.469-2.381 1.236-3.221-.124-.303-.535-1.524.117-3.176 0 0 1.008-.322 3.301 1.23.957-.266 1.983-.399 3.003-.404 1.02.005 2.047.138 3.006.404 2.291-1.552 3.297-1.23 3.297-1.23.653 1.653.242 2.874.118 3.176.77.84 1.235 1.911 1.235 3.221 0 4.609-2.807 5.624-5.479 5.921.43.372.823 1.102.823 2.222v3.293c0 .319.192.694.801.576 4.765-1.589 8.199-6.086 8.199-11.386 0-6.627-5.373-12-12-12z"/>
                    </svg>
                    <span>View on GitHub</span>
                </a>
            </div>
        ` : ''}

        <div style="margin-bottom: var(--space-4);">
            <h4 style="margin-bottom: var(--space-2); color: var(--text-primary);">📝 Commit Message</h4>
            <p style="color: var(--text-secondary); font-weight: 600; font-size: 15px;">${nav.escapeHtml(commit.subject)}</p>
        </div>

        ${commit.body ? `
            <div style="margin-bottom: var(--space-4);">
                <h4 style="margin-bottom: var(--space-2); color: var(--text-primary);">📄 Description</h4>
                <div style="padding: var(--space-3); background: var(--bg-tertiary); border-radius: var(--radius-sm); max-height: 300px; overflow-y: auto;">
                    <pre style="margin: 0; white-space: pre-wrap; font-family: 'SF Mono', Monaco, monospace; font-size: 13px; line-height: 1.6; color: var(--text-secondary);">${nav.escapeHtml(commit.body)}</pre>
                </div>
            </div>
        ` : ''}

        ${commit.files_changed && commit.files_changed.length > 0 ? `
            <div style="margin-bottom: var(--space-4);">
                <h4 style="margin-bottom: var(--space-2); color: var(--text-primary);">📂 Files Changed (${commit.files_changed.length})</h4>
                <div style="max-height: 200px; overflow-y: auto; background: var(--bg-tertiary); padding: var(--space-3); border-radius: var(--radius-sm);">
                    ${commit.files_changed.slice(0, 30).map(file => `
                        <div style="margin-bottom: var(--space-1); font-family: monospace; font-size: 12px; color: var(--text-secondary);">
                            📄 ${nav.escapeHtml(file)}
                        </div>
                    `).join('')}
                    ${commit.files_changed.length > 30 ? `<div style="margin-top: var(--space-2); font-style: italic; color: var(--text-tertiary);">...and ${commit.files_changed.length - 30} more</div>` : ''}
                </div>
            </div>
        ` : ''}

        <div style="margin-top: var(--space-4); padding-top: var(--space-3); border-top: 2px solid var(--border-primary); text-align: center;">
            <button onclick="document.getElementById('timeline-detail-panel').style.display='none'"
                    style="background: #ffffff; color: #24292f; font-weight: 600; font-size: 14px;
                           padding: 10px 20px; border-radius: 6px; border: 2px solid #d0d7de;
                           min-height: 44px; min-width: 44px; cursor: pointer;
                           transition: all 0.2s ease;"
                    onmouseover="this.style.background='#f6f8fa'; this.style.borderColor='#d0d7de';"
                    onmouseout="this.style.background='#ffffff'; this.style.borderColor='#d0d7de';"
                    onfocus="this.style.outline='3px solid #0969da'; this.style.outlineOffset='2px';"
                    onblur="this.style.outline='none';">
                Close
            </button>
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

        <div style="margin-top: var(--space-4); padding-top: var(--space-3); border-top: 1px solid var(--border-primary); text-align: center;">
            <a href="#checkpoints/${checkpoint.id}" class="btn btn-primary" style="padding: var(--space-2) var(--space-4); font-size: 13px; text-decoration: none;">
                View Details →
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

// Show detailed session information panel
function showDetailPanel(sessionData, nav) {
    console.log('showDetailPanel called with:', sessionData);
    const panel = document.getElementById('timeline-detail-panel');
    const content = document.getElementById('detail-panel-content');

    console.log('Panel element:', panel);
    console.log('Content element:', content);

    if (!panel || !content) {
        console.error('Panel or content element not found!');
        return;
    }

    // Format the session details
    content.innerHTML = `
        <div style="margin-bottom: var(--space-6);">
            <h2 style="margin: 0 0 var(--space-4) 0; color: var(--primary-500); font-size: 24px;">
                Session Details
            </h2>
            <button onclick="document.getElementById('timeline-detail-panel').style.display='none'"
                    style="position: absolute; top: var(--space-4); right: var(--space-4); background: #ffffff; color: #24292f; font-weight: 600; font-size: 14px; padding: 10px 20px; border-radius: 6px; border: 2px solid #d0d7de; min-height: 44px; min-width: 44px; cursor: pointer; transition: all 0.2s ease;"
                    onmouseover="this.style.background='#f6f8fa'; this.style.borderColor='#d0d7de';"
                    onmouseout="this.style.background='#ffffff'; this.style.borderColor='#d0d7de';"
                    onfocus="this.style.outline='3px solid #0969da'; this.style.outlineOffset='2px';"
                    onblur="this.style.outline='none';">
                Close
            </button>
        </div>

        <div style="display: grid; gap: var(--space-4);">
            <div>
                <div style="font-weight: 600; color: var(--text-secondary); margin-bottom: var(--space-2);">Title</div>
                <div style="font-size: 18px; color: var(--text-primary);">${sessionData.title || 'Untitled Session'}</div>
            </div>

            <div>
                <div style="font-weight: 600; color: var(--text-secondary); margin-bottom: var(--space-2);">Date</div>
                <div style="color: var(--text-primary);">${sessionData.date.toLocaleDateString('en-US', { weekday: 'long', year: 'numeric', month: 'long', day: 'numeric' })}</div>
            </div>

            <div>
                <div style="font-weight: 600; color: var(--text-secondary); margin-bottom: var(--space-2);">Messages</div>
                <div style="color: var(--text-primary); font-size: 20px; font-weight: 600;">${sessionData.messageCount.toLocaleString()}</div>
            </div>

            ${sessionData.filename ? `
                <div>
                    <div style="font-weight: 600; color: var(--text-secondary); margin-bottom: var(--space-2);">Filename</div>
                    <div style="color: var(--text-primary); font-family: monospace; background: var(--bg-secondary); padding: var(--space-2); border-radius: var(--radius-sm);">${sessionData.filename}</div>
                </div>
            ` : ''}

            ${sessionData.topics && sessionData.topics.length > 0 ? `
                <div>
                    <div style="font-weight: 600; color: var(--text-secondary); margin-bottom: var(--space-2);">Topics</div>
                    <div style="display: flex; flex-wrap: wrap; gap: var(--space-2);">
                        ${sessionData.topics.map(topic => `
                            <span style="background: var(--primary-100); color: var(--primary-700); padding: 4px 12px; border-radius: var(--radius-full); font-size: 13px; font-weight: 500;">
                                ${topic}
                            </span>
                        `).join('')}
                    </div>
                </div>
            ` : ''}

            ${sessionData.summary ? `
                <div>
                    <div style="font-weight: 600; color: var(--text-secondary); margin-bottom: var(--space-2);">Summary</div>
                    <div style="color: var(--text-primary); line-height: 1.6;">${sessionData.summary}</div>
                </div>
            ` : ''}
        </div>
    `;

    console.log('Setting session panel display to block');
    panel.style.display = 'block';
    console.log('Session panel display is now:', panel.style.display);
    console.log('Session panel computed display:', window.getComputedStyle(panel).display);
}

// Show detailed commit information panel
function showCommitDetailPanel(commitData, nav) {
    console.log('showCommitDetailPanel called with:', commitData);
    const panel = document.getElementById('timeline-detail-panel');
    const content = document.getElementById('detail-panel-content');

    console.log('Commit Panel element:', panel);
    console.log('Commit Content element:', content);

    if (!panel || !content) {
        console.error('Commit panel or content element not found!');
        return;
    }

    // Format the commit details
    content.innerHTML = `
        <div style="margin-bottom: var(--space-6);">
            <h2 style="margin: 0 0 var(--space-4) 0; color: var(--primary-500); font-size: 24px;">
                Git Commit Details
            </h2>
            <button onclick="document.getElementById('timeline-detail-panel').style.display='none'"
                    style="position: absolute; top: var(--space-4); right: var(--space-4); background: #ffffff; color: #24292f; font-weight: 600; font-size: 14px; padding: 10px 20px; border-radius: 6px; border: 2px solid #d0d7de; min-height: 44px; min-width: 44px; cursor: pointer; transition: all 0.2s ease;"
                    onmouseover="this.style.background='#f6f8fa'; this.style.borderColor='#d0d7de';"
                    onmouseout="this.style.background='#ffffff'; this.style.borderColor='#d0d7de';"
                    onfocus="this.style.outline='3px solid #0969da'; this.style.outlineOffset='2px';"
                    onblur="this.style.outline='none';">
                Close
            </button>
        </div>

        <div style="display: grid; gap: var(--space-4);">
            ${commitData.github_url ? `
                <div style="margin-bottom: var(--space-4);">
                    <a href="${commitData.github_url}" target="_blank" rel="noopener noreferrer"
                       style="display: inline-flex; align-items: center; justify-content: center; gap: 8px; background: #0969da; color: #ffffff; font-weight: 600; font-size: 14px; padding: 10px 16px; border-radius: 6px; text-decoration: none; border: 2px solid #0969da; min-height: 44px; min-width: 44px; transition: all 0.2s ease;"
                       onmouseover="this.style.background='#0550ae'; this.style.borderColor='#0550ae';"
                       onmouseout="this.style.background='#0969da'; this.style.borderColor='#0969da';"
                       onfocus="this.style.outline='3px solid #0969da'; this.style.outlineOffset='2px';"
                       onblur="this.style.outline='none';">
                        <svg style="width: 20px; height: 20px; fill: #ffffff;" viewBox="0 0 24 24" aria-hidden="true">
                            <path d="M12 0c-6.626 0-12 5.373-12 12 0 5.302 3.438 9.8 8.207 11.387.599.111.793-.261.793-.577v-2.234c-3.338.726-4.033-1.416-4.033-1.416-.546-1.387-1.333-1.756-1.333-1.756-1.089-.745.083-.729.083-.729 1.205.084 1.839 1.237 1.839 1.237 1.07 1.834 2.807 1.304 3.492.997.107-.775.418-1.305.762-1.604-2.665-.305-5.467-1.334-5.467-5.931 0-1.311.469-2.381 1.236-3.221-.124-.303-.535-1.524.117-3.176 0 0 1.008-.322 3.301 1.23.957-.266 1.983-.399 3.003-.404 1.02.005 2.047.138 3.006.404 2.291-1.552 3.297-1.23 3.297-1.23.653 1.653.242 2.874.118 3.176.77.84 1.235 1.911 1.235 3.221 0 4.609-2.807 5.624-5.479 5.921.43.372.823 1.102.823 2.222v3.293c0 .319.192.694.801.576 4.765-1.589 8.199-6.086 8.199-11.386 0-6.627-5.373-12-12-12z"/>
                        </svg>
                        <span>View on GitHub</span>
                    </a>
                </div>
            ` : ''}

            <div>
                <div style="font-weight: 600; color: var(--text-secondary); margin-bottom: var(--space-2);">Commit Message</div>
                <div style="font-size: 16px; color: var(--text-primary); line-height: 1.6;">${commitData.message || 'No message'}</div>
            </div>

            <div>
                <div style="font-weight: 600; color: var(--text-secondary); margin-bottom: var(--space-2);">Date</div>
                <div style="color: var(--text-primary);">${commitData.date.toLocaleDateString('en-US', { weekday: 'long', year: 'numeric', month: 'long', day: 'numeric', hour: '2-digit', minute: '2-digit' })}</div>
            </div>

            ${commitData.author ? `
                <div>
                    <div style="font-weight: 600; color: var(--text-secondary); margin-bottom: var(--space-2);">Author</div>
                    <div style="color: var(--text-primary);">${commitData.author}</div>
                </div>
            ` : ''}

            ${commitData.hash ? `
                <div>
                    <div style="font-weight: 600; color: var(--text-secondary); margin-bottom: var(--space-2);">Commit Hash</div>
                    <div style="color: var(--text-primary); font-family: monospace; background: var(--bg-secondary); padding: var(--space-2); border-radius: var(--radius-sm);">${commitData.hash}</div>
                </div>
            ` : ''}

            ${commitData.files ? `
                <div>
                    <div style="font-weight: 600; color: var(--text-secondary); margin-bottom: var(--space-2);">Files Changed</div>
                    <div style="color: var(--text-primary); font-size: 20px; font-weight: 600;">${commitData.files}</div>
                </div>
            ` : ''}
        </div>
    `;

    console.log('Setting commit panel display to block');
    panel.style.display = 'block';
    console.log('Commit panel display is now:', panel.style.display);
    console.log('Commit panel computed display:', window.getComputedStyle(panel).display);
}

// Export for use in navigation.js
if (typeof window !== 'undefined') {
    window.initD3TimelineEnhanced = initD3TimelineEnhanced;
    window.showDateRangeModal = showDateRangeModal;
    window.showDetailPanel = showDetailPanel;
    window.showCommitDetailPanel = showCommitDetailPanel;
}
