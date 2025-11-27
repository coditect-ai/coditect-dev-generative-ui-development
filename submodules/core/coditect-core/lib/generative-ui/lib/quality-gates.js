"use strict";
/**
 * Quality Gates
 * Quality validation system for generated UI code
 * @module lib/quality-gates
 */
Object.defineProperty(exports, "__esModule", { value: true });
exports.QualityGatesValidator = void 0;
/**
 * Quality Gates Validator
 * Validates generated code against quality standards
 */
class QualityGatesValidator {
    /**
     * Validate WCAG accessibility compliance
     * @param files - Generated code files
     * @param targetLevel - Target WCAG level
     * @returns Accessibility validation result
     */
    validateAccessibility(files, targetLevel) {
        const violations = [];
        const warnings = [];
        const passed = [];
        for (const file of files) {
            const content = file.content.toLowerCase();
            // Check for semantic HTML
            if (this.hasSemanticHTML(content)) {
                passed.push('semantic-html');
            }
            else {
                violations.push({
                    rule: 'semantic-html',
                    wcagLevel: 'A',
                    description: 'Missing semantic HTML elements',
                    impact: 'serious',
                    selector: file.filePath,
                    remediation: 'Use semantic elements like <button>, <nav>, <main> instead of <div>',
                });
            }
            // Check for ARIA attributes
            const ariaCheck = this.checkARIAAttributes(content);
            if (ariaCheck.passed) {
                passed.push('aria-attributes');
            }
            else {
                violations.push(...ariaCheck.violations);
                warnings.push(...ariaCheck.warnings);
            }
            // Check for keyboard navigation
            if (this.hasKeyboardNavigation(content)) {
                passed.push('keyboard-navigation');
            }
            else {
                violations.push({
                    rule: 'keyboard-navigation',
                    wcagLevel: 'A',
                    description: 'Missing keyboard navigation support',
                    impact: 'critical',
                    remediation: 'Add onKeyDown/onKeyPress handlers for interactive elements',
                });
            }
            // Check for focus management
            const focusCheck = this.checkFocusManagement(content);
            if (focusCheck.passed) {
                passed.push('focus-management');
            }
            else {
                violations.push(...focusCheck.violations);
            }
            // Check for color contrast (basic heuristic)
            const contrastCheck = this.checkColorContrast(content);
            if (contrastCheck.passed) {
                passed.push('color-contrast');
            }
            else {
                if (targetLevel === 'AAA') {
                    violations.push(...contrastCheck.violations);
                }
                else {
                    warnings.push(...contrastCheck.warnings);
                }
            }
            // Check for alt text on images
            const altTextCheck = this.checkAltText(content);
            if (altTextCheck.passed) {
                passed.push('alt-text');
            }
            else {
                violations.push(...altTextCheck.violations);
            }
        }
        // Calculate score
        const criticalCount = violations.filter((v) => v.impact === 'critical').length;
        const seriousCount = violations.filter((v) => v.impact === 'serious').length;
        const moderateCount = violations.filter((v) => v.impact === 'moderate').length;
        let score = 100;
        score -= criticalCount * 20;
        score -= seriousCount * 10;
        score -= moderateCount * 5;
        score -= warnings.length * 2;
        score = Math.max(0, score);
        // Determine achieved level
        let achievedLevel = 'AAA';
        if (score < 95)
            achievedLevel = 'AA';
        if (score < 85)
            achievedLevel = 'A';
        return {
            level: achievedLevel,
            score,
            violations,
            warnings,
            passed,
        };
    }
    /**
     * Validate TypeScript strict mode compliance
     * @param files - Generated code files
     * @returns TypeScript validation result
     */
    validateTypeScript(files) {
        const errors = [];
        const warnings = [];
        for (const file of files) {
            const content = file.content;
            // Check for any types
            const anyMatches = content.matchAll(/:\s*any\b/g);
            for (const match of anyMatches) {
                const line = this.getLineNumber(content, match.index || 0);
                warnings.push({
                    type: 'implicit-any',
                    description: `Explicit 'any' type found at line ${line}`,
                    file: file.filePath,
                    line,
                });
            }
            // Check for missing return types
            const functionMatches = content.matchAll(/(?:function|const|let)\s+\w+\s*(?:<[^>]+>)?\s*\([^)]*\)\s*(?:=>)?\s*\{/g);
            for (const match of functionMatches) {
                const matchStr = match[0];
                if (!matchStr.includes(':') || !matchStr.includes('=>')) {
                    const line = this.getLineNumber(content, match.index || 0);
                    warnings.push({
                        type: 'missing-return-type',
                        description: `Missing return type annotation at line ${line}`,
                        file: file.filePath,
                        line,
                    });
                }
            }
            // Check for unsafe assignments
            const unsafePatterns = [
                /as\s+any\b/g,
                /\@ts-ignore/g,
                /\@ts-nocheck/g,
                /\@ts-expect-error/g,
            ];
            for (const pattern of unsafePatterns) {
                const matches = content.matchAll(pattern);
                for (const match of matches) {
                    const line = this.getLineNumber(content, match.index || 0);
                    errors.push({
                        code: 'unsafe-type-assertion',
                        message: `Unsafe type operation found at line ${line}: ${match[0]}`,
                        file: file.filePath,
                        line,
                    });
                }
            }
        }
        // Calculate score
        let score = 100;
        score -= errors.length * 15;
        score -= warnings.length * 5;
        score = Math.max(0, score);
        const strictCompliant = errors.length === 0 && warnings.length === 0;
        return {
            strictCompliant,
            score,
            errors,
            warnings,
        };
    }
    /**
     * Validate performance characteristics
     * @param files - Generated code files
     * @returns Performance validation result
     */
    validatePerformance(files) {
        const issues = [];
        const recommendations = [];
        // Calculate bundle size
        const bundleSize = files.reduce((sum, file) => sum + file.content.length, 0);
        // Bundle size thresholds
        const BUNDLE_SIZE_WARNING = 50000; // 50KB
        const BUNDLE_SIZE_CRITICAL = 100000; // 100KB
        if (bundleSize > BUNDLE_SIZE_CRITICAL) {
            issues.push({
                type: 'bundle-size',
                severity: 'critical',
                description: `Bundle size (${Math.round(bundleSize / 1000)}KB) exceeds critical threshold`,
                impact: 'Significant impact on load time and Time to Interactive',
                remediation: 'Consider code splitting, lazy loading, and tree shaking',
            });
            recommendations.push('Implement code splitting for large components');
            recommendations.push('Use dynamic imports for non-critical features');
        }
        else if (bundleSize > BUNDLE_SIZE_WARNING) {
            issues.push({
                type: 'bundle-size',
                severity: 'warning',
                description: `Bundle size (${Math.round(bundleSize / 1000)}KB) approaching threshold`,
                impact: 'May affect load time on slower connections',
                remediation: 'Optimize imports and remove unused code',
            });
            recommendations.push('Review and optimize import statements');
        }
        // Check for performance anti-patterns
        for (const file of files) {
            const content = file.content;
            // Check for inline functions in render
            if (content.includes('onClick={() =>') || content.includes('onChange={() =>')) {
                issues.push({
                    type: 'render-performance',
                    severity: 'warning',
                    description: 'Inline arrow functions in render may cause unnecessary re-renders',
                    impact: 'Minor performance impact on complex UIs',
                    remediation: 'Use useCallback or extract to class methods',
                });
                recommendations.push('Use useCallback for event handlers');
            }
            // Check for missing React.memo or useMemo
            if (content.includes('export const') && !content.includes('memo(')) {
                recommendations.push('Consider using React.memo for expensive components');
            }
            // Check for large data structures
            if (content.includes('[...Array(') && content.includes('map(')) {
                issues.push({
                    type: 'memory-usage',
                    severity: 'info',
                    description: 'Large array operations detected',
                    impact: 'May impact memory usage',
                    remediation: 'Consider virtualization for large lists',
                });
                recommendations.push('Use react-window or react-virtualized for large lists');
            }
        }
        // Calculate performance metrics (estimates)
        const fcp = this.estimateFCP(bundleSize);
        const tti = this.estimateTTI(bundleSize, issues.length);
        const lighthouse = this.estimateLighthouseScore(bundleSize, issues);
        // Calculate overall score
        let score = 100;
        score -= issues.filter((i) => i.severity === 'critical').length * 25;
        score -= issues.filter((i) => i.severity === 'warning').length * 10;
        score -= issues.filter((i) => i.severity === 'info').length * 5;
        score = Math.max(0, Math.min(100, score));
        return {
            score,
            bundleSize,
            metrics: { fcp, tti, lighthouse },
            issues,
            recommendations,
        };
    }
    /**
     * Validate code quality (ESLint, Prettier)
     * @param files - Generated code files
     * @returns Code quality validation result
     */
    validateCodeQuality(files) {
        const eslintViolations = [];
        const prettierViolations = [];
        const codeSmells = [];
        for (const file of files) {
            const content = file.content;
            // Basic ESLint checks
            const eslintChecks = this.checkESLintRules(content, file.filePath);
            eslintViolations.push(...eslintChecks);
            // Basic Prettier checks
            const prettierChecks = this.checkPrettierFormatting(content, file.filePath);
            prettierViolations.push(...prettierChecks);
            // Code smell detection
            const smells = this.detectCodeSmells(content, file.filePath);
            codeSmells.push(...smells);
        }
        // Calculate score
        let score = 100;
        score -= eslintViolations.filter((v) => v.severity === 'error').length * 10;
        score -= eslintViolations.filter((v) => v.severity === 'warning').length * 5;
        score -= prettierViolations.length * 3;
        score -= codeSmells.length * 5;
        score = Math.max(0, score);
        return {
            score,
            eslintViolations,
            prettierViolations,
            codeSmells,
        };
    }
    /**
     * Run all quality gates
     * @param files - Generated code files
     * @param wcagLevel - Target WCAG level
     * @returns Array of quality gate results
     */
    validateAll(files, wcagLevel = 'AA') {
        const results = [];
        // Accessibility gate
        const a11yResult = this.validateAccessibility(files, wcagLevel);
        results.push({
            name: 'Accessibility',
            passed: a11yResult.score >= 90,
            score: a11yResult.score,
            threshold: 90,
            details: `WCAG ${wcagLevel} compliance: ${a11yResult.violations.length} violations, ${a11yResult.warnings.length} warnings`,
            recommendations: a11yResult.violations.slice(0, 3).map((v) => v.remediation),
        });
        // TypeScript gate
        const tsResult = this.validateTypeScript(files);
        results.push({
            name: 'TypeScript Strict Mode',
            passed: tsResult.strictCompliant,
            score: tsResult.score,
            threshold: 100,
            details: `${tsResult.errors.length} errors, ${tsResult.warnings.length} warnings`,
            recommendations: tsResult.errors.slice(0, 3).map((e) => e.message),
        });
        // Performance gate
        const perfResult = this.validatePerformance(files);
        results.push({
            name: 'Performance',
            passed: perfResult.score >= 90,
            score: perfResult.score,
            threshold: 90,
            details: `Bundle: ${Math.round(perfResult.bundleSize / 1000)}KB, Lighthouse: ~${perfResult.metrics.lighthouse}`,
            recommendations: perfResult.recommendations.slice(0, 3),
        });
        // Code quality gate
        const qualityResult = this.validateCodeQuality(files);
        results.push({
            name: 'Code Quality',
            passed: qualityResult.score >= 85,
            score: qualityResult.score,
            threshold: 85,
            details: `${qualityResult.eslintViolations.length} ESLint issues, ${qualityResult.codeSmells.length} code smells`,
            recommendations: qualityResult.eslintViolations
                .slice(0, 3)
                .map((v) => `${v.rule}: ${v.message}`),
        });
        return results;
    }
    // Helper methods
    hasSemanticHTML(content) {
        const semanticTags = ['<button', '<nav', '<main', '<header', '<footer', '<article', '<section'];
        return semanticTags.some((tag) => content.includes(tag));
    }
    checkARIAAttributes(content) {
        const violations = [];
        const warnings = [];
        // Check for interactive elements without ARIA
        if ((content.includes('<div') || content.includes('<span')) &&
            content.includes('onclick') &&
            !content.includes('role=')) {
            violations.push({
                rule: 'interactive-elements-role',
                wcagLevel: 'A',
                description: 'Interactive div/span without role attribute',
                impact: 'serious',
                remediation: 'Add appropriate role attribute (e.g., role="button")',
            });
        }
        return {
            passed: violations.length === 0,
            violations,
            warnings,
        };
    }
    hasKeyboardNavigation(content) {
        return content.includes('onkeydown') ||
            content.includes('onkeypress') ||
            content.includes('onkeyup') ||
            content.includes('tabindex');
    }
    checkFocusManagement(content) {
        const violations = [];
        // Check for focus styles
        if (!content.includes('focus:') && !content.includes(':focus')) {
            violations.push({
                rule: 'focus-visible',
                wcagLevel: 'AA',
                description: 'Missing focus styles',
                impact: 'moderate',
                remediation: 'Add visible focus states using focus: or :focus pseudo-class',
            });
        }
        return { passed: violations.length === 0, violations };
    }
    checkColorContrast(content) {
        // Basic heuristic check
        const warnings = [];
        if (content.includes('text-gray-400') || content.includes('opacity-50')) {
            warnings.push({
                rule: 'color-contrast',
                description: 'Low contrast color classes detected',
                recommendation: 'Verify color contrast ratios meet WCAG standards',
            });
        }
        return { passed: warnings.length === 0, violations: [], warnings };
    }
    checkAltText(content) {
        const violations = [];
        // Check for img tags without alt
        if (content.includes('<img') && !content.includes('alt=')) {
            violations.push({
                rule: 'img-alt',
                wcagLevel: 'A',
                description: 'Image without alt attribute',
                impact: 'critical',
                remediation: 'Add descriptive alt text to all images',
            });
        }
        return { passed: violations.length === 0, violations };
    }
    checkESLintRules(content, file) {
        const violations = [];
        // Check for console.log
        const consoleMatches = content.matchAll(/console\.(log|warn|error)/g);
        for (const match of consoleMatches) {
            violations.push({
                rule: 'no-console',
                severity: 'warning',
                message: 'Unexpected console statement',
                file,
                line: this.getLineNumber(content, match.index || 0),
            });
        }
        return violations;
    }
    checkPrettierFormatting(content, file) {
        const violations = [];
        // Basic formatting checks
        if (content.includes('  \n') || content.includes('\t')) {
            violations.push({
                file,
                issue: 'Inconsistent whitespace',
            });
        }
        return violations;
    }
    detectCodeSmells(content, file) {
        const smells = [];
        // Long functions (> 50 lines)
        const functionMatches = content.matchAll(/(?:function|const)\s+\w+[^{]*\{([^}]*)\}/gs);
        for (const match of functionMatches) {
            const functionBody = match[1];
            if (functionBody) {
                const lineCount = functionBody.split('\n').length;
                if (lineCount > 50) {
                    smells.push({
                        type: 'long-function',
                        description: `Function exceeds 50 lines (${lineCount} lines)`,
                        file,
                        suggestion: 'Consider breaking into smaller functions',
                    });
                }
            }
        }
        return smells;
    }
    estimateFCP(bundleSize) {
        // Simple estimation: ~0.1ms per byte over network
        return Math.round(bundleSize * 0.1);
    }
    estimateTTI(bundleSize, issueCount) {
        const baseTime = this.estimateFCP(bundleSize);
        const parseTime = bundleSize * 0.05; // Parsing overhead
        const issueOverhead = issueCount * 100; // Each issue adds overhead
        return Math.round(baseTime + parseTime + issueOverhead);
    }
    estimateLighthouseScore(bundleSize, issues) {
        let score = 100;
        // Bundle size impact
        if (bundleSize > 100000)
            score -= 30;
        else if (bundleSize > 50000)
            score -= 15;
        // Issues impact
        score -= issues.filter((i) => i.severity === 'critical').length * 20;
        score -= issues.filter((i) => i.severity === 'warning').length * 10;
        return Math.max(0, Math.min(100, score));
    }
    getLineNumber(content, index) {
        return content.substring(0, index).split('\n').length;
    }
}
exports.QualityGatesValidator = QualityGatesValidator;
//# sourceMappingURL=quality-gates.js.map