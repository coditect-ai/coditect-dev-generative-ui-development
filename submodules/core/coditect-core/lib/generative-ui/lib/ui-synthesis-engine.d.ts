/**
 * UI Synthesis Engine
 * Main orchestration engine for multi-agent UI generation pipeline
 * @module lib/ui-synthesis-engine
 */
import { UISpec, GenerationConfig, GeneratedCode, QualityGateResult } from '../types';
import { UIArchitecture } from '../agents/specialists/ui-architect';
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
 * UI Synthesis Engine
 * Orchestrates multi-agent pipeline for UI generation
 */
export declare class UISynthesisEngine {
    private config;
    private cache;
    private circuitBreakers;
    private intentAnalyzer;
    private uiArchitect;
    private codeGenerator;
    constructor(config?: Partial<SynthesisEngineConfig>);
    /**
     * Execute complete UI generation pipeline
     * @param description - User's natural language description
     * @param generationConfig - Optional generation configuration
     * @returns Pipeline execution result
     */
    generateUI(description: string, generationConfig?: GenerationConfig): Promise<PipelineResult>;
    /**
     * Execute agent with circuit breaker pattern
     */
    private executeWithCircuitBreaker;
    /**
     * Validate quality gates
     */
    private validateQualityGates;
    /**
     * Calculate accessibility score
     */
    private calculateAccessibilityScore;
    /**
     * Check TypeScript strict mode compliance
     */
    private checkStrictTypes;
    /**
     * Estimate performance score based on bundle size
     */
    private estimatePerformanceScore;
    /**
     * Get or create circuit breaker for agent
     */
    private getCircuitBreaker;
    /**
     * Record failure for circuit breaker
     */
    private recordFailure;
    /**
     * Check cache for result
     */
    private checkCache;
    /**
     * Cache result
     */
    private cacheResult;
    /**
     * Generate cache key from description
     */
    private generateCacheKey;
    /**
     * Generate unique execution ID
     */
    private generateExecutionId;
    /**
     * Create error result
     */
    private createErrorResult;
    /**
     * Log message
     */
    private log;
    /**
     * Get cache statistics
     */
    getCacheStats(): {
        size: number;
        entries: Array<{
            key: string;
            hits: number;
            age: number;
        }>;
    };
    /**
     * Clear cache
     */
    clearCache(): void;
    /**
     * Reset circuit breakers
     */
    resetCircuitBreakers(): void;
}
//# sourceMappingURL=ui-synthesis-engine.d.ts.map