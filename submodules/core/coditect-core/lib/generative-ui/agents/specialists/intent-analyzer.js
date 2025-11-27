"use strict";
/**
 * Intent Analyzer Agent
 * Parses user requirements and converts them into structured UI specifications
 * @module agents/specialists/intent-analyzer
 */
Object.defineProperty(exports, "__esModule", { value: true });
exports.IntentAnalyzer = void 0;
const base_1 = require("../base");
/**
 * Intent Analyzer Agent
 * Analyzes user intent and generates structured UI specifications
 */
class IntentAnalyzer extends base_1.BaseAgent {
    constructor() {
        super({
            name: 'intent-analyzer',
            role: base_1.AgentRole.SPECIALIST,
            description: 'Analyzes user intent and converts to structured UI specifications',
            capabilities: [
                'parse-natural-language',
                'extract-requirements',
                'identify-ui-patterns',
                'suggest-components',
            ],
        });
    }
    /**
     * Execute intent analysis
     */
    async execute(input, _context) {
        this.log('info', 'Starting intent analysis', { input });
        if (!this.validateInput(input)) {
            return {
                success: false,
                error: {
                    message: 'Invalid input: description is required',
                    code: 'INVALID_INPUT',
                },
                tokens: { prompt: 0, completion: 0 },
            };
        }
        try {
            const spec = await this.analyzeIntent(input);
            this.log('info', 'Intent analysis complete', { spec });
            return {
                success: true,
                data: spec,
                tokens: {
                    prompt: this.estimateTokens(input),
                    completion: this.estimateTokens(spec),
                },
            };
        }
        catch (error) {
            this.log('error', 'Intent analysis failed', { error });
            return {
                success: false,
                error: {
                    message: error instanceof Error ? error.message : 'Unknown error',
                    code: 'ANALYSIS_FAILED',
                    details: error,
                },
                tokens: { prompt: 0, completion: 0 },
            };
        }
    }
    /**
     * Validate input
     */
    validateInput(input) {
        return !!input.description && input.description.trim().length > 0;
    }
    /**
     * Analyze user intent and generate UI spec
     */
    async analyzeIntent(input) {
        const { description, context } = input;
        // Detect UI type from description
        const type = this.detectUIType(description);
        // Extract framework preference
        const framework = context?.targetFramework || this.detectFramework(description);
        // Extract styling preference
        const styling = this.detectStyling(description);
        // Analyze requirements
        const requirements = this.extractRequirements(description);
        // Extract component-specific options
        const componentOptions = type === 'component'
            ? this.extractComponentOptions(description)
            : undefined;
        // Extract layout-specific options
        const layoutOptions = type === 'layout'
            ? this.extractLayoutOptions(description)
            : undefined;
        return {
            type,
            description,
            framework,
            styling,
            requirements,
            componentOptions,
            layoutOptions,
        };
    }
    /**
     * Detect UI type from description
     */
    detectUIType(description) {
        const lower = description.toLowerCase();
        if (lower.includes('dashboard') ||
            lower.includes('layout') ||
            lower.includes('page') ||
            lower.includes('wizard')) {
            return 'layout';
        }
        if (lower.includes('app') ||
            lower.includes('application') ||
            lower.includes('full')) {
            return 'application';
        }
        return 'component';
    }
    /**
     * Detect framework from description
     */
    detectFramework(description) {
        const lower = description.toLowerCase();
        if (lower.includes('vue'))
            return 'vue';
        if (lower.includes('svelte'))
            return 'svelte';
        return 'react'; // Default to React
    }
    /**
     * Detect styling approach from description
     */
    detectStyling(description) {
        const lower = description.toLowerCase();
        if (lower.includes('tailwind') || lower.includes('utility'))
            return 'tailwind';
        if (lower.includes('styled-components') || lower.includes('styled'))
            return 'styled-components';
        if (lower.includes('css modules'))
            return 'css-modules';
        return 'tailwind'; // Default to Tailwind
    }
    /**
     * Extract requirements from description
     */
    extractRequirements(description) {
        const lower = description.toLowerCase();
        return {
            accessibility: lower.includes('wcag aaa') || lower.includes('aaa') ? 'AAA' : 'AA',
            animations: lower.includes('animated') || lower.includes('motion'),
            responsive: !lower.includes('desktop only'),
            strictTypes: true, // Always enforce strict TypeScript
        };
    }
    /**
     * Extract component options from description
     */
    extractComponentOptions(description) {
        const lower = description.toLowerCase();
        // Extract variants
        const variants = [];
        if (lower.includes('primary'))
            variants.push('primary');
        if (lower.includes('secondary'))
            variants.push('secondary');
        if (lower.includes('ghost'))
            variants.push('ghost');
        if (lower.includes('outline'))
            variants.push('outline');
        // Extract sizes
        const sizes = [];
        if (lower.includes('small') || lower.includes('sm'))
            sizes.push('sm');
        if (lower.includes('medium') || lower.includes('md'))
            sizes.push('md');
        if (lower.includes('large') || lower.includes('lg'))
            sizes.push('lg');
        // Detect if stateful
        const stateful = lower.includes('state') || lower.includes('toggle') || lower.includes('controlled');
        return {
            variants: variants.length > 0 ? variants : ['primary'],
            sizes: sizes.length > 0 ? sizes : ['md'],
            stateful,
        };
    }
    /**
     * Extract layout options from description
     */
    extractLayoutOptions(description) {
        const lower = description.toLowerCase();
        // Detect pattern
        let pattern = 'dashboard';
        if (lower.includes('wizard') || lower.includes('multi-step'))
            pattern = 'wizard';
        if (lower.includes('landing'))
            pattern = 'landing';
        if (lower.includes('settings'))
            pattern = 'settings';
        // Extract sections
        const sections = [];
        if (lower.includes('sidebar'))
            sections.push('sidebar');
        if (lower.includes('header') || lower.includes('topbar'))
            sections.push('header');
        if (lower.includes('footer'))
            sections.push('footer');
        if (lower.includes('main') || lower.includes('content'))
            sections.push('main');
        return {
            pattern,
            sections: sections.length > 0 ? sections : ['header', 'main'],
        };
    }
}
exports.IntentAnalyzer = IntentAnalyzer;
//# sourceMappingURL=intent-analyzer.js.map