/**
 * Token Optimizer
 * Token optimization strategies and cost management for UI generation
 * @module lib/token-optimizer
 */

import { TokenUsage } from '../types';

/**
 * Optimization strategy type
 */
export type OptimizationStrategy =
  | 'component-caching'
  | 'incremental-generation'
  | 'template-hybridization'
  | 'prompt-compression';

/**
 * Optimization recommendation
 */
export interface OptimizationRecommendation {
  /** Strategy name */
  strategy: OptimizationStrategy;
  /** Estimated token savings */
  estimatedSavings: number;
  /** Estimated cost savings in USD */
  estimatedCostSavings: number;
  /** Confidence level (0-1) */
  confidence: number;
  /** Recommendation description */
  description: string;
  /** Implementation effort */
  effort: 'low' | 'medium' | 'high';
}

/**
 * Cost estimation parameters
 */
export interface CostParameters {
  /** Cost per 1M input tokens in USD */
  inputTokenCost: number;
  /** Cost per 1M output tokens in USD */
  outputTokenCost: number;
  /** Model name */
  model: string;
}

/**
 * Generation type cost profile
 */
export interface GenerationCostProfile {
  /** Generation type */
  type: 'component' | 'layout' | 'application';
  /** Average prompt tokens */
  avgPromptTokens: number;
  /** Average completion tokens */
  avgCompletionTokens: number;
  /** Average total tokens */
  avgTotalTokens: number;
  /** Average cost in USD */
  avgCost: number;
  /** Sample count */
  sampleCount: number;
}

/**
 * Token usage statistics
 */
export interface TokenStatistics {
  /** Total tokens used */
  totalTokens: number;
  /** Total cost in USD */
  totalCost: number;
  /** Average tokens per generation */
  avgTokensPerGeneration: number;
  /** Cost breakdown by generation type */
  byGenerationType: Record<string, GenerationCostProfile>;
  /** Token usage over time */
  timeline: Array<{
    timestamp: Date;
    tokens: number;
    cost: number;
  }>;
}

/**
 * Default cost parameters (Claude Sonnet 4.5)
 */
const DEFAULT_COST_PARAMS: CostParameters = {
  inputTokenCost: 3.0, // $3 per 1M tokens
  outputTokenCost: 15.0, // $15 per 1M tokens
  model: 'claude-sonnet-4.5',
};

/**
 * Token Optimizer
 * Manages token optimization strategies and cost tracking
 */
export class TokenOptimizer {
  private costParams: CostParameters;
  private usageHistory: TokenUsage[];
  private componentCache: Map<string, CachedComponent>;

  constructor(costParams: Partial<CostParameters> = {}) {
    this.costParams = { ...DEFAULT_COST_PARAMS, ...costParams };
    this.usageHistory = [];
    this.componentCache = new Map();
  }

  /**
   * Calculate cost for token usage
   * @param promptTokens - Number of prompt tokens
   * @param completionTokens - Number of completion tokens
   * @returns Cost in USD
   */
  calculateCost(promptTokens: number, completionTokens: number): number {
    const inputCost = (promptTokens / 1_000_000) * this.costParams.inputTokenCost;
    const outputCost = (completionTokens / 1_000_000) * this.costParams.outputTokenCost;
    return inputCost + outputCost;
  }

  /**
   * Record token usage
   * @param usage - Token usage to record
   */
  recordUsage(usage: TokenUsage): void {
    this.usageHistory.push(usage);
  }

  /**
   * Get optimization recommendations
   * @param generationType - Type of generation to optimize
   * @returns Array of recommendations
   */
  getOptimizationRecommendations(
    generationType: 'component' | 'layout' | 'application'
  ): OptimizationRecommendation[] {
    const recommendations: OptimizationRecommendation[] = [];

    // Component caching recommendation
    const cachingRecommendation = this.analyzeComponentCaching(generationType);
    if (cachingRecommendation) {
      recommendations.push(cachingRecommendation);
    }

    // Incremental generation recommendation
    const incrementalRecommendation = this.analyzeIncrementalGeneration(generationType);
    if (incrementalRecommendation) {
      recommendations.push(incrementalRecommendation);
    }

    // Template hybridization recommendation
    const hybridRecommendation = this.analyzeTemplateHybridization(generationType);
    if (hybridRecommendation) {
      recommendations.push(hybridRecommendation);
    }

    // Prompt compression recommendation
    const compressionRecommendation = this.analyzePromptCompression(generationType);
    if (compressionRecommendation) {
      recommendations.push(compressionRecommendation);
    }

    // Sort by estimated savings (highest first)
    return recommendations.sort((a, b) => b.estimatedSavings - a.estimatedSavings);
  }

  /**
   * Analyze component caching opportunity
   */
  private analyzeComponentCaching(
    generationType: 'component' | 'layout' | 'application'
  ): OptimizationRecommendation | null {
    const profile = this.getGenerationProfile(generationType);
    if (!profile) return null;

    // Caching is most effective for components
    const savingsMultiplier = generationType === 'component' ? 0.5 : 0.4;
    const estimatedSavings = Math.round(profile.avgTotalTokens * savingsMultiplier);
    const estimatedCostSavings = this.calculateCost(
      Math.round(profile.avgPromptTokens * savingsMultiplier),
      Math.round(profile.avgCompletionTokens * savingsMultiplier)
    );

    return {
      strategy: 'component-caching',
      estimatedSavings,
      estimatedCostSavings,
      confidence: 0.85,
      description:
        'Cache successfully generated components and reuse them for similar requests. ' +
        'Reduces token usage by 40-60% for repeated component patterns.',
      effort: 'low',
    };
  }

  /**
   * Analyze incremental generation opportunity
   */
  private analyzeIncrementalGeneration(
    generationType: 'component' | 'layout' | 'application'
  ): OptimizationRecommendation | null {
    const profile = this.getGenerationProfile(generationType);
    if (!profile) return null;

    // Incremental generation is most effective for large generations
    if (generationType === 'component') return null;

    const savingsMultiplier = generationType === 'application' ? 0.4 : 0.35;
    const estimatedSavings = Math.round(profile.avgTotalTokens * savingsMultiplier);
    const estimatedCostSavings = this.calculateCost(
      Math.round(profile.avgPromptTokens * savingsMultiplier),
      Math.round(profile.avgCompletionTokens * savingsMultiplier)
    );

    return {
      strategy: 'incremental-generation',
      estimatedSavings,
      estimatedCostSavings,
      confidence: 0.75,
      description:
        'Generate UI iteratively by building components one at a time rather than all at once. ' +
        'Reduces token usage by 30-50% for complex layouts and applications.',
      effort: 'medium',
    };
  }

  /**
   * Analyze template hybridization opportunity
   */
  private analyzeTemplateHybridization(
    generationType: 'component' | 'layout' | 'application'
  ): OptimizationRecommendation | null {
    const profile = this.getGenerationProfile(generationType);
    if (!profile) return null;

    const savingsMultiplier = 0.3;
    const estimatedSavings = Math.round(profile.avgTotalTokens * savingsMultiplier);
    const estimatedCostSavings = this.calculateCost(
      Math.round(profile.avgPromptTokens * savingsMultiplier),
      Math.round(profile.avgCompletionTokens * savingsMultiplier)
    );

    return {
      strategy: 'template-hybridization',
      estimatedSavings,
      estimatedCostSavings,
      confidence: 0.7,
      description:
        'Combine static templates with AI-generated customizations. Use templates for ' +
        'boilerplate code and generate only unique variations. Reduces token usage by 20-40%.',
      effort: 'medium',
    };
  }

  /**
   * Analyze prompt compression opportunity
   */
  private analyzePromptCompression(
    generationType: 'component' | 'layout' | 'application'
  ): OptimizationRecommendation | null {
    const profile = this.getGenerationProfile(generationType);
    if (!profile) return null;

    // Focus on reducing prompt tokens
    const savingsMultiplier = 0.25;
    const estimatedSavings = Math.round(profile.avgPromptTokens * savingsMultiplier);
    const estimatedCostSavings = this.calculateCost(
      Math.round(profile.avgPromptTokens * savingsMultiplier),
      0
    );

    return {
      strategy: 'prompt-compression',
      estimatedSavings,
      estimatedCostSavings,
      confidence: 0.8,
      description:
        'Optimize prompts by removing redundant context and using concise instructions. ' +
        'Reduces prompt token usage by 20-30% without sacrificing quality.',
      effort: 'low',
    };
  }

  /**
   * Get generation profile for type
   */
  private getGenerationProfile(
    generationType: 'component' | 'layout' | 'application'
  ): GenerationCostProfile | null {
    const typeUsage = this.usageHistory.filter((u) => u.generationType === generationType);

    if (typeUsage.length === 0) {
      // Return default profiles if no data
      return this.getDefaultProfile(generationType);
    }

    const avgPromptTokens =
      typeUsage.reduce((sum, u) => sum + u.promptTokens, 0) / typeUsage.length;
    const avgCompletionTokens =
      typeUsage.reduce((sum, u) => sum + u.completionTokens, 0) / typeUsage.length;
    const avgTotalTokens =
      typeUsage.reduce((sum, u) => sum + u.totalTokens, 0) / typeUsage.length;
    const avgCost = typeUsage.reduce((sum, u) => sum + u.estimatedCost, 0) / typeUsage.length;

    return {
      type: generationType,
      avgPromptTokens,
      avgCompletionTokens,
      avgTotalTokens,
      avgCost,
      sampleCount: typeUsage.length,
    };
  }

  /**
   * Get default profile for generation type
   */
  private getDefaultProfile(
    generationType: 'component' | 'layout' | 'application'
  ): GenerationCostProfile {
    const profiles: Record<'component' | 'layout' | 'application', GenerationCostProfile> = {
      component: {
        type: 'component',
        avgPromptTokens: 200,
        avgCompletionTokens: 800,
        avgTotalTokens: 1000,
        avgCost: 0.001,
        sampleCount: 0,
      },
      layout: {
        type: 'layout',
        avgPromptTokens: 500,
        avgCompletionTokens: 3000,
        avgTotalTokens: 3500,
        avgCost: 0.004,
        sampleCount: 0,
      },
      application: {
        type: 'application',
        avgPromptTokens: 1500,
        avgCompletionTokens: 15000,
        avgTotalTokens: 16500,
        avgCost: 0.02,
        sampleCount: 0,
      },
    };

    return profiles[generationType];
  }

  /**
   * Cache component for reuse
   * @param key - Cache key (component description hash)
   * @param component - Component code
   * @param tokensSaved - Tokens saved by using cache
   */
  cacheComponent(key: string, component: string, tokensSaved: number): void {
    this.componentCache.set(key, {
      key,
      component,
      timestamp: new Date(),
      hits: 0,
      tokensSaved,
    });
  }

  /**
   * Get cached component
   * @param key - Cache key
   * @returns Cached component or null
   */
  getCachedComponent(key: string): string | null {
    const cached = this.componentCache.get(key);
    if (!cached) return null;

    cached.hits++;
    return cached.component;
  }

  /**
   * Get token statistics
   * @returns Comprehensive token usage statistics
   */
  getStatistics(): TokenStatistics {
    const totalTokens = this.usageHistory.reduce((sum, u) => sum + u.totalTokens, 0);
    const totalCost = this.usageHistory.reduce((sum, u) => sum + u.estimatedCost, 0);
    const avgTokensPerGeneration =
      this.usageHistory.length > 0 ? totalTokens / this.usageHistory.length : 0;

    // Group by generation type
    const byGenerationType: Record<string, GenerationCostProfile> = {};
    for (const type of ['component', 'layout', 'application'] as const) {
      const profile = this.getGenerationProfile(type);
      if (profile) {
        byGenerationType[type] = profile;
      }
    }

    // Create timeline
    const timeline = this.usageHistory.map((u) => ({
      timestamp: u.timestamp,
      tokens: u.totalTokens,
      cost: u.estimatedCost,
    }));

    return {
      totalTokens,
      totalCost,
      avgTokensPerGeneration,
      byGenerationType,
      timeline,
    };
  }

  /**
   * Get cache statistics
   */
  getCacheStatistics(): {
    size: number;
    totalHits: number;
    totalTokensSaved: number;
    entries: Array<{
      key: string;
      hits: number;
      tokensSaved: number;
      age: number;
    }>;
  } {
    const now = Date.now();
    let totalHits = 0;
    let totalTokensSaved = 0;

    const entries = Array.from(this.componentCache.values()).map((entry) => {
      totalHits += entry.hits;
      totalTokensSaved += entry.tokensSaved * entry.hits;

      return {
        key: entry.key,
        hits: entry.hits,
        tokensSaved: entry.tokensSaved,
        age: now - entry.timestamp.getTime(),
      };
    });

    return {
      size: this.componentCache.size,
      totalHits,
      totalTokensSaved,
      entries,
    };
  }

  /**
   * Clear cache
   */
  clearCache(): void {
    this.componentCache.clear();
  }

  /**
   * Clear usage history
   */
  clearHistory(): void {
    this.usageHistory = [];
  }

  /**
   * Estimate cost for generation
   * @param generationType - Type of generation
   * @param customTokens - Custom token estimates (optional)
   * @returns Estimated cost in USD
   */
  estimateCost(
    generationType: 'component' | 'layout' | 'application',
    customTokens?: { prompt: number; completion: number }
  ): number {
    if (customTokens) {
      return this.calculateCost(customTokens.prompt, customTokens.completion);
    }

    const profile = this.getGenerationProfile(generationType);
    if (!profile) return 0;

    return this.calculateCost(
      Math.round(profile.avgPromptTokens),
      Math.round(profile.avgCompletionTokens)
    );
  }

  /**
   * Get ROI for optimization strategy
   * @param strategy - Optimization strategy
   * @param monthlyGenerations - Number of generations per month
   * @returns ROI analysis
   */
  getOptimizationROI(
    strategy: OptimizationStrategy,
    monthlyGenerations: number
  ): {
    strategy: OptimizationStrategy;
    monthlySavings: number;
    annualSavings: number;
    implementationCost: number;
    breakEvenMonths: number;
    roi: number;
  } {
    const recommendations = this.getOptimizationRecommendations('component');
    const recommendation = recommendations.find((r) => r.strategy === strategy);

    if (!recommendation) {
      return {
        strategy,
        monthlySavings: 0,
        annualSavings: 0,
        implementationCost: 0,
        breakEvenMonths: 0,
        roi: 0,
      };
    }

    const monthlySavings = recommendation.estimatedCostSavings * monthlyGenerations;
    const annualSavings = monthlySavings * 12;

    // Estimate implementation cost based on effort
    const implementationCosts = {
      low: 1000, // ~5 hours at $200/hr
      medium: 4000, // ~20 hours at $200/hr
      high: 10000, // ~50 hours at $200/hr
    };
    const implementationCost = implementationCosts[recommendation.effort];

    const breakEvenMonths = implementationCost / monthlySavings;
    const roi = ((annualSavings - implementationCost) / implementationCost) * 100;

    return {
      strategy,
      monthlySavings,
      annualSavings,
      implementationCost,
      breakEvenMonths,
      roi,
    };
  }
}

/**
 * Cached component entry
 */
interface CachedComponent {
  key: string;
  component: string;
  timestamp: Date;
  hits: number;
  tokensSaved: number;
}
