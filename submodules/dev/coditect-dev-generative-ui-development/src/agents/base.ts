/**
 * Base agent class for CODITECT Generative UI system
 * @module agents/base
 */

import { AgentContext, AgentResult } from '../types';

/**
 * Agent role classification
 */
export enum AgentRole {
  ORCHESTRATOR = 'orchestrator',
  SPECIALIST = 'specialist',
  VALIDATOR = 'validator',
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
export abstract class BaseAgent<TInput = unknown, TOutput = unknown> {
  protected config: AgentConfig;

  constructor(config: AgentConfig) {
    this.config = config;
  }

  /**
   * Get agent name
   */
  getName(): string {
    return this.config.name;
  }

  /**
   * Get agent role
   */
  getRole(): AgentRole {
    return this.config.role;
  }

  /**
   * Get agent capabilities
   */
  getCapabilities(): string[] {
    return this.config.capabilities;
  }

  /**
   * Check if agent can handle a specific capability
   */
  canHandle(capability: string): boolean {
    return this.config.capabilities.includes(capability);
  }

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
  protected estimateTokens(input: TInput): number {
    // Default implementation - override in subclasses
    const inputStr = JSON.stringify(input);
    return Math.ceil(inputStr.length / 4); // Rough approximation: 1 token ≈ 4 chars
  }

  /**
   * Log agent activity
   */
  protected log(level: 'info' | 'warn' | 'error', message: string, data?: unknown): void {
    const logEntry = {
      timestamp: new Date().toISOString(),
      agent: this.config.name,
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
}
