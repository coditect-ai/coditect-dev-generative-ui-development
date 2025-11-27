/**
 * Accessibility Auditor Agent
 * Validates WCAG 2.1 AA/AAA compliance for generated UI code
 * @module agents/specialists/accessibility-auditor
 */
import { BaseAgent } from '../base';
import { AgentContext, AgentResult } from '../../types';
/**
 * Accessibility audit input
 */
export interface AccessibilityAuditInput {
    /** Generated code to audit */
    code: string;
    /** UI specification for context */
    spec?: {
        type: 'component' | 'layout' | 'application';
        framework: 'react' | 'vue' | 'svelte';
        requirements?: {
            accessibility?: 'AA' | 'AAA';
        };
    };
}
/**
 * Accessibility violation
 */
export interface AccessibilityViolation {
    /** Violation ID */
    id: string;
    /** WCAG criterion */
    wcagCriterion: string;
    /** Severity level */
    severity: 'critical' | 'serious' | 'moderate' | 'minor';
    /** Violation description */
    description: string;
    /** Location in code */
    location?: {
        line?: number;
        column?: number;
        snippet?: string;
    };
    /** Recommendation to fix */
    recommendation: string;
    /** Impact on users */
    impact: string;
}
/**
 * Accessibility audit report
 */
export interface AccessibilityReport {
    /** Overall accessibility score (0-100) */
    score: number;
    /** WCAG level achieved */
    wcagLevel: 'A' | 'AA' | 'AAA' | 'FAIL';
    /** Total violations found */
    violationCount: number;
    /** Violations by severity */
    violations: AccessibilityViolation[];
    /** Passed checks */
    passedChecks: string[];
    /** Summary */
    summary: string;
    /** Recommendations */
    recommendations: string[];
}
/**
 * Accessibility Auditor Agent
 * Performs comprehensive WCAG 2.1 AA/AAA compliance validation
 */
export declare class AccessibilityAuditor extends BaseAgent<AccessibilityAuditInput, AccessibilityReport> {
    constructor();
    /**
     * Execute accessibility audit
     */
    execute(input: AccessibilityAuditInput, _context: AgentContext): Promise<AgentResult<AccessibilityReport>>;
    /**
     * Validate input
     */
    protected validateInput(input: AccessibilityAuditInput): boolean;
    /**
     * Perform comprehensive accessibility audit
     */
    private auditAccessibility;
    /**
     * Validate semantic HTML usage
     */
    private validateSemanticHTML;
    /**
     * Validate ARIA attributes
     */
    private validateARIAAttributes;
    /**
     * Validate keyboard navigation
     */
    private validateKeyboardNavigation;
    /**
     * Validate color contrast
     */
    private validateColorContrast;
    /**
     * Validate focus management
     */
    private validateFocusManagement;
    /**
     * Validate screen reader compatibility
     */
    private validateScreenReaderCompat;
    /**
     * Determine WCAG level achieved
     */
    private determineWCAGLevel;
    /**
     * Generate recommendations based on violations
     */
    private generateRecommendations;
    /**
     * Generate summary message
     */
    private generateSummary;
}
export default AccessibilityAuditor;
//# sourceMappingURL=accessibility-auditor.d.ts.map