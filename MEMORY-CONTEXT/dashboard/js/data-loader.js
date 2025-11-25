// CODITECT Dashboard - Data Loading System (Task 1.4)
// Handles JSON data loading with caching and error handling
// Works with both file:// and http:// protocols

console.log('✓ Data loader module loading...');

/**
 * Data Loader
 * Loads JSON data files with caching, prefetching, and error handling
 */
class DataLoader {
    constructor() {
        this.cache = new Map();
        this.loading = new Map();
        this.errors = new Map();

        // Performance monitoring
        this.loadTimes = new Map();
        this.cacheHits = 0;
        this.cacheMisses = 0;

        console.log('✓ DataLoader initialized');
    }

    /**
     * Load JSON data file with caching
     * @param {string} path - Relative path to JSON file (e.g., 'data/checkpoints.json')
     * @returns {Promise<Object>} Parsed JSON data
     */
    async load(path) {
        // Check cache first
        if (this.cache.has(path)) {
            this.cacheHits++;
            console.log(`✓ Cache hit: ${path} (${this.cacheHits} hits, ${this.cacheMisses} misses)`);
            return this.cache.get(path);
        }

        // Check if already loading
        if (this.loading.has(path)) {
            console.log(`⏳ Already loading: ${path}`);
            return this.loading.get(path);
        }

        // Load fresh
        this.cacheMisses++;
        console.log(`⬇️  Loading: ${path}`);

        const loadPromise = this._loadFile(path);
        this.loading.set(path, loadPromise);

        try {
            const data = await loadPromise;
            this.cache.set(path, data);
            this.errors.delete(path);
            return data;
        } catch (error) {
            this.errors.set(path, error);
            throw error;
        } finally {
            this.loading.delete(path);
        }
    }

    async _loadFile(path) {
        const startTime = performance.now();

        try {
            const response = await fetch(path);

            if (!response.ok) {
                throw new Error(`HTTP ${response.status}: ${response.statusText}`);
            }

            const data = await response.json();

            const loadTime = performance.now() - startTime;
            this.loadTimes.set(path, loadTime);
            console.log(`✓ Loaded ${path} in ${loadTime.toFixed(2)}ms`);

            return data;
        } catch (error) {
            console.error(`❌ Failed to load ${path}:`, error.message);
            throw new Error(`Failed to load ${path}: ${error.message}`);
        }
    }

    /**
     * Preload multiple files in parallel
     * @param {string[]} paths - Array of file paths to preload
     */
    async preload(paths) {
        console.log(`⬇️  Preloading ${paths.length} files...`);

        try {
            await Promise.all(paths.map(path => this.load(path)));
            console.log(`✓ Preloaded ${paths.length} files`);
        } catch (error) {
            console.warn('⚠️  Some preloads failed:', error);
        }
    }

    /**
     * Clear cache for specific path or all cached data
     * @param {string} [path] - Optional specific path to clear
     */
    clearCache(path = null) {
        if (path) {
            this.cache.delete(path);
            console.log(`🗑️  Cleared cache: ${path}`);
        } else {
            this.cache.clear();
            console.log('🗑️  Cleared all cache');
        }
    }

    /**
     * Get cache statistics
     * @returns {Object} Cache performance stats
     */
    getStats() {
        const totalRequests = this.cacheHits + this.cacheMisses;
        const hitRate = totalRequests > 0
            ? ((this.cacheHits / totalRequests) * 100).toFixed(1)
            : 0;

        return {
            cacheSize: this.cache.size,
            cacheHits: this.cacheHits,
            cacheMisses: this.cacheMisses,
            hitRate: `${hitRate}%`,
            errors: this.errors.size,
            avgLoadTime: this._calculateAvgLoadTime()
        };
    }

    _calculateAvgLoadTime() {
        if (this.loadTimes.size === 0) return 0;

        const times = Array.from(this.loadTimes.values());
        const avg = times.reduce((a, b) => a + b, 0) / times.length;
        return `${avg.toFixed(2)}ms`;
    }

    /**
     * Check if data is cached
     * @param {string} path - File path to check
     * @returns {boolean}
     */
    isCached(path) {
        return this.cache.has(path);
    }

    /**
     * Get cached data without loading
     * @param {string} path - File path
     * @returns {Object|null} Cached data or null
     */
    getCached(path) {
        return this.cache.get(path) || null;
    }
}

/**
 * Dashboard Data Manager
 * Higher-level API for loading dashboard data
 */
class DashboardDataManager {
    constructor(dataLoader) {
        this.loader = dataLoader;
        this.dataFiles = {
            messages: 'data/messages.json',
            topics: 'data/topics.json',
            files: 'data/files.json',
            checkpoints: 'data/checkpoints.json',
            commands: 'data/commands.json',
            gitCommits: 'data/git-commits.json'
        };
    }

    /**
     * Load overview data (stats + recent activity)
     */
    async loadOverviewData() {
        console.log('📊 Loading overview data...');

        try {
            const [messages, topics, checkpoints, commands, files] = await Promise.all([
                this.loader.load(this.dataFiles.messages),
                this.loader.load(this.dataFiles.topics),
                this.loader.load(this.dataFiles.checkpoints),
                this.loader.load(this.dataFiles.commands),
                this.loader.load(this.dataFiles.files)
            ]);

            return {
                stats: {
                    totalMessages: messages.total_messages,
                    totalCheckpoints: checkpoints.checkpoints.length,
                    totalFiles: files.total_files || 0,
                    totalCommands: commands.commands.length
                },
                recentSessions: checkpoints.checkpoints.slice(0, 5),
                topTopics: topics.topics.slice(0, 6)
            };
        } catch (error) {
            console.error('❌ Failed to load overview data:', error);
            throw error;
        }
    }

    /**
     * Load all topics
     */
    async loadTopics() {
        console.log('🏷️  Loading topics...');
        const data = await this.loader.load(this.dataFiles.topics);
        return data.topics;
    }

    /**
     * Load all checkpoints
     */
    async loadCheckpoints() {
        console.log('💬 Loading checkpoints...');
        const data = await this.loader.load(this.dataFiles.checkpoints);
        return data.checkpoints;
    }

    /**
     * Load specific checkpoint by ID
     */
    async loadCheckpoint(id) {
        console.log(`💬 Loading checkpoint: ${id}`);
        const checkpoints = await this.loadCheckpoints();
        console.log(`📊 Total checkpoints loaded: ${checkpoints.length}`);
        console.log(`🔍 Searching for ID: "${id}"`);
        console.log(`🔍 First checkpoint ID: "${checkpoints[0]?.id}"`);

        const found = checkpoints.find(c => {
            const match = c.id === id;
            if (match) {
                console.log(`✅ Found matching checkpoint!`);
            }
            return match;
        });

        if (!found) {
            console.log(`❌ No match found. Checking for similar IDs...`);
            const similar = checkpoints.filter(c => c.id.includes('2025-11-17'));
            console.log(`📋 Checkpoints containing '2025-11-17':`, similar.map(c => c.id));
        }

        return found || null;
    }

    /**
     * Load checkpoint markdown file with git commit data
     */
    async loadCheckpointMarkdown(checkpointId) {
        console.log(`📄 Loading checkpoint markdown: ${checkpointId}`);

        // Try different possible paths
        const possiblePaths = [
            `../checkpoints/${checkpointId}.md`,
            `../../checkpoints/${checkpointId}.md`,
            `checkpoints/${checkpointId}.md`
        ];

        for (const path of possiblePaths) {
            try {
                const response = await fetch(path);
                if (response.ok) {
                    const markdown = await response.text();
                    console.log(`✓ Loaded checkpoint markdown from ${path}`);
                    return this.parseCheckpointMarkdown(markdown);
                }
            } catch (error) {
                // Continue to next path
            }
        }

        console.warn(`⚠️  Could not load checkpoint markdown for ${checkpointId}`);
        return null;
    }

    /**
     * Parse checkpoint markdown to extract git data
     */
    parseCheckpointMarkdown(markdown) {
        const data = {
            commits: [],
            branch: '',
            workingDirStatus: '',
            submodules: [],
            filesChanged: []
        };

        // Extract branch
        const branchMatch = markdown.match(/### Current Branch\s*```\s*([^\s]+)\s*```/);
        if (branchMatch) {
            data.branch = branchMatch[1];
        }

        // Extract recent commits
        const commitsMatch = markdown.match(/### Recent Commits\s*```\s*([\s\S]*?)```/);
        if (commitsMatch) {
            const commitLines = commitsMatch[1].trim().split('\n');
            data.commits = commitLines.map(line => {
                const match = line.match(/^([a-f0-9]+)\s+(.+)$/);
                if (match) {
                    return { hash: match[1], message: match[2] };
                }
                return null;
            }).filter(c => c !== null);
        }

        // Extract working directory status
        const statusMatch = markdown.match(/### Working Directory Status\s*```\s*([\s\S]*?)```/);
        if (statusMatch) {
            data.workingDirStatus = statusMatch[1].trim();
        }

        // Extract submodules
        const submoduleSection = markdown.match(/### Updated Submodules.*?\n\n([\s\S]*?)(?=\n---|\n##|$)/);
        if (submoduleSection) {
            const submoduleBlocks = submoduleSection[1].split('\n\n**');
            data.submodules = submoduleBlocks.map(block => {
                const nameMatch = block.match(/^([^\*]+)/);
                const commitMatch = block.match(/- Commit: `([^`]+)`/);
                const latestMatch = block.match(/- Latest: ([a-f0-9]+)\s+(.+)/);

                if (nameMatch) {
                    return {
                        name: nameMatch[1].replace('**', '').trim(),
                        commit: commitMatch ? commitMatch[1] : '',
                        latest: latestMatch ? { hash: latestMatch[1], message: latestMatch[2] } : null
                    };
                }
                return null;
            }).filter(s => s !== null);
        }

        return data;
    }

    /**
     * Load all commands
     */
    async loadCommands() {
        console.log('⚡ Loading commands...');
        const data = await this.loader.load(this.dataFiles.commands);
        return data.commands;
    }

    /**
     * Load all files
     */
    async loadFiles() {
        console.log('📁 Loading files...');
        const data = await this.loader.load(this.dataFiles.files);
        return data;
    }

    /**
     * Load all git commits
     */
    async loadGitCommits() {
        console.log('🔀 Loading git commits...');
        const data = await this.loader.load(this.dataFiles.gitCommits);
        return data;
    }

    /**
     * Load git commits for specific checkpoint
     */
    async loadGitCommitsForCheckpoint(checkpointId) {
        console.log(`🔀 Loading git commits for: ${checkpointId}`);
        const data = await this.loadGitCommits();

        // Check if sessions property exists (it might not in current data structure)
        if (!data.sessions) {
            console.warn('⚠️  git-commits.json has no sessions property');
            console.log('📊 Available properties:', Object.keys(data));
            // Return empty structure instead of null to prevent rendering errors
            return {
                checkpoint_id: checkpointId,
                commits: [],
                branch: null,
                file_modified_time: null,
                file_created_time: null,
                working_dir_status: null,
                submodules: []
            };
        }

        const session = data.sessions.find(s => s.checkpoint_id === checkpointId);
        return session || {
            checkpoint_id: checkpointId,
            commits: [],
            branch: null,
            file_modified_time: null,
            file_created_time: null,
            working_dir_status: null,
            submodules: []
        };
    }

    /**
     * Load message page
     */
    async loadMessagePage(pageNum) {
        const paddedNum = String(pageNum).padStart(3, '0');
        const path = `data/messages-page-${paddedNum}.json`;
        console.log(`📄 Loading message page ${pageNum}...`);
        return await this.loader.load(path);
    }

    /**
     * Load messages filtered by topic tag
     */
    async loadMessagesByTopic(topicTag) {
        console.log(`🔍 Loading messages for topic: ${topicTag}`);

        // Load main messages file
        const messagesData = await this.loader.load(this.dataFiles.messages);

        // Filter messages by tag
        const filtered = messagesData.messages.filter(msg =>
            msg.tags && msg.tags.includes(topicTag)
        );

        console.log(`✓ Found ${filtered.length} messages with tag: ${topicTag}`);

        return filtered;
    }

    /**
     * Preload critical data for fast initial render
     */
    async preloadCritical() {
        console.log('⚡ Preloading critical data...');
        await this.loader.preload([
            this.dataFiles.messages,
            this.dataFiles.topics,
            this.dataFiles.checkpoints,
            this.dataFiles.commands
        ]);
    }

    /**
     * Preload message pages (adjacent to current)
     */
    async prefetchAdjacentPages(currentPage, totalPages = 103) {
        const pagesToPrefetch = [];

        // Prefetch previous page
        if (currentPage > 1) {
            pagesToPrefetch.push(currentPage - 1);
        }

        // Prefetch next page
        if (currentPage < totalPages) {
            pagesToPrefetch.push(currentPage + 1);
        }

        console.log(`⚡ Prefetching pages: ${pagesToPrefetch.join(', ')}`);

        await Promise.all(
            pagesToPrefetch.map(page =>
                this.loadMessagePage(page).catch(() => {}) // Ignore errors
            )
        );
    }
}

// Create global instances
window.dataLoader = new DataLoader();
window.dashboardData = new DashboardDataManager(window.dataLoader);

// Preload critical data on page load
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', () => {
        window.dashboardData.preloadCritical()
            .then(() => console.log('✓ Critical data preloaded'))
            .catch(err => console.warn('⚠️  Preload failed:', err));
    });
} else {
    window.dashboardData.preloadCritical()
        .then(() => console.log('✓ Critical data preloaded'))
        .catch(err => console.warn('⚠️  Preload failed:', err));
}

console.log('✓ Data loader module loaded');
