/**
 * Complete Workflow Example
 * Demonstrates all 5 specialist agents working together
 */

import {
  IntentAnalyzer,
  UIArchitect,
  CodeGenerator,
  AccessibilityAuditor,
  QualityReviewer,
  type AgentContext,
} from '../src';

async function completeGenerationWorkflow() {
  console.log('🚀 CODITECT Generative UI - Complete Workflow Demo\n');

  // Create execution context
  const context: AgentContext = {
    executionId: `exec_${Date.now()}`,
    spec: {} as any,
    config: {
      qualityGates: {
        accessibility: 85,
        strictTypes: true,
      },
    },
    tokens: { prompt: 0, completion: 0, total: 0 },
    metadata: { startTime: new Date() },
  };

  // User's natural language request
  const userRequest =
    'Build a primary button component with variants (primary, secondary, ghost) and sizes (sm, md, lg)';

  console.log('📝 User Request:', userRequest);
  console.log('\n' + '='.repeat(80) + '\n');

  // STEP 1: Intent Analysis
  console.log('🔍 STEP 1: Intent Analysis');
  const intentAnalyzer = new IntentAnalyzer();
  const intentResult = await intentAnalyzer.execute({ description: userRequest }, context);

  if (!intentResult.success || !intentResult.data) {
    throw new Error('Intent analysis failed');
  }

  console.log('✅ Intent analyzed successfully');
  console.log('   - Type:', intentResult.data.type);
  console.log('   - Framework:', intentResult.data.framework);
  console.log('   - Styling:', intentResult.data.styling);
  console.log(
    '   - Variants:',
    intentResult.data.componentOptions?.variants?.join(', ')
  );
  console.log('   - Sizes:', intentResult.data.componentOptions?.sizes?.join(', '));
  console.log('   - Tokens:', intentResult.tokens);
  console.log('\n' + '='.repeat(80) + '\n');

  context.spec = intentResult.data;
  context.tokens.prompt += intentResult.tokens.prompt;
  context.tokens.completion += intentResult.tokens.completion;

  // STEP 2: UI Architecture Design
  console.log('🏗️  STEP 2: UI Architecture Design');
  const uiArchitect = new UIArchitect();
  const architectResult = await uiArchitect.execute(intentResult.data, context);

  if (!architectResult.success || !architectResult.data) {
    throw new Error('UI architecture design failed');
  }

  console.log('✅ Architecture designed successfully');
  console.log('   - Components:', architectResult.data.components.length);
  console.log(
    '   - Component name:',
    architectResult.data.components[0]?.name
  );
  console.log('   - Patterns:', architectResult.data.patterns.join(', '));
  console.log('   - Dependencies:', architectResult.data.dependencies.join(', '));
  console.log('   - Tokens:', architectResult.tokens);
  console.log('\n' + '='.repeat(80) + '\n');

  context.tokens.prompt += architectResult.tokens.prompt;
  context.tokens.completion += architectResult.tokens.completion;

  // STEP 3: Code Generation
  console.log('💻 STEP 3: Code Generation');
  const codeGenerator = new CodeGenerator();
  const codeResult = await codeGenerator.execute(
    {
      architecture: architectResult.data,
      framework: intentResult.data.framework,
      styling: intentResult.data.styling,
      strictTypes: true,
    },
    context
  );

  if (!codeResult.success || !codeResult.data) {
    throw new Error('Code generation failed');
  }

  console.log('✅ Code generated successfully');
  console.log('   - Files generated:', codeResult.data.length);
  codeResult.data.forEach((file) => {
    console.log(
      `   - ${file.filePath} (${file.content.length} chars, ${file.language})`
    );
  });
  console.log('   - Tokens:', codeResult.tokens);
  console.log('\n' + '='.repeat(80) + '\n');

  context.tokens.prompt += codeResult.tokens.prompt;
  context.tokens.completion += codeResult.tokens.completion;

  // STEP 4: Accessibility Audit
  console.log('♿ STEP 4: Accessibility Audit');
  const accessibilityAuditor = new AccessibilityAuditor();

  // Audit the first generated file
  const mainFile = codeResult.data[0];
  if (!mainFile) {
    throw new Error('No files generated');
  }

  const a11yResult = await accessibilityAuditor.execute(
    {
      code: mainFile.content,
      spec: {
        type: intentResult.data.type,
        framework: intentResult.data.framework,
        requirements: intentResult.data.requirements,
      },
    },
    context
  );

  if (!a11yResult.data) {
    throw new Error('Accessibility audit failed');
  }

  console.log(
    a11yResult.success ? '✅ Accessibility audit passed' : '⚠️  Accessibility issues found'
  );
  console.log('   - Score:', a11yResult.data.score, '/100');
  console.log('   - WCAG Level:', a11yResult.data.wcagLevel);
  console.log('   - Violations:', a11yResult.data.violationCount);
  console.log('   - Passed checks:', a11yResult.data.passedChecks.length);
  console.log('   - Tokens:', a11yResult.tokens);

  if (a11yResult.data.violations.length > 0) {
    console.log('\n   Top violations:');
    a11yResult.data.violations.slice(0, 3).forEach((v) => {
      console.log(
        `   - [${v.severity.toUpperCase()}] ${v.wcagCriterion}: ${v.description}`
      );
    });
  }

  console.log('\n' + '='.repeat(80) + '\n');

  context.tokens.prompt += a11yResult.tokens.prompt;
  context.tokens.completion += a11yResult.tokens.completion;

  // STEP 5: Quality Review
  console.log('🔎 STEP 5: Quality Review');
  const qualityReviewer = new QualityReviewer();
  const qualityResult = await qualityReviewer.execute(
    {
      code: mainFile.content,
      architecture: architectResult.data,
      accessibilityReport: {
        score: a11yResult.data.score,
        wcagLevel: a11yResult.data.wcagLevel,
        violationCount: a11yResult.data.violationCount,
      },
    },
    context
  );

  if (!qualityResult.data) {
    throw new Error('Quality review failed');
  }

  console.log(
    qualityResult.success
      ? '✅ Quality review approved'
      : '❌ Quality review failed - fixes required'
  );
  console.log('   - Score:', qualityResult.data.score, '/100');
  console.log('   - Issues found:', qualityResult.data.issueCount);
  console.log('   - Strengths:', qualityResult.data.strengths.length);
  console.log('   - Tokens:', qualityResult.tokens);

  console.log('\n   Metrics:');
  console.log(
    '   - TypeScript strict:',
    qualityResult.data.metrics.typeStrict ? 'Yes' : 'No'
  );
  console.log(
    '   - Bundle size:',
    Math.round(qualityResult.data.metrics.estimatedBundleSize / 1000),
    'KB'
  );
  console.log('   - Complexity:', qualityResult.data.metrics.complexity, '/10');
  console.log(
    '   - Test coverage potential:',
    qualityResult.data.metrics.testCoveragePotential,
    '%'
  );

  if (qualityResult.data.issues.length > 0) {
    console.log('\n   Top issues:');
    qualityResult.data.issues.slice(0, 3).forEach((issue) => {
      console.log(
        `   - [${issue.severity.toUpperCase()}] ${issue.category}: ${issue.description}`
      );
    });
  }

  console.log('\n' + '='.repeat(80) + '\n');

  context.tokens.prompt += qualityResult.tokens.prompt;
  context.tokens.completion += qualityResult.tokens.completion;

  // FINAL SUMMARY
  const endTime = new Date();
  const duration = endTime.getTime() - context.metadata.startTime.getTime();
  context.metadata.endTime = endTime;
  context.metadata.duration = duration;
  context.tokens.total = context.tokens.prompt + context.tokens.completion;

  console.log('📊 WORKFLOW SUMMARY\n');
  console.log('Duration:', Math.round(duration), 'ms');
  console.log('Total tokens:', context.tokens.total);
  console.log('  - Prompt:', context.tokens.prompt);
  console.log('  - Completion:', context.tokens.completion);
  console.log(
    'Estimated cost: $',
    ((context.tokens.prompt * 0.003 + context.tokens.completion * 0.015) / 1000).toFixed(4)
  );

  console.log('\nFinal Status:');
  console.log('  - Intent Analysis:', intentResult.success ? '✅' : '❌');
  console.log('  - Architecture Design:', architectResult.success ? '✅' : '❌');
  console.log('  - Code Generation:', codeResult.success ? '✅' : '❌');
  console.log('  - Accessibility Audit:', a11yResult.success ? '✅' : '⚠️');
  console.log('  - Quality Review:', qualityResult.success ? '✅' : '❌');

  const overallSuccess =
    intentResult.success &&
    architectResult.success &&
    codeResult.success &&
    qualityResult.success;

  console.log(
    '\n' +
      (overallSuccess
        ? '🎉 All agents completed successfully! Code is production-ready.'
        : '⚠️  Some quality gates failed. Review issues before deployment.')
  );

  // Output generated code preview
  console.log('\n' + '='.repeat(80));
  console.log('📄 GENERATED CODE PREVIEW\n');
  console.log(mainFile.filePath);
  console.log('-'.repeat(80));
  console.log(mainFile.content.split('\n').slice(0, 30).join('\n'));
  console.log('... (truncated)');
  console.log('='.repeat(80));

  return {
    success: overallSuccess,
    spec: intentResult.data,
    architecture: architectResult.data,
    files: codeResult.data,
    accessibility: a11yResult.data,
    quality: qualityResult.data,
    metadata: {
      tokens: context.tokens,
      duration,
    },
  };
}

// Run the workflow
if (require.main === module) {
  completeGenerationWorkflow()
    .then((result) => {
      console.log(
        '\n✅ Workflow completed:',
        result.success ? 'SUCCESS' : 'WITH ISSUES'
      );
      process.exit(result.success ? 0 : 1);
    })
    .catch((error) => {
      console.error('\n❌ Workflow failed:', error);
      process.exit(1);
    });
}

export { completeGenerationWorkflow };
