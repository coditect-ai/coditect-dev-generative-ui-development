/**
 * Base agent class for CODITECT Generative UI system
 * @module agents/base
 */
import { AgentContext, AgentResult } from '../types';
/**
 * Agent role classification
 */
export declare enum AgentRole {
    ORCHESTRATOR = "orchestrator",
    SPECIALIST = "specialist",
    VALIDATOR = "validator"
}
/**
 * Agent configuration
 */
export interface AgentConfig {
    /** Agent name */
    name: string;
    /** Agent role */
    role: AgentRole;
    /** Agent description */
    description: string;
    /** Agent capabilities */
    capabilities: string[];
    /** Token budget (optional) */
    tokenBudget?: number;
}
/**
 * Base agent class that all specialized agents extend
 */
export declare abstract class BaseAgent<TInput = unknown, TOutput = unknown> {
    protected config: AgentConfig;
    constructor(config: AgentConfig);
    /**
     * Get agent name
     */
    getName(): string;
    /**
     * Get agent role
     */
    getRole(): AgentRole;
    /**
     * Get agent capabilities
     */
    getCapabilities(): string[];
    /**
     * Check if agent can handle a specific capability
     */
    canHandle(capability: string): boolean;
    /**
     * Execute the agent's primary task
     * @param input - Input data for the agent
     * @param context - Execution context
     * @returns Agent result with output data
     */
    abstract execute(input: TInput, context: AgentContext): Promise<AgentResult<TOutput>>;
    /**
     * Validate input before execution
     * @param input - Input to validate
     * @returns True if valid, false otherwise
     */
    protected abstract validateInput(input: TInput): boolean;
    /**
     * Calculate token usage estimate
     * @param input - Input data
     * @returns Estimated token count
     */
    protected estimateTokens(input: TInput): number;
    /**
     * Log agent activity
     */
    protected log(level: 'info' | 'warn' | 'error', message: string, data?: unknown): void;
}
//# sourceMappingURL=base.d.ts.map