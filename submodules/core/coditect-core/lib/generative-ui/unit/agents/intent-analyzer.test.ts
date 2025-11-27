/**
 * Intent Analyzer Agent - Unit Tests
 */

import { IntentAnalyzer } from '../../../src/agents/specialists/intent-analyzer';
import { AgentContext } from '../../../src/types';

describe('IntentAnalyzer', () => {
  let agent: IntentAnalyzer;
  let context: AgentContext;

  beforeEach(() => {
    agent = new IntentAnalyzer();
    context = {
      executionId: 'test-exec-1',
      spec: {} as any,
      config: {},
      tokens: { prompt: 0, completion: 0, total: 0 },
      metadata: { startTime: new Date() },
    };
  });

  describe('Component Detection', () => {
    it('should detect component type from description', async () => {
      const result = await agent.execute(
        { description: 'Create a Button component with primary and secondary variants' },
        context
      );

      expect(result.success).toBe(true);
      expect(result.data?.type).toBe('component');
    });

    it('should extract component variants', async () => {
      const result = await agent.execute(
        { description: 'Button with primary, secondary, and ghost variants' },
        context
      );

      expect(result.success).toBe(true);
      expect(result.data?.componentOptions?.variants).toContain('primary');
      expect(result.data?.componentOptions?.variants).toContain('secondary');
      expect(result.data?.componentOptions?.variants).toContain('ghost');
    });

    it('should extract component sizes', async () => {
      const result = await agent.execute(
        { description: 'Create a Button with small, medium, and large sizes' },
        context
      );

      expect(result.success).toBe(true);
      expect(result.data?.componentOptions?.sizes).toContain('sm');
      expect(result.data?.componentOptions?.sizes).toContain('md');
      expect(result.data?.componentOptions?.sizes).toContain('lg');
    });
  });

  describe('Layout Detection', () => {
    it('should detect layout type from description', async () => {
      const result = await agent.execute(
        { description: 'Create a dashboard layout with sidebar and header' },
        context
      );

      expect(result.success).toBe(true);
      expect(result.data?.type).toBe('layout');
      expect(result.data?.layoutOptions?.pattern).toBe('dashboard');
    });

    it('should extract layout sections', async () => {
      const result = await agent.execute(
        { description: 'Dashboard with sidebar, header, and footer' },
        context
      );

      expect(result.success).toBe(true);
      expect(result.data?.layoutOptions?.sections).toContain('sidebar');
      expect(result.data?.layoutOptions?.sections).toContain('header');
      expect(result.data?.layoutOptions?.sections).toContain('footer');
    });
  });

  describe('Framework Detection', () => {
    it('should detect React from description', async () => {
      const result = await agent.execute(
        { description: 'Create a React button component' },
        context
      );

      expect(result.success).toBe(true);
      expect(result.data?.framework).toBe('react');
    });

    it('should detect Vue from description', async () => {
      const result = await agent.execute(
        { description: 'Create a Vue button component' },
        context
      );

      expect(result.success).toBe(true);
      expect(result.data?.framework).toBe('vue');
    });

    it('should default to React if not specified', async () => {
      const result = await agent.execute(
        { description: 'Create a button component' },
        context
      );

      expect(result.success).toBe(true);
      expect(result.data?.framework).toBe('react');
    });
  });

  describe('Requirements Detection', () => {
    it('should detect accessibility requirements', async () => {
      const result = await agent.execute(
        { description: 'Create an accessible button with WCAG AAA compliance' },
        context
      );

      expect(result.success).toBe(true);
      expect(result.data?.requirements?.accessibility).toBe('AAA');
    });

    it('should detect animation requirements', async () => {
      const result = await agent.execute(
        { description: 'Create an animated button component' },
        context
      );

      expect(result.success).toBe(true);
      expect(result.data?.requirements?.animations).toBe(true);
    });

    it('should detect responsive requirements', async () => {
      const result = await agent.execute(
        { description: 'Create a responsive button component' },
        context
      );

      expect(result.success).toBe(true);
      expect(result.data?.requirements?.responsive).toBe(true);
    });
  });

  describe('Error Handling', () => {
    it('should fail with empty description', async () => {
      const result = await agent.execute({ description: '' }, context);

      expect(result.success).toBe(false);
      expect(result.error?.code).toBe('INVALID_INPUT');
    });

    it('should fail with missing description', async () => {
      const result = await agent.execute({} as any, context);

      expect(result.success).toBe(false);
      expect(result.error?.code).toBe('INVALID_INPUT');
    });
  });
});
