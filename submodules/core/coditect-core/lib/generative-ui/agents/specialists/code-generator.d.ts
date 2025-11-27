/**
 * Code Generator Agent
 * Generates production-ready TypeScript/React code from UI architecture
 * @module agents/specialists/code-generator
 */
import { BaseAgent } from '../base';
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
export declare class CodeGenerator extends BaseAgent<CodeGenerationInput, GeneratedCode[]> {
    constructor();
    /**
     * Execute code generation
     */
    execute(input: CodeGenerationInput, _context: AgentContext): Promise<AgentResult<GeneratedCode[]>>;
    /**
     * Validate input
     */
    protected validateInput(input: CodeGenerationInput): boolean;
    /**
     * Generate code files
     */
    private generateCode;
    /**
     * Generate React component
     */
    private generateReactComponent;
    /**
     * Generate props interface
     */
    private generatePropsInterface;
    /**
     * Generate component body
     */
    private generateComponentBody;
    /**
     * Generate component test
     */
    private generateComponentTest;
    /**
     * Generate types file
     */
    private generateTypesFile;
}
//# sourceMappingURL=code-generator.d.ts.map