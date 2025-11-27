/**
 * Quality Gates
 * Quality validation system for generated UI code
 * @module lib/quality-gates
 */
import { GeneratedCode, QualityGateResult } from '../types';
/**
 * WCAG compliance level
 */
export type WCAGLevel = 'A' | 'AA' | 'AAA';
/**
 * Accessibility validation result
 */
export interface AccessibilityValidation {
    /** Compliance level achieved */
    level: WCAGLevel;
    /** Overall score (0-100) */
    score: number;
    /** Violations found */
    violations: AccessibilityViolation[];
    /** Warnings */
    warnings: AccessibilityWarning[];
    /** Passed checks */
    passed: string[];
}
/**
 * Accessibility violation
 */
export interface AccessibilityViolation {
    /** Rule ID */
    rule: string;
    /** WCAG level */
    wcagLevel: WCAGLevel;
    /** Description */
    description: string;
    /** Impact level */
    impact: 'critical' | 'serious' | 'moderate' | 'minor';
    /** Element selector */
    selector?: string;
    /** Line number */
    line?: number;
    /** Remediation suggestion */
    remediation: string;
}
/**
 * Accessibility warning
 */
export interface AccessibilityWarning {
    /** Rule ID */
    rule: string;
    /** Description */
    description: string;
    /** Recommendation */
    recommendation: string;
}
/**
 * TypeScript validation result
 */
export interface TypeScriptValidation {
    /** Strict mode compliance */
    strictCompliant: boolean;
    /** Overall score (0-100) */
    score: number;
    /** Type errors */
    errors: TypeScriptError[];
    /** Warnings */
    warnings: TypeScriptWarning[];
}
/**
 * TypeScript error
 */
export interface TypeScriptError {
    /** Error code */
    code: string;
    /** Error message */
    message: string;
    /** File path */
    file: string;
    /** Line number */
    line?: number;
    /** Column number */
    column?: number;
}
/**
 * TypeScript warning
 */
export interface TypeScriptWarning {
    /** Warning type */
    type: 'implicit-any' | 'unsafe-assignment' | 'missing-return-type';
    /** Description */
    description: string;
    /** File path */
    file: string;
    /** Line number */
    line?: number;
}
/**
 * Performance validation result
 */
export interface PerformanceValidation {
    /** Overall score (0-100) */
    score: number;
    /** Bundle size estimate in bytes */
    bundleSize: number;
    /** Metrics */
    metrics: {
        /** Estimated First Contentful Paint (ms) */
        fcp: number;
        /** Estimated Time to Interactive (ms) */
        tti: number;
        /** Estimated Lighthouse score */
        lighthouse: number;
    };
    /** Performance issues */
    issues: PerformanceIssue[];
    /** Recommendations */
    recommendations: string[];
}
/**
 * Performance issue
 */
export interface PerformanceIssue {
    /** Issue type */
    type: 'bundle-size' | 'render-performance' | 'memory-usage';
    /** Severity */
    severity: 'critical' | 'warning' | 'info';
    /** Description */
    description: string;
    /** Impact estimate */
    impact: string;
    /** Remediation */
    remediation: string;
}
/**
 * Code quality validation result
 */
export interface CodeQualityValidation {
    /** Overall score (0-100) */
    score: number;
    /** ESLint violations */
    eslintViolations: Array<{
        rule: string;
        severity: 'error' | 'warning';
        message: string;
        file: string;
        line?: number;
    }>;
    /** Prettier violations */
    prettierViolations: Array<{
        file: string;
        line?: number;
        issue: string;
    }>;
    /** Code smells */
    codeSmells: Array<{
        type: string;
        description: string;
        file: string;
        suggestion: string;
    }>;
}
/**
 * Quality Gates Validator
 * Validates generated code against quality standards
 */
export declare class QualityGatesValidator {
    /**
     * Validate WCAG accessibility compliance
     * @param files - Generated code files
     * @param targetLevel - Target WCAG level
     * @returns Accessibility validation result
     */
    validateAccessibility(files: GeneratedCode[], targetLevel: WCAGLevel): AccessibilityValidation;
    /**
     * Validate TypeScript strict mode compliance
     * @param files - Generated code files
     * @returns TypeScript validation result
     */
    validateTypeScript(files: GeneratedCode[]): TypeScriptValidation;
    /**
     * Validate performance characteristics
     * @param files - Generated code files
     * @returns Performance validation result
     */
    validatePerformance(files: GeneratedCode[]): PerformanceValidation;
    /**
     * Validate code quality (ESLint, Prettier)
     * @param files - Generated code files
     * @returns Code quality validation result
     */
    validateCodeQuality(files: GeneratedCode[]): CodeQualityValidation;
    /**
     * Run all quality gates
     * @param files - Generated code files
     * @param wcagLevel - Target WCAG level
     * @returns Array of quality gate results
     */
    validateAll(files: GeneratedCode[], wcagLevel?: WCAGLevel): QualityGateResult[];
    private hasSemanticHTML;
    private checkARIAAttributes;
    private hasKeyboardNavigation;
    private checkFocusManagement;
    private checkColorContrast;
    private checkAltText;
    private checkESLintRules;
    private checkPrettierFormatting;
    private detectCodeSmells;
    private estimateFCP;
    private estimateTTI;
    private estimateLighthouseScore;
    private getLineNumber;
}
//# sourceMappingURL=quality-gates.d.ts.map