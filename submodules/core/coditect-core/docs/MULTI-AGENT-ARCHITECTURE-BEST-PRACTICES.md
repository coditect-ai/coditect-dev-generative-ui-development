# Multi-Agent AI Systems: Architecture Best Practices & Implementation Guide

**Research Date:** November 13, 2025
**Context:** Best practices for .claude framework multi-agent orchestration
**Status:** Complete Research Report

---

## Executive Summary

This comprehensive research report covers five critical domains for production multi-agent AI systems:

1. **Multi-Agent Communication Patterns** - Message passing, coordination, orchestration
2. **Distributed Task Queue with Dependencies** - Durable workflows and dependency resolution
3. **LLM Circuit Breaker Patterns** - Resilience and fault tolerance
4. **Distributed State Management** - Consistency and synchronization
5. **Observability for AI Agents** - Monitoring, tracing, and debugging

Each section provides architectural patterns, Python libraries, code examples, and actionable recommendations for the `.claude` framework.

---

## Table of Contents

- [1. Multi-Agent Communication Patterns](#1-multi-agent-communication-patterns)
- [2. Distributed Task Queue with Dependencies](#2-distributed-task-queue-with-dependencies)
- [3. LLM Circuit Breaker Patterns](#3-llm-circuit-breaker-patterns)
- [4. Distributed State Management](#4-distributed-state-management)
- [5. Observability for AI Agents](#5-observability-for-ai-agents)
- [6. Recommendations for .claude Framework](#6-recommendations-for-claude-framework)

---

## 1. Multi-Agent Communication Patterns

### 1.1 Overview

Production multi-agent systems implement various communication architectures depending on coordination requirements. Three dominant frameworks lead the space: LangGraph, CrewAI, and AutoGen.

### 1.2 Architectural Patterns

#### Pattern 1: Graph-Based State Sharing (LangGraph)

**Architecture:**
- Agents are nodes in a directed graph
- Edges represent communication pathways
- Shared state serves as communication medium

**Key Characteristics:**
- **Collaborative Shared State**: All agents read/write to unified scratchpad
- **Supervisor-Routed**: Central supervisor routes tasks to specialized agents
- **Hierarchical Teams**: Nested graphs for complex workflows

**Implementation Example:**

```python
from langgraph.graph import StateGraph, END
from langchain_core.messages import HumanMessage

# Define shared state
class MultiAgentState(TypedDict):
    messages: List[HumanMessage]
    current_agent: str
    results: Dict[str, Any]

# Create graph
graph = StateGraph(MultiAgentState)

# Add agent nodes
graph.add_node("researcher", researcher_agent)
graph.add_node("analyst", analyst_agent)
graph.add_node("writer", writer_agent)

# Define routing logic
def route_next_agent(state: MultiAgentState) -> str:
    if state["current_agent"] == "researcher":
        return "analyst"
    elif state["current_agent"] == "analyst":
        return "writer"
    return END

graph.add_conditional_edges("researcher", route_next_agent)
graph.add_conditional_edges("analyst", route_next_agent)
graph.add_conditional_edges("writer", route_next_agent)

# Compile and run
app = graph.compile()
result = app.invoke({"messages": [HumanMessage(content="Research AI trends")]})
```

**Strengths:**
- ✅ Flexible routing based on state
- ✅ Asynchronous coordination without tight coupling
- ✅ Visual representation of agent workflows
- ✅ Support for cycles and conditional branching

**Weaknesses:**
- ❌ Complexity increases with number of agents
- ❌ State management requires careful design
- ❌ Limited inter-graph communication

**Best For:** Complex workflows with conditional routing and state-dependent coordination

---

#### Pattern 2: Role-Based Delegation (CrewAI)

**Architecture:**
- Agents defined by role, goal, and capabilities
- Task-based coordination with explicit delegation
- Crew structure manages execution flow

**Key Characteristics:**
- Direct agent-to-agent task delegation
- Sequential or parallel task execution
- Built-in memory and context management

**Implementation Example:**

```python
from crewai import Agent, Task, Crew

# Define specialized agents
researcher = Agent(
    role="Research Analyst",
    goal="Gather comprehensive data on assigned topics",
    backstory="Expert researcher with 10 years experience",
    allow_delegation=True,  # Can delegate to other agents
    verbose=True
)

analyst = Agent(
    role="Data Analyst",
    goal="Analyze research findings and extract insights",
    backstory="Statistical analysis expert",
    allow_delegation=False,
    verbose=True
)

writer = Agent(
    role="Technical Writer",
    goal="Create clear documentation from analysis",
    backstory="Technical communication specialist",
    allow_delegation=False,
    verbose=True
)

# Define task sequence with dependencies
task1 = Task(
    description="Research recent AI developments in multi-agent systems",
    agent=researcher,
    expected_output="Comprehensive research report"
)

task2 = Task(
    description="Analyze research findings for key trends and patterns",
    agent=analyst,
    expected_output="Statistical analysis with visualizations",
    context=[task1]  # Receives output from task1
)

task3 = Task(
    description="Write executive summary of analysis",
    agent=writer,
    expected_output="Executive summary document",
    context=[task1, task2]  # Receives outputs from both previous tasks
)

# Create crew and execute
crew = Crew(
    agents=[researcher, analyst, writer],
    tasks=[task1, task2, task3],
    verbose=True
)

result = crew.kickoff()
```

**Strengths:**
- ✅ Intuitive role-based design
- ✅ Automatic context propagation between tasks
- ✅ Built-in delegation mechanism
- ✅ Simple to understand and implement

**Weaknesses:**
- ❌ Less flexible routing than graph-based approaches
- ❌ Primarily sequential execution model
- ❌ Limited support for complex conditional logic

**Best For:** Well-defined workflows with clear role specialization and sequential dependencies

---

#### Pattern 3: Conversational Messaging (AutoGen)

**Architecture:**
- Message-based agent communication
- Agents implement send/receive protocols
- Flexible conversation topologies

**Key Characteristics:**
- **Message Passing**: Asynchronous message exchange between agents
- **Event-Driven**: Agents respond to messages via registered reply functions
- **Flexible Topologies**: Supports two-agent, group chat, hierarchical, and nested patterns

**Implementation Example:**

```python
from autogen import AssistantAgent, UserProxyAgent, GroupChat, GroupChatManager
import os

# Configure LLM
config_list = [{
    "model": "gpt-4",
    "api_key": os.environ["OPENAI_API_KEY"]
}]

# Create specialized assistant agents
researcher = AssistantAgent(
    name="researcher",
    system_message="You are a research specialist. Gather information and cite sources.",
    llm_config={"config_list": config_list}
)

analyst = AssistantAgent(
    name="analyst",
    system_message="You analyze data and extract insights. Focus on patterns and trends.",
    llm_config={"config_list": config_list}
)

critic = AssistantAgent(
    name="critic",
    system_message="You critically review work and suggest improvements.",
    llm_config={"config_list": config_list}
)

# Create user proxy for execution
user_proxy = UserProxyAgent(
    name="user_proxy",
    human_input_mode="TERMINATE",  # Auto-terminate on specific message
    max_consecutive_auto_reply=10,
    code_execution_config={
        "work_dir": "workspace",
        "use_docker": False
    }
)

# Setup group chat with custom speaker selection
groupchat = GroupChat(
    agents=[user_proxy, researcher, analyst, critic],
    messages=[],
    max_round=12,
    speaker_selection_method="round_robin"  # or "auto" for LLM-based selection
)

manager = GroupChatManager(
    groupchat=groupchat,
    llm_config={"config_list": config_list}
)

# Initiate multi-agent conversation
user_proxy.initiate_chat(
    manager,
    message="Research and analyze the current state of multi-agent AI systems"
)
```

**Advanced: Dynamic Speaker Selection**

```python
def custom_speaker_selection(last_speaker, groupchat):
    """Custom logic for selecting next speaker based on conversation state"""
    messages = groupchat.messages

    if last_speaker is user_proxy:
        return researcher  # Always start with researcher
    elif last_speaker is researcher:
        return analyst  # Analyze research findings
    elif last_speaker is analyst:
        return critic  # Review analysis
    elif last_speaker is critic:
        # Check if revisions needed
        if "needs improvement" in messages[-1]["content"].lower():
            return researcher  # Loop back for more research
        else:
            return user_proxy  # Finish conversation

groupchat = GroupChat(
    agents=[user_proxy, researcher, analyst, critic],
    messages=[],
    max_round=20,
    speaker_selection_method=custom_speaker_selection
)
```

**Strengths:**
- ✅ Highly flexible conversation patterns
- ✅ Support for dynamic topologies
- ✅ Built-in code execution and human-in-the-loop
- ✅ Both autonomous and supervised modes

**Weaknesses:**
- ❌ More complex to reason about message flows
- ❌ Requires careful state management across conversations
- ❌ Can lead to unpredictable conversation patterns

**Best For:** Exploratory workflows, code generation tasks, and scenarios requiring dynamic agent coordination

---

### 1.3 Comparison Matrix

| Feature | LangGraph | CrewAI | AutoGen |
|---------|-----------|--------|---------|
| **Communication Model** | Shared state + graph edges | Task delegation | Message passing |
| **Coordination** | Graph-based routing | Role-based workflow | Conversational |
| **Flexibility** | High (conditional edges) | Medium (sequential/parallel) | Very High (dynamic) |
| **Learning Curve** | Medium | Low | Medium-High |
| **Determinism** | High | High | Medium |
| **Code Execution** | Via tools | Via tools | Native support |
| **Human-in-Loop** | Via custom nodes | Via callbacks | Native modes |
| **Visualization** | Built-in graph viz | Limited | Via logging |
| **Best Use Case** | Complex stateful workflows | Team-based delegation | Exploratory problem-solving |

### 1.4 Key Takeaways

1. **No Single Best Pattern**: Choice depends on workflow complexity, coordination needs, and team expertise
2. **Hybrid Approaches Work**: Combine patterns (e.g., LangGraph with CrewAI-style roles)
3. **Message Passing Is Universal**: All frameworks ultimately use message passing at some level
4. **State Management Is Critical**: Explicit state design prevents coordination failures
5. **Start Simple, Add Complexity**: Begin with sequential delegation, evolve to graphs/conversations as needed

### 1.5 Recommendations for .claude Framework

**Immediate Actions:**
1. ✅ Implement **graph-based orchestration** similar to LangGraph for complex workflows
2. ✅ Add **role-based task delegation** inspired by CrewAI for simple agent coordination
3. ✅ Design **shared state schema** for agent communication via persistent storage
4. ✅ Create **message passing interface** for async agent-to-agent communication

**Architecture Decision:**
```python
# .claude/framework/agent_communication.py

from typing import TypedDict, List, Dict, Any, Literal
from dataclasses import dataclass
from abc import ABC, abstractmethod

# Define communication protocols
class AgentMessage(TypedDict):
    sender: str
    recipient: str
    content: str
    metadata: Dict[str, Any]
    timestamp: float

class SharedState(TypedDict):
    """Global state accessible to all agents"""
    messages: List[AgentMessage]
    context: Dict[str, Any]
    current_agent: str
    workflow_status: Literal["running", "paused", "completed", "failed"]

# Abstract agent interface
class CommunicatingAgent(ABC):
    def __init__(self, name: str, role: str):
        self.name = name
        self.role = role

    @abstractmethod
    async def receive_message(self, message: AgentMessage) -> None:
        """Handle incoming messages from other agents"""
        pass

    @abstractmethod
    async def send_message(self, recipient: str, content: str) -> None:
        """Send message to another agent"""
        pass

    @abstractmethod
    async def execute(self, state: SharedState) -> SharedState:
        """Execute agent logic and update shared state"""
        pass

# Message broker for agent coordination
class AgentMessageBroker:
    def __init__(self):
        self.agents: Dict[str, CommunicatingAgent] = {}
        self.message_queue: List[AgentMessage] = []

    def register_agent(self, agent: CommunicatingAgent):
        self.agents[agent.name] = agent

    async def route_message(self, message: AgentMessage):
        recipient = self.agents.get(message["recipient"])
        if recipient:
            await recipient.receive_message(message)
        else:
            self.message_queue.append(message)  # Queue for future delivery

    async def broadcast(self, sender: str, content: str):
        """Send message to all agents except sender"""
        for name, agent in self.agents.items():
            if name != sender:
                message: AgentMessage = {
                    "sender": sender,
                    "recipient": name,
                    "content": content,
                    "metadata": {"type": "broadcast"},
                    "timestamp": time.time()
                }
                await agent.receive_message(message)
```

**Long-term:**
- Build visual graph editor for workflow design
- Add conversation history and replay capabilities
- Implement agent capability discovery and dynamic routing
- Create distributed message queue for multi-node deployments

---

## 2. Distributed Task Queue with Dependencies

### 2.1 Overview

Durable task queues with dependency resolution enable reliable execution of complex multi-step workflows. Three primary approaches exist: workflow orchestration platforms (Temporal), DAG schedulers (Airflow), and distributed task queues (Celery).

### 2.2 Architecture Patterns

#### Pattern 1: Workflow Orchestration (Temporal)

**Architecture:**
- Workflows define business logic (deterministic)
- Activities handle side effects (non-deterministic)
- Workers poll task queues for execution
- Temporal Server manages state and coordination

**Key Characteristics:**
- **Durable Execution**: State persisted across failures
- **Automatic Retries**: Failed activities retry with backoff
- **Long-Running Workflows**: Support for months-long executions
- **Human-in-the-Loop**: Signals enable external input

**Implementation Example:**

```python
from temporalio import workflow, activity
from temporalio.client import Client
from temporalio.worker import Worker
from datetime import timedelta
from typing import List

# Define activities (non-deterministic operations)
@activity.defn
async def fetch_data(url: str) -> dict:
    """Fetch data from external API"""
    # This can fail, will be retried automatically
    import httpx
    async with httpx.AsyncClient() as client:
        response = await client.get(url)
        return response.json()

@activity.defn
async def process_data(data: dict) -> dict:
    """Process fetched data"""
    # CPU-intensive or I/O operations
    return {"processed": True, "result": data}

@activity.defn
async def store_results(results: dict) -> str:
    """Store results in database"""
    # Database operations with retry
    return "success"

# Define workflow (deterministic orchestration logic)
@workflow.defn
class DataPipelineWorkflow:
    @workflow.run
    async def run(self, urls: List[str]) -> dict:
        # Sequential execution with automatic retries
        all_results = []

        for url in urls:
            # Execute activity with timeout and retry policy
            data = await workflow.execute_activity(
                fetch_data,
                url,
                start_to_close_timeout=timedelta(seconds=30),
                retry_policy={
                    "initial_interval": timedelta(seconds=1),
                    "maximum_interval": timedelta(seconds=60),
                    "backoff_coefficient": 2.0,
                    "maximum_attempts": 5
                }
            )

            # Process data
            processed = await workflow.execute_activity(
                process_data,
                data,
                start_to_close_timeout=timedelta(minutes=5)
            )

            all_results.append(processed)

        # Store all results
        status = await workflow.execute_activity(
            store_results,
            {"results": all_results},
            start_to_close_timeout=timedelta(seconds=10)
        )

        return {"status": status, "count": len(all_results)}

# Worker setup
async def main():
    # Connect to Temporal server
    client = await Client.connect("localhost:7233")

    # Create worker
    worker = Worker(
        client,
        task_queue="data-pipeline-queue",
        workflows=[DataPipelineWorkflow],
        activities=[fetch_data, process_data, store_results]
    )

    # Run worker (blocks until shutdown)
    await worker.run()

# Start workflow from client
async def start_workflow():
    client = await Client.connect("localhost:7233")

    result = await client.execute_workflow(
        DataPipelineWorkflow.run,
        ["https://api.example.com/data1", "https://api.example.com/data2"],
        id="data-pipeline-123",
        task_queue="data-pipeline-queue"
    )

    print(f"Workflow completed: {result}")
```

**Advanced: Complex Dependencies with Child Workflows**

```python
@workflow.defn
class ParentOrchestrator:
    @workflow.run
    async def run(self, job_ids: List[str]) -> dict:
        # Execute child workflows in parallel
        child_handles = []

        for job_id in job_ids:
            handle = await workflow.start_child_workflow(
                DataPipelineWorkflow.run,
                [f"https://api.example.com/{job_id}"],
                id=f"child-{job_id}"
            )
            child_handles.append(handle)

        # Wait for all children to complete
        results = []
        for handle in child_handles:
            result = await handle.result()
            results.append(result)

        # Aggregate results
        return {"total_jobs": len(results), "results": results}
```

**Strengths:**
- ✅ Automatic state persistence and recovery
- ✅ Built-in retry and timeout handling
- ✅ Support for extremely long-running workflows
- ✅ Deterministic replay for debugging
- ✅ Horizontal scalability

**Weaknesses:**
- ❌ Steep learning curve
- ❌ Requires Temporal Server infrastructure
- ❌ Workflow code must be deterministic
- ❌ Complex setup compared to simple task queues

**Best For:** Mission-critical workflows requiring durability, complex multi-step processes, and long-running operations

---

#### Pattern 2: DAG Scheduling (Airflow)

**Architecture:**
- Directed Acyclic Graphs (DAGs) define task dependencies
- Scheduler triggers tasks based on dependencies and schedule
- Executors run tasks on workers
- Metadata database tracks state

**Key Characteristics:**
- **Explicit Dependencies**: Tasks declare upstream/downstream relationships
- **Schedule-Driven**: DAGs run on cron schedules or external triggers
- **Rich Operators**: Built-in operators for common tasks
- **Cross-DAG Dependencies**: Support via sensors

**Implementation Example:**

```python
from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.operators.bash import BashOperator
from airflow.sensors.external_task import ExternalTaskSensor
from datetime import datetime, timedelta

# Default arguments for all tasks
default_args = {
    'owner': 'data-team',
    'depends_on_past': False,
    'email_on_failure': True,
    'email_on_retry': False,
    'retries': 3,
    'retry_delay': timedelta(minutes=5),
    'retry_exponential_backoff': True,
    'max_retry_delay': timedelta(minutes=30)
}

# Define DAG
with DAG(
    'multi_agent_pipeline',
    default_args=default_args,
    description='Multi-agent data processing pipeline',
    schedule_interval='@hourly',
    start_date=datetime(2025, 1, 1),
    catchup=False,
    tags=['agents', 'pipeline']
) as dag:

    # Task 1: Data extraction
    extract_data = PythonOperator(
        task_id='extract_data',
        python_callable=lambda: extract_from_api(),
        op_kwargs={'source': 'production_db'}
    )

    # Task 2 & 3: Parallel processing
    process_branch_a = PythonOperator(
        task_id='process_branch_a',
        python_callable=lambda data: process_with_agent_a(data)
    )

    process_branch_b = PythonOperator(
        task_id='process_branch_b',
        python_callable=lambda data: process_with_agent_b(data)
    )

    # Task 4: Merge results (depends on both branches)
    merge_results = PythonOperator(
        task_id='merge_results',
        python_callable=lambda a, b: merge_outputs(a, b),
        trigger_rule='all_success'  # Wait for all upstreams
    )

    # Task 5: Quality check
    quality_check = PythonOperator(
        task_id='quality_check',
        python_callable=lambda results: validate_quality(results)
    )

    # Task 6: Conditional storage
    store_results = PythonOperator(
        task_id='store_results',
        python_callable=lambda results: save_to_warehouse(results),
        trigger_rule='none_failed'  # Run even if upstream skipped
    )

    # Define dependencies using bitshift operators
    extract_data >> [process_branch_a, process_branch_b]  # Fan-out
    [process_branch_a, process_branch_b] >> merge_results  # Fan-in
    merge_results >> quality_check >> store_results

# Cross-DAG dependency example
with DAG('downstream_dag', ...) as downstream_dag:
    # Wait for upstream DAG to complete
    wait_for_upstream = ExternalTaskSensor(
        task_id='wait_for_data_pipeline',
        external_dag_id='multi_agent_pipeline',
        external_task_id='store_results',
        timeout=600,
        mode='poke',
        poke_interval=60
    )

    process_downstream = PythonOperator(
        task_id='process_downstream',
        python_callable=lambda: process_data()
    )

    wait_for_upstream >> process_downstream
```

**Dynamic DAG Generation:**

```python
def generate_agent_tasks(agent_configs: List[dict]) -> DAG:
    """Dynamically create tasks based on agent configurations"""
    with DAG('dynamic_multi_agent', ...) as dag:
        start = PythonOperator(task_id='start', python_callable=lambda: None)
        end = PythonOperator(task_id='end', python_callable=lambda: None)

        previous_tasks = [start]

        for config in agent_configs:
            task = PythonOperator(
                task_id=f"agent_{config['name']}",
                python_callable=config['callable'],
                op_kwargs=config.get('kwargs', {})
            )

            # Set dependencies based on config
            for prev in previous_tasks:
                prev >> task

            if config.get('blocking', True):
                previous_tasks = [task]  # Sequential
            else:
                previous_tasks.append(task)  # Parallel

        for task in previous_tasks:
            task >> end

        return dag
```

**Strengths:**
- ✅ Visual DAG representation
- ✅ Rich ecosystem of operators
- ✅ Strong scheduling capabilities
- ✅ Extensive monitoring and logging
- ✅ Battle-tested in production

**Weaknesses:**
- ❌ Not designed for sub-minute latency
- ❌ Complex setup and maintenance
- ❌ DAG definition can become unwieldy
- ❌ Limited support for event-driven workflows

**Best For:** Scheduled batch processing, ETL pipelines, and workflows with clear dependency structures

---

#### Pattern 3: Distributed Task Queue (Celery)

**Architecture:**
- Message broker (Redis/RabbitMQ) queues tasks
- Workers poll queues and execute tasks
- Result backend stores task outcomes
- Beat scheduler handles periodic tasks

**Key Characteristics:**
- **Asynchronous Execution**: Non-blocking task dispatch
- **Distributed Workers**: Horizontal scaling
- **Task Primitives**: Chains, groups, chords for composition
- **Flexible Routing**: Task routing to specific queues/workers

**Implementation Example:**

```python
from celery import Celery, group, chain, chord
from celery.result import AsyncResult
from typing import List

# Initialize Celery
app = Celery(
    'agent_tasks',
    broker='redis://localhost:6379/0',
    backend='redis://localhost:6379/0'
)

# Configure retries and timeouts
app.conf.update(
    task_serializer='json',
    result_serializer='json',
    accept_content=['json'],
    timezone='UTC',
    enable_utc=True,
    task_acks_late=True,  # Acknowledge after completion
    task_reject_on_worker_lost=True,
    task_track_started=True
)

# Define tasks
@app.task(
    bind=True,
    max_retries=3,
    default_retry_delay=60,
    autoretry_for=(Exception,),
    retry_backoff=True,
    retry_backoff_max=600,
    retry_jitter=True
)
def agent_research(self, query: str) -> dict:
    """Research task with automatic retry"""
    try:
        # Simulate research agent
        results = perform_research(query)
        return {"query": query, "results": results}
    except Exception as exc:
        # Retry with exponential backoff
        raise self.retry(exc=exc)

@app.task
def agent_analyze(research_data: dict) -> dict:
    """Analysis task"""
    return {"analysis": analyze_data(research_data)}

@app.task
def agent_synthesize(analysis_data: dict) -> dict:
    """Synthesis task"""
    return {"report": synthesize_report(analysis_data)}

@app.task
def aggregate_results(results: List[dict]) -> dict:
    """Aggregate multiple results"""
    return {"aggregated": merge_all(results)}

# Task composition patterns

# 1. Chain: Sequential execution (A -> B -> C)
def sequential_pipeline(query: str):
    """Execute tasks sequentially with result passing"""
    workflow = chain(
        agent_research.s(query),
        agent_analyze.s(),
        agent_synthesize.s()
    )
    return workflow.apply_async()

# 2. Group: Parallel execution
def parallel_research(queries: List[str]):
    """Execute multiple research tasks in parallel"""
    job = group(agent_research.s(q) for q in queries)
    return job.apply_async()

# 3. Chord: Parallel with callback (Group + Final Task)
def parallel_with_aggregation(queries: List[str]):
    """Execute in parallel then aggregate results"""
    workflow = chord(
        (agent_research.s(q) for q in queries),
        aggregate_results.s()  # Called after all parallel tasks complete
    )
    return workflow.apply_async()

# 4. Complex dependencies
def complex_workflow():
    """Multi-stage workflow with dependencies"""
    # Stage 1: Parallel research
    research_tasks = group(
        agent_research.s("topic1"),
        agent_research.s("topic2"),
        agent_research.s("topic3")
    )

    # Stage 2: Analyze each result (parallel)
    # Stage 3: Synthesize all analyses
    workflow = chord(
        research_tasks | group(agent_analyze.s()),  # Chain group to group
        agent_synthesize.s()
    )

    return workflow.apply_async()

# Task dependency management with celery-tasktree
from celery_tasktree import task_with_context, TaskTree

@task_with_context
def dependent_task_a(context):
    return "Result A"

@task_with_context
def dependent_task_b(context, a_result):
    return f"Result B depends on {a_result}"

@task_with_context
def dependent_task_c(context, a_result, b_result):
    return f"Result C depends on {a_result} and {b_result}"

def dependency_tree():
    """Execute tasks with explicit dependencies"""
    tree = TaskTree()

    task_a = tree.add_task(dependent_task_a)
    task_b = tree.add_task(dependent_task_b, dependencies=[task_a])
    task_c = tree.add_task(dependent_task_c, dependencies=[task_a, task_b])

    return tree.apply_async()

# Monitor task status
def check_workflow_status(result_id: str):
    """Check status of async task"""
    result = AsyncResult(result_id, app=app)

    if result.ready():
        if result.successful():
            return {"status": "completed", "result": result.result}
        else:
            return {"status": "failed", "error": str(result.info)}
    else:
        return {"status": "pending", "state": result.state}

# Routing to specific queues
@app.task(queue='high_priority')
def urgent_task():
    pass

@app.task(queue='low_priority')
def background_task():
    pass

# Start worker: celery -A agent_tasks worker --queues=high_priority,low_priority
```

**Strengths:**
- ✅ Simple async task execution
- ✅ Lightweight compared to Airflow/Temporal
- ✅ Flexible task routing
- ✅ Rich composition primitives

**Weaknesses:**
- ❌ No built-in workflow visualization
- ❌ Limited dependency management (requires libraries like celery-tasktree)
- ❌ No automatic state persistence across failures
- ❌ Requires external scheduler for cron-like scheduling

**Best For:** Asynchronous background tasks, high-throughput job processing, and simple task coordination

---

### 2.3 Comparison Matrix

| Feature | Temporal | Airflow | Celery |
|---------|----------|---------|--------|
| **Use Case** | Durable workflows | Scheduled DAGs | Async tasks |
| **State Management** | Built-in durable | Metadata DB | Result backend |
| **Dependency Resolution** | Child workflows | DAG edges | Chains/chords |
| **Failure Recovery** | Automatic retry | Task retries | Manual retry |
| **Scalability** | Horizontal | Horizontal | Horizontal |
| **Latency** | Low (sub-second) | High (minutes) | Low (sub-second) |
| **Visualization** | Web UI | Rich UI | Flower (basic) |
| **Learning Curve** | High | Medium | Low |
| **Best For** | Mission-critical | Batch ETL | Background jobs |

### 2.4 Key Takeaways

1. **Match Tool to Use Case**: Temporal for durability, Airflow for scheduling, Celery for async
2. **Dependencies Are First-Class**: Explicitly model dependencies to avoid race conditions
3. **Retries Are Essential**: All patterns support retries, but implementation varies
4. **State Management Matters**: Choose architecture based on state persistence requirements
5. **Monitoring Is Critical**: Implement observability for production workflows

### 2.5 Recommendations for .claude Framework

**Immediate Actions:**
1. ✅ Start with **Celery** for simple task queuing and async execution
2. ✅ Add **celery-tasktree** for explicit dependency management
3. ✅ Implement **result callbacks** for task completion notifications
4. ✅ Use **Redis** as broker and backend for simplicity

**Sample Integration:**

```python
# .claude/framework/task_queue.py

from celery import Celery, Task
from typing import Callable, Any, List, Optional
import json

class ClaudeTask(Task):
    """Base task class with .claude framework integration"""

    def on_failure(self, exc, task_id, args, kwargs, einfo):
        """Log task failure to .claude framework"""
        from .logging import log_task_failure
        log_task_failure(task_id, exc, einfo)

    def on_success(self, retval, task_id, args, kwargs):
        """Log task success to .claude framework"""
        from .logging import log_task_success
        log_task_success(task_id, retval)

# Initialize Celery with custom task class
celery_app = Celery(
    'claude_agents',
    broker='redis://localhost:6379/0',
    backend='redis://localhost:6379/0',
    task_cls=ClaudeTask
)

# Configure for agent workloads
celery_app.conf.update(
    task_serializer='json',
    result_serializer='json',
    task_track_started=True,
    task_time_limit=3600,  # 1 hour max per task
    task_soft_time_limit=3300,  # Soft limit at 55 minutes
    worker_prefetch_multiplier=1,  # Disable prefetch for long tasks
    worker_max_tasks_per_child=50  # Restart workers to prevent memory leaks
)

# Decorator for agent tasks
def agent_task(name: str, max_retries: int = 3, queue: str = 'default'):
    """Decorator to create agent task with retry logic"""
    def decorator(func: Callable):
        @celery_app.task(
            bind=True,
            name=f"agent.{name}",
            max_retries=max_retries,
            queue=queue,
            autoretry_for=(Exception,),
            retry_backoff=True,
            retry_backoff_max=600,
            retry_jitter=True
        )
        def wrapper(self, *args, **kwargs):
            try:
                return func(*args, **kwargs)
            except Exception as exc:
                # Log and retry
                self.retry(exc=exc)
        return wrapper
    return decorator

# Usage example
@agent_task(name="research", queue="research_queue")
def research_agent_task(query: str) -> dict:
    """Research agent task"""
    # Agent logic here
    return {"results": [...]}

@agent_task(name="analyze", queue="analysis_queue")
def analysis_agent_task(data: dict) -> dict:
    """Analysis agent task"""
    # Agent logic here
    return {"insights": [...]}
```

**Long-term Migration Path:**
- Evaluate **Temporal** for mission-critical agent workflows requiring durability
- Consider **Airflow** if scheduling becomes primary concern
- Build abstraction layer to support multiple backends

---

## 3. LLM Circuit Breaker Patterns

### 3.1 Overview

LLM APIs are inherently unreliable due to rate limits, timeouts, and transient failures. Circuit breakers prevent cascading failures by detecting problems and failing fast, giving systems time to recover.

### 3.2 Core Circuit Breaker Pattern

**States:**
1. **CLOSED**: Normal operation, requests pass through
2. **OPEN**: Failures exceeded threshold, requests fail immediately
3. **HALF-OPEN**: Testing recovery, limited requests allowed

**State Transitions:**
- CLOSED → OPEN: After `fail_max` consecutive failures
- OPEN → HALF-OPEN: After `reset_timeout` seconds
- HALF-OPEN → CLOSED: After `success_threshold` successes
- HALF-OPEN → OPEN: On any failure during recovery

### 3.3 Implementation Patterns

#### Pattern 1: PyBreaker (Thread-Safe, Synchronous)

**Installation:**
```bash
pip install pybreaker
```

**Basic Implementation:**

```python
import pybreaker
from typing import Optional
import time

# Create circuit breaker for LLM API
llm_breaker = pybreaker.CircuitBreaker(
    fail_max=5,  # Open after 5 failures
    reset_timeout=60,  # Try recovery after 60 seconds
    success_threshold=2,  # Close after 2 successes
    exclude=[ValueError, KeyError],  # Don't count business logic errors
)

@llm_breaker
def call_claude_api(prompt: str, model: str = "claude-3-sonnet") -> str:
    """Call Claude API with circuit breaker protection"""
    import anthropic

    client = anthropic.Anthropic()
    response = client.messages.create(
        model=model,
        max_tokens=1024,
        messages=[{"role": "user", "content": prompt}]
    )

    return response.content[0].text

# Usage
try:
    result = call_claude_api("Explain quantum computing")
    print(result)
except pybreaker.CircuitBreakerError:
    # Circuit is open, use fallback
    print("LLM service unavailable, using cached response")
    result = get_cached_response()
```

**Advanced: Custom Listener for Monitoring**

```python
import logging

class LLMCircuitBreakerListener(pybreaker.CircuitBreakerListener):
    """Custom listener for observability"""

    def __init__(self):
        self.logger = logging.getLogger('llm.circuit_breaker')

    def state_change(self, cb, old_state, new_state):
        """Track state transitions"""
        self.logger.warning(
            f"Circuit breaker '{cb.name}': {old_state.name} → {new_state.name}"
        )

        if new_state == pybreaker.STATE_OPEN:
            # Alert on circuit opening
            send_alert(f"LLM circuit breaker opened for {cb.name}")

    def failure(self, cb, exc):
        """Log each failure"""
        self.logger.error(f"LLM call failed: {exc}")

    def success(self, cb):
        """Log successful calls"""
        self.logger.debug("LLM call succeeded")

    def before_call(self, cb, func, *args, **kwargs):
        """Track call latency"""
        cb._start_time = time.time()

    def call_succeeded(self, cb, elapsed):
        """Monitor performance"""
        if elapsed > 5.0:  # Slow response
            self.logger.warning(f"Slow LLM response: {elapsed:.2f}s")

# Create breaker with listener
llm_breaker = pybreaker.CircuitBreaker(
    fail_max=10,
    reset_timeout=300,
    listeners=[LLMCircuitBreakerListener()]
)
```

**Multi-Model Circuit Breakers:**

```python
# Separate circuit breakers per model/provider
claude_breaker = pybreaker.CircuitBreaker(
    name="claude",
    fail_max=5,
    reset_timeout=60
)

gpt4_breaker = pybreaker.CircuitBreaker(
    name="gpt4",
    fail_max=5,
    reset_timeout=60
)

gemini_breaker = pybreaker.CircuitBreaker(
    name="gemini",
    fail_max=5,
    reset_timeout=60
)

@claude_breaker
def call_claude(prompt: str) -> str:
    # Claude implementation
    pass

@gpt4_breaker
def call_gpt4(prompt: str) -> str:
    # GPT-4 implementation
    pass

@gemini_breaker
def call_gemini(prompt: str) -> str:
    # Gemini implementation
    pass

def call_llm_with_fallback(prompt: str) -> str:
    """Try multiple providers with circuit breakers"""
    providers = [
        ("Claude", call_claude),
        ("GPT-4", call_gpt4),
        ("Gemini", call_gemini)
    ]

    for name, provider_func in providers:
        try:
            return provider_func(prompt)
        except pybreaker.CircuitBreakerError:
            print(f"{name} circuit open, trying next provider")
            continue
        except Exception as e:
            print(f"{name} failed with {e}, trying next provider")
            continue

    # All providers failed
    raise Exception("All LLM providers unavailable")
```

---

#### Pattern 2: aiobreaker (Asyncio-Compatible)

**Installation:**
```bash
pip install aiobreaker
```

**Async Implementation:**

```python
import aiobreaker
import asyncio
from anthropic import AsyncAnthropic

# Async circuit breaker
async_llm_breaker = aiobreaker.CircuitBreaker(
    fail_max=10,
    timeout=300,
    success_threshold=3
)

@async_llm_breaker
async def call_claude_async(prompt: str) -> str:
    """Async Claude API call with circuit breaker"""
    client = AsyncAnthropic()

    response = await client.messages.create(
        model="claude-3-sonnet-20240229",
        max_tokens=1024,
        messages=[{"role": "user", "content": prompt}]
    )

    return response.content[0].text

# Batch processing with circuit breaker
async def process_batch(prompts: list[str]) -> list[str]:
    """Process multiple prompts with circuit breaker protection"""
    results = []

    for prompt in prompts:
        try:
            result = await call_claude_async(prompt)
            results.append(result)
        except aiobreaker.CircuitBreakerError:
            # Circuit open, add placeholder
            results.append("[LLM UNAVAILABLE]")
            await asyncio.sleep(1)  # Rate limit retries

    return results

# Run batch
async def main():
    prompts = ["Question 1", "Question 2", "Question 3"]
    results = await process_batch(prompts)
    print(results)

asyncio.run(main())
```

---

#### Pattern 3: Manual Circuit Breaker with Context Manager

```python
from dataclasses import dataclass
from enum import Enum
from datetime import datetime, timedelta
from typing import Optional, Callable, Any
import threading

class CircuitState(Enum):
    CLOSED = "closed"
    OPEN = "open"
    HALF_OPEN = "half_open"

@dataclass
class CircuitBreakerConfig:
    failure_threshold: int = 5
    recovery_timeout: int = 60
    success_threshold: int = 2
    expected_exception: type = Exception

class CircuitBreaker:
    """Manual circuit breaker implementation"""

    def __init__(self, config: CircuitBreakerConfig):
        self.config = config
        self.state = CircuitState.CLOSED
        self.failure_count = 0
        self.success_count = 0
        self.last_failure_time: Optional[datetime] = None
        self._lock = threading.Lock()

    def calling(self):
        """Context manager for protected calls"""
        return self

    def __enter__(self):
        with self._lock:
            if self.state == CircuitState.OPEN:
                # Check if recovery timeout elapsed
                if self.last_failure_time and \
                   datetime.now() - self.last_failure_time > timedelta(seconds=self.config.recovery_timeout):
                    self.state = CircuitState.HALF_OPEN
                    self.success_count = 0
                else:
                    raise Exception("Circuit breaker is OPEN")
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type is None:
            # Success
            self._record_success()
        elif issubclass(exc_type, self.config.expected_exception):
            # Expected failure
            self._record_failure()

        return False  # Don't suppress exception

    def _record_success(self):
        with self._lock:
            self.failure_count = 0

            if self.state == CircuitState.HALF_OPEN:
                self.success_count += 1
                if self.success_count >= self.config.success_threshold:
                    self.state = CircuitState.CLOSED
                    self.success_count = 0

    def _record_failure(self):
        with self._lock:
            self.failure_count += 1
            self.last_failure_time = datetime.now()

            if self.failure_count >= self.config.failure_threshold:
                self.state = CircuitState.OPEN
                self.failure_count = 0

# Usage
llm_circuit = CircuitBreaker(CircuitBreakerConfig(
    failure_threshold=5,
    recovery_timeout=60,
    success_threshold=2
))

def call_llm(prompt: str) -> str:
    """LLM call protected by circuit breaker"""
    with llm_circuit.calling():
        # Make API call
        return api_call(prompt)
```

### 3.4 Integration with Retry Logic

**Combined Circuit Breaker + Retry Pattern:**

```python
from tenacity import (
    retry,
    stop_after_attempt,
    wait_exponential,
    retry_if_exception_type,
    before_sleep_log
)
import pybreaker
import logging

logger = logging.getLogger(__name__)

# Circuit breaker
llm_breaker = pybreaker.CircuitBreaker(
    fail_max=10,
    reset_timeout=300
)

# Retry decorator with exponential backoff
@retry(
    retry=retry_if_exception_type((TimeoutError, ConnectionError)),
    stop=stop_after_attempt(3),
    wait=wait_exponential(multiplier=1, min=4, max=10),
    before_sleep=before_sleep_log(logger, logging.WARNING)
)
@llm_breaker
def resilient_llm_call(prompt: str) -> str:
    """LLM call with both retry and circuit breaker"""
    # If circuit is open, this raises immediately
    # If circuit is closed, retries on transient failures
    return call_api(prompt)

# Usage
try:
    result = resilient_llm_call("Your prompt")
except pybreaker.CircuitBreakerError:
    # Circuit open, all retries exhausted
    result = fallback_response()
```

### 3.5 Best Practices

**1. Separate Circuit Breakers by Failure Domain:**
```python
# Don't mix different services in one breaker
claude_breaker = pybreaker.CircuitBreaker(name="claude")
embedding_breaker = pybreaker.CircuitBreaker(name="embeddings")
database_breaker = pybreaker.CircuitBreaker(name="database")
```

**2. Exclude Business Logic Errors:**
```python
# Don't open circuit for validation errors
breaker = pybreaker.CircuitBreaker(
    exclude=[ValueError, ValidationError, AuthenticationError]
)
```

**3. Configure Timeouts Appropriately:**
```python
# Fast-failing API: short timeout
api_breaker = pybreaker.CircuitBreaker(
    fail_max=3,
    reset_timeout=30
)

# Batch processing: longer timeout
batch_breaker = pybreaker.CircuitBreaker(
    fail_max=10,
    reset_timeout=300
)
```

**4. Implement Graceful Degradation:**
```python
def get_llm_response(prompt: str) -> str:
    try:
        return call_llm_with_breaker(prompt)
    except pybreaker.CircuitBreakerError:
        # Fallback strategies
        return try_cache_or_simpler_model(prompt)

def try_cache_or_simpler_model(prompt: str) -> str:
    # Try cache first
    cached = get_from_cache(prompt)
    if cached:
        return cached

    # Fall back to smaller/cheaper model
    try:
        return call_small_model(prompt)
    except:
        # Last resort: canned response
        return "Service temporarily unavailable. Please try again."
```

**5. Monitor Circuit Breaker State:**
```python
# Export metrics for monitoring
def export_breaker_metrics(breaker: pybreaker.CircuitBreaker):
    return {
        "name": breaker.name,
        "state": breaker.current_state.name,
        "failure_count": breaker.fail_counter,
        "success_count": breaker.success_counter,
        "last_failure": breaker.last_failure
    }

# Periodic metric export
import time
while True:
    metrics = export_breaker_metrics(llm_breaker)
    send_to_monitoring(metrics)
    time.sleep(60)
```

### 3.6 Recommendations for .claude Framework

**Immediate Actions:**
1. ✅ Install and integrate **pybreaker** for all LLM API calls
2. ✅ Create separate circuit breakers per LLM provider
3. ✅ Implement custom listener for logging and alerting
4. ✅ Add fallback strategies for graceful degradation

**Sample Integration:**

```python
# .claude/framework/llm_resilience.py

import pybreaker
from typing import Dict, Optional, Callable, Any
from dataclasses import dataclass
from enum import Enum

class LLMProvider(Enum):
    CLAUDE = "claude"
    GPT4 = "gpt4"
    GEMINI = "gemini"
    LOCAL = "local"

@dataclass
class LLMCircuitBreakerConfig:
    provider: LLMProvider
    fail_max: int = 5
    reset_timeout: int = 60
    success_threshold: int = 2

class LLMCircuitBreakerManager:
    """Manage circuit breakers for all LLM providers"""

    def __init__(self):
        self.breakers: Dict[LLMProvider, pybreaker.CircuitBreaker] = {}
        self.fallback_order = [
            LLMProvider.CLAUDE,
            LLMProvider.GPT4,
            LLMProvider.GEMINI,
            LLMProvider.LOCAL
        ]

    def register_provider(self, config: LLMCircuitBreakerConfig):
        """Register circuit breaker for provider"""
        breaker = pybreaker.CircuitBreaker(
            name=config.provider.value,
            fail_max=config.fail_max,
            reset_timeout=config.reset_timeout,
            success_threshold=config.success_threshold,
            listeners=[LLMCircuitBreakerListener()]
        )
        self.breakers[config.provider] = breaker

    def call_with_fallback(
        self,
        provider_calls: Dict[LLMProvider, Callable[[], Any]]
    ) -> Any:
        """Call LLM with automatic fallback to other providers"""
        for provider in self.fallback_order:
            if provider not in provider_calls:
                continue

            breaker = self.breakers.get(provider)
            if not breaker:
                continue

            try:
                return breaker.call(provider_calls[provider])
            except pybreaker.CircuitBreakerError:
                continue
            except Exception:
                continue

        raise Exception("All LLM providers unavailable")

# Global manager instance
llm_circuit_manager = LLMCircuitBreakerManager()

# Register providers
llm_circuit_manager.register_provider(
    LLMCircuitBreakerConfig(provider=LLMProvider.CLAUDE)
)
llm_circuit_manager.register_provider(
    LLMCircuitBreakerConfig(provider=LLMProvider.GPT4)
)
```

---

## 4. Distributed State Management

### 4.1 Overview

Distributed state management is the #1 challenge for agentic AI systems. Multiple agents accessing shared state create race conditions, conflicts, and consistency issues. Solutions range from distributed locks to event sourcing to CRDTs.

### 4.2 Architecture Patterns

#### Pattern 1: Redis Distributed Locks (Redlock Algorithm)

**Use Case:** Mutual exclusion for critical sections across distributed agents

**Architecture:**
- Acquire locks across N Redis masters (typically 5)
- Lock considered acquired if majority (N/2+1) succeed
- Automatic expiration prevents deadlocks

**Implementation with python-redis-lock:**

```python
import redis
import redis_lock
from contextlib import contextmanager
from typing import Optional
import time

# Redis connection pool
redis_client = redis.Redis(
    host='localhost',
    port=6379,
    db=0,
    decode_responses=True
)

@contextmanager
def agent_lock(resource: str, timeout: int = 10, auto_renewal: bool = True):
    """
    Distributed lock for agent coordination

    Args:
        resource: Resource identifier (e.g., "booking:123")
        timeout: Lock expiration in seconds
        auto_renewal: Automatically renew lock while held
    """
    lock = redis_lock.Lock(
        redis_client,
        name=f"lock:{resource}",
        expire=timeout,
        auto_renewal=auto_renewal
    )

    try:
        # Try to acquire lock with timeout
        if lock.acquire(blocking=True, timeout=timeout):
            yield lock
        else:
            raise Exception(f"Failed to acquire lock for {resource}")
    finally:
        # Always release lock
        try:
            lock.release()
        except:
            pass  # Lock may have expired

# Usage in agent
def agent_update_booking(booking_id: str, updates: dict):
    """Update booking with distributed lock"""
    with agent_lock(f"booking:{booking_id}", timeout=30):
        # Critical section - only one agent at a time
        booking = fetch_booking(booking_id)
        booking.update(updates)
        save_booking(booking)

# Pattern: Lock with retry
def agent_with_retry(resource: str, max_attempts: int = 3):
    """Retry lock acquisition with exponential backoff"""
    for attempt in range(max_attempts):
        try:
            with agent_lock(resource, timeout=10):
                # Perform critical operation
                perform_operation(resource)
                return True
        except Exception as e:
            if attempt < max_attempts - 1:
                # Exponential backoff
                wait_time = 2 ** attempt
                time.sleep(wait_time)
            else:
                raise e
    return False
```

**Advanced: Redlock with Multiple Redis Instances**

```python
from redlock import Redlock

# Connect to multiple Redis instances for fault tolerance
redlock = Redlock([
    {"host": "redis1.example.com", "port": 6379, "db": 0},
    {"host": "redis2.example.com", "port": 6379, "db": 0},
    {"host": "redis3.example.com", "port": 6379, "db": 0},
    {"host": "redis4.example.com", "port": 6379, "db": 0},
    {"host": "redis5.example.com", "port": 6379, "db": 0},
])

def distributed_agent_operation(resource_id: str):
    """Operation protected by Redlock algorithm"""
    # Try to acquire lock across majority of Redis instances
    lock = redlock.lock(f"resource:{resource_id}", 10000)  # 10 second TTL

    if lock:
        try:
            # Critical section
            perform_operation(resource_id)
        finally:
            # Release lock across all instances
            redlock.unlock(lock)
    else:
        raise Exception(f"Could not acquire distributed lock for {resource_id}")
```

**Strengths:**
- ✅ Prevents race conditions in distributed systems
- ✅ Automatic deadlock prevention via expiration
- ✅ Fault-tolerant with multiple Redis instances
- ✅ Simple API with context managers

**Weaknesses:**
- ❌ Not suitable for long-held locks (use workflow orchestration instead)
- ❌ Clock drift can cause issues
- ❌ Network partitions reduce availability
- ❌ Requires Redis infrastructure

**Best For:** Short-duration mutual exclusion (< 30 seconds), preventing double-booking, coordinating agent access to shared resources

---

#### Pattern 2: Event Sourcing with Immutable Log

**Use Case:** Consistent state across agents via append-only event log

**Architecture:**
- All state changes recorded as events
- Events are immutable and ordered
- Agents replay events to reconstruct state
- No conflicting writes - events always append

**Implementation:**

```python
from dataclasses import dataclass, asdict
from datetime import datetime
from typing import List, Dict, Any, Optional
import json
import uuid

@dataclass
class Event:
    """Base event class"""
    event_id: str
    event_type: str
    aggregate_id: str  # Resource this event applies to
    timestamp: datetime
    data: Dict[str, Any]
    agent_id: Optional[str] = None
    version: int = 1

class EventStore:
    """Persistent event storage"""

    def __init__(self, redis_client):
        self.redis = redis_client

    def append(self, event: Event) -> bool:
        """Append event to log (atomic operation)"""
        key = f"events:{event.aggregate_id}"
        event_json = json.dumps(asdict(event), default=str)

        # Use Redis LIST for append-only log
        self.redis.rpush(key, event_json)

        # Also add to global event stream
        self.redis.rpush("events:all", event_json)

        return True

    def get_events(
        self,
        aggregate_id: str,
        since_version: int = 0
    ) -> List[Event]:
        """Retrieve events for aggregate"""
        key = f"events:{aggregate_id}"
        events_json = self.redis.lrange(key, since_version, -1)

        events = []
        for event_json in events_json:
            event_data = json.loads(event_json)
            event_data['timestamp'] = datetime.fromisoformat(event_data['timestamp'])
            events.append(Event(**event_data))

        return events

    def get_all_events_since(self, timestamp: datetime) -> List[Event]:
        """Get all events since timestamp (for synchronization)"""
        all_events = self.redis.lrange("events:all", 0, -1)

        events = []
        for event_json in all_events:
            event_data = json.loads(event_json)
            event_time = datetime.fromisoformat(event_data['timestamp'])

            if event_time >= timestamp:
                event_data['timestamp'] = event_time
                events.append(Event(**event_data))

        return events

class BookingAggregate:
    """Example aggregate with event sourcing"""

    def __init__(self, booking_id: str, event_store: EventStore):
        self.booking_id = booking_id
        self.event_store = event_store
        self.version = 0

        # Current state (rebuilt from events)
        self.status = "pending"
        self.customer_id = None
        self.tour_id = None
        self.participants = 0

        # Rebuild state from events
        self._replay_events()

    def _replay_events(self):
        """Rebuild state from event log"""
        events = self.event_store.get_events(self.booking_id)

        for event in events:
            self._apply_event(event)
            self.version = event.version

    def _apply_event(self, event: Event):
        """Apply event to update state"""
        if event.event_type == "booking_created":
            self.customer_id = event.data['customer_id']
            self.tour_id = event.data['tour_id']
            self.participants = event.data['participants']
            self.status = "pending"

        elif event.event_type == "booking_confirmed":
            self.status = "confirmed"

        elif event.event_type == "booking_cancelled":
            self.status = "cancelled"

        elif event.event_type == "participants_updated":
            self.participants = event.data['new_count']

    def create_booking(self, customer_id: str, tour_id: str, participants: int):
        """Create booking by appending event"""
        event = Event(
            event_id=str(uuid.uuid4()),
            event_type="booking_created",
            aggregate_id=self.booking_id,
            timestamp=datetime.now(),
            data={
                "customer_id": customer_id,
                "tour_id": tour_id,
                "participants": participants
            },
            version=self.version + 1
        )

        self.event_store.append(event)
        self._apply_event(event)
        self.version = event.version

    def confirm_booking(self):
        """Confirm booking by appending event"""
        if self.status != "pending":
            raise Exception(f"Cannot confirm booking in status: {self.status}")

        event = Event(
            event_id=str(uuid.uuid4()),
            event_type="booking_confirmed",
            aggregate_id=self.booking_id,
            timestamp=datetime.now(),
            data={},
            version=self.version + 1
        )

        self.event_store.append(event)
        self._apply_event(event)
        self.version = event.version

# Agent usage
def agent_confirm_booking(booking_id: str, event_store: EventStore):
    """Agent confirms booking using event sourcing"""
    booking = BookingAggregate(booking_id, event_store)
    booking.confirm_booking()  # Appends event, updates state

# Multiple agents can safely append events concurrently
# No locks needed - events are immutable and append-only
```

**Event-Driven Agent Coordination:**

```python
class AgentCoordinator:
    """Coordinate agents via event subscriptions"""

    def __init__(self, event_store: EventStore):
        self.event_store = event_store
        self.subscribers: Dict[str, List[callable]] = {}
        self.last_processed_timestamp = datetime.now()

    def subscribe(self, event_type: str, handler: callable):
        """Register handler for event type"""
        if event_type not in self.subscribers:
            self.subscribers[event_type] = []
        self.subscribers[event_type].append(handler)

    async def poll_and_dispatch(self):
        """Poll for new events and dispatch to subscribers"""
        while True:
            # Get new events since last poll
            new_events = self.event_store.get_all_events_since(
                self.last_processed_timestamp
            )

            # Dispatch to subscribers
            for event in new_events:
                if event.event_type in self.subscribers:
                    for handler in self.subscribers[event.event_type]:
                        await handler(event)

                self.last_processed_timestamp = event.timestamp

            # Poll interval
            await asyncio.sleep(1)

# Agent subscribes to events
coordinator = AgentCoordinator(event_store)

async def handle_booking_confirmed(event: Event):
    """Agent reacts to booking confirmation"""
    booking_id = event.aggregate_id
    # Send confirmation email, update calendar, etc.
    await send_confirmation_email(booking_id)

coordinator.subscribe("booking_confirmed", handle_booking_confirmed)

# Start event dispatcher
await coordinator.poll_and_dispatch()
```

**Strengths:**
- ✅ Complete audit trail of all changes
- ✅ No conflicting writes (append-only)
- ✅ Time-travel debugging (replay to any point)
- ✅ Event-driven agent coordination

**Weaknesses:**
- ❌ More complex than CRUD
- ❌ Eventual consistency model
- ❌ Storage grows over time (requires snapshotting)
- ❌ Query performance requires projections

**Best For:** Audit-critical systems, complex domain logic, event-driven agent coordination

---

#### Pattern 3: Conflict-Free Replicated Data Types (CRDTs)

**Use Case:** Collaborative state updates without coordination

**Architecture:**
- Data structures designed to merge automatically
- No locks or coordination required
- Commutative operations guarantee consistency

**Implementation:**

```python
from typing import Dict, Set, Any
from dataclasses import dataclass
from datetime import datetime

# CRDT: Last-Write-Wins Register (LWW-Register)
@dataclass
class LWWRegister:
    """Last-write-wins register CRDT"""
    value: Any
    timestamp: datetime
    agent_id: str

    def update(self, new_value: Any, agent_id: str):
        """Update value with timestamp"""
        new_timestamp = datetime.now()

        # Only update if newer (or use agent_id as tiebreaker)
        if new_timestamp > self.timestamp or \
           (new_timestamp == self.timestamp and agent_id > self.agent_id):
            self.value = new_value
            self.timestamp = new_timestamp
            self.agent_id = agent_id

    def merge(self, other: 'LWWRegister'):
        """Merge with another replica"""
        if other.timestamp > self.timestamp or \
           (other.timestamp == self.timestamp and other.agent_id > self.agent_id):
            self.value = other.value
            self.timestamp = other.timestamp
            self.agent_id = other.agent_id

# CRDT: Grow-Only Set (G-Set)
class GSet:
    """Grow-only set CRDT (elements can only be added)"""

    def __init__(self):
        self.elements: Set[Any] = set()

    def add(self, element: Any):
        """Add element to set"""
        self.elements.add(element)

    def contains(self, element: Any) -> bool:
        """Check if element in set"""
        return element in self.elements

    def merge(self, other: 'GSet'):
        """Merge with another replica (union)"""
        self.elements = self.elements.union(other.elements)

# CRDT: Observed-Remove Set (OR-Set)
@dataclass
class ORElement:
    value: Any
    unique_id: str  # Unique tag for each add operation

    def __hash__(self):
        return hash((self.value, self.unique_id))

class ORSet:
    """Observed-remove set CRDT (add and remove)"""

    def __init__(self):
        self.elements: Set[ORElement] = set()
        self.tombstones: Set[str] = set()  # Removed unique IDs

    def add(self, value: Any) -> str:
        """Add element with unique tag"""
        unique_id = f"{value}:{uuid.uuid4()}"
        element = ORElement(value, unique_id)
        self.elements.add(element)
        return unique_id

    def remove(self, value: Any):
        """Remove all instances of value"""
        to_remove = [e for e in self.elements if e.value == value]
        for element in to_remove:
            self.tombstones.add(element.unique_id)
            self.elements.discard(element)

    def contains(self, value: Any) -> bool:
        """Check if value exists"""
        return any(e.value == value for e in self.elements)

    def merge(self, other: 'ORSet'):
        """Merge with another replica"""
        # Union of elements
        self.elements = self.elements.union(other.elements)

        # Union of tombstones
        self.tombstones = self.tombstones.union(other.tombstones)

        # Remove tombstoned elements
        self.elements = {
            e for e in self.elements
            if e.unique_id not in self.tombstones
        }

# CRDT: Counter (G-Counter and PN-Counter)
class GCounter:
    """Grow-only counter CRDT"""

    def __init__(self, agent_id: str):
        self.agent_id = agent_id
        self.counts: Dict[str, int] = {agent_id: 0}

    def increment(self, amount: int = 1):
        """Increment counter"""
        self.counts[self.agent_id] = self.counts.get(self.agent_id, 0) + amount

    def value(self) -> int:
        """Get current counter value"""
        return sum(self.counts.values())

    def merge(self, other: 'GCounter'):
        """Merge with another replica (take max per agent)"""
        for agent_id, count in other.counts.items():
            self.counts[agent_id] = max(
                self.counts.get(agent_id, 0),
                count
            )

class PNCounter:
    """Positive-negative counter CRDT (increment and decrement)"""

    def __init__(self, agent_id: str):
        self.agent_id = agent_id
        self.positive = GCounter(agent_id)
        self.negative = GCounter(agent_id)

    def increment(self, amount: int = 1):
        """Increment counter"""
        self.positive.increment(amount)

    def decrement(self, amount: int = 1):
        """Decrement counter"""
        self.negative.increment(amount)

    def value(self) -> int:
        """Get current counter value"""
        return self.positive.value() - self.negative.value()

    def merge(self, other: 'PNCounter'):
        """Merge with another replica"""
        self.positive.merge(other.positive)
        self.negative.merge(other.negative)

# Example: Multi-agent collaborative document
class CollaborativeAgentState:
    """Agent state using CRDTs for conflict-free collaboration"""

    def __init__(self, agent_id: str):
        self.agent_id = agent_id

        # Agent status (LWW-Register)
        self.status = LWWRegister("idle", datetime.now(), agent_id)

        # Tasks assigned to agent (OR-Set)
        self.assigned_tasks = ORSet()

        # Completed task count (G-Counter)
        self.completed_count = GCounter(agent_id)

        # Active connections (PN-Counter)
        self.active_connections = PNCounter(agent_id)

    def update_status(self, new_status: str):
        """Update agent status"""
        self.status.update(new_status, self.agent_id)

    def assign_task(self, task_id: str):
        """Assign task to agent"""
        self.assigned_tasks.add(task_id)

    def complete_task(self, task_id: str):
        """Mark task as completed"""
        self.assigned_tasks.remove(task_id)
        self.completed_count.increment()

    def connect(self):
        """Agent connected"""
        self.active_connections.increment()

    def disconnect(self):
        """Agent disconnected"""
        self.active_connections.decrement()

    def merge(self, other: 'CollaborativeAgentState'):
        """Merge state from another agent replica"""
        self.status.merge(other.status)
        self.assigned_tasks.merge(other.assigned_tasks)
        self.completed_count.merge(other.completed_count)
        self.active_connections.merge(other.active_connections)

# Usage: Agents synchronize state without coordination
agent1 = CollaborativeAgentState("agent1")
agent2 = CollaborativeAgentState("agent2")

# Agent 1 updates
agent1.assign_task("task-123")
agent1.update_status("working")
agent1.connect()

# Agent 2 updates
agent2.assign_task("task-456")
agent2.update_status("working")
agent2.connect()

# Synchronize (no conflicts!)
agent1.merge(agent2)
agent2.merge(agent1)

# Both agents now have consistent state
assert agent1.assigned_tasks.contains("task-123")
assert agent1.assigned_tasks.contains("task-456")
assert agent2.assigned_tasks.contains("task-123")
assert agent2.assigned_tasks.contains("task-456")
```

**Strengths:**
- ✅ No coordination required
- ✅ Automatic conflict resolution
- ✅ Works offline (synchronize later)
- ✅ High availability

**Weaknesses:**
- ❌ Limited data structures
- ❌ Can grow unbounded (requires garbage collection)
- ❌ Complex semantics for some operations
- ❌ Not suitable for all use cases

**Best For:** Collaborative editing, distributed counters, eventually-consistent systems

---

### 4.3 Comparison Matrix

| Pattern | Consistency | Coordination | Latency | Complexity | Best For |
|---------|-------------|--------------|---------|------------|----------|
| **Distributed Locks** | Strong | Required | Low | Low | Mutual exclusion |
| **Event Sourcing** | Eventual | Append-only | Medium | High | Audit trails |
| **CRDTs** | Eventual | None | Very Low | Medium | Collaborative editing |

### 4.4 Recommendations for .claude Framework

**Immediate Actions:**
1. ✅ Implement **Redis distributed locks** for critical sections
2. ✅ Use **event sourcing** for agent workflow history
3. ✅ Add **CRDTs** for collaborative agent state (task lists, counters)

**Sample Integration:**

```python
# .claude/framework/state_management.py

from typing import Optional, Dict, Any
from contextlib import contextmanager
import redis
import redis_lock

class ClaudeStateManager:
    """Distributed state management for .claude agents"""

    def __init__(self, redis_url: str = "redis://localhost:6379"):
        self.redis = redis.from_url(redis_url, decode_responses=True)
        self.event_store = EventStore(self.redis)

    @contextmanager
    def exclusive_access(self, resource: str, timeout: int = 30):
        """Acquire exclusive access to resource"""
        lock = redis_lock.Lock(
            self.redis,
            name=f"lock:claude:{resource}",
            expire=timeout,
            auto_renewal=True
        )

        try:
            if lock.acquire(blocking=True, timeout=timeout):
                yield lock
            else:
                raise Exception(f"Could not acquire lock for {resource}")
        finally:
            try:
                lock.release()
            except:
                pass

    def append_event(self, event: Event):
        """Append event to agent event log"""
        self.event_store.append(event)

    def get_agent_state(self, agent_id: str) -> Dict[str, Any]:
        """Get current agent state (rebuilt from events)"""
        events = self.event_store.get_events(agent_id)
        # Rebuild state from events
        return rebuild_state(events)

# Global state manager
state_manager = ClaudeStateManager()

# Usage in agent
def agent_execute_task(task_id: str):
    """Execute task with distributed state management"""
    with state_manager.exclusive_access(f"task:{task_id}"):
        # Critical section - only one agent at a time
        task = fetch_task(task_id)
        result = execute_task(task)
        save_result(result)

        # Append event to audit log
        state_manager.append_event(Event(
            event_id=str(uuid.uuid4()),
            event_type="task_completed",
            aggregate_id=task_id,
            timestamp=datetime.now(),
            data={"result": result}
        ))
```

---

## 5. Observability for AI Agents

### 5.1 Overview

Observability enables understanding of complex multi-agent system behavior through instrumentation, metrics collection, distributed tracing, and log aggregation. Critical for debugging, performance tuning, and production monitoring.

### 5.2 Architecture Patterns

#### Pattern 1: OpenTelemetry Tracing for LLM Applications

**Architecture:**
- Instrumentation SDK captures traces and spans
- Exporters send data to observability backends
- Distributed context propagation links related operations

**Implementation with OpenLLMetry:**

```bash
pip install traceloop-sdk
```

**Basic Setup:**

```python
from traceloop.sdk import Traceloop
from opentelemetry import trace
from anthropic import Anthropic

# Initialize OpenLLMetry (auto-instruments LLM libraries)
Traceloop.init(
    app_name="claude-multi-agent",
    disable_batch=False,  # Enable batching for production
    api_endpoint="https://your-observability-backend.com"
)

# Get tracer
tracer = trace.get_tracer(__name__)

# Instrument agent execution
def execute_agent(agent_name: str, task: dict):
    """Execute agent with automatic tracing"""
    with tracer.start_as_current_span(
        name=f"agent.{agent_name}.execute",
        attributes={
            "agent.name": agent_name,
            "agent.task_id": task['id'],
            "agent.task_type": task['type']
        }
    ) as span:
        try:
            # Agent logic (auto-instrumented by OpenLLMetry)
            client = Anthropic()
            response = client.messages.create(
                model="claude-3-sonnet-20240229",
                max_tokens=1024,
                messages=[{"role": "user", "content": task['prompt']}]
            )

            # Add custom metrics to span
            span.set_attribute("agent.tokens_used", response.usage.total_tokens)
            span.set_attribute("agent.status", "success")

            return response.content[0].text

        except Exception as e:
            # Record exception in span
            span.set_attribute("agent.status", "failed")
            span.record_exception(e)
            raise

# Multi-agent workflow tracing
def multi_agent_workflow(task: dict):
    """Trace entire workflow across multiple agents"""
    with tracer.start_as_current_span("workflow.multi_agent") as workflow_span:
        workflow_span.set_attribute("workflow.task_id", task['id'])

        # Agent 1: Research
        research_results = execute_agent("researcher", {
            **task,
            "prompt": "Research the topic"
        })

        # Agent 2: Analysis
        analysis_results = execute_agent("analyst", {
            **task,
            "prompt": f"Analyze these findings: {research_results}"
        })

        # Agent 3: Synthesis
        final_report = execute_agent("synthesizer", {
            **task,
            "prompt": f"Synthesize analysis into report: {analysis_results}"
        })

        workflow_span.set_attribute("workflow.status", "completed")

        return final_report
```

**Advanced: Custom Instrumentation**

```python
from opentelemetry import trace, metrics
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.metrics import MeterProvider
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
from opentelemetry.exporter.otlp.proto.grpc.metric_exporter import OTLPMetricExporter
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.sdk.metrics.export import PeriodicExportingMetricReader

# Setup custom tracing
trace.set_tracer_provider(TracerProvider())
trace.get_tracer_provider().add_span_processor(
    BatchSpanProcessor(OTLPSpanExporter(endpoint="localhost:4317"))
)

# Setup metrics
metrics.set_meter_provider(MeterProvider(
    metric_readers=[PeriodicExportingMetricReader(
        OTLPMetricExporter(endpoint="localhost:4317")
    )]
))

# Create meter for custom metrics
meter = metrics.get_meter(__name__)

# Define metrics
agent_execution_counter = meter.create_counter(
    name="agent.executions",
    description="Number of agent executions",
    unit="1"
)

agent_duration_histogram = meter.create_histogram(
    name="agent.duration",
    description="Agent execution duration",
    unit="ms"
)

agent_token_usage_counter = meter.create_counter(
    name="agent.tokens",
    description="Total tokens used",
    unit="tokens"
)

# Instrument agent with custom metrics
import time

def instrumented_agent_execution(agent_name: str, task: dict):
    """Agent execution with custom metrics"""
    start_time = time.time()

    with tracer.start_as_current_span(f"agent.{agent_name}") as span:
        try:
            result = execute_agent_logic(task)

            # Record metrics
            duration_ms = (time.time() - start_time) * 1000

            agent_execution_counter.add(1, {
                "agent.name": agent_name,
                "agent.status": "success"
            })

            agent_duration_histogram.record(duration_ms, {
                "agent.name": agent_name
            })

            agent_token_usage_counter.add(result['tokens_used'], {
                "agent.name": agent_name,
                "model": result['model']
            })

            return result

        except Exception as e:
            agent_execution_counter.add(1, {
                "agent.name": agent_name,
                "agent.status": "failed"
            })
            raise
```

**Context Propagation Across Agents:**

```python
from opentelemetry.propagate import inject, extract
from opentelemetry.trace.propagation.tracecontext import TraceContextTextMapPropagator

propagator = TraceContextTextMapPropagator()

# Agent 1: Create span and propagate context
def agent1_executes():
    with tracer.start_as_current_span("agent1") as span:
        # Inject trace context into carrier (e.g., message headers)
        carrier = {}
        propagator.inject(carrier)

        # Send message to Agent 2 with trace context
        send_message_to_agent2({"data": "...", "trace_context": carrier})

# Agent 2: Extract context and continue trace
def agent2_executes(message: dict):
    # Extract trace context from message
    carrier = message.get("trace_context", {})
    context = propagator.extract(carrier)

    # Continue trace from Agent 1's span
    with tracer.start_as_current_span("agent2", context=context) as span:
        # Agent 2 logic
        pass
```

---

#### Pattern 2: Agent-Specific Metrics & Monitoring

**Key Metrics for Multi-Agent Systems:**

```python
from dataclasses import dataclass
from typing import Dict, List
from datetime import datetime, timedelta
import time

@dataclass
class AgentMetrics:
    """Comprehensive agent metrics"""

    # Performance
    total_executions: int = 0
    successful_executions: int = 0
    failed_executions: int = 0
    average_latency_ms: float = 0.0
    p95_latency_ms: float = 0.0
    p99_latency_ms: float = 0.0

    # Resource Usage
    total_tokens_used: int = 0
    total_cost_usd: float = 0.0
    avg_tokens_per_request: float = 0.0

    # Quality
    average_confidence_score: float = 0.0
    retry_rate: float = 0.0
    timeout_rate: float = 0.0

    # Collaboration
    messages_sent: int = 0
    messages_received: int = 0
    delegations_made: int = 0
    delegations_received: int = 0

class AgentMonitor:
    """Monitor agent performance and behavior"""

    def __init__(self, agent_id: str):
        self.agent_id = agent_id
        self.metrics = AgentMetrics()
        self.latency_samples: List[float] = []
        self.start_times: Dict[str, float] = {}

    def start_execution(self, execution_id: str):
        """Track execution start"""
        self.start_times[execution_id] = time.time()

    def end_execution(
        self,
        execution_id: str,
        success: bool,
        tokens_used: int = 0,
        cost_usd: float = 0.0
    ):
        """Track execution completion"""
        if execution_id not in self.start_times:
            return

        # Calculate latency
        latency_ms = (time.time() - self.start_times[execution_id]) * 1000
        self.latency_samples.append(latency_ms)
        del self.start_times[execution_id]

        # Update metrics
        self.metrics.total_executions += 1
        if success:
            self.metrics.successful_executions += 1
        else:
            self.metrics.failed_executions += 1

        self.metrics.total_tokens_used += tokens_used
        self.metrics.total_cost_usd += cost_usd

        # Calculate averages
        if self.metrics.total_executions > 0:
            self.metrics.average_latency_ms = sum(self.latency_samples) / len(self.latency_samples)
            self.metrics.avg_tokens_per_request = self.metrics.total_tokens_used / self.metrics.total_executions

        # Calculate percentiles
        if len(self.latency_samples) >= 20:
            sorted_latencies = sorted(self.latency_samples)
            self.metrics.p95_latency_ms = sorted_latencies[int(len(sorted_latencies) * 0.95)]
            self.metrics.p99_latency_ms = sorted_latencies[int(len(sorted_latencies) * 0.99)]

    def record_delegation(self, to_agent: str):
        """Track delegation to another agent"""
        self.metrics.delegations_made += 1

    def record_message(self, direction: str):
        """Track inter-agent message"""
        if direction == "sent":
            self.metrics.messages_sent += 1
        else:
            self.metrics.messages_received += 1

    def get_dashboard_data(self) -> dict:
        """Export metrics for dashboard"""
        return {
            "agent_id": self.agent_id,
            "performance": {
                "success_rate": self.metrics.successful_executions / max(self.metrics.total_executions, 1),
                "avg_latency_ms": self.metrics.average_latency_ms,
                "p95_latency_ms": self.metrics.p95_latency_ms,
                "p99_latency_ms": self.metrics.p99_latency_ms
            },
            "resource_usage": {
                "total_tokens": self.metrics.total_tokens_used,
                "total_cost_usd": self.metrics.total_cost_usd,
                "avg_tokens_per_request": self.metrics.avg_tokens_per_request
            },
            "collaboration": {
                "messages_sent": self.metrics.messages_sent,
                "messages_received": self.metrics.messages_received,
                "delegations_made": self.metrics.delegations_made
            }
        }

# Usage in agent
monitor = AgentMonitor("research_agent")

def agent_execute(task: dict):
    execution_id = str(uuid.uuid4())
    monitor.start_execution(execution_id)

    try:
        result = perform_task(task)
        monitor.end_execution(
            execution_id,
            success=True,
            tokens_used=result['tokens'],
            cost_usd=result['cost']
        )
        return result
    except Exception as e:
        monitor.end_execution(execution_id, success=False)
        raise

# Export metrics periodically
import asyncio

async def export_metrics_loop():
    while True:
        dashboard_data = monitor.get_dashboard_data()
        send_to_monitoring_backend(dashboard_data)
        await asyncio.sleep(60)  # Every minute
```

---

#### Pattern 3: Distributed Tracing for Multi-Agent Systems

**Unified Trace Across Agents:**

```python
from opentelemetry import trace
from opentelemetry.propagate import inject, extract
from typing import Dict, Any
import json

class MultiAgentTracer:
    """Distributed tracing for multi-agent workflows"""

    def __init__(self):
        self.tracer = trace.get_tracer(__name__)

    def start_workflow(self, workflow_id: str, workflow_type: str) -> Dict[str, Any]:
        """Start workflow and return trace context"""
        span = self.tracer.start_span(
            name=f"workflow.{workflow_type}",
            attributes={
                "workflow.id": workflow_id,
                "workflow.type": workflow_type
            }
        )

        # Inject context for propagation
        context = {}
        inject(context)

        return {
            "span": span,
            "trace_context": context
        }

    def agent_step(
        self,
        agent_name: str,
        step_name: str,
        parent_context: Dict[str, Any]
    ):
        """Create span for agent step"""
        # Extract parent context
        ctx = extract(parent_context)

        # Create child span
        span = self.tracer.start_span(
            name=f"agent.{agent_name}.{step_name}",
            context=ctx,
            attributes={
                "agent.name": agent_name,
                "agent.step": step_name
            }
        )

        return span

    def llm_call(self, span, model: str, prompt: str, response: str, tokens: int):
        """Add LLM call details to span"""
        span.set_attribute("llm.model", model)
        span.set_attribute("llm.prompt_length", len(prompt))
        span.set_attribute("llm.response_length", len(response))
        span.set_attribute("llm.tokens", tokens)

    def record_error(self, span, error: Exception):
        """Record error in span"""
        span.set_attribute("error", True)
        span.set_attribute("error.type", type(error).__name__)
        span.set_attribute("error.message", str(error))
        span.record_exception(error)

# Usage in multi-agent workflow
tracer = MultiAgentTracer()

def multi_agent_research_workflow(query: str):
    """Research workflow with distributed tracing"""
    workflow_id = str(uuid.uuid4())
    workflow_ctx = tracer.start_workflow(workflow_id, "research")

    try:
        # Agent 1: Search
        with tracer.agent_step("searcher", "search", workflow_ctx["trace_context"]) as span:
            search_results = search_agent(query)
            span.set_attribute("results.count", len(search_results))

        # Agent 2: Analyze (parallel)
        analysis_results = []
        for idx, result in enumerate(search_results):
            with tracer.agent_step("analyzer", f"analyze_{idx}", workflow_ctx["trace_context"]) as span:
                analysis = analyze_agent(result)
                analysis_results.append(analysis)
                span.set_attribute("analysis.confidence", analysis['confidence'])

        # Agent 3: Synthesize
        with tracer.agent_step("synthesizer", "synthesize", workflow_ctx["trace_context"]) as span:
            final_report = synthesize_agent(analysis_results)
            span.set_attribute("report.length", len(final_report))

        workflow_ctx["span"].set_attribute("workflow.status", "completed")
        return final_report

    except Exception as e:
        tracer.record_error(workflow_ctx["span"], e)
        raise
    finally:
        workflow_ctx["span"].end()
```

---

### 5.3 Observability Stack Recommendations

**Full Observability Stack:**

```yaml
# docker-compose.yml for local observability stack

version: '3.8'

services:
  # OpenTelemetry Collector
  otel-collector:
    image: otel/opentelemetry-collector:latest
    command: ["--config=/etc/otel-collector-config.yaml"]
    volumes:
      - ./otel-collector-config.yaml:/etc/otel-collector-config.yaml
    ports:
      - "4317:4317"  # OTLP gRPC
      - "4318:4318"  # OTLP HTTP

  # Jaeger for tracing
  jaeger:
    image: jaegertracing/all-in-one:latest
    ports:
      - "16686:16686"  # Jaeger UI
      - "14250:14250"  # gRPC

  # Prometheus for metrics
  prometheus:
    image: prom/prometheus:latest
    volumes:
      - ./prometheus.yml:/etc/prometheus/prometheus.yml
    ports:
      - "9090:9090"

  # Grafana for visualization
  grafana:
    image: grafana/grafana:latest
    ports:
      - "3000:3000"
    environment:
      - GF_SECURITY_ADMIN_PASSWORD=admin

  # Loki for logs
  loki:
    image: grafana/loki:latest
    ports:
      - "3100:3100"
```

**OpenTelemetry Collector Config:**

```yaml
# otel-collector-config.yaml

receivers:
  otlp:
    protocols:
      grpc:
        endpoint: 0.0.0.0:4317
      http:
        endpoint: 0.0.0.0:4318

processors:
  batch:
    timeout: 10s
    send_batch_size: 1024

exporters:
  jaeger:
    endpoint: jaeger:14250
    tls:
      insecure: true

  prometheus:
    endpoint: "0.0.0.0:8889"

  logging:
    loglevel: debug

service:
  pipelines:
    traces:
      receivers: [otlp]
      processors: [batch]
      exporters: [jaeger, logging]

    metrics:
      receivers: [otlp]
      processors: [batch]
      exporters: [prometheus, logging]
```

### 5.4 Recommendations for .claude Framework

**Immediate Actions:**
1. ✅ Install **OpenLLMetry** for automatic LLM instrumentation
2. ✅ Add **custom spans** for agent execution
3. ✅ Implement **AgentMonitor** class for metrics collection
4. ✅ Export metrics to Prometheus/Grafana

**Sample Integration:**

```python
# .claude/framework/observability.py

from traceloop.sdk import Traceloop
from opentelemetry import trace
from typing import Optional
import os

class ClaudeObservability:
    """Observability for .claude framework"""

    def __init__(self):
        # Initialize OpenLLMetry
        Traceloop.init(
            app_name="claude-framework",
            api_endpoint=os.getenv("OTEL_EXPORTER_OTLP_ENDPOINT", "http://localhost:4317"),
            disable_batch=False
        )

        self.tracer = trace.get_tracer("claude.framework")
        self.monitors = {}  # agent_id -> AgentMonitor

    def get_monitor(self, agent_id: str) -> AgentMonitor:
        """Get or create monitor for agent"""
        if agent_id not in self.monitors:
            self.monitors[agent_id] = AgentMonitor(agent_id)
        return self.monitors[agent_id]

    def trace_agent_execution(self, agent_id: str, task: dict):
        """Context manager for tracing agent execution"""
        return self.tracer.start_as_current_span(
            f"agent.{agent_id}.execute",
            attributes={
                "agent.id": agent_id,
                "task.id": task.get('id'),
                "task.type": task.get('type')
            }
        )

# Global observability instance
observability = ClaudeObservability()
```

---

## 6. Recommendations for .claude Framework

### 6.1 Immediate Implementation Priorities

**1. Multi-Agent Communication (High Priority)**
- ✅ Implement graph-based orchestration (LangGraph-inspired)
- ✅ Add message broker for agent-to-agent communication
- ✅ Create shared state schema with Redis backend
- ✅ Build agent coordination primitives (chain, group, chord)

**2. Task Queue & Dependencies (High Priority)**
- ✅ Integrate Celery for async task execution
- ✅ Add celery-tasktree for dependency management
- ✅ Implement task result callbacks
- ✅ Configure Redis as broker and backend

**3. Circuit Breakers (Critical)**
- ✅ Install pybreaker for LLM API protection
- ✅ Create separate breakers per LLM provider
- ✅ Add custom listener for monitoring
- ✅ Implement fallback strategies

**4. State Management (Medium Priority)**
- ✅ Implement Redis distributed locks for critical sections
- ✅ Add event sourcing for agent workflow history
- ✅ Create CRDT-based collaborative state (if needed)

**5. Observability (High Priority)**
- ✅ Install OpenLLMetry for automatic instrumentation
- ✅ Add custom metrics (AgentMonitor class)
- ✅ Implement distributed tracing across agents
- ✅ Setup Prometheus + Grafana stack

### 6.2 Architecture Diagram

```
┌─────────────────────────────────────────────────────────────┐
│                    .claude Framework                        │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  ┌──────────────────────────────────────────────────────┐  │
│  │           Agent Coordination Layer                   │  │
│  │  - Graph-based orchestration (LangGraph-style)       │  │
│  │  - Message broker (Redis Pub/Sub)                    │  │
│  │  - Shared state (Redis)                              │  │
│  └──────────────────────────────────────────────────────┘  │
│                           │                                 │
│  ┌──────────────────────────────────────────────────────┐  │
│  │           Task Queue Layer (Celery)                  │  │
│  │  - Async task execution                              │  │
│  │  - Dependency resolution (celery-tasktree)           │  │
│  │  - Retry logic with backoff                          │  │
│  └──────────────────────────────────────────────────────┘  │
│                           │                                 │
│  ┌──────────────────────────────────────────────────────┐  │
│  │           Resilience Layer                           │  │
│  │  - Circuit breakers (pybreaker) per provider         │  │
│  │  - Retry strategies (tenacity)                       │  │
│  │  - Fallback mechanisms                               │  │
│  └──────────────────────────────────────────────────────┘  │
│                           │                                 │
│  ┌──────────────────────────────────────────────────────┐  │
│  │           State Management Layer                     │  │
│  │  - Distributed locks (Redis Redlock)                 │  │
│  │  - Event sourcing (append-only log)                  │  │
│  │  - CRDTs (for collaborative state)                   │  │
│  └──────────────────────────────────────────────────────┘  │
│                           │                                 │
│  ┌──────────────────────────────────────────────────────┐  │
│  │           Observability Layer                        │  │
│  │  - OpenTelemetry tracing (OpenLLMetry)               │  │
│  │  - Metrics collection (Prometheus)                   │  │
│  │  - Distributed tracing (Jaeger)                      │  │
│  │  - Dashboards (Grafana)                              │  │
│  └──────────────────────────────────────────────────────┘  │
│                                                             │
└─────────────────────────────────────────────────────────────┘
                            │
                            ↓
┌─────────────────────────────────────────────────────────────┐
│                  External Services                          │
├─────────────────────────────────────────────────────────────┤
│  - LLM APIs (Claude, GPT-4, Gemini)                         │
│  - Redis (state, locks, pub/sub, task queue)                │
│  - Observability Backend (Jaeger, Prometheus, Grafana)      │
└─────────────────────────────────────────────────────────────┘
```

### 6.3 Sample Unified Implementation

```python
# .claude/framework/unified_system.py

from typing import Dict, Any, Callable, Optional, List
from dataclasses import dataclass
from enum import Enum
import asyncio
import redis
from celery import Celery
import pybreaker
from traceloop.sdk import Traceloop
from opentelemetry import trace

# Initialize all subsystems
class ClaudeFramework:
    """Unified multi-agent framework with all best practices"""

    def __init__(self, redis_url: str = "redis://localhost:6379"):
        # Redis client
        self.redis = redis.from_url(redis_url, decode_responses=True)

        # Celery app
        self.celery = Celery(
            'claude_agents',
            broker=redis_url,
            backend=redis_url
        )

        # Circuit breakers
        self.circuit_breakers = {
            "claude": pybreaker.CircuitBreaker(name="claude", fail_max=5, reset_timeout=60),
            "gpt4": pybreaker.CircuitBreaker(name="gpt4", fail_max=5, reset_timeout=60),
            "gemini": pybreaker.CircuitBreaker(name="gemini", fail_max=5, reset_timeout=60)
        }

        # Observability
        Traceloop.init(app_name="claude-framework")
        self.tracer = trace.get_tracer("claude.framework")

        # State management
        self.state_manager = ClaudeStateManager(self.redis)

        # Agent registry
        self.agents: Dict[str, 'Agent'] = {}

    def register_agent(self, agent: 'Agent'):
        """Register agent in framework"""
        self.agents[agent.name] = agent

    def create_workflow(self, workflow_type: str):
        """Create new workflow with tracing"""
        return WorkflowBuilder(self, workflow_type)

    def execute_task(self, task_id: str, agent_name: str, task_data: dict):
        """Execute task with full framework integration"""
        with self.tracer.start_as_current_span(f"task.{task_id}") as span:
            # Get agent
            agent = self.agents.get(agent_name)
            if not agent:
                raise ValueError(f"Agent {agent_name} not found")

            # Acquire lock if needed
            if task_data.get('exclusive'):
                with self.state_manager.exclusive_access(f"task:{task_id}"):
                    result = agent.execute(task_data)
            else:
                result = agent.execute(task_data)

            # Record metrics
            span.set_attribute("task.status", "completed")
            span.set_attribute("task.result_size", len(str(result)))

            return result

@dataclass
class Agent:
    """Agent with framework integration"""
    name: str
    role: str
    llm_provider: str
    framework: ClaudeFramework

    def execute(self, task: dict) -> dict:
        """Execute task with circuit breaker protection"""
        breaker = self.framework.circuit_breakers[self.llm_provider]

        try:
            return breaker.call(self._execute_llm, task)
        except pybreaker.CircuitBreakerError:
            # Fallback to alternative provider
            return self._fallback_execution(task)

    def _execute_llm(self, task: dict) -> dict:
        """LLM execution (auto-instrumented by OpenLLMetry)"""
        # LLM call here
        pass

    def _fallback_execution(self, task: dict) -> dict:
        """Fallback when primary LLM unavailable"""
        # Try alternative providers
        pass

class WorkflowBuilder:
    """Build complex multi-agent workflows"""

    def __init__(self, framework: ClaudeFramework, workflow_type: str):
        self.framework = framework
        self.workflow_type = workflow_type
        self.steps: List[Callable] = []

    def add_agent_step(self, agent_name: str, task_data: dict):
        """Add agent execution step"""
        def step():
            return self.framework.execute_task(
                task_id=str(uuid.uuid4()),
                agent_name=agent_name,
                task_data=task_data
            )
        self.steps.append(step)
        return self

    def add_parallel_steps(self, agent_tasks: List[tuple]):
        """Add parallel agent execution"""
        def parallel_step():
            from celery import group
            job = group(
                self.framework.celery.send_task(
                    'execute_agent',
                    args=(agent_name, task_data)
                )
                for agent_name, task_data in agent_tasks
            )
            return job.apply_async().get()

        self.steps.append(parallel_step)
        return self

    async def execute(self):
        """Execute workflow"""
        with self.framework.tracer.start_as_current_span(f"workflow.{self.workflow_type}"):
            results = []
            for step in self.steps:
                result = await step() if asyncio.iscoroutinefunction(step) else step()
                results.append(result)
            return results

# Usage example
framework = ClaudeFramework()

# Register agents
researcher = Agent("researcher", "Research Specialist", "claude", framework)
analyst = Agent("analyst", "Data Analyst", "gpt4", framework)
writer = Agent("writer", "Technical Writer", "gemini", framework)

framework.register_agent(researcher)
framework.register_agent(analyst)
framework.register_agent(writer)

# Build workflow
workflow = (
    framework.create_workflow("research_pipeline")
    .add_agent_step("researcher", {"query": "AI trends"})
    .add_agent_step("analyst", {"action": "analyze"})
    .add_agent_step("writer", {"action": "synthesize"})
)

# Execute
result = asyncio.run(workflow.execute())
```

### 6.4 Migration Path

**Phase 1 (Week 1-2): Foundation**
1. Setup Redis infrastructure
2. Install and configure Celery
3. Add circuit breakers for existing LLM calls
4. Basic observability with OpenLLMetry

**Phase 2 (Week 3-4): Agent Coordination**
1. Implement message broker
2. Create shared state schema
3. Build graph-based orchestration
4. Add distributed locks for critical sections

**Phase 3 (Week 5-6): Advanced Features**
1. Event sourcing for workflow history
2. CRDTs for collaborative state (if needed)
3. Advanced metrics and dashboards
4. Performance optimization

**Phase 4 (Week 7-8): Production Readiness**
1. Load testing and tuning
2. Monitoring and alerting setup
3. Documentation and runbooks
4. Disaster recovery procedures

---

## 7. Conclusion

This comprehensive research covers five critical domains for production multi-agent AI systems:

**✅ Multi-Agent Communication**: Implement graph-based orchestration (LangGraph), role-based delegation (CrewAI), or conversational messaging (AutoGen) based on complexity needs.

**✅ Distributed Task Queue**: Use Temporal for durable workflows, Airflow for scheduled DAGs, or Celery for simple async tasks.

**✅ Circuit Breakers**: Integrate pybreaker for all LLM API calls with per-provider breakers and graceful fallback strategies.

**✅ State Management**: Employ Redis distributed locks for mutual exclusion, event sourcing for audit trails, and CRDTs for collaborative editing.

**✅ Observability**: Deploy OpenTelemetry tracing with OpenLLMetry, custom metrics via AgentMonitor, and distributed tracing across agents.

### Key Insights

1. **No Silver Bullet**: Each pattern solves specific problems - choose based on requirements
2. **Start Simple**: Begin with Celery + pybreaker + OpenLLMetry, evolve to Temporal/LangGraph as complexity grows
3. **Observability First**: Instrument from day one - impossible to debug without traces
4. **State is Hard**: Distributed state management is the #1 challenge - invest time upfront
5. **Resilience Matters**: LLMs will fail - circuit breakers and retries are non-negotiable

### Next Steps for .claude Framework

1. Review this document with engineering team
2. Prioritize features based on current pain points
3. Begin Phase 1 implementation (foundation)
4. Iterate based on real-world usage and feedback

---

**Document prepared by:** Claude Code Research System
**Last updated:** November 13, 2025
**Version:** 1.0.0
