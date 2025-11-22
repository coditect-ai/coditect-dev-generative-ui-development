#!/usr/bin/env python3
"""
AI Curriculum Content Generator

Generates multi-level educational content with NotebookLM optimization
"""

import yaml
from typing import Dict, List, Any
from dataclasses import dataclass
from enum import Enum

class SkillLevel(Enum):
    BEGINNER = "beginner"
    INTERMEDIATE = "intermediate" 
    ADVANCED = "advanced"
    EXPERT = "expert"

class BloomLevel(Enum):
    REMEMBER = "remember"
    UNDERSTAND = "understand"
    APPLY = "apply"
    ANALYZE = "analyze"
    EVALUATE = "evaluate"
    CREATE = "create"

@dataclass
class LearningObjective:
    bloom_level: BloomLevel
    description: str
    skill_level: SkillLevel
    assessment_methods: List[str]

@dataclass
class ContentMetadata:
    skill_level: SkillLevel
    module: str
    week: int
    topic: str
    estimated_time: int
    difficulty_score: int
    bloom_levels: List[BloomLevel]
    prerequisites: List[str]
    learning_objectives: List[LearningObjective]
    cross_references: Dict[str, List[str]]

class ContentGenerator:
    """Generate multi-level AI curriculum content"""
    
    def __init__(self):
        self.bloom_distributions = {
            SkillLevel.BEGINNER: {
                BloomLevel.REMEMBER: 40,
                BloomLevel.UNDERSTAND: 35, 
                BloomLevel.APPLY: 20,
                BloomLevel.ANALYZE: 5,
                BloomLevel.EVALUATE: 0,
                BloomLevel.CREATE: 0
            },
            SkillLevel.INTERMEDIATE: {
                BloomLevel.REMEMBER: 15,
                BloomLevel.UNDERSTAND: 25,
                BloomLevel.APPLY: 35,
                BloomLevel.ANALYZE: 20,
                BloomLevel.EVALUATE: 5,
                BloomLevel.CREATE: 0
            },
            SkillLevel.ADVANCED: {
                BloomLevel.REMEMBER: 5,
                BloomLevel.UNDERSTAND: 15,
                BloomLevel.APPLY: 25,
                BloomLevel.ANALYZE: 30,
                BloomLevel.EVALUATE: 20,
                BloomLevel.CREATE: 5
            },
            SkillLevel.EXPERT: {
                BloomLevel.REMEMBER: 5,
                BloomLevel.UNDERSTAND: 10,
                BloomLevel.APPLY: 25,
                BloomLevel.ANALYZE: 25,
                BloomLevel.EVALUATE: 20,
                BloomLevel.CREATE: 15
            }
        }
        
    def generate_learning_objectives(self, topic: str, skill_level: SkillLevel) -> List[LearningObjective]:
        """Generate skill-appropriate learning objectives"""
        
        distribution = self.bloom_distributions[skill_level]
        objectives = []
        
        for bloom_level, percentage in distribution.items():
            if percentage > 0:
                obj = self._create_objective(topic, bloom_level, skill_level, percentage)
                if obj:
                    objectives.append(obj)
                    
        return objectives
    
    def _create_objective(self, topic: str, bloom_level: BloomLevel, 
                         skill_level: SkillLevel, weight: int) -> LearningObjective:
        """Create specific learning objective"""
        
        # Bloom level keywords and patterns
        bloom_keywords = {
            BloomLevel.REMEMBER: ["identify", "list", "recall", "recognize"],
            BloomLevel.UNDERSTAND: ["explain", "describe", "interpret", "summarize"],
            BloomLevel.APPLY: ["implement", "execute", "use", "demonstrate"],
            BloomLevel.ANALYZE: ["compare", "categorize", "examine", "break down"],
            BloomLevel.EVALUATE: ["critique", "assess", "judge", "recommend"],
            BloomLevel.CREATE: ["design", "develop", "formulate", "produce"]
        }
        
        # Assessment methods by Bloom level
        assessment_methods = {
            BloomLevel.REMEMBER: ["multiple_choice", "true_false", "matching"],
            BloomLevel.UNDERSTAND: ["short_answer", "concept_mapping", "explanation"],
            BloomLevel.APPLY: ["coding_exercise", "practical_problem", "simulation"],
            BloomLevel.ANALYZE: ["case_study", "comparison_task", "breakdown_exercise"],
            BloomLevel.EVALUATE: ["critique_task", "peer_review", "recommendation"],
            BloomLevel.CREATE: ["original_project", "research_proposal", "innovation_challenge"]
        }
        
        # Generate objective description based on skill level and bloom level
        keyword = bloom_keywords[bloom_level][0]  # Primary keyword
        
        if skill_level == SkillLevel.BEGINNER:
            description = f"{keyword.title()} basic {topic} concepts through visual examples and analogies"
        elif skill_level == SkillLevel.INTERMEDIATE:
            description = f"{keyword.title()} {topic} through hands-on implementation and practical exercises"
        elif skill_level == SkillLevel.ADVANCED:
            description = f"{keyword.title()} {topic} optimization strategies and research applications"
        else:  # EXPERT
            description = f"{keyword.title()} innovative {topic} approaches and theoretical foundations"
            
        return LearningObjective(
            bloom_level=bloom_level,
            description=description,
            skill_level=skill_level,
            assessment_methods=assessment_methods[bloom_level]
        )
    
    def generate_content_metadata(self, module: str, week: int, topic: str, 
                                 skill_level: SkillLevel) -> ContentMetadata:
        """Generate comprehensive content metadata"""
        
        objectives = self.generate_learning_objectives(topic, skill_level)
        bloom_levels = [obj.bloom_level for obj in objectives]
        
        # Calculate difficulty score based on skill level and Bloom distribution
        difficulty_map = {
            SkillLevel.BEGINNER: 1.5,
            SkillLevel.INTERMEDIATE: 2.5, 
            SkillLevel.ADVANCED: 4.0,
            SkillLevel.EXPERT: 4.8
        }
        
        # Estimate time based on skill level complexity
        time_map = {
            SkillLevel.BEGINNER: 3,
            SkillLevel.INTERMEDIATE: 5,
            SkillLevel.ADVANCED: 8,
            SkillLevel.EXPERT: 12
        }
        
        # Generate prerequisites based on skill level
        prerequisites = self._generate_prerequisites(topic, skill_level, week)
        
        # Generate cross-references
        cross_references = self._generate_cross_references(topic, skill_level)
        
        return ContentMetadata(
            skill_level=skill_level,
            module=module,
            week=week,
            topic=topic,
            estimated_time=time_map[skill_level],
            difficulty_score=int(difficulty_map[skill_level]),
            bloom_levels=bloom_levels,
            prerequisites=prerequisites,
            learning_objectives=objectives,
            cross_references=cross_references
        )
    
    def _generate_prerequisites(self, topic: str, skill_level: SkillLevel, week: int) -> List[str]:
        """Generate prerequisite list based on topic and skill level"""
        
        base_prerequisites = {
            "neural_networks": {
                SkillLevel.BEGINNER: ["basic_math", "programming_basics"],
                SkillLevel.INTERMEDIATE: ["linear_algebra", "python_programming", "basic_ml"],
                SkillLevel.ADVANCED: ["calculus", "statistics", "intermediate_programming"],
                SkillLevel.EXPERT: ["advanced_mathematics", "research_methodology", "academic_writing"]
            },
            "machine_learning": {
                SkillLevel.BEGINNER: ["basic_statistics", "programming_basics"],
                SkillLevel.INTERMEDIATE: ["python_programming", "data_structures"],
                SkillLevel.ADVANCED: ["advanced_statistics", "algorithm_design"],
                SkillLevel.EXPERT: ["theoretical_cs", "optimization_theory"]
            }
        }
        
        # Add week-based prerequisites (previous weeks)
        week_prerequisites = []
        if week > 1:
            prev_skill_level = skill_level
            if skill_level != SkillLevel.BEGINNER and week == 1:
                # First week of non-beginner level requires previous level completion
                prev_levels = [SkillLevel.BEGINNER, SkillLevel.INTERMEDIATE, SkillLevel.ADVANCED]
                if skill_level in prev_levels[1:]:
                    idx = prev_levels.index(skill_level)
                    prev_skill_level = prev_levels[idx - 1] 
                    week_prerequisites.append(f"completed_{prev_skill_level.value}_level")
            else:
                week_prerequisites.append(f"week_{week-1}_{skill_level.value}")
        
        topic_prereqs = base_prerequisites.get(topic, {}).get(skill_level, [])
        return week_prerequisites + topic_prereqs
    
    def _generate_cross_references(self, topic: str, skill_level: SkillLevel) -> Dict[str, List[str]]:
        """Generate topic cross-references for knowledge graph"""
        
        cross_ref_map = {
            "neural_networks": {
                "related_concepts": ["machine_learning", "deep_learning", "backpropagation"],
                "applications": ["computer_vision", "natural_language_processing", "speech_recognition"],
                "mathematical_foundations": ["linear_algebra", "calculus", "optimization"],
                "advanced_topics": ["transformer_architecture", "attention_mechanisms", "regularization"]
            },
            "machine_learning": {
                "related_concepts": ["statistics", "data_mining", "pattern_recognition"],
                "applications": ["recommendation_systems", "fraud_detection", "predictive_modeling"],
                "mathematical_foundations": ["probability", "linear_algebra", "optimization"],
                "advanced_topics": ["ensemble_methods", "feature_engineering", "model_selection"]
            }
        }
        
        base_refs = cross_ref_map.get(topic, {
            "related_concepts": [topic.replace("_", " ")],
            "applications": ["real_world_applications"],
            "mathematical_foundations": ["basic_mathematics"],
            "advanced_topics": ["advanced_" + topic]
        })
        
        # Filter cross-references based on skill level
        if skill_level == SkillLevel.BEGINNER:
            return {
                "related_concepts": base_refs["related_concepts"][:2],
                "applications": base_refs["applications"][:2]
            }
        elif skill_level == SkillLevel.INTERMEDIATE:
            return {
                "related_concepts": base_refs["related_concepts"],
                "applications": base_refs["applications"],
                "mathematical_foundations": base_refs["mathematical_foundations"][:2]
            }
        else:  # ADVANCED or EXPERT
            return base_refs
    
    def export_metadata_yaml(self, metadata: ContentMetadata) -> str:
        """Export metadata as YAML for NotebookLM optimization"""
        
        metadata_dict = {
            "content_metadata": {
                "skill_level": metadata.skill_level.value,
                "module": metadata.module,
                "week": metadata.week,
                "topic": metadata.topic,
                "estimated_time": metadata.estimated_time,
                "difficulty_score": metadata.difficulty_score,
                "bloom_levels": [bl.value for bl in metadata.bloom_levels],
                "prerequisites": metadata.prerequisites,
                "cross_references": metadata.cross_references
            },
            "learning_objectives": [
                {
                    "bloom_level": obj.bloom_level.value,
                    "description": obj.description,
                    "skill_level": obj.skill_level.value,
                    "assessment_methods": obj.assessment_methods
                }
                for obj in metadata.learning_objectives
            ]
        }
        
        return yaml.dump(metadata_dict, default_flow_style=False, indent=2)


def main():
    """Example usage of ContentGenerator"""
    
    generator = ContentGenerator()
    
    # Generate metadata for different skill levels
    topics = ["neural_networks", "machine_learning", "deep_learning"]
    skill_levels = [SkillLevel.BEGINNER, SkillLevel.INTERMEDIATE, 
                   SkillLevel.ADVANCED, SkillLevel.EXPERT]
    
    for topic in topics:
        print(f"\n=== {topic.upper().replace('_', ' ')} ===")
        for skill_level in skill_levels:
            print(f"\n--- {skill_level.value.title()} Level ---")
            
            metadata = generator.generate_content_metadata(
                module="module1_foundations",
                week=1,
                topic=topic,
                skill_level=skill_level
            )
            
            # Print learning objectives
            print("Learning Objectives:")
            for obj in metadata.learning_objectives:
                print(f"  - [{obj.bloom_level.value}] {obj.description}")
            
            # Print metadata summary
            print(f"Estimated Time: {metadata.estimated_time} hours")
            print(f"Difficulty Score: {metadata.difficulty_score}/5")
            print(f"Prerequisites: {', '.join(metadata.prerequisites) if metadata.prerequisites else 'None'}")
            
            # Export YAML for one example
            if topic == "neural_networks" and skill_level == SkillLevel.INTERMEDIATE:
                print("\nExample YAML Export:")
                print(generator.export_metadata_yaml(metadata))

if __name__ == "__main__":
    main()