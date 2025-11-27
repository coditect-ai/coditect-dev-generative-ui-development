"use strict";
/**
 * UI Architect Agent
 * Designs component hierarchies and layout structures from UI specifications
 * @module agents/specialists/ui-architect
 */
Object.defineProperty(exports, "__esModule", { value: true });
exports.UIArchitect = void 0;
const base_1 = require("../base");
/**
 * UI Architect Agent
 * Designs component architectures and layout structures
 */
class UIArchitect extends base_1.BaseAgent {
    constructor() {
        super({
            name: 'ui-architect',
            role: base_1.AgentRole.SPECIALIST,
            description: 'Designs component hierarchies and layout structures',
            capabilities: [
                'design-component-hierarchy',
                'design-layout-structure',
                'recommend-patterns',
                'define-accessibility',
            ],
        });
    }
    /**
     * Execute UI architecture design
     */
    async execute(input, _context) {
        this.log('info', 'Starting UI architecture design', { spec: input });
        if (!this.validateInput(input)) {
            return {
                success: false,
                error: {
                    message: 'Invalid UI specification',
                    code: 'INVALID_SPEC',
                },
                tokens: { prompt: 0, completion: 0 },
            };
        }
        try {
            const architecture = await this.designArchitecture(input);
            this.log('info', 'UI architecture design complete', { architecture });
            // Calculate completion tokens from architecture size
            const completionTokens = Math.ceil(JSON.stringify(architecture).length / 4);
            return {
                success: true,
                data: architecture,
                tokens: {
                    prompt: this.estimateTokens(input),
                    completion: completionTokens,
                },
            };
        }
        catch (error) {
            this.log('error', 'UI architecture design failed', { error });
            return {
                success: false,
                error: {
                    message: error instanceof Error ? error.message : 'Unknown error',
                    code: 'DESIGN_FAILED',
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
        return !!input.type && !!input.description;
    }
    /**
     * Design UI architecture
     */
    async designArchitecture(spec) {
        if (spec.type === 'component') {
            return this.designComponent(spec);
        }
        else if (spec.type === 'layout') {
            return this.designLayout(spec);
        }
        else {
            return this.designApplication(spec);
        }
    }
    /**
     * Design component architecture
     */
    designComponent(spec) {
        const componentName = this.extractComponentName(spec.description);
        const variants = spec.componentOptions?.variants || ['default'];
        const component = {
            name: componentName,
            type: 'interactive',
            props: {
                variant: variants.length > 1 ? `'${variants.join("' | '")}'` : `'${variants[0]}'`,
                size: spec.componentOptions?.sizes
                    ? `'${spec.componentOptions.sizes.join("' | '")}'`
                    : "'md'",
                disabled: 'boolean',
                onClick: '() => void',
            },
            a11y: {
                role: 'button',
                keyboardNav: true,
            },
        };
        return {
            components: [component],
            patterns: ['compound-component', 'composition'],
            dependencies: [
                spec.framework === 'react' ? 'react' : spec.framework,
                spec.styling === 'tailwind' ? 'tailwindcss' : 'styled-components',
            ],
        };
    }
    /**
     * Design layout architecture
     */
    designLayout(spec) {
        const sections = spec.layoutOptions?.sections || ['header', 'main'];
        const layoutStructure = {
            pattern: 'grid',
            breakpoints: {
                sm: '640px',
                md: '768px',
                lg: '1024px',
                xl: '1280px',
            },
            sections: sections.map((name) => ({
                name,
                position: this.getLayoutPosition(name),
                components: [this.capitalize(name)],
            })),
        };
        const components = sections.map((name) => ({
            name: this.capitalize(name),
            type: 'container',
            props: {},
            a11y: {
                role: this.getSemanticRole(name),
            },
        }));
        return {
            components,
            layout: layoutStructure,
            patterns: ['layout-composition', 'responsive-design'],
            dependencies: [
                spec.framework === 'react' ? 'react' : spec.framework,
                'tailwindcss',
            ],
        };
    }
    /**
     * Design application architecture
     */
    designApplication(spec) {
        const mainLayout = this.designLayout({
            ...spec,
            type: 'layout',
            layoutOptions: {
                pattern: 'dashboard',
                sections: ['header', 'sidebar', 'main', 'footer'],
            },
        });
        return {
            ...mainLayout,
            patterns: [...(mainLayout.patterns || []), 'app-shell', 'routing'],
            dependencies: [
                ...(mainLayout.dependencies || []),
                'react-router-dom',
            ],
        };
    }
    /**
     * Extract component name from description
     */
    extractComponentName(description) {
        // Simple extraction - look for "Button", "Input", etc.
        const match = description.match(/\b([A-Z][a-z]+(?:[A-Z][a-z]+)*)\b/);
        return match?.[1] ?? 'Component';
    }
    /**
     * Get layout position for section
     */
    getLayoutPosition(section) {
        const positions = {
            header: 'top',
            sidebar: 'left',
            main: 'center',
            footer: 'bottom',
        };
        return positions[section] || 'center';
    }
    /**
     * Get semantic role for section
     */
    getSemanticRole(section) {
        const roles = {
            header: 'banner',
            sidebar: 'navigation',
            main: 'main',
            footer: 'contentinfo',
        };
        return roles[section] || 'region';
    }
    /**
     * Capitalize first letter
     */
    capitalize(str) {
        return str.charAt(0).toUpperCase() + str.slice(1);
    }
}
exports.UIArchitect = UIArchitect;
//# sourceMappingURL=ui-architect.js.map