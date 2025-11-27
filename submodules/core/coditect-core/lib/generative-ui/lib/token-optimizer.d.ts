/**
 * Token Optimizer
 * Token optimization strategies and cost management for UI generation
 * @module lib/token-optimizer
 */
import { TokenUsage } from '../types';
/**
 * Optimization strategy type
 */
export type OptimizationStrategy = 'component-caching' | 'incremental-generation' | 'template-hybridization' | 'prompt-compression';
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
 * Token Optimizer
 * Manages token optimization strategies and cost tracking
 */
export declare class TokenOptimizer {
    private costParams;
    private usageHistory;
    private componentCache;
    constructor(costParams?: Partial<CostParameters>);
    /**
     * Calculate cost for token usage
     * @param promptTokens - Number of prompt tokens
     * @param completionTokens - Number of completion tokens
     * @returns Cost in USD
     */
    calculateCost(promptTokens: number, completionTokens: number): number;
    /**
     * Record token usage
     * @param usage - Token usage to record
     */
    recordUsage(usage: TokenUsage): void;
    /**
     * Get optimization recommendations
     * @param generationType - Type of generation to optimize
     * @returns Array of recommendations
     */
    getOptimizationRecommendations(generationType: 'component' | 'layout' | 'application'): OptimizationRecommendation[];
    /**
     * Analyze component caching opportunity
     */
    private analyzeComponentCaching;
    /**
     * Analyze incremental generation opportunity
     */
    private analyzeIncrementalGeneration;
    /**
     * Analyze template hybridization opportunity
     */
    private analyzeTemplateHybridization;
    /**
     * Analyze prompt compression opportunity
     */
    private analyzePromptCompression;
    /**
     * Get generation profile for type
     */
    private getGenerationProfile;
    /**
     * Get default profile for generation type
     */
    private getDefaultProfile;
    /**
     * Cache component for reuse
     * @param key - Cache key (component description hash)
     * @param component - Component code
     * @param tokensSaved - Tokens saved by using cache
     */
    cacheComponent(key: string, component: string, tokensSaved: number): void;
    /**
     * Get cached component
     * @param key - Cache key
     * @returns Cached component or null
     */
    getCachedComponent(key: string): string | null;
    /**
     * Get token statistics
     * @returns Comprehensive token usage statistics
     */
    getStatistics(): TokenStatistics;
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
    };
    /**
     * Clear cache
     */
    clearCache(): void;
    /**
     * Clear usage history
     */
    clearHistory(): void;
    /**
     * Estimate cost for generation
     * @param generationType - Type of generation
     * @param customTokens - Custom token estimates (optional)
     * @returns Estimated cost in USD
     */
    estimateCost(generationType: 'component' | 'layout' | 'application', customTokens?: {
        prompt: number;
        completion: number;
    }): number;
    /**
     * Get ROI for optimization strategy
     * @param strategy - Optimization strategy
     * @param monthlyGenerations - Number of generations per month
     * @returns ROI analysis
     */
    getOptimizationROI(strategy: OptimizationStrategy, monthlyGenerations: number): {
        strategy: OptimizationStrategy;
        monthlySavings: number;
        annualSavings: number;
        implementationCost: number;
        breakEvenMonths: number;
        roi: number;
    };
}
//# sourceMappingURL=token-optimizer.d.ts.map