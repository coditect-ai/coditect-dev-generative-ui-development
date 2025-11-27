/**
 * Core type definitions for CODITECT Generative UI system
 * @module types
 */

/**
 * UI specification from user intent
 */
export interface UISpec {
  /** Type of UI to generate */
  type: 'component' | 'layout' | 'application';
  /** User's description or requirements */
  description: string;
  /** Target framework */
  framework: 'react' | 'vue' | 'svelte';
  /** Styling approach */
  styling: 'tailwind' | 'css-modules' | 'styled-components';
  /** Additional requirements */
  requirements?: {
    /** Accessibility level (AA or AAA) */
    accessibility?: 'AA' | 'AAA';
    /** Animation requirements */
    animations?: boolean;
    /** Responsive breakpoints */
    responsive?: boolean;
    /** TypeScript strict mode */
    strictTypes?: boolean;
  };
  /** Component-specific options */
  componentOptions?: {
    /** Component variants */
    variants?: string[];
    /** Component sizes */
    sizes?: string[];
    /** State management */
    stateful?: boolean;
  };
  /** Layout-specific options */
  layoutOptions?: {
    /** Layout pattern */
    pattern?: 'dashboard' | 'wizard' | 'landing' | 'settings';
    /** Layout sections */
    sections?: string[];
  };
}

/**
 * Generation configuration
 */
export interface GenerationConfig {
  /** Token budget for generation */
  tokenBudget?: number;
  /** Quality gates to enforce */
  qualityGates?: {
    /** Minimum accessibility score (0-100) */
    accessibility?: number;
    /** Minimum performance score (0-100) */
    performance?: number;
    /** Require TypeScript strict mode */
    strictTypes?: boolean;
    /** Maximum bundle size in KB */
    maxBundleSize?: number;
  };
  /** Enable caching */
  enableCaching?: boolean;
  /** Validation mode */
  validationMode?: 'strict' | 'standard' | 'lenient';
}

/**
 * Agent execution context
 */
export interface AgentContext {
  /** Unique execution ID */
  executionId: string;
  /** UI specification */
  spec: UISpec;
  /** Generation configuration */
  config: GenerationConfig;
  /** Token usage tracking */
  tokens: {
    prompt: number;
    completion: number;
    total: number;
  };
  /** Execution metadata */
  metadata: {
    startTime: Date;
    endTime?: Date;
    duration?: number;
  };
}

/**
 * Agent result
 */
export interface AgentResult<T = unknown> {
  /** Success status */
  success: boolean;
  /** Result data */
  data?: T;
  /** Error information */
  error?: {
    message: string;
    code: string;
    details?: unknown;
  };
  /** Token usage */
  tokens: {
    prompt: number;
    completion: number;
  };
  /** Validation results */
  validation?: ValidationResult[];
}

/**
 * Validation result
 */
export interface ValidationResult {
  /** Validation rule name */
  rule: string;
  /** Pass/fail status */
  passed: boolean;
  /** Validation message */
  message: string;
  /** Severity level */
  severity: 'error' | 'warning' | 'info';
  /** Additional details */
  details?: unknown;
}

/**
 * Generated code output
 */
export interface GeneratedCode {
  /** File path */
  filePath: string;
  /** Generated code content */
  content: string;
  /** Language */
  language: 'typescript' | 'javascript' | 'tsx' | 'jsx';
  /** Imports required */
  imports?: string[];
  /** Test file content */
  testContent?: string;
}

/**
 * Component metadata
 */
export interface ComponentMetadata {
  /** Component name */
  name: string;
  /** Component description */
  description: string;
  /** Props interface */
  props: Record<string, PropMetadata>;
  /** Variants */
  variants?: string[];
  /** Examples */
  examples?: ComponentExample[];
}

/**
 * Prop metadata
 */
export interface PropMetadata {
  /** Prop type */
  type: string;
  /** Required flag */
  required: boolean;
  /** Default value */
  defaultValue?: unknown;
  /** Description */
  description?: string;
}

/**
 * Component example
 */
export interface ComponentExample {
  /** Example title */
  title: string;
  /** Example code */
  code: string;
  /** Description */
  description?: string;
}

/**
 * Token usage statistics
 */
export interface TokenUsage {
  /** Prompt tokens */
  promptTokens: number;
  /** Completion tokens */
  completionTokens: number;
  /** Total tokens */
  totalTokens: number;
  /** Estimated cost in USD */
  estimatedCost: number;
  /** Generation type */
  generationType: 'component' | 'layout' | 'application';
  /** Timestamp */
  timestamp: Date;
}

/**
 * Quality gate result
 */
export interface QualityGateResult {
  /** Gate name */
  name: string;
  /** Pass/fail status */
  passed: boolean;
  /** Score (0-100) */
  score: number;
  /** Threshold */
  threshold: number;
  /** Details */
  details: string;
  /** Recommendations */
  recommendations?: string[];
}
