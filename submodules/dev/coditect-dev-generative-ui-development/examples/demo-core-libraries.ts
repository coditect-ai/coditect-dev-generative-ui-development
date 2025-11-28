/**
 * Demo: Core Libraries in Action
 * Demonstrates UISynthesisEngine, TokenOptimizer, and QualityGatesValidator
 */

import {
  UISynthesisEngine,
  TokenOptimizer,
  QualityGatesValidator,
} from '../src';

/**
 * Demo 1: UI Synthesis Engine
 * Complete multi-agent pipeline for UI generation
 */
async function demoUISynthesisEngine() {
  console.log('\n=== Demo 1: UI Synthesis Engine ===\n');

  const engine = new UISynthesisEngine({
    maxTokenBudget: 20000,
    enableCaching: true,
    qualityGates: {
      accessibility: 90,
      performance: 90,
      strictTypes: true,
    },
  });

  const result = await engine.generateUI(
    'Create a Button component with primary, secondary, and ghost variants. Include small, medium, and large sizes. Ensure WCAG AA compliance and keyboard navigation.'
  );

  console.log('✅ Pipeline Result:');
  console.log(`  Success: ${result.success}`);
  console.log(`  Files Generated: ${result.files?.length ?? 0}`);
  console.log(`  Token Usage:`);
  console.log(`    - Intent Analysis: ${result.tokenUsage.intentAnalysis}`);
  console.log(`    - UI Architecture: ${result.tokenUsage.uiArchitecture}`);
  console.log(`    - Code Generation: ${result.tokenUsage.codeGeneration}`);
  console.log(`    - Total: ${result.tokenUsage.total}`);
  console.log(`  Duration: ${result.metadata.duration}ms`);

  if (result.qualityGates) {
    console.log('\n  Quality Gates:');
    result.qualityGates.forEach((gate) => {
      const status = gate.passed ? '✓' : '✗';
      console.log(`    ${status} ${gate.name}: ${gate.score}/${gate.threshold}`);
    });
  }

  // Demo caching
  console.log('\n🔄 Testing cache (re-running same generation):');
  const cachedResult = await engine.generateUI(
    'Create a Button component with primary, secondary, and ghost variants. Include small, medium, and large sizes. Ensure WCAG AA compliance and keyboard navigation.'
  );
  console.log(`  Cache Hit: ${cachedResult.tokenUsage.total === 0 ? 'YES' : 'NO'}`);

  const cacheStats = engine.getCacheStats();
  console.log(`\n📊 Cache Statistics:`);
  console.log(`  Total Entries: ${cacheStats.size}`);
  console.log(`  Entries: ${cacheStats.entries.map(e => `${e.hits} hits`).join(', ')}`);
}

/**
 * Demo 2: Token Optimizer
 * Cost tracking and optimization recommendations
 */
async function demoTokenOptimizer() {
  console.log('\n\n=== Demo 2: Token Optimizer ===\n');

  const optimizer = new TokenOptimizer({
    inputTokenCost: 3.0, // $3 per 1M tokens
    outputTokenCost: 15.0, // $15 per 1M tokens
    model: 'claude-sonnet-4.5',
  });

  // Record some usage
  optimizer.recordUsage({
    promptTokens: 200,
    completionTokens: 800,
    totalTokens: 1000,
    estimatedCost: optimizer.calculateCost(200, 800),
    generationType: 'component',
    timestamp: new Date(),
  });

  optimizer.recordUsage({
    promptTokens: 500,
    completionTokens: 3000,
    totalTokens: 3500,
    estimatedCost: optimizer.calculateCost(500, 3000),
    generationType: 'layout',
    timestamp: new Date(),
  });

  // Get statistics
  const stats = optimizer.getStatistics();
  console.log('📈 Token Usage Statistics:');
  console.log(`  Total Tokens: ${stats.totalTokens}`);
  console.log(`  Total Cost: $${stats.totalCost.toFixed(4)}`);
  console.log(`  Average Tokens/Generation: ${Math.round(stats.avgTokensPerGeneration)}`);

  console.log('\n  By Generation Type:');
  Object.entries(stats.byGenerationType).forEach(([type, profile]) => {
    console.log(`    ${type}:`);
    console.log(`      - Avg Tokens: ${Math.round(profile.avgTotalTokens)}`);
    console.log(`      - Avg Cost: $${profile.avgCost.toFixed(4)}`);
    console.log(`      - Samples: ${profile.sampleCount}`);
  });

  // Get optimization recommendations
  console.log('\n💡 Optimization Recommendations:');
  const recommendations = optimizer.getOptimizationRecommendations('component');
  recommendations.forEach((rec, idx) => {
    console.log(`\n  ${idx + 1}. ${rec.strategy} (${rec.effort} effort)`);
    console.log(`     Savings: ${rec.estimatedSavings} tokens ($${rec.estimatedCostSavings.toFixed(4)})`);
    console.log(`     Confidence: ${Math.round(rec.confidence * 100)}%`);
    console.log(`     ${rec.description}`);
  });

  // ROI analysis
  console.log('\n💰 ROI Analysis (100 generations/month):');
  const strategies: Array<'component-caching' | 'incremental-generation' | 'template-hybridization' | 'prompt-compression'> = [
    'component-caching',
    'incremental-generation',
    'template-hybridization',
    'prompt-compression',
  ];

  strategies.forEach((strategy) => {
    const roi = optimizer.getOptimizationROI(strategy, 100);
    console.log(`\n  ${strategy}:`);
    console.log(`    - Monthly Savings: $${roi.monthlySavings.toFixed(2)}`);
    console.log(`    - Annual Savings: $${roi.annualSavings.toFixed(2)}`);
    console.log(`    - Implementation Cost: $${roi.implementationCost.toFixed(2)}`);
    console.log(`    - Break-even: ${roi.breakEvenMonths.toFixed(1)} months`);
    console.log(`    - ROI: ${roi.roi.toFixed(1)}%`);
  });

  // Demo component caching
  console.log('\n🗄️  Component Caching:');
  optimizer.cacheComponent('button-primary', '<Button>Code here</Button>', 500);
  optimizer.cacheComponent('input-text', '<Input>Code here</Input>', 400);

  const cacheStats = optimizer.getCacheStatistics();
  console.log(`  Cached Components: ${cacheStats.size}`);
  console.log(`  Total Token Savings: ${cacheStats.totalTokensSaved}`);
}

/**
 * Demo 3: Quality Gates Validator
 * Validate generated code against quality standards
 */
async function demoQualityGates() {
  console.log('\n\n=== Demo 3: Quality Gates Validator ===\n');

  const validator = new QualityGatesValidator();

  // Sample generated code
  const sampleFiles = [
    {
      filePath: 'src/components/Button.tsx',
      content: `import { FC } from 'react';

export interface ButtonProps {
  variant: 'primary' | 'secondary' | 'ghost';
  size: 'sm' | 'md' | 'lg';
  disabled?: boolean;
  onClick?: () => void;
  children: React.ReactNode;
}

export const Button: FC<ButtonProps> = (props) => {
  return (
    <button
      className="px-4 py-2 rounded-md transition-colors focus:outline-none focus:ring-2"
      onClick={props.onClick}
      disabled={props.disabled}
      aria-label={props.children as string}
      role="button"
    >
      {props.children}
    </button>
  );
};

Button.displayName = 'Button';
`,
      language: 'tsx' as const,
    },
  ];

  // Run all quality gates
  console.log('🔍 Running Quality Gates...\n');
  const results = validator.validateAll(sampleFiles, 'AA');

  results.forEach((gate) => {
    const status = gate.passed ? '✅' : '❌';
    console.log(`${status} ${gate.name}`);
    console.log(`   Score: ${gate.score}/${gate.threshold}`);
    console.log(`   Details: ${gate.details}`);
    if (gate.recommendations && gate.recommendations.length > 0) {
      console.log(`   Recommendations:`);
      gate.recommendations.forEach((rec) => {
        console.log(`     - ${rec}`);
      });
    }
    console.log('');
  });

  // Individual validations
  console.log('\n📋 Detailed Accessibility Validation:');
  const a11yResult = validator.validateAccessibility(sampleFiles, 'AA');
  console.log(`  Level Achieved: WCAG ${a11yResult.level}`);
  console.log(`  Score: ${a11yResult.score}/100`);
  console.log(`  Violations: ${a11yResult.violations.length}`);
  console.log(`  Warnings: ${a11yResult.warnings.length}`);
  console.log(`  Passed Checks: ${a11yResult.passed.join(', ')}`);

  if (a11yResult.violations.length > 0) {
    console.log('\n  Violations:');
    a11yResult.violations.forEach((v) => {
      console.log(`    - [${v.impact}] ${v.description}`);
      console.log(`      Fix: ${v.remediation}`);
    });
  }

  console.log('\n🔧 TypeScript Strict Mode Validation:');
  const tsResult = validator.validateTypeScript(sampleFiles);
  console.log(`  Strict Compliant: ${tsResult.strictCompliant ? 'YES' : 'NO'}`);
  console.log(`  Score: ${tsResult.score}/100`);
  console.log(`  Errors: ${tsResult.errors.length}`);
  console.log(`  Warnings: ${tsResult.warnings.length}`);

  console.log('\n⚡ Performance Validation:');
  const perfResult = validator.validatePerformance(sampleFiles);
  console.log(`  Score: ${perfResult.score}/100`);
  console.log(`  Bundle Size: ${Math.round(perfResult.bundleSize / 1000)}KB`);
  console.log(`  Metrics:`);
  console.log(`    - First Contentful Paint: ~${perfResult.metrics.fcp}ms`);
  console.log(`    - Time to Interactive: ~${perfResult.metrics.tti}ms`);
  console.log(`    - Lighthouse Score: ~${perfResult.metrics.lighthouse}`);
  console.log(`  Issues: ${perfResult.issues.length}`);

  if (perfResult.recommendations.length > 0) {
    console.log(`  Recommendations:`);
    perfResult.recommendations.forEach((rec) => {
      console.log(`    - ${rec}`);
    });
  }

  console.log('\n✨ Code Quality Validation:');
  const qualityResult = validator.validateCodeQuality(sampleFiles);
  console.log(`  Score: ${qualityResult.score}/100`);
  console.log(`  ESLint Violations: ${qualityResult.eslintViolations.length}`);
  console.log(`  Prettier Violations: ${qualityResult.prettierViolations.length}`);
  console.log(`  Code Smells: ${qualityResult.codeSmells.length}`);
}

/**
 * Run all demos
 */
async function main() {
  console.log('🚀 CODITECT Generative UI - Core Libraries Demo');
  console.log('================================================\n');

  try {
    await demoUISynthesisEngine();
    await demoTokenOptimizer();
    await demoQualityGates();

    console.log('\n\n✅ All demos completed successfully!\n');
  } catch (error) {
    console.error('\n❌ Demo failed:', error);
    process.exit(1);
  }
}

// Run if executed directly
if (require.main === module) {
  main();
}
