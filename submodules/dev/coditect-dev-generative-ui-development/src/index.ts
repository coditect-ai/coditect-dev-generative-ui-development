/**
 * CODITECT Generative UI - Main Entry Point
 * @module index
 */

// Export types
export * from './types';

// Export base agent
export { BaseAgent, AgentRole, type AgentConfig } from './agents/base';

// Export specialist agents
export { IntentAnalyzer, type IntentAnalysisInput } from './agents/specialists/intent-analyzer';
export {
  UIArchitect,
  type UIArchitecture,
  type ComponentNode,
  type LayoutStructure,
} from './agents/specialists/ui-architect';
export {
  CodeGenerator,
  type CodeGenerationInput,
} from './agents/specialists/code-generator';

// Export orchestrator (to be implemented)
// export { Orchestrator } from './agents/core/orchestrator';

/**
 * Library version
 */
export const VERSION = '0.1.0';

/**
 * Quick helper to generate a UI component
 */
export async function generateUI(description: string) {
  const { IntentAnalyzer } = await import('./agents/specialists/intent-analyzer');
  const { UIArchitect } = await import('./agents/specialists/ui-architect');
  const { CodeGenerator } = await import('./agents/specialists/code-generator');

  // Create execution context
  const context = {
    executionId: `exec_${Date.now()}`,
    spec: {} as any,
    config: {},
    tokens: { prompt: 0, completion: 0, total: 0 },
    metadata: { startTime: new Date() },
  };

  // Step 1: Analyze intent
  const intentAnalyzer = new IntentAnalyzer();
  const intentResult = await intentAnalyzer.execute({ description }, context);

  if (!intentResult.success || !intentResult.data) {
    throw new Error('Intent analysis failed');
  }

  context.spec = intentResult.data;

  // Step 2: Design architecture
  const uiArchitect = new UIArchitect();
  const architectResult = await uiArchitect.execute(intentResult.data, context);

  if (!architectResult.success || !architectResult.data) {
    throw new Error('UI architecture design failed');
  }

  // Step 3: Generate code
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

  // Calculate total tokens
  context.tokens.total =
    (intentResult.tokens.prompt + intentResult.tokens.completion) +
    (architectResult.tokens.prompt + architectResult.tokens.completion) +
    (codeResult.tokens.prompt + codeResult.tokens.completion);

  context.metadata.endTime = new Date();
  context.metadata.duration =
    context.metadata.endTime.getTime() - context.metadata.startTime.getTime();

  return {
    spec: intentResult.data,
    architecture: architectResult.data,
    files: codeResult.data,
    metadata: {
      tokens: context.tokens,
      duration: context.metadata.duration,
    },
  };
}
