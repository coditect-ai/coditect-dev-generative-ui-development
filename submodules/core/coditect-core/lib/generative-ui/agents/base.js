"use strict";
/**
 * Base agent class for CODITECT Generative UI system
 * @module agents/base
 */
Object.defineProperty(exports, "__esModule", { value: true });
exports.BaseAgent = exports.AgentRole = void 0;
/**
 * Agent role classification
 */
var AgentRole;
(function (AgentRole) {
    AgentRole["ORCHESTRATOR"] = "orchestrator";
    AgentRole["SPECIALIST"] = "specialist";
    AgentRole["VALIDATOR"] = "validator";
})(AgentRole || (exports.AgentRole = AgentRole = {}));
/**
 * Base agent class that all specialized agents extend
 */
class BaseAgent {
    config;
    constructor(config) {
        this.config = config;
    }
    /**
     * Get agent name
     */
    getName() {
        return this.config.name;
    }
    /**
     * Get agent role
     */
    getRole() {
        return this.config.role;
    }
    /**
     * Get agent capabilities
     */
    getCapabilities() {
        return this.config.capabilities;
    }
    /**
     * Check if agent can handle a specific capability
     */
    canHandle(capability) {
        return this.config.capabilities.includes(capability);
    }
    /**
     * Calculate token usage estimate
     * @param input - Input data
     * @returns Estimated token count
     */
    estimateTokens(input) {
        // Default implementation - override in subclasses
        const inputStr = JSON.stringify(input);
        return Math.ceil(inputStr.length / 4); // Rough approximation: 1 token ≈ 4 chars
    }
    /**
     * Log agent activity
     */
    log(level, message, data) {
        const logEntry = {
            timestamp: new Date().toISOString(),
            agent: this.config.name,
            level,
            message,
            data,
        };
        if (level === 'error') {
            console.error(JSON.stringify(logEntry));
        }
        else if (level === 'warn') {
            console.warn(JSON.stringify(logEntry));
        }
        else {
            console.log(JSON.stringify(logEntry));
        }
    }
}
exports.BaseAgent = BaseAgent;
//# sourceMappingURL=base.js.map