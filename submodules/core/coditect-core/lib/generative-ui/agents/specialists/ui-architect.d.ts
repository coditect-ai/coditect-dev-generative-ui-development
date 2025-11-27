/**
 * UI Architect Agent
 * Designs component hierarchies and layout structures from UI specifications
 * @module agents/specialists/ui-architect
 */
import { BaseAgent } from '../base';
import { AgentContext, AgentResult, UISpec } from '../../types';
/**
 * UI architecture output
 */
export interface UIArchitecture {
    /** Component hierarchy */
    components: ComponentNode[];
    /** Layout structure */
    layout?: LayoutStructure;
    /** Recommended patterns */
    patterns: string[];
    /** Dependencies */
    dependencies: string[];
}
/**
 * Component node in the hierarchy
 */
export interface ComponentNode {
    /** Component name */
    name: string;
    /** Component type */
    type: 'container' | 'presentational' | 'form' | 'interactive';
    /** Props interface */
    props: Record<string, string>;
    /** Child components */
    children?: ComponentNode[];
    /** Accessibility requirements */
    a11y: {
        role?: string;
        ariaLabel?: string;
        ariaDescribedBy?: string;
        keyboardNav?: boolean;
    };
}
/**
 * Layout structure
 */
export interface LayoutStructure {
    /** Layout pattern */
    pattern: 'grid' | 'flex' | 'stack' | 'masonry';
    /** Responsive breakpoints */
    breakpoints: {
        sm?: string;
        md?: string;
        lg?: string;
        xl?: string;
    };
    /** Sections */
    sections: LayoutSection[];
}
/**
 * Layout section
 */
export interface LayoutSection {
    /** Section name */
    name: string;
    /** Position */
    position: string;
    /** Components in this section */
    components: string[];
}
/**
 * UI Architect Agent
 * Designs component architectures and layout structures
 */
export declare class UIArchitect extends BaseAgent<UISpec, UIArchitecture> {
    constructor();
    /**
     * Execute UI architecture design
     */
    execute(input: UISpec, _context: AgentContext): Promise<AgentResult<UIArchitecture>>;
    /**
     * Validate input
     */
    protected validateInput(input: UISpec): boolean;
    /**
     * Design UI architecture
     */
    private designArchitecture;
    /**
     * Design component architecture
     */
    private designComponent;
    /**
     * Design layout architecture
     */
    private designLayout;
    /**
     * Design application architecture
     */
    private designApplication;
    /**
     * Extract component name from description
     */
    private extractComponentName;
    /**
     * Get layout position for section
     */
    private getLayoutPosition;
    /**
     * Get semantic role for section
     */
    private getSemanticRole;
    /**
     * Capitalize first letter
     */
    private capitalize;
}
//# sourceMappingURL=ui-architect.d.ts.map