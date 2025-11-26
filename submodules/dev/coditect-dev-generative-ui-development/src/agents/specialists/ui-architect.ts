/**
 * UI Architect Agent
 * Designs component hierarchies and layout structures from UI specifications
 * @module agents/specialists/ui-architect
 */

import { BaseAgent, AgentRole } from '../base';
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
export class UIArchitect extends BaseAgent<UISpec, UIArchitecture> {
  constructor() {
    super({
      name: 'ui-architect',
      role: AgentRole.SPECIALIST,
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
  async execute(
    input: UISpec,
    context: AgentContext
  ): Promise<AgentResult<UIArchitecture>> {
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

      return {
        success: true,
        data: architecture,
        tokens: {
          prompt: this.estimateTokens(input),
          completion: this.estimateTokens(architecture),
        },
      };
    } catch (error) {
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
  protected validateInput(input: UISpec): boolean {
    return !!input.type && !!input.description;
  }

  /**
   * Design UI architecture
   */
  private async designArchitecture(spec: UISpec): Promise<UIArchitecture> {
    if (spec.type === 'component') {
      return this.designComponent(spec);
    } else if (spec.type === 'layout') {
      return this.designLayout(spec);
    } else {
      return this.designApplication(spec);
    }
  }

  /**
   * Design component architecture
   */
  private designComponent(spec: UISpec): UIArchitecture {
    const componentName = this.extractComponentName(spec.description);
    const variants = spec.componentOptions?.variants || ['default'];

    const component: ComponentNode = {
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
  private designLayout(spec: UISpec): UIArchitecture {
    const pattern = spec.layoutOptions?.pattern || 'dashboard';
    const sections = spec.layoutOptions?.sections || ['header', 'main'];

    const layoutStructure: LayoutStructure = {
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

    const components = sections.map((name): ComponentNode => ({
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
  private designApplication(spec: UISpec): UIArchitecture {
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
  private extractComponentName(description: string): string {
    // Simple extraction - look for "Button", "Input", etc.
    const match = description.match(/\b([A-Z][a-z]+(?:[A-Z][a-z]+)*)\b/);
    return match ? match[1] : 'Component';
  }

  /**
   * Get layout position for section
   */
  private getLayoutPosition(section: string): string {
    const positions: Record<string, string> = {
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
  private getSemanticRole(section: string): string {
    const roles: Record<string, string> = {
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
  private capitalize(str: string): string {
    return str.charAt(0).toUpperCase() + str.slice(1);
  }
}
