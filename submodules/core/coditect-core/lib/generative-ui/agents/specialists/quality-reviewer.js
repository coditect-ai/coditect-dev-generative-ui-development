"use strict";
/**
 * Quality Reviewer Agent
 * Ensures production-ready React + TypeScript code quality
 * @module agents/specialists/quality-reviewer
 */
Object.defineProperty(exports, "__esModule", { value: true });
exports.QualityReviewer = void 0;
const base_1 = require("../base");
/**
 * Quality Reviewer Agent
 * Performs comprehensive code quality review for production readiness
 */
class QualityReviewer extends base_1.BaseAgent {
    constructor() {
        super({
            name: 'quality-reviewer',
            role: base_1.AgentRole.VALIDATOR,
            description: 'Ensures production-ready React + TypeScript code quality and best practices',
            capabilities: [
                'validate-typescript-strict',
                'review-react-patterns',
                'analyze-performance',
                'check-code-style',
                'assess-testability',
                'identify-security-risks',
            ],
        });
    }
    /**
     * Execute quality review
     */
    async execute(input, _context) {
        this.log('info', 'Starting quality review', {
            codeLength: input.code.length,
            hasArchitecture: !!input.architecture,
            hasA11yReport: !!input.accessibilityReport,
        });
        if (!this.validateInput(input)) {
            return {
                success: false,
                error: {
                    message: 'Invalid quality review input: code is required',
                    code: 'INVALID_INPUT',
                },
                tokens: { prompt: 0, completion: 0 },
            };
        }
        try {
            const report = await this.reviewQuality(input);
            this.log('info', 'Quality review complete', {
                score: report.score,
                approved: report.approved,
                issueCount: report.issueCount,
            });
            // Convert issues to validation results
            const validation = report.issues.map((issue) => ({
                rule: issue.rule,
                passed: false,
                message: issue.description,
                severity: issue.severity === 'blocker' || issue.severity === 'critical'
                    ? 'error'
                    : issue.severity === 'major'
                        ? 'warning'
                        : 'info',
                details: {
                    id: issue.id,
                    category: issue.category,
                    recommendation: issue.recommendation,
                    location: issue.location,
                },
            }));
            // Add strengths as validation results
            report.strengths.forEach((strength) => {
                validation.push({
                    rule: 'quality-strength',
                    passed: true,
                    message: `Strength: ${strength}`,
                    severity: 'info',
                });
            });
            return {
                success: report.approved,
                data: report,
                tokens: {
                    prompt: this.estimateTokens(input),
                    completion: Math.ceil(JSON.stringify(report).length / 4),
                },
                validation,
            };
        }
        catch (error) {
            this.log('error', 'Quality review failed', { error });
            return {
                success: false,
                error: {
                    message: error instanceof Error ? error.message : 'Unknown error',
                    code: 'REVIEW_FAILED',
                    details: error,
                },
                tokens: { prompt: 0, completion: 0 },
            };
        }
    }
    /**
     * Validate input
     */
    validateInput(input) {
        return !!input.code && input.code.trim().length > 0;
    }
    /**
     * Perform comprehensive quality review
     */
    async reviewQuality(input) {
        const issues = [];
        const strengths = [];
        // 1. TypeScript strict mode compliance
        const tsResults = this.reviewTypeScript(input.code);
        issues.push(...tsResults.issues);
        strengths.push(...tsResults.strengths);
        // 2. React best practices
        const reactResults = this.reviewReactPatterns(input.code);
        issues.push(...reactResults.issues);
        strengths.push(...reactResults.strengths);
        // 3. Performance analysis
        const perfResults = this.analyzePerformance(input.code);
        issues.push(...perfResults.issues);
        strengths.push(...perfResults.strengths);
        // 4. Code style and conventions
        const styleResults = this.reviewCodeStyle(input.code);
        issues.push(...styleResults.issues);
        strengths.push(...styleResults.strengths);
        // 5. Testability assessment
        const testResults = this.assessTestability(input.code);
        issues.push(...testResults.issues);
        strengths.push(...testResults.strengths);
        // 6. Security risk identification
        const securityResults = this.identifySecurityRisks(input.code);
        issues.push(...securityResults.issues);
        strengths.push(...securityResults.strengths);
        // Calculate metrics
        const metrics = this.calculateMetrics(input.code, issues);
        // Calculate score (100 - deductions for issues)
        const deductions = issues.reduce((sum, issue) => {
            const severityPoints = {
                blocker: 30,
                critical: 20,
                major: 10,
                minor: 5,
                info: 1,
            };
            return sum + severityPoints[issue.severity];
        }, 0);
        const score = Math.max(0, 100 - deductions);
        // Determine approval status
        const blockers = issues.filter((i) => i.severity === 'blocker').length;
        const critical = issues.filter((i) => i.severity === 'critical').length;
        const approved = blockers === 0 && critical === 0 && score >= 70;
        // Generate recommendations
        const recommendations = this.generateRecommendations(issues, metrics);
        // Generate summary
        const summary = this.generateSummary(score, approved, issues.length);
        return {
            score,
            approved,
            issueCount: issues.length,
            issues,
            strengths,
            summary,
            recommendations,
            metrics,
        };
    }
    /**
     * Review TypeScript strict mode compliance
     */
    reviewTypeScript(code) {
        const issues = [];
        const strengths = [];
        // Check for 'any' type usage
        const anyMatches = code.match(/:\s*any\b/g);
        if (anyMatches && anyMatches.length > 0) {
            issues.push({
                id: 'ts-001',
                category: 'typescript',
                severity: 'blocker',
                description: `Found ${anyMatches.length} instances of 'any' type`,
                rule: 'no-any-types',
                recommendation: 'Replace all "any" types with specific types or "unknown"',
            });
        }
        else {
            strengths.push('Strict TypeScript typing (no "any" types)');
        }
        // Check for proper interface/type definitions
        if (code.includes('interface ') || code.includes('type ')) {
            strengths.push('Uses TypeScript interfaces/types');
        }
        else if (code.length > 100) {
            issues.push({
                id: 'ts-002',
                category: 'typescript',
                severity: 'major',
                description: 'Missing explicit type definitions',
                rule: 'explicit-types',
                recommendation: 'Define interfaces for component props and state',
            });
        }
        // Check for type assertions (as Type)
        const typeAssertions = code.match(/as\s+\w+/g);
        if (typeAssertions && typeAssertions.length > 2) {
            issues.push({
                id: 'ts-003',
                category: 'typescript',
                severity: 'minor',
                description: `Excessive type assertions (${typeAssertions.length} found)`,
                rule: 'minimal-type-assertions',
                recommendation: 'Refactor to avoid type assertions; improve type inference',
            });
        }
        // Check for non-null assertions (!)
        const nonNullAssertions = code.match(/!\./g) || code.match(/!\)/g);
        if (nonNullAssertions && nonNullAssertions.length > 0) {
            issues.push({
                id: 'ts-004',
                category: 'typescript',
                severity: 'major',
                description: 'Non-null assertions (!) can cause runtime errors',
                rule: 'no-non-null-assertion',
                recommendation: 'Use optional chaining (?.) or null checks instead',
            });
        }
        return { issues, strengths };
    }
    /**
     * Review React best practices
     */
    reviewReactPatterns(code) {
        const issues = [];
        const strengths = [];
        // Check for proper component declaration (FC, memo)
        if (code.includes(': FC<') || code.includes(': React.FC<')) {
            strengths.push('Uses FC type for functional components');
        }
        // Check for hooks usage rules
        if (code.includes('useState') || code.includes('useEffect')) {
            strengths.push('Uses React hooks');
            // Check for useEffect cleanup
            if (code.includes('useEffect') && !code.match(/return\s*\(\s*\)\s*=>/)) {
                issues.push({
                    id: 'react-001',
                    category: 'react',
                    severity: 'minor',
                    description: 'useEffect may be missing cleanup function',
                    rule: 'useeffect-cleanup',
                    recommendation: 'Add cleanup function to useEffect if it sets up subscriptions/timers',
                });
            }
        }
        // Check for key prop in lists
        if (code.includes('.map(') && !code.includes('key=')) {
            issues.push({
                id: 'react-002',
                category: 'react',
                severity: 'critical',
                description: 'Missing key prop in list rendering',
                rule: 'react-key-prop',
                recommendation: 'Add unique key prop to mapped elements',
            });
        }
        // Check for proper event handler typing
        if (code.match(/onClick.*=.*\{.*\}/) &&
            !code.includes('MouseEvent') &&
            !code.includes('() => void')) {
            issues.push({
                id: 'react-003',
                category: 'react',
                severity: 'minor',
                description: 'Event handlers may lack proper typing',
                rule: 'typed-event-handlers',
                recommendation: 'Type event handlers: onClick: (e: React.MouseEvent) => void',
            });
        }
        // Check for useMemo/useCallback optimization
        if ((code.includes('.map(') || code.includes('filter(')) &&
            !code.includes('useMemo')) {
            issues.push({
                id: 'react-004',
                category: 'react',
                severity: 'info',
                description: 'Consider memoization for expensive computations',
                rule: 'performance-optimization',
                recommendation: 'Wrap expensive operations in useMemo',
            });
        }
        else if (code.includes('useMemo') || code.includes('useCallback')) {
            strengths.push('Implements performance optimizations (memoization)');
        }
        // Check for prop spreading (...props)
        if (code.includes('{...props}') && !code.includes('Omit<')) {
            issues.push({
                id: 'react-005',
                category: 'react',
                severity: 'minor',
                description: 'Prop spreading without type restrictions',
                rule: 'explicit-props',
                recommendation: 'Use Omit<> to exclude specific props when spreading',
            });
        }
        return { issues, strengths };
    }
    /**
     * Analyze performance characteristics
     */
    analyzePerformance(code) {
        const issues = [];
        const strengths = [];
        // Estimate bundle size (rough approximation)
        const estimatedSize = code.length;
        if (estimatedSize > 50000) {
            issues.push({
                id: 'perf-001',
                category: 'performance',
                severity: 'major',
                description: `Large component size (~${Math.round(estimatedSize / 1000)}KB)`,
                rule: 'bundle-size-limit',
                recommendation: 'Split into smaller components or use code splitting',
            });
        }
        else if (estimatedSize < 10000) {
            strengths.push('Compact component size');
        }
        // Check for lazy loading
        if (code.includes('React.lazy') || code.includes('dynamic import')) {
            strengths.push('Implements code splitting / lazy loading');
        }
        // Check for heavy dependencies
        const heavyDeps = ['moment', 'lodash'];
        heavyDeps.forEach((dep) => {
            if (code.includes(`from '${dep}'`) && !code.includes('import(')) {
                issues.push({
                    id: `perf-002-${dep}`,
                    category: 'performance',
                    severity: 'minor',
                    description: `Heavy dependency: ${dep}`,
                    rule: 'lightweight-dependencies',
                    recommendation: `Consider lighter alternative or tree-shaking (import { specific } from '${dep}')`,
                });
            }
        });
        // Check for inline function definitions in JSX
        const inlineFunctions = code.match(/onClick=\{.*=>.*\}/g);
        if (inlineFunctions && inlineFunctions.length > 3) {
            issues.push({
                id: 'perf-003',
                category: 'performance',
                severity: 'info',
                description: `${inlineFunctions.length} inline arrow functions in JSX`,
                rule: 'avoid-inline-functions',
                recommendation: 'Extract to useCallback for stable references',
            });
        }
        // Check for React.memo usage
        if (code.includes('React.memo') || code.includes('memo(')) {
            strengths.push('Uses React.memo for component memoization');
        }
        return { issues, strengths };
    }
    /**
     * Review code style and conventions
     */
    reviewCodeStyle(code) {
        const issues = [];
        const strengths = [];
        // Check for consistent naming conventions
        const componentNameMatch = code.match(/(?:export )?(?:const|function) (\w+)/);
        if (componentNameMatch && componentNameMatch[1]) {
            const componentName = componentNameMatch[1];
            if (componentName[0] && componentName[0] !== componentName[0].toUpperCase()) {
                issues.push({
                    id: 'style-001',
                    category: 'style',
                    severity: 'minor',
                    description: 'Component name should start with uppercase',
                    rule: 'pascal-case-components',
                    recommendation: `Rename ${componentName} to ${componentName[0].toUpperCase() + componentName.slice(1)}`,
                });
            }
            else {
                strengths.push('Follows PascalCase naming for components');
            }
        }
        // Check for displayName
        if (code.includes('.displayName')) {
            strengths.push('Includes displayName for debugging');
        }
        // Check for JSDoc comments
        if (code.includes('/**')) {
            strengths.push('Includes JSDoc documentation');
        }
        else if (code.length > 200) {
            issues.push({
                id: 'style-002',
                category: 'style',
                severity: 'info',
                description: 'Missing JSDoc comments',
                rule: 'component-documentation',
                recommendation: 'Add JSDoc comments for props and component purpose',
            });
        }
        // Check for consistent quote style
        const singleQuotes = (code.match(/'/g) || []).length;
        const doubleQuotes = (code.match(/"/g) || []).length;
        if (singleQuotes > 10 && doubleQuotes > 10) {
            issues.push({
                id: 'style-003',
                category: 'style',
                severity: 'info',
                description: 'Inconsistent quote style (mix of single and double)',
                rule: 'consistent-quotes',
                recommendation: 'Configure Prettier to enforce consistent quotes',
            });
        }
        return { issues, strengths };
    }
    /**
     * Assess testability
     */
    assessTestability(code) {
        const issues = [];
        const strengths = [];
        // Check for testable patterns (props-based, pure functions)
        if (code.includes('export interface') && code.includes('Props')) {
            strengths.push('Well-defined props interface (testable)');
        }
        // Check for hard-coded values (makes testing harder)
        const hardCodedValues = code.match(/=\s*['"]http|=\s*['"]\/api/g);
        if (hardCodedValues && hardCodedValues.length > 0) {
            issues.push({
                id: 'test-001',
                category: 'testing',
                severity: 'minor',
                description: 'Hard-coded URLs/endpoints reduce testability',
                rule: 'configurable-dependencies',
                recommendation: 'Pass URLs as props or use environment variables',
            });
        }
        // Check for side effects in render (reduces testability)
        if (code.includes('useEffect') && code.includes('fetch(')) {
            issues.push({
                id: 'test-002',
                category: 'testing',
                severity: 'info',
                description: 'API calls in useEffect complicate testing',
                rule: 'testable-side-effects',
                recommendation: 'Extract data fetching to custom hook or service layer',
            });
        }
        // Check for data-testid attributes
        if (code.includes('data-testid')) {
            strengths.push('Includes test IDs for reliable testing');
        }
        return { issues, strengths };
    }
    /**
     * Identify security risks
     */
    identifySecurityRisks(code) {
        const issues = [];
        const strengths = [];
        // Check for dangerouslySetInnerHTML
        if (code.includes('dangerouslySetInnerHTML')) {
            issues.push({
                id: 'security-001',
                category: 'security',
                severity: 'blocker',
                description: 'Use of dangerouslySetInnerHTML can lead to XSS attacks',
                rule: 'no-dangerous-html',
                recommendation: 'Sanitize HTML or use safer alternatives (markdown libraries)',
            });
        }
        else {
            strengths.push('No use of dangerouslySetInnerHTML');
        }
        // Check for eval() usage
        if (code.includes('eval(')) {
            issues.push({
                id: 'security-002',
                category: 'security',
                severity: 'blocker',
                description: 'eval() is a security risk',
                rule: 'no-eval',
                recommendation: 'Remove eval() and use safer alternatives',
            });
        }
        // Check for localStorage without encryption
        if (code.includes('localStorage.setItem') && code.includes('token')) {
            issues.push({
                id: 'security-003',
                category: 'security',
                severity: 'critical',
                description: 'Storing sensitive data (token) in localStorage',
                rule: 'secure-storage',
                recommendation: 'Use httpOnly cookies or encrypt sensitive data',
            });
        }
        return { issues, strengths };
    }
    /**
     * Calculate quality metrics
     */
    calculateMetrics(code, issues) {
        // TypeScript strict mode compliance
        const typeStrict = !issues.some((i) => i.id === 'ts-001');
        // Estimated bundle size
        const estimatedBundleSize = code.length;
        // Component complexity (1-10 scale based on code size, nesting, hooks)
        const lines = code.split('\n').length;
        const hooksCount = (code.match(/use\w+/g) || []).length;
        const nestingDepth = Math.max(...code.split('\n').map((line) => line.match(/^\s*/)?.[0].length || 0)) /
            2;
        const complexity = Math.min(10, Math.ceil((lines / 50 + hooksCount / 3 + nestingDepth / 5) / 3));
        // Test coverage potential (0-100, higher is easier to test)
        const hasExplicitProps = code.includes('interface') && code.includes('Props');
        const hasTestIds = code.includes('data-testid');
        const hasHardCodedDeps = issues.some((i) => i.id === 'test-001');
        const testCoveragePotential = (hasExplicitProps ? 40 : 0) +
            (hasTestIds ? 30 : 0) +
            (hasHardCodedDeps ? 0 : 30);
        return {
            typeStrict,
            estimatedBundleSize,
            complexity,
            testCoveragePotential,
        };
    }
    /**
     * Generate actionable recommendations
     */
    generateRecommendations(issues, metrics) {
        const recommendations = [];
        // Critical fixes first
        const blockers = issues.filter((i) => i.severity === 'blocker');
        if (blockers.length > 0) {
            recommendations.push(`🔴 BLOCKERS: Fix ${blockers.length} blocking issues before deployment`);
            blockers.forEach((b) => recommendations.push(`  • ${b.recommendation}`));
        }
        const critical = issues.filter((i) => i.severity === 'critical');
        if (critical.length > 0) {
            recommendations.push(`🟠 CRITICAL: Address ${critical.length} critical issues for production readiness`);
        }
        // TypeScript strict mode
        if (!metrics.typeStrict) {
            recommendations.push('🎯 PRIORITY: Eliminate all "any" types for type safety');
        }
        // Performance recommendations
        if (metrics.estimatedBundleSize > 30000) {
            recommendations.push('⚡ PERFORMANCE: Consider code splitting to reduce bundle size');
        }
        // Testability recommendations
        if (metrics.testCoveragePotential < 50) {
            recommendations.push('🧪 TESTING: Improve testability by adding props interfaces and test IDs');
        }
        return recommendations;
    }
    /**
     * Generate summary message
     */
    generateSummary(score, approved, issueCount) {
        if (approved && score >= 90) {
            return `Excellent code quality! Production-ready with ${issueCount} minor improvements suggested.`;
        }
        else if (approved && score >= 80) {
            return `Good code quality. Approved for deployment with ${issueCount} recommended fixes.`;
        }
        else if (approved) {
            return `Acceptable quality (baseline met). Address ${issueCount} issues for improved maintainability.`;
        }
        else {
            return `Quality issues detected. ${issueCount} issues must be resolved before deployment approval.`;
        }
    }
}
exports.QualityReviewer = QualityReviewer;
exports.default = QualityReviewer;
//# sourceMappingURL=quality-reviewer.js.map