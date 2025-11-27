/**
 * CODITECT Generative UI - Main Entry Point
 * @module index
 */
export * from './types';
export { BaseAgent, AgentRole, type AgentConfig } from './agents/base';
export { IntentAnalyzer, type IntentAnalysisInput } from './agents/specialists/intent-analyzer';
export { UIArchitect, type UIArchitecture, type ComponentNode, type LayoutStructure, } from './agents/specialists/ui-architect';
export { CodeGenerator, type CodeGenerationInput, } from './agents/specialists/code-generator';
export { AccessibilityAuditor, type AccessibilityAuditInput, type AccessibilityViolation as AccessibilityAuditorViolation, type AccessibilityReport, } from './agents/specialists/accessibility-auditor';
export { QualityReviewer, type QualityReviewInput, type QualityIssue, type QualityReport, } from './agents/specialists/quality-reviewer';
export { UISynthesisEngine, type SynthesisEngineConfig, type PipelineResult, } from './lib/ui-synthesis-engine';
export { TokenOptimizer, type OptimizationStrategy, type OptimizationRecommendation, type CostParameters, type GenerationCostProfile, type TokenStatistics, } from './lib/token-optimizer';
export { QualityGatesValidator, type WCAGLevel, type AccessibilityValidation, type AccessibilityViolation, type TypeScriptValidation, type PerformanceValidation, type CodeQualityValidation, } from './lib/quality-gates';
/**
 * Library version
 */
export declare const VERSION = "0.1.0";
/**
 * Quick helper to generate a UI component
 */
export declare function generateUI(description: string): Promise<{
    spec: import("./types").UISpec;
    architecture: import("./agents/specialists/ui-architect").UIArchitecture;
    files: import("./types").GeneratedCode[];
    metadata: {
        tokens: {
            prompt: number;
            completion: number;
            total: number;
        };
        duration: number;
    };
}>;
//# sourceMappingURL=index.d.ts.map