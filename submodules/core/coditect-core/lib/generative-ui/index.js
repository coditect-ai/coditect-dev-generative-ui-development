"use strict";
/**
 * CODITECT Generative UI - Main Entry Point
 * @module index
 */
Object.defineProperty(exports, "__esModule", { value: true });
exports.VERSION = exports.QualityGatesValidator = exports.TokenOptimizer = exports.UISynthesisEngine = exports.QualityReviewer = exports.AccessibilityAuditor = exports.CodeGenerator = exports.UIArchitect = exports.IntentAnalyzer = exports.AgentRole = exports.BaseAgent = void 0;
exports.generateUI = generateUI;
const tslib_1 = require("tslib");
// Export types
tslib_1.__exportStar(require("./types"), exports);
// Export base agent
var base_1 = require("./agents/base");
Object.defineProperty(exports, "BaseAgent", { enumerable: true, get: function () { return base_1.BaseAgent; } });
Object.defineProperty(exports, "AgentRole", { enumerable: true, get: function () { return base_1.AgentRole; } });
// Export specialist agents
var intent_analyzer_1 = require("./agents/specialists/intent-analyzer");
Object.defineProperty(exports, "IntentAnalyzer", { enumerable: true, get: function () { return intent_analyzer_1.IntentAnalyzer; } });
var ui_architect_1 = require("./agents/specialists/ui-architect");
Object.defineProperty(exports, "UIArchitect", { enumerable: true, get: function () { return ui_architect_1.UIArchitect; } });
var code_generator_1 = require("./agents/specialists/code-generator");
Object.defineProperty(exports, "CodeGenerator", { enumerable: true, get: function () { return code_generator_1.CodeGenerator; } });
var accessibility_auditor_1 = require("./agents/specialists/accessibility-auditor");
Object.defineProperty(exports, "AccessibilityAuditor", { enumerable: true, get: function () { return accessibility_auditor_1.AccessibilityAuditor; } });
var quality_reviewer_1 = require("./agents/specialists/quality-reviewer");
Object.defineProperty(exports, "QualityReviewer", { enumerable: true, get: function () { return quality_reviewer_1.QualityReviewer; } });
// Export core libraries
var ui_synthesis_engine_1 = require("./lib/ui-synthesis-engine");
Object.defineProperty(exports, "UISynthesisEngine", { enumerable: true, get: function () { return ui_synthesis_engine_1.UISynthesisEngine; } });
var token_optimizer_1 = require("./lib/token-optimizer");
Object.defineProperty(exports, "TokenOptimizer", { enumerable: true, get: function () { return token_optimizer_1.TokenOptimizer; } });
var quality_gates_1 = require("./lib/quality-gates");
Object.defineProperty(exports, "QualityGatesValidator", { enumerable: true, get: function () { return quality_gates_1.QualityGatesValidator; } });
/**
 * Library version
 */
exports.VERSION = '0.1.0';
/**
 * Quick helper to generate a UI component
 */
async function generateUI(description) {
    const { IntentAnalyzer } = await Promise.resolve().then(() => tslib_1.__importStar(require('./agents/specialists/intent-analyzer')));
    const { UIArchitect } = await Promise.resolve().then(() => tslib_1.__importStar(require('./agents/specialists/ui-architect')));
    const { CodeGenerator } = await Promise.resolve().then(() => tslib_1.__importStar(require('./agents/specialists/code-generator')));
    // Create execution context
    const context = {
        executionId: `exec_${Date.now()}`,
        spec: {},
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
    const codeResult = await codeGenerator.execute({
        architecture: architectResult.data,
        framework: intentResult.data.framework,
        styling: intentResult.data.styling,
        strictTypes: true,
    }, context);
    if (!codeResult.success || !codeResult.data) {
        throw new Error('Code generation failed');
    }
    // Calculate total tokens
    context.tokens.total =
        (intentResult.tokens.prompt + intentResult.tokens.completion) +
            (architectResult.tokens.prompt + architectResult.tokens.completion) +
            (codeResult.tokens.prompt + codeResult.tokens.completion);
    const endTime = new Date();
    const duration = endTime.getTime() - context.metadata.startTime.getTime();
    return {
        spec: intentResult.data,
        architecture: architectResult.data,
        files: codeResult.data,
        metadata: {
            tokens: context.tokens,
            duration,
        },
    };
}
//# sourceMappingURL=index.js.map