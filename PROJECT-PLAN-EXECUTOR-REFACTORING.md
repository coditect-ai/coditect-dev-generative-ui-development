# Project Plan: Refactoring `TaskExecutor` for LLM Interoperability

## 1. Introduction

This document outlines the plan to refactor the `TaskExecutor` in `submodules/core/coditect-core/orchestration/executor.py` to achieve complete interoperability with various Large Language Models (LLMs) through a new abstraction layer (`llm_abstractions`). The goal is to replace the current script-based LLM execution with a more modular, object-oriented approach, enhancing flexibility, maintainability, and scalability.

## 2. Goals

*   Integrate the newly created `llm_abstractions` (e.g., `BaseLlm`, `Gemini`) into the `TaskExecutor`.
*   Decouple `TaskExecutor` from direct calls to external LLM execution scripts (e.g., `execute_gemini.py`).
*   Enable `TaskExecutor` to dynamically select and use any LLM that adheres to the `BaseLlm` interface.
*   Centralize LLM interaction logic, making it easier to add new LLMs in the future.
*   Improve code readability and maintainability.

## 3. High-Level Plan

1.  **Modify `TaskExecutor._execute_api`:** Update this method to use the `llm_abstractions` instead of executing external scripts.
2.  **Implement an LLM Factory/Resolver:** Create a mechanism within `TaskExecutor` to map `AgentType` (from `agent_registry.py`) to the appropriate concrete LLM class (e.g., `Gemini`, `Claude`, `Gpt`) from `llm_abstractions`.
3.  **Instantiate and Execute LLM:** Dynamically instantiate the selected LLM class and call its `generate_content_async` method.
4.  **Remove Legacy Script References:** Clean up or deprecate the old `_get_execution_script` method and its associated logic.
5.  **Update Agent Registry (if necessary):** Ensure `AgentRegistry` is configured to correctly provide the necessary parameters for the new LLM classes.
6.  **Test the Refactoring:** Implement or update unit and integration tests to ensure the new execution flow works as expected for all supported LLMs.

## 4. Detailed Steps

### Step 4.1: Update `executor.py` Imports

*   Add imports for `BaseLlm` and specific LLM implementations (e.g., `Gemini`) from `llm_abstractions`.
    ```python
    # submodules/core/coditect-core/orchestration/executor.py
    # ...
    from ..llm_abstractions.base_llm import BaseLlm
    from ..llm_abstractions.gemini import Gemini
    # from ..llm_abstractions.claude import Claude # Future
    # from ..llm_abstractions.gpt import Gpt     # Future
    # ...
    ```

### Step 4.2: Implement LLM Factory/Resolver in `TaskExecutor`

*   Add a new attribute to `TaskExecutor` (e.g., `_llm_factory`) that maps `AgentType` to the corresponding `BaseLlm` subclass.

    ```python
    # In TaskExecutor.__init__
    self._llm_factory: Dict[AgentType, Type[BaseLlm]] = {
        AgentType.GOOGLE_GEMINI: Gemini,
        # AgentType.ANTHROPIC_CLAUDE: Claude, # Future
        # AgentType.OPENAI_GPT: Gpt,         # Future
    }
    ```

### Step 4.3: Modify `TaskExecutor._execute_api`

*   Refactor the `_execute_api` method to:
    1.  Get the `AgentConfig` from the `AgentRegistry`.
    2.  Use the `_llm_factory` to get the appropriate LLM class based on `agent_config.agent_type`.
    3.  Instantiate the LLM class, passing relevant parameters from `agent_config` (e.g., `model`, `api_key`).
    4.  Prepare the `messages` list for the LLM.
    5.  Call the LLM's `generate_content_async` method.
    6.  Process the response and update the `ExecutionResult`.

    ```python
    # In TaskExecutor._execute_api
    async def _execute_api(
        self,
        task: AgentTask,
        agent_config: AgentConfig,
        result: ExecutionResult
    ) -> ExecutionResult:
        result.status = ExecutionStatus.IN_PROGRESS
        try:
            llm_class = self._llm_factory.get(agent_config.agent_type)
            if not llm_class:
                raise ValueError(f"No LLM implementation found for agent type: {agent_config.agent_type.value}")

            # Instantiate the LLM
            llm_instance = llm_class(
                model=agent_config.model,
                api_key=agent_config.api_key # Assuming API key is passed here
            )

            # Prepare messages (simplified for plan, actual implementation might be more complex)
            messages = [
                {"role": "user", "content": task.description} # Example
            ]

            # Call the LLM's async method
            llm_output = await llm_instance.generate_content_async(messages)

            result.status = ExecutionStatus.SUCCESS
            result.output = llm_output
            result.completed_at = datetime.now()

        except Exception as e:
            result.status = ExecutionStatus.FAILED
            result.error = str(e)
            result.completed_at = datetime.now()

        return result
    ```
    *   **Note:** The `_execute_api` method is currently not `async`. I will need to make it `async` or find a way to run the `generate_content_async` synchronously, but running it asynchronously is the preferred way. This will require changes to `ProjectOrchestrator.execute_task` as well. This is a significant change, so I will address this in a separate sub-step.

### Step 4.4: Update `ProjectOrchestrator.execute_task` for Async Calls

*   The `execute_task` method in `ProjectOrchestrator` will need to be made `async` to correctly await the `_execute_api` method. This will propagate through the call stack.

    ```python
    # In ProjectOrchestrator.execute_task
    # ...
    async def execute_task(
        self,
        task_id: str,
        agent: Optional[str] = None
    ) -> ExecutionResult:
        # ...
        result = await self.executor.execute(task, agent=agent) # Await the executor
        # ...
    ```
    *   This will also require `ProjectOrchestrator` to be used in an async context.

### Step 4.5: Deprecate/Remove `_get_execution_script`

*   The `_get_execution_script` method within `TaskExecutor` will no longer be necessary for API-based LLM execution. It can be removed or modified to only handle interactive/CLI modes if those persist.

### Step 4.6: Update `AgentRegistry` (Review)

*   No direct changes might be needed, but it's important to ensure `AgentConfig` correctly stores `model` and `api_key` for the new `BaseLlm` implementations. (Already handled by previous changes).

### Step 4.7: Testing

*   Create or modify unit tests for `TaskExecutor` to ensure it correctly instantiates and calls the new LLM classes.
*   Verify that `ProjectOrchestrator` can still execute tasks using the new flow.

## 5. Potential Challenges and Risks

*   **Asynchronous Propagation:** Making `execute_task` and potentially its callers `async` will require changes throughout the system's execution flow.
*   **Error Handling:** Ensuring robust error handling and logging for the new LLM integration.
*   **API Key Management:** The `api_key` passing mechanism needs to be secure and consistent.
*   **LLM-specific parameters:** Different LLMs might have unique parameters that need to be passed. The `**kwargs` in `generate_content_async` should handle this, but the orchestration needs to provide them.

## 6. Future Work

*   Implement `Claude` and `Gpt` classes in `llm_abstractions`.
*   Migrate existing `execute_*.py` script logic into their respective `llm_abstractions` classes.
*   Remove the `scripts/llm_execution` directory and its contents entirely.
*   Enhance `AgentConfig` to store more LLM-specific parameters if needed.

## 7. Confirmation

This plan outlines a significant architectural shift. Your confirmation is required before proceeding with these changes.
