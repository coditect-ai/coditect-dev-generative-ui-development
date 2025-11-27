/**
 * Quality Reviewer Agent
 * Ensures production-ready React + TypeScript code quality
 * @module agents/specialists/quality-reviewer
 */
import { BaseAgent } from '../base';
import { AgentContext, AgentResult } from '../../types';
/**
 * Quality review input
 */
export interface QualityReviewInput {
    /** Generated code to review */
    code: string;
    /** UI architecture for context */
    architecture?: unknown;
    /** Accessibility report */
    accessibilityReport?: {
        score: number;
        wcagLevel: string;
        violationCount: number;
    };
}
/**
 * Code quality issue
 */
export interface QualityIssue {
    /** Issue ID */
    id: string;
    /** Category */
    category: 'typescript' | 'react' | 'performance' | 'style' | 'testing' | 'security';
    /** Severity level */
    severity: 'blocker' | 'critical' | 'major' | 'minor' | 'info';
    /** Issue description */
    description: string;
    /** Location in code */
    location?: {
        line?: number;
        column?: number;
        snippet?: string;
    };
    /** Recommendation to fix */
    recommendation: string;
    /** Rule violated */
    rule: string;
}
/**
 * Quality review report
 */
export interface QualityReport {
    /** Overall quality score (0-100) */
    score: number;
    /** Approval status */
    approved: boolean;
    /** Total issues found */
    issueCount: number;
    /** Issues by category */
    issues: QualityIssue[];
    /** Strengths identified */
    strengths: string[];
    /** Summary */
    summary: string;
    /** Actionable recommendations */
    recommendations: string[];
    /** Metrics */
    metrics: {
        /** TypeScript strict mode compliance */
        typeStrict: boolean;
        /** Estimated bundle size (bytes) */
        estimatedBundleSize: number;
        /** Component complexity (1-10) */
        complexity: number;
        /** Test coverage potential (0-100) */
        testCoveragePotential: number;
    };
}
/**
 * Quality Reviewer Agent
 * Performs comprehensive code quality review for production readiness
 */
export declare class QualityReviewer extends BaseAgent<QualityReviewInput, QualityReport> {
    constructor();
    /**
     * Execute quality review
     */
    execute(input: QualityReviewInput, _context: AgentContext): Promise<AgentResult<QualityReport>>;
    /**
     * Validate input
     */
    protected validateInput(input: QualityReviewInput): boolean;
    /**
     * Perform comprehensive quality review
     */
    private reviewQuality;
    /**
     * Review TypeScript strict mode compliance
     */
    private reviewTypeScript;
    /**
     * Review React best practices
     */
    private reviewReactPatterns;
    /**
     * Analyze performance characteristics
     */
    private analyzePerformance;
    /**
     * Review code style and conventions
     */
    private reviewCodeStyle;
    /**
     * Assess testability
     */
    private assessTestability;
    /**
     * Identify security risks
     */
    private identifySecurityRisks;
    /**
     * Calculate quality metrics
     */
    private calculateMetrics;
    /**
     * Generate actionable recommendations
     */
    private generateRecommendations;
    /**
     * Generate summary message
     */
    private generateSummary;
}
export default QualityReviewer;
//# sourceMappingURL=quality-reviewer.d.ts.map