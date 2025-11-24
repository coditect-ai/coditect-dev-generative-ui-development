#!/usr/bin/env python3
"""
Test Framework Knowledge System

Quick test to verify FrameworkKnowledgeLoader and SystemPromptBuilder work correctly.

Author: AZ1.AI INC.
"""

import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from llm_abstractions import (
    get_framework_knowledge,
    SystemPromptBuilder
)


def test_framework_knowledge():
    """Test framework knowledge loader."""
    print("🧪 Testing Framework Knowledge System")
    print("=" * 60)

    # Test 1: Get knowledge instance
    print("\n📖 Test 1: Loading framework knowledge...")
    knowledge = get_framework_knowledge()

    if knowledge.registry:
        print(f"   ✅ Registry loaded successfully")
        print(f"   📊 Agents: {len(knowledge.registry.agents)}")
        print(f"   📊 Skills: {len(knowledge.registry.skills)}")
        print(f"   📊 Commands: {len(knowledge.registry.commands)}")
        print(f"   📊 Scripts: {len(knowledge.registry.scripts)}")
    else:
        print("   ❌ Failed to load registry")
        return False

    # Test 2: Get specific agent metadata
    print("\n📖 Test 2: Getting agent metadata...")
    agent = knowledge.get_agent_metadata("ai-specialist")
    if agent:
        print(f"   ✅ Found agent: {agent.name}")
        print(f"   📝 Description: {agent.description[:80]}...")
    else:
        # Try another agent
        all_agents = knowledge.get_all_agents()
        if all_agents:
            agent = all_agents[0]
            print(f"   ✅ Found agent: {agent.name}")
            print(f"   📝 Description: {agent.description[:80]}...")
        else:
            print("   ❌ No agents found")

    # Test 3: Get component summary
    print("\n📖 Test 3: Getting component summary...")
    summary = knowledge.get_component_summary("all")
    print(f"   ✅ Summary: {summary}")

    # Test 4: Recommend agents
    print("\n📖 Test 4: Recommending agents for task...")
    recommendations = knowledge.recommend_agent("analyze code architecture and design patterns")
    if recommendations:
        print(f"   ✅ Recommended {len(recommendations)} agents:")
        for agent_id in recommendations[:3]:
            agent = knowledge.get_agent_metadata(agent_id)
            if agent:
                print(f"      - {agent.name} ({agent_id})")
    else:
        print("   ⚠️  No recommendations found")

    # Test 5: System prompt builder
    print("\n📖 Test 5: Building system prompts...")
    builder = SystemPromptBuilder(knowledge)

    prompt = builder.build_prompt(
        task_type="general",
        include_agents=True,
        include_skills=True,
        custom_context="Testing framework awareness"
    )

    print(f"   ✅ Built system prompt ({len(prompt)} characters)")
    print(f"   📝 Preview:\n")
    print("   " + "\n   ".join(prompt[:500].split("\n")))
    print("   ...")

    # Test 6: Agent invocation prompt
    print("\n📖 Test 6: Building agent invocation prompt...")
    if agent:
        agent_prompt = builder.build_agent_invocation_prompt(agent.id)
        print(f"   ✅ Built agent prompt ({len(agent_prompt)} characters)")
        print(f"   📝 Preview:\n")
        print("   " + "\n   ".join(agent_prompt[:300].split("\n")))
        print("   ...")

    print("\n" + "=" * 60)
    print("✅ All tests passed!")
    print("=" * 60)

    return True


if __name__ == "__main__":
    success = test_framework_knowledge()
    sys.exit(0 if success else 1)
