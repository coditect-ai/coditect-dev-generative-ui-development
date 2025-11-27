/**
 * Intent Analyzer Agent
 * Parses user requirements and converts them into structured UI specifications
 * @module agents/specialists/intent-analyzer
 */
import { BaseAgent } from '../base';
import { AgentContext, AgentResult, UISpec } from '../../types';
/**
 * Input for intent analysis
 */
export interface IntentAnalysisInput {
    /** User's natural language description */
    description: string;
    /** Additional context or constraints */
    context?: {
        targetFramework?: 'react' | 'vue' | 'svelte';
        existingComponents?: string[];
        designSystem?: string;
    };
}
/**
 * Intent Analyzer Agent
 * Analyzes user intent and generates structured UI specifications
 */
export declare class IntentAnalyzer extends BaseAgent<IntentAnalysisInput, UISpec> {
    constructor();
    /**
     * Execute intent analysis
     */
    execute(input: IntentAnalysisInput, _context: AgentContext): Promise<AgentResult<UISpec>>;
    /**
     * Validate input
     */
    protected validateInput(input: IntentAnalysisInput): boolean;
    /**
     * Analyze user intent and generate UI spec
     */
    private analyzeIntent;
    /**
     * Detect UI type from description
     */
    private detectUIType;
    /**
     * Detect framework from description
     */
    private detectFramework;
    /**
     * Detect styling approach from description
     */
    private detectStyling;
    /**
     * Extract requirements from description
     */
    private extractRequirements;
    /**
     * Extract component options from description
     */
    private extractComponentOptions;
    /**
     * Extract layout options from description
     */
    private extractLayoutOptions;
}
//# sourceMappingURL=intent-analyzer.d.ts.map