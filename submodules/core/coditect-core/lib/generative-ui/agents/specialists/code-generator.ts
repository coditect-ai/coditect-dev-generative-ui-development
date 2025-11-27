/**
 * Code Generator Agent
 * Generates production-ready TypeScript/React code from UI architecture
 * @module agents/specialists/code-generator
 */

import { BaseAgent, AgentRole } from '../base';
import { AgentContext, AgentResult, GeneratedCode } from '../../types';
import { UIArchitecture } from './ui-architect';

/**
 * Code generation input
 */
export interface CodeGenerationInput {
  /** UI architecture */
  architecture: UIArchitecture;
  /** Target framework */
  framework: 'react' | 'vue' | 'svelte';
  /** Styling approach */
  styling: 'tailwind' | 'css-modules' | 'styled-components';
  /** TypeScript strict mode */
  strictTypes: boolean;
}

/**
 * Code Generator Agent
 * Generates production-ready code from UI architectures
 */
export class CodeGenerator extends BaseAgent<CodeGenerationInput, GeneratedCode[]> {
  constructor() {
    super({
      name: 'code-generator',
      role: AgentRole.SPECIALIST,
      description: 'Generates production-ready TypeScript/React code',
      capabilities: [
        'generate-react-components',
        'generate-typescript-types',
        'generate-tests',
        'optimize-code',
      ],
    });
  }

  /**
   * Execute code generation
   */
  async execute(
    input: CodeGenerationInput,
    _context: AgentContext
  ): Promise<AgentResult<GeneratedCode[]>> {
    this.log('info', 'Starting code generation', { input });

    if (!this.validateInput(input)) {
      return {
        success: false,
        error: {
          message: 'Invalid code generation input',
          code: 'INVALID_INPUT',
        },
        tokens: { prompt: 0, completion: 0 },
      };
    }

    try {
      const generatedFiles = await this.generateCode(input);

      this.log('info', 'Code generation complete', {
        fileCount: generatedFiles.length,
      });

      // Calculate completion tokens from generated file sizes
      const completionTokens = generatedFiles.reduce(
        (sum, file) => sum + Math.ceil(file.content.length / 4),
        0
      );

      return {
        success: true,
        data: generatedFiles,
        tokens: {
          prompt: this.estimateTokens(input),
          completion: completionTokens,
        },
      };
    } catch (error) {
      this.log('error', 'Code generation failed', { error });
      return {
        success: false,
        error: {
          message: error instanceof Error ? error.message : 'Unknown error',
          code: 'GENERATION_FAILED',
          details: error,
        },
        tokens: { prompt: 0, completion: 0 },
      };
    }
  }

  /**
   * Validate input
   */
  protected validateInput(input: CodeGenerationInput): boolean {
    return !!input.architecture && input.architecture.components.length > 0;
  }

  /**
   * Generate code files
   */
  private async generateCode(input: CodeGenerationInput): Promise<GeneratedCode[]> {
    const { architecture, framework, styling, strictTypes } = input;
    const files: GeneratedCode[] = [];

    // Generate component files
    for (const component of architecture.components) {
      if (framework === 'react') {
        const code = this.generateReactComponent(component, styling, strictTypes);
        const test = this.generateComponentTest(component, framework);

        files.push({
          filePath: `src/components/${component.name}.tsx`,
          content: code,
          language: 'tsx',
          testContent: test,
        });
      }
    }

    // Generate types file if needed
    if (strictTypes) {
      const typesCode = this.generateTypesFile(architecture);
      files.push({
        filePath: 'src/types/index.ts',
        content: typesCode,
        language: 'typescript',
      });
    }

    return files;
  }

  /**
   * Generate React component
   */
  private generateReactComponent(
    component: UIArchitecture['components'][0],
    styling: string,
    _strictTypes: boolean
  ): string {
    const propsInterface = this.generatePropsInterface(component);
    const componentBody = this.generateComponentBody(component, styling);

    return `import { FC } from 'react';
${styling === 'tailwind' ? '' : "import styled from 'styled-components';"}

${propsInterface}

export const ${component.name}: FC<${component.name}Props> = (props) => {
${componentBody}
};

${component.name}.displayName = '${component.name}';
`;
  }

  /**
   * Generate props interface
   */
  private generatePropsInterface(component: UIArchitecture['components'][0]): string {
    const props = Object.entries(component.props)
      .map(([key, type]) => {
        const optional = type.includes('?') ? '?' : '';
        const cleanType = type.replace('?', '');
        return `  ${key}${optional}: ${cleanType};`;
      })
      .join('\n');

    return `export interface ${component.name}Props {
${props}
}`;
  }

  /**
   * Generate component body
   */
  private generateComponentBody(
    component: UIArchitecture['components'][0],
    styling: string
  ): string {
    const { a11y } = component;

    if (styling === 'tailwind') {
      return `  return (
    <button
      className="px-4 py-2 rounded-md transition-colors focus:outline-none focus:ring-2"
      onClick={props.onClick}
      disabled={props.disabled}
      aria-label={props['aria-label']}
      role="${a11y.role || 'button'}"
    >
      {props.children}
    </button>
  );`;
    }

    return `  return (
    <StyledButton
      onClick={props.onClick}
      disabled={props.disabled}
      role="${a11y.role || 'button'}"
    >
      {props.children}
    </StyledButton>
  );`;
  }

  /**
   * Generate component test
   */
  private generateComponentTest(
    component: UIArchitecture['components'][0],
    framework: string
  ): string {
    if (framework !== 'react') return '';

    return `import { render, screen } from '@testing-library/react';
import { ${component.name} } from './${component.name}';

describe('${component.name}', () => {
  it('should render correctly', () => {
    render(<${component.name}>Test</${component.name}>);
    expect(screen.getByText('Test')).toBeInTheDocument();
  });

  it('should be accessible', () => {
    const { container } = render(<${component.name}>Test</${component.name}>);
    expect(container.firstChild).toHaveAttribute('role', '${component.a11y.role || 'button'}');
  });
});
`;
  }

  /**
   * Generate types file
   */
  private generateTypesFile(_architecture: UIArchitecture): string {
    return `/**
 * Generated type definitions
 */

export interface ComponentProps {
  children?: React.ReactNode;
  className?: string;
}

// Add more types as needed
`;
  }
}
