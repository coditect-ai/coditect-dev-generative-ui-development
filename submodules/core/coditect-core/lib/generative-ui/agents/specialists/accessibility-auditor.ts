/**
 * Accessibility Auditor Agent
 * Validates WCAG 2.1 AA/AAA compliance for generated UI code
 * @module agents/specialists/accessibility-auditor
 */

import { BaseAgent, AgentRole } from '../base';
import { AgentContext, AgentResult, ValidationResult } from '../../types';

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
export class AccessibilityAuditor extends BaseAgent<
  AccessibilityAuditInput,
  AccessibilityReport
> {
  constructor() {
    super({
      name: 'accessibility-auditor',
      role: AgentRole.VALIDATOR,
      description: 'Validates WCAG 2.1 AA/AAA compliance for generated UI code',
      capabilities: [
        'validate-semantic-html',
        'check-aria-attributes',
        'verify-keyboard-navigation',
        'audit-color-contrast',
        'validate-focus-management',
        'check-screen-reader-compat',
      ],
    });
  }

  /**
   * Execute accessibility audit
   */
  async execute(
    input: AccessibilityAuditInput,
    _context: AgentContext
  ): Promise<AgentResult<AccessibilityReport>> {
    this.log('info', 'Starting accessibility audit', {
      codeLength: input.code.length,
      spec: input.spec,
    });

    if (!this.validateInput(input)) {
      return {
        success: false,
        error: {
          message: 'Invalid accessibility audit input: code is required',
          code: 'INVALID_INPUT',
        },
        tokens: { prompt: 0, completion: 0 },
      };
    }

    try {
      const report = await this.auditAccessibility(input);

      this.log('info', 'Accessibility audit complete', {
        score: report.score,
        wcagLevel: report.wcagLevel,
        violationCount: report.violationCount,
      });

      // Convert violations to validation results
      const validation: ValidationResult[] = report.violations.map((v) => ({
        rule: v.wcagCriterion,
        passed: false,
        message: v.description,
        severity: v.severity === 'critical' || v.severity === 'serious' ? 'error' : 'warning',
        details: {
          id: v.id,
          impact: v.impact,
          recommendation: v.recommendation,
          location: v.location,
        },
      }));

      // Add passed checks as validation results
      report.passedChecks.forEach((check) => {
        validation.push({
          rule: check,
          passed: true,
          message: `Passed: ${check}`,
          severity: 'info',
        });
      });

      return {
        success: report.score >= 70, // 70+ is acceptable
        data: report,
        tokens: {
          prompt: this.estimateTokens(input),
          completion: Math.ceil(JSON.stringify(report).length / 4),
        },
        validation,
      };
    } catch (error) {
      this.log('error', 'Accessibility audit failed', { error });
      return {
        success: false,
        error: {
          message: error instanceof Error ? error.message : 'Unknown error',
          code: 'AUDIT_FAILED',
          details: error,
        },
        tokens: { prompt: 0, completion: 0 },
      };
    }
  }

  /**
   * Validate input
   */
  protected validateInput(input: AccessibilityAuditInput): boolean {
    return !!input.code && input.code.trim().length > 0;
  }

  /**
   * Perform comprehensive accessibility audit
   */
  private async auditAccessibility(
    input: AccessibilityAuditInput
  ): Promise<AccessibilityReport> {
    const violations: AccessibilityViolation[] = [];
    const passedChecks: string[] = [];

    // 1. Semantic HTML validation
    const semanticResults = this.validateSemanticHTML(input.code);
    violations.push(...semanticResults.violations);
    passedChecks.push(...semanticResults.passed);

    // 2. ARIA attributes validation
    const ariaResults = this.validateARIAAttributes(input.code);
    violations.push(...ariaResults.violations);
    passedChecks.push(...ariaResults.passed);

    // 3. Keyboard navigation validation
    const keyboardResults = this.validateKeyboardNavigation(input.code);
    violations.push(...keyboardResults.violations);
    passedChecks.push(...keyboardResults.passed);

    // 4. Color contrast validation
    const contrastResults = this.validateColorContrast(input.code);
    violations.push(...contrastResults.violations);
    passedChecks.push(...contrastResults.passed);

    // 5. Focus management validation
    const focusResults = this.validateFocusManagement(input.code);
    violations.push(...focusResults.violations);
    passedChecks.push(...focusResults.passed);

    // 6. Screen reader compatibility
    const screenReaderResults = this.validateScreenReaderCompat(input.code);
    violations.push(...screenReaderResults.violations);
    passedChecks.push(...screenReaderResults.passed);

    // Calculate score (100 - points deducted for violations)
    const deductions = violations.reduce((sum, v) => {
      const severityPoints = {
        critical: 25,
        serious: 15,
        moderate: 8,
        minor: 3,
      };
      return sum + severityPoints[v.severity];
    }, 0);

    const score = Math.max(0, 100 - deductions);

    // Determine WCAG level
    const wcagLevel = this.determineWCAGLevel(violations, score);

    // Generate recommendations
    const recommendations = this.generateRecommendations(violations);

    // Generate summary
    const summary = this.generateSummary(score, wcagLevel, violations.length);

    return {
      score,
      wcagLevel,
      violationCount: violations.length,
      violations,
      passedChecks,
      summary,
      recommendations,
    };
  }

  /**
   * Validate semantic HTML usage
   */
  private validateSemanticHTML(code: string): {
    violations: AccessibilityViolation[];
    passed: string[];
  } {
    const violations: AccessibilityViolation[] = [];
    const passed: string[] = [];

    // Check for proper heading hierarchy
    if (code.includes('<h')) {
      const headings = code.match(/<h[1-6]/g) || [];
      if (headings.length > 0) {
        passed.push('Uses heading elements');
      }
    }

    // Check for div/span soup instead of semantic elements
    const divCount = (code.match(/<div/g) || []).length;
    const semanticElements = [
      '<nav',
      '<main',
      '<aside',
      '<header',
      '<footer',
      '<article',
      '<section',
    ];
    const semanticCount = semanticElements.reduce(
      (count, el) => count + (code.includes(el) ? 1 : 0),
      0
    );

    if (divCount > 5 && semanticCount === 0) {
      violations.push({
        id: 'semantic-html-001',
        wcagCriterion: '1.3.1 Info and Relationships (A)',
        severity: 'serious',
        description: 'Code uses excessive <div> elements without semantic HTML',
        recommendation:
          'Replace <div> with semantic elements like <nav>, <main>, <section>, <header>, <footer>',
        impact: 'Screen reader users cannot navigate by landmarks',
      });
    } else if (semanticCount > 0) {
      passed.push('Uses semantic HTML landmarks');
    }

    // Check for buttons vs div onClick
    if (code.match(/onClick.*<div/)) {
      violations.push({
        id: 'semantic-html-002',
        wcagCriterion: '4.1.2 Name, Role, Value (A)',
        severity: 'critical',
        description: 'Interactive <div> with onClick instead of <button>',
        recommendation: 'Use <button> element for clickable actions',
        impact: 'Keyboard users cannot activate the control',
      });
    } else if (code.includes('<button')) {
      passed.push('Uses native <button> elements for actions');
    }

    return { violations, passed };
  }

  /**
   * Validate ARIA attributes
   */
  private validateARIAAttributes(code: string): {
    violations: AccessibilityViolation[];
    passed: string[];
  } {
    const violations: AccessibilityViolation[] = [];
    const passed: string[] = [];

    // Check for aria-label on elements that need labels
    const ariaLabelPattern = /aria-label=/g;
    if (ariaLabelPattern.test(code)) {
      passed.push('Includes aria-label attributes');
    }

    // Check for redundant ARIA (e.g., role="button" on <button>)
    if (code.match(/<button[^>]*role="button"/)) {
      violations.push({
        id: 'aria-001',
        wcagCriterion: '4.1.2 Name, Role, Value (A)',
        severity: 'minor',
        description: 'Redundant role="button" on native <button> element',
        recommendation: 'Remove role attribute from native <button> elements',
        impact: 'Minor: Adds unnecessary verbosity for screen readers',
      });
    }

    // Check for invalid ARIA roles
    const invalidRoles = code.match(/role="(unknown|invalid|custom)"/);
    if (invalidRoles) {
      violations.push({
        id: 'aria-002',
        wcagCriterion: '4.1.2 Name, Role, Value (A)',
        severity: 'serious',
        description: `Invalid ARIA role: ${invalidRoles[1]}`,
        recommendation: 'Use valid ARIA 1.2 roles only',
        impact: 'Screen readers may ignore or misinterpret the element',
      });
    }

    return { violations, passed };
  }

  /**
   * Validate keyboard navigation
   */
  private validateKeyboardNavigation(code: string): {
    violations: AccessibilityViolation[];
    passed: string[];
  } {
    const violations: AccessibilityViolation[] = [];
    const passed: string[] = [];

    // Check for disabled tabIndex (-1 without good reason)
    if (code.match(/tabIndex={?-1}?/) && !code.includes('aria-hidden')) {
      violations.push({
        id: 'keyboard-001',
        wcagCriterion: '2.1.1 Keyboard (A)',
        severity: 'serious',
        description: 'Element with tabIndex={-1} removes keyboard access',
        recommendation: 'Only use tabIndex={-1} for programmatic focus management',
        impact: 'Keyboard users cannot reach this element',
      });
    }

    // Check for positive tabIndex (anti-pattern)
    if (code.match(/tabIndex={?[1-9]/)) {
      violations.push({
        id: 'keyboard-002',
        wcagCriterion: '2.4.3 Focus Order (A)',
        severity: 'serious',
        description: 'Positive tabIndex disrupts natural tab order',
        recommendation: 'Remove positive tabIndex values; use natural DOM order',
        impact: 'Confusing tab order for keyboard users',
      });
    } else {
      passed.push('No positive tabIndex values found');
    }

    // Check for onKeyDown handlers (keyboard support)
    if (code.includes('onKeyDown') || code.includes('onKeyPress')) {
      passed.push('Implements keyboard event handlers');
    }

    return { violations, passed };
  }

  /**
   * Validate color contrast
   */
  private validateColorContrast(code: string): {
    violations: AccessibilityViolation[];
    passed: string[];
  } {
    const violations: AccessibilityViolation[] = [];
    const passed: string[] = [];

    // Check for inline styles with low contrast (simple heuristic)
    const lowContrastPatterns = [
      /color:.*#[a-fA-F0-9]{6}.*background.*#[a-fA-F0-9]{6}/,
      /text-gray-[1-4]/,
    ];

    lowContrastPatterns.forEach((pattern, index) => {
      if (pattern.test(code)) {
        violations.push({
          id: `contrast-00${index + 1}`,
          wcagCriterion: '1.4.3 Contrast (Minimum) (AA)',
          severity: 'moderate',
          description: 'Potential low color contrast detected',
          recommendation:
            'Verify contrast ratio: 4.5:1 for text, 3:1 for UI components (WCAG AA)',
          impact: 'Users with low vision may struggle to read text',
        });
      }
    });

    // Check for color-only information
    if (code.match(/color:|text-red|text-green|bg-red|bg-green/) && !code.includes('aria-')) {
      violations.push({
        id: 'contrast-003',
        wcagCriterion: '1.4.1 Use of Color (A)',
        severity: 'moderate',
        description: 'Color used as sole indicator (e.g., red for error)',
        recommendation: 'Add text label or icon alongside color',
        impact: 'Colorblind users cannot distinguish states',
      });
    }

    if (violations.length === 0) {
      passed.push('No obvious contrast violations detected');
    }

    return { violations, passed };
  }

  /**
   * Validate focus management
   */
  private validateFocusManagement(code: string): {
    violations: AccessibilityViolation[];
    passed: string[];
  } {
    const violations: AccessibilityViolation[] = [];
    const passed: string[] = [];

    // Check for visible focus styles
    if (code.includes('focus:') || code.includes(':focus')) {
      passed.push('Includes focus styles');
    } else if (code.includes('outline-none') && !code.includes('focus:ring')) {
      violations.push({
        id: 'focus-001',
        wcagCriterion: '2.4.7 Focus Visible (AA)',
        severity: 'critical',
        description: 'Focus outline removed without replacement',
        recommendation: 'Add visible focus indicator (e.g., focus:ring-2)',
        impact: 'Keyboard users cannot see where focus is',
      });
    }

    // Check for focus traps (modal dialogs should manage focus)
    if (code.includes('modal') || code.includes('dialog')) {
      if (!code.includes('autoFocus') && !code.includes('focus()')) {
        violations.push({
          id: 'focus-002',
          wcagCriterion: '2.4.3 Focus Order (A)',
          severity: 'moderate',
          description: 'Modal/dialog may not manage focus properly',
          recommendation: 'Set initial focus on first interactive element',
          impact: 'Keyboard users may lose focus context',
        });
      } else {
        passed.push('Modal/dialog includes focus management');
      }
    }

    return { violations, passed };
  }

  /**
   * Validate screen reader compatibility
   */
  private validateScreenReaderCompat(code: string): {
    violations: AccessibilityViolation[];
    passed: string[];
  } {
    const violations: AccessibilityViolation[] = [];
    const passed: string[] = [];

    // Check for alt text on images
    if (code.includes('<img') && !code.includes('alt=')) {
      violations.push({
        id: 'screenreader-001',
        wcagCriterion: '1.1.1 Non-text Content (A)',
        severity: 'critical',
        description: 'Image missing alt attribute',
        recommendation: 'Add descriptive alt text or alt="" for decorative images',
        impact: 'Screen reader users cannot understand image content',
      });
    } else if (code.includes('alt=')) {
      passed.push('Images include alt attributes');
    }

    // Check for aria-live regions (for dynamic content)
    if (
      (code.includes('loading') || code.includes('error') || code.includes('success')) &&
      !code.includes('aria-live')
    ) {
      violations.push({
        id: 'screenreader-002',
        wcagCriterion: '4.1.3 Status Messages (AA)',
        severity: 'moderate',
        description: 'Dynamic status updates missing aria-live region',
        recommendation: 'Add aria-live="polite" or "assertive" for status messages',
        impact: 'Screen readers do not announce status changes',
      });
    }

    // Check for hidden content
    if (code.includes('aria-hidden="true"') && code.includes('onClick')) {
      violations.push({
        id: 'screenreader-003',
        wcagCriterion: '4.1.2 Name, Role, Value (A)',
        severity: 'serious',
        description: 'Interactive element hidden from screen readers',
        recommendation: 'Remove aria-hidden or make element non-interactive',
        impact: 'Screen reader users cannot access functionality',
      });
    }

    return { violations, passed };
  }

  /**
   * Determine WCAG level achieved
   */
  private determineWCAGLevel(
    violations: AccessibilityViolation[],
    score: number
  ): 'A' | 'AA' | 'AAA' | 'FAIL' {
    const criticalViolations = violations.filter(
      (v) => v.severity === 'critical'
    ).length;
    const seriousViolations = violations.filter(
      (v) => v.severity === 'serious'
    ).length;

    if (criticalViolations > 0) return 'FAIL';
    if (seriousViolations > 0 || score < 70) return 'FAIL';
    if (score >= 95) return 'AAA';
    if (score >= 85) return 'AA';
    if (score >= 70) return 'A';
    return 'FAIL';
  }

  /**
   * Generate recommendations based on violations
   */
  private generateRecommendations(violations: AccessibilityViolation[]): string[] {
    const recommendations: string[] = [];

    // Group by severity
    const critical = violations.filter((v) => v.severity === 'critical');
    const serious = violations.filter((v) => v.severity === 'serious');

    if (critical.length > 0) {
      recommendations.push(
        `🔴 CRITICAL: Fix ${critical.length} critical violations first (keyboard access, alt text, focus indicators)`
      );
    }

    if (serious.length > 0) {
      recommendations.push(
        `🟡 IMPORTANT: Address ${serious.length} serious violations (semantic HTML, ARIA roles, contrast)`
      );
    }

    // Add specific recommendations
    const uniqueRecommendations = new Set(
      violations.map((v) => v.recommendation)
    );
    uniqueRecommendations.forEach((rec) => recommendations.push(`• ${rec}`));

    return recommendations;
  }

  /**
   * Generate summary message
   */
  private generateSummary(
    score: number,
    wcagLevel: string,
    violationCount: number
  ): string {
    if (score >= 95) {
      return `Excellent accessibility! Achieved WCAG ${wcagLevel} with ${violationCount} minor issues.`;
    } else if (score >= 85) {
      return `Good accessibility baseline. Achieved WCAG ${wcagLevel}. Address ${violationCount} violations for AAA.`;
    } else if (score >= 70) {
      return `Basic accessibility met (WCAG ${wcagLevel}). ${violationCount} violations need attention.`;
    } else {
      return `Accessibility issues detected. ${violationCount} violations must be fixed before deployment.`;
    }
  }
}

export default AccessibilityAuditor;
