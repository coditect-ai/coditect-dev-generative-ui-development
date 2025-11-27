/**
 * UI Synthesis Engine
 * Main orchestration engine for multi-agent UI generation pipeline
 * @module lib/ui-synthesis-engine
 */

import {
  AgentContext,
  AgentResult,
  UISpec,
  GenerationConfig,
  GeneratedCode,
  QualityGateResult,
} from '../types';
import { IntentAnalyzer } from '../agents/specialists/intent-analyzer';
import { UIArchitect, UIArchitecture } from '../agents/specialists/ui-architect';
import { CodeGenerator, CodeGenerationInput } from '../agents/specialists/code-generator';

/**
 * Pipeline execution result
 */
export interface PipelineResult {
  /** Success status */
  success: boolean;
  /** UI specification */
  spec?: UISpec;
  /** UI architecture */
  architecture?: UIArchitecture;
  /** Generated code files */
  files?: GeneratedCode[];
  /** Quality gate results */
  qualityGates?: QualityGateResult[];
  /** Token usage breakdown */
  tokenUsage: {
    intentAnalysis: number;
    uiArchitecture: number;
    codeGeneration: number;
    total: number;
  };
  /** Execution metadata */
  metadata: {
    executionId: string;
    duration: number;
    startTime: Date;
    endTime: Date;
  };
  /** Error information if failed */
  error?: {
    message: string;
    code: string;
    stage: 'intent' | 'architecture' | 'generation' | 'validation';
    details?: unknown;
  };
}

/**
 * Circuit breaker state
 */
interface CircuitBreakerState {
  failures: number;
  lastFailureTime?: Date;
  isOpen: boolean;
}

/**
 * Cache entry
 */
interface CacheEntry {
  key: string;
  result: PipelineResult;
  timestamp: Date;
  hits: number;
}

/**
 * UI Synthesis Engine configuration
 */
export interface SynthesisEngineConfig {
  /** Maximum token budget for entire pipeline */
  maxTokenBudget: number;
  /** Enable result caching */
  enableCaching: boolean;
  /** Cache TTL in milliseconds */
  cacheTTL: number;
  /** Circuit breaker config */
  circuitBreaker: {
    failureThreshold: number;
    resetTimeout: number;
  };
  /** Quality gate thresholds */
  qualityGates: {
    accessibility: number;
    performance: number;
    strictTypes: boolean;
  };
}

/**
 * Default engine configuration
 */
const DEFAULT_CONFIG: SynthesisEngineConfig = {
  maxTokenBudget: 20000,
  enableCaching: true,
  cacheTTL: 3600000, // 1 hour
  circuitBreaker: {
    failureThreshold: 5,
    resetTimeout: 60000, // 1 minute
  },
  qualityGates: {
    accessibility: 90,
    performance: 90,
    strictTypes: true,
  },
};

/**
 * UI Synthesis Engine
 * Orchestrates multi-agent pipeline for UI generation
 */
export class UISynthesisEngine {
  private config: SynthesisEngineConfig;
  private cache: Map<string, CacheEntry>;
  private circuitBreakers: Map<string, CircuitBreakerState>;

  // Agent instances
  private intentAnalyzer: IntentAnalyzer;
  private uiArchitect: UIArchitect;
  private codeGenerator: CodeGenerator;

  constructor(config: Partial<SynthesisEngineConfig> = {}) {
    this.config = { ...DEFAULT_CONFIG, ...config };
    this.cache = new Map();
    this.circuitBreakers = new Map();

    // Initialize agents
    this.intentAnalyzer = new IntentAnalyzer();
    this.uiArchitect = new UIArchitect();
    this.codeGenerator = new CodeGenerator();
  }

  /**
   * Execute complete UI generation pipeline
   * @param description - User's natural language description
   * @param generationConfig - Optional generation configuration
   * @returns Pipeline execution result
   */
  async generateUI(
    description: string,
    generationConfig?: GenerationConfig
  ): Promise<PipelineResult> {
    const executionId = this.generateExecutionId();
    const startTime = new Date();

    this.log('info', 'Starting UI generation pipeline', {
      executionId,
      description,
    });

    // Check cache if enabled
    if (this.config.enableCaching) {
      const cached = this.checkCache(description);
      if (cached) {
        this.log('info', 'Cache hit - returning cached result', { executionId });
        return cached;
      }
    }

    // Create execution context
    const context: AgentContext = {
      executionId,
      spec: {} as UISpec,
      config: generationConfig || {},
      tokens: { prompt: 0, completion: 0, total: 0 },
      metadata: { startTime },
    };

    try {
      // Phase 1: Intent Analysis
      const intentResult = await this.executeWithCircuitBreaker(
        'intent-analysis',
        async () => this.intentAnalyzer.execute({ description }, context)
      );

      if (!intentResult.success || !intentResult.data) {
        return this.createErrorResult(
          executionId,
          startTime,
          'Intent analysis failed',
          'INTENT_ANALYSIS_FAILED',
          'intent',
          intentResult.error
        );
      }

      context.spec = intentResult.data;
      const intentTokens = intentResult.tokens.prompt + intentResult.tokens.completion;

      this.log('info', 'Intent analysis complete', {
        executionId,
        tokens: intentTokens,
      });

      // Phase 2: UI Architecture
      const architectResult = await this.executeWithCircuitBreaker(
        'ui-architecture',
        async () => this.uiArchitect.execute(intentResult.data!, context)
      );

      if (!architectResult.success || !architectResult.data) {
        return this.createErrorResult(
          executionId,
          startTime,
          'UI architecture design failed',
          'ARCHITECTURE_FAILED',
          'architecture',
          architectResult.error
        );
      }

      const architectTokens =
        architectResult.tokens.prompt + architectResult.tokens.completion;

      this.log('info', 'UI architecture design complete', {
        executionId,
        tokens: architectTokens,
      });

      // Check token budget
      const totalTokens = intentTokens + architectTokens;
      if (totalTokens > this.config.maxTokenBudget * 0.7) {
        this.log('warn', 'Token budget approaching limit', {
          executionId,
          used: totalTokens,
          budget: this.config.maxTokenBudget,
        });
      }

      // Phase 3: Code Generation
      const codeInput: CodeGenerationInput = {
        architecture: architectResult.data,
        framework: intentResult.data.framework,
        styling: intentResult.data.styling,
        strictTypes: this.config.qualityGates.strictTypes,
      };

      const codeResult = await this.executeWithCircuitBreaker(
        'code-generation',
        async () => this.codeGenerator.execute(codeInput, context)
      );

      if (!codeResult.success || !codeResult.data) {
        return this.createErrorResult(
          executionId,
          startTime,
          'Code generation failed',
          'CODE_GENERATION_FAILED',
          'generation',
          codeResult.error
        );
      }

      const codeTokens = codeResult.tokens.prompt + codeResult.tokens.completion;

      this.log('info', 'Code generation complete', {
        executionId,
        tokens: codeTokens,
        fileCount: codeResult.data.length,
      });

      // Phase 4: Quality Gate Validation
      const qualityGates = await this.validateQualityGates(
        codeResult.data,
        intentResult.data
      );

      const failedGates = qualityGates.filter((gate) => !gate.passed);
      if (failedGates.length > 0) {
        this.log('warn', 'Quality gate failures detected', {
          executionId,
          failures: failedGates.map((g) => g.name),
        });
      }

      // Calculate final metrics
      const endTime = new Date();
      const totalTokenUsage = intentTokens + architectTokens + codeTokens;

      const result: PipelineResult = {
        success: true,
        spec: intentResult.data,
        architecture: architectResult.data,
        files: codeResult.data,
        qualityGates,
        tokenUsage: {
          intentAnalysis: intentTokens,
          uiArchitecture: architectTokens,
          codeGeneration: codeTokens,
          total: totalTokenUsage,
        },
        metadata: {
          executionId,
          duration: endTime.getTime() - startTime.getTime(),
          startTime,
          endTime,
        },
      };

      // Cache result if enabled
      if (this.config.enableCaching) {
        this.cacheResult(description, result);
      }

      this.log('info', 'UI generation pipeline complete', {
        executionId,
        duration: result.metadata.duration,
        tokens: totalTokenUsage,
      });

      return result;
    } catch (error) {
      return this.createErrorResult(
        executionId,
        startTime,
        error instanceof Error ? error.message : 'Unknown error',
        'PIPELINE_FAILED',
        'generation',
        error
      );
    }
  }

  /**
   * Execute agent with circuit breaker pattern
   */
  private async executeWithCircuitBreaker<T>(
    agentName: string,
    execution: () => Promise<AgentResult<T>>
  ): Promise<AgentResult<T>> {
    const breaker = this.getCircuitBreaker(agentName);

    // Check if circuit is open
    if (breaker.isOpen) {
      const timeSinceFailure = breaker.lastFailureTime
        ? Date.now() - breaker.lastFailureTime.getTime()
        : Infinity;

      if (timeSinceFailure < this.config.circuitBreaker.resetTimeout) {
        throw new Error(`Circuit breaker open for ${agentName}`);
      }

      // Reset circuit breaker
      breaker.isOpen = false;
      breaker.failures = 0;
    }

    try {
      const result = await execution();

      if (!result.success) {
        this.recordFailure(agentName);
      } else {
        // Reset on success
        breaker.failures = 0;
      }

      return result;
    } catch (error) {
      this.recordFailure(agentName);
      throw error;
    }
  }

  /**
   * Validate quality gates
   */
  private async validateQualityGates(
    files: GeneratedCode[],
    spec: UISpec
  ): Promise<QualityGateResult[]> {
    const results: QualityGateResult[] = [];

    // Accessibility gate
    const accessibilityScore = this.calculateAccessibilityScore(files);
    results.push({
      name: 'Accessibility',
      passed: accessibilityScore >= this.config.qualityGates.accessibility,
      score: accessibilityScore,
      threshold: this.config.qualityGates.accessibility,
      details: `WCAG ${spec.requirements?.accessibility || 'AA'} compliance`,
      recommendations:
        accessibilityScore < this.config.qualityGates.accessibility
          ? ['Add ARIA labels', 'Ensure keyboard navigation', 'Check color contrast']
          : undefined,
    });

    // TypeScript strict mode gate
    const strictTypesScore = this.checkStrictTypes(files);
    results.push({
      name: 'TypeScript Strict Mode',
      passed: strictTypesScore === 100,
      score: strictTypesScore,
      threshold: 100,
      details: 'No any types, fully typed',
      recommendations:
        strictTypesScore < 100 ? ['Remove any types', 'Add explicit types'] : undefined,
    });

    // Performance gate (bundle size estimate)
    const performanceScore = this.estimatePerformanceScore(files);
    results.push({
      name: 'Performance',
      passed: performanceScore >= this.config.qualityGates.performance,
      score: performanceScore,
      threshold: this.config.qualityGates.performance,
      details: 'Estimated bundle size and runtime performance',
      recommendations:
        performanceScore < this.config.qualityGates.performance
          ? ['Reduce bundle size', 'Optimize re-renders', 'Add code splitting']
          : undefined,
    });

    return results;
  }

  /**
   * Calculate accessibility score
   */
  private calculateAccessibilityScore(files: GeneratedCode[]): number {
    let score = 100;

    for (const file of files) {
      const content = file.content.toLowerCase();

      // Check for semantic HTML
      if (!content.includes('<button') && !content.includes('role=')) {
        score -= 20;
      }

      // Check for ARIA attributes
      if (!content.includes('aria-')) {
        score -= 15;
      }

      // Check for keyboard navigation
      if (!content.includes('onkeydown') && !content.includes('onkeypress')) {
        score -= 15;
      }
    }

    return Math.max(0, score);
  }

  /**
   * Check TypeScript strict mode compliance
   */
  private checkStrictTypes(files: GeneratedCode[]): number {
    let score = 100;

    for (const file of files) {
      const content = file.content;

      // Check for any types
      const anyCount = (content.match(/:\s*any/g) || []).length;
      score -= anyCount * 10;
    }

    return Math.max(0, score);
  }

  /**
   * Estimate performance score based on bundle size
   */
  private estimatePerformanceScore(files: GeneratedCode[]): number {
    const totalSize = files.reduce((sum, file) => sum + file.content.length, 0);
    const maxSize = 50000; // 50KB threshold

    if (totalSize <= maxSize) {
      return 100;
    }

    const ratio = maxSize / totalSize;
    return Math.max(0, Math.round(ratio * 100));
  }

  /**
   * Get or create circuit breaker for agent
   */
  private getCircuitBreaker(agentName: string): CircuitBreakerState {
    if (!this.circuitBreakers.has(agentName)) {
      this.circuitBreakers.set(agentName, {
        failures: 0,
        isOpen: false,
      });
    }
    return this.circuitBreakers.get(agentName)!;
  }

  /**
   * Record failure for circuit breaker
   */
  private recordFailure(agentName: string): void {
    const breaker = this.getCircuitBreaker(agentName);
    breaker.failures++;
    breaker.lastFailureTime = new Date();

    if (breaker.failures >= this.config.circuitBreaker.failureThreshold) {
      breaker.isOpen = true;
      this.log('error', `Circuit breaker opened for ${agentName}`, {
        failures: breaker.failures,
      });
    }
  }

  /**
   * Check cache for result
   */
  private checkCache(description: string): PipelineResult | null {
    const key = this.generateCacheKey(description);
    const entry = this.cache.get(key);

    if (!entry) {
      return null;
    }

    const age = Date.now() - entry.timestamp.getTime();
    if (age > this.config.cacheTTL) {
      this.cache.delete(key);
      return null;
    }

    entry.hits++;
    return entry.result;
  }

  /**
   * Cache result
   */
  private cacheResult(description: string, result: PipelineResult): void {
    const key = this.generateCacheKey(description);
    this.cache.set(key, {
      key,
      result,
      timestamp: new Date(),
      hits: 0,
    });
  }

  /**
   * Generate cache key from description
   */
  private generateCacheKey(description: string): string {
    // Simple hash function for cache key
    let hash = 0;
    for (let i = 0; i < description.length; i++) {
      const char = description.charCodeAt(i);
      hash = (hash << 5) - hash + char;
      hash = hash & hash; // Convert to 32-bit integer
    }
    return `cache_${hash.toString(16)}`;
  }

  /**
   * Generate unique execution ID
   */
  private generateExecutionId(): string {
    return `exec_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`;
  }

  /**
   * Create error result
   */
  private createErrorResult(
    executionId: string,
    startTime: Date,
    message: string,
    code: string,
    stage: 'intent' | 'architecture' | 'generation' | 'validation',
    details?: unknown
  ): PipelineResult {
    const endTime = new Date();

    return {
      success: false,
      tokenUsage: {
        intentAnalysis: 0,
        uiArchitecture: 0,
        codeGeneration: 0,
        total: 0,
      },
      metadata: {
        executionId,
        duration: endTime.getTime() - startTime.getTime(),
        startTime,
        endTime,
      },
      error: {
        message,
        code,
        stage,
        details,
      },
    };
  }

  /**
   * Log message
   */
  private log(level: 'info' | 'warn' | 'error', message: string, data?: unknown): void {
    const logEntry = {
      timestamp: new Date().toISOString(),
      component: 'UISynthesisEngine',
      level,
      message,
      data,
    };

    if (level === 'error') {
      console.error(JSON.stringify(logEntry));
    } else if (level === 'warn') {
      console.warn(JSON.stringify(logEntry));
    } else {
      console.log(JSON.stringify(logEntry));
    }
  }

  /**
   * Get cache statistics
   */
  getCacheStats(): {
    size: number;
    entries: Array<{ key: string; hits: number; age: number }>;
  } {
    const now = Date.now();
    const entries = Array.from(this.cache.values()).map((entry) => ({
      key: entry.key,
      hits: entry.hits,
      age: now - entry.timestamp.getTime(),
    }));

    return {
      size: this.cache.size,
      entries,
    };
  }

  /**
   * Clear cache
   */
  clearCache(): void {
    this.cache.clear();
    this.log('info', 'Cache cleared');
  }

  /**
   * Reset circuit breakers
   */
  resetCircuitBreakers(): void {
    this.circuitBreakers.clear();
    this.log('info', 'Circuit breakers reset');
  }
}
