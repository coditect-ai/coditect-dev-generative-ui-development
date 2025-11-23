#!/usr/bin/env python3
"""
CODITECT NESTED LEARNING Processor

Extracts reusable patterns from sessions for knowledge accumulation.
Implements workflow, decision, and code pattern recognition with
knowledge graph construction and similarity scoring.

NESTED = Networked Extraction System for Transferable Experience and Decisions

Features:
- Workflow pattern recognition (task sequences)
- Decision pattern extraction (rationale capture)
- Code pattern detection (reusable templates)
- Knowledge graph construction (pattern relationships)
- Similarity scoring (pattern matching)
- Incremental learning (pattern evolution)

Usage:
    from nested_learning import NestedLearningProcessor, PatternType

    processor = NestedLearningProcessor()

    # Extract patterns from session
    patterns = processor.extract_patterns(session_data)

    # Find similar patterns
    similar = processor.find_similar_patterns(query_pattern, threshold=0.7)

    # Update pattern library
    processor.update_pattern_library(new_patterns)

Author: AZ1.AI CODITECT Team
Sprint: Sprint +1 - MEMORY-CONTEXT Implementation Day 4
Date: 2025-11-16
"""

import os
import sys
import re
import json
import sqlite3
import logging
from enum import Enum
from pathlib import Path
from typing import Dict, List, Optional, Set, Tuple, Any
from dataclasses import dataclass, asdict, field
from datetime import datetime, timezone
from collections import Counter, defaultdict

# Add project root to path
PROJECT_ROOT = Path(__file__).parent.parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

# Configure logging to output to both stdout and file
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler('coditect-nested-learning.log')
    ]
)
logger = logging.getLogger(__name__)


# Custom exception hierarchy for better error handling
class NestedLearningError(Exception):
    """Base exception for NESTED LEARNING errors."""
    pass


class PatternExtractionError(NestedLearningError):
    """Raised when pattern extraction fails."""
    pass


class PatternStorageError(NestedLearningError):
    """Raised when pattern storage fails."""
    pass


class DatabaseError(NestedLearningError):
    """Raised when database operations fail."""
    pass


class ConfigurationError(NestedLearningError):
    """Raised when configuration is invalid."""
    pass


class PatternType(Enum):
    """Types of patterns that can be extracted."""
    WORKFLOW = "workflow"       # Task sequences and workflows
    DECISION = "decision"       # Decision points and rationale
    CODE = "code"              # Code templates and structures
    ERROR = "error"            # Error patterns and fixes
    ARCHITECTURE = "architecture"  # Architectural decisions
    CONFIGURATION = "configuration"  # Config patterns


@dataclass
class Pattern:
    """Represents an extracted pattern."""
    pattern_id: str
    pattern_type: PatternType
    name: str
    description: str

    # Pattern content
    template: str
    example: Optional[str] = None
    variations: List[str] = field(default_factory=list)

    # Metadata
    category: Optional[str] = None
    tags: List[str] = field(default_factory=list)

    # Quality metrics
    confidence: float = 0.5  # 0.0 to 1.0
    quality_score: float = 0.5  # 0.0 to 1.0

    # Usage statistics
    frequency: int = 1
    reuse_count: int = 0
    success_rate: float = 1.0
    last_used: Optional[str] = None

    # Relationships
    source_session_id: Optional[str] = None
    related_patterns: List[str] = field(default_factory=list)

    # Versioning
    version: int = 1
    parent_pattern_id: Optional[str] = None
    deprecated: bool = False

    # Timestamps
    created_at: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    updated_at: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())


@dataclass
class WorkflowPattern(Pattern):
    """Workflow-specific pattern with task sequence."""
    steps: List[str] = field(default_factory=list)
    conditions: Dict[str, str] = field(default_factory=dict)
    estimated_duration: Optional[int] = None  # minutes


@dataclass
class DecisionPattern(Pattern):
    """Decision-specific pattern with options and rationale."""
    options: List[str] = field(default_factory=list)
    chosen_option: Optional[str] = None
    rationale: Optional[str] = None
    context: Dict[str, Any] = field(default_factory=dict)
    alternatives_considered: List[str] = field(default_factory=list)
    outcome: Optional[str] = None


@dataclass
class CodePattern(Pattern):
    """Code-specific pattern with language and structure."""
    language: Optional[str] = None
    framework: Optional[str] = None  # React, FastAPI, Flask, etc.
    structure_type: Optional[str] = None  # class, function, module, API, component
    imports: List[str] = field(default_factory=list)
    dependencies: List[str] = field(default_factory=list)
    anti_patterns: List[str] = field(default_factory=list)
    design_patterns: List[str] = field(default_factory=list)  # Singleton, Factory, etc.


@dataclass
class ErrorPattern(Pattern):
    """Error-specific pattern with error type and solution."""
    error_type: Optional[str] = None  # TypeError, ValueError, etc.
    error_message: Optional[str] = None
    stack_trace: Optional[str] = None
    solution: Optional[str] = None
    root_cause: Optional[str] = None
    prevention: Optional[str] = None


@dataclass
class ArchitecturePattern(Pattern):
    """Architecture-specific pattern with design decisions."""
    architecture_type: Optional[str] = None  # microservices, monolith, serverless
    components: List[str] = field(default_factory=list)
    integrations: List[str] = field(default_factory=list)
    constraints: Dict[str, str] = field(default_factory=dict)
    trade_offs: Dict[str, str] = field(default_factory=dict)


@dataclass
class ConfigurationPattern(Pattern):
    """Configuration-specific pattern with setup instructions."""
    config_type: Optional[str] = None  # env, yaml, json, docker
    environment: Optional[str] = None  # dev, staging, prod
    settings: Dict[str, Any] = field(default_factory=dict)
    secrets: List[str] = field(default_factory=list)  # Keys to be replaced
    prerequisites: List[str] = field(default_factory=list)


class NestedLearningProcessor:
    """
    NESTED LEARNING: Networked Extraction System for Transferable Experience and Decisions

    Extracts, stores, and retrieves reusable patterns from sessions.
    """

    def __init__(self, db_path: Optional[Path] = None, config_path: Optional[Path] = None):
        """
        Initialize NESTED LEARNING processor.

        Args:
            db_path: Path to SQLite database
            config_path: Path to configuration file

        Raises:
            ConfigurationError: If configuration cannot be loaded
            DatabaseError: If database path is invalid
        """
        try:
            # Set paths with validation
            self.db_path = db_path or PROJECT_ROOT / "MEMORY-CONTEXT" / "memory-context.db"
            self.config_path = config_path or PROJECT_ROOT / "MEMORY-CONTEXT" / "nested-learning.config.json"

            # Validate db_path parent directory exists
            if not self.db_path.parent.exists():
                try:
                    self.db_path.parent.mkdir(parents=True, exist_ok=True)
                    logger.info(f"Created database directory: {self.db_path.parent}")
                except OSError as e:
                    error_msg = f"Cannot create database directory '{self.db_path.parent}': {e}"
                    logger.error(error_msg)
                    raise DatabaseError(error_msg) from e

            # Load configuration
            self.config = self._load_config()

            # Initialize pattern extractors (6 total) with error handling
            try:
                self.workflow_extractor = WorkflowPatternExtractor(self.config)
                self.decision_extractor = DecisionPatternExtractor(self.config)
                self.code_extractor = CodePatternExtractor(self.config)
                self.error_extractor = ErrorPatternExtractor(self.config)
                self.architecture_extractor = ArchitecturePatternExtractor(self.config)
                self.configuration_extractor = ConfigurationPatternExtractor(self.config)
            except Exception as e:
                error_msg = f"Failed to initialize pattern extractors: {e}"
                logger.error(error_msg, exc_info=True)
                raise ConfigurationError(error_msg) from e

            # Pattern library cache
            self.pattern_cache: Dict[str, Pattern] = {}

            logger.info(f"NESTED LEARNING processor initialized")
            logger.info(f"Database: {self.db_path}")
            logger.info(f"Config: {self.config_path}")

        except (ConfigurationError, DatabaseError):
            raise
        except Exception as e:
            error_msg = f"Failed to initialize NESTED LEARNING processor: {e}"
            logger.error(error_msg, exc_info=True)
            raise NestedLearningError(error_msg) from e

    def _load_config(self) -> Dict[str, Any]:
        """
        Load configuration from file or create default.

        Returns:
            Configuration dictionary

        Raises:
            ConfigurationError: If configuration file is invalid
        """
        try:
            if self.config_path.exists():
                try:
                    with open(self.config_path, 'r') as f:
                        config = json.load(f)
                    logger.info(f"Loaded config from {self.config_path}")
                    return config
                except json.JSONDecodeError as e:
                    error_msg = f"Invalid JSON in config file '{self.config_path}': {e}"
                    logger.error(error_msg)
                    raise ConfigurationError(error_msg) from e
                except OSError as e:
                    error_msg = f"Cannot read config file '{self.config_path}': {e}"
                    logger.error(error_msg)
                    raise ConfigurationError(error_msg) from e
            else:
                # Default configuration
                config = {
                    "min_pattern_confidence": 0.6,
                    "min_similarity_threshold": 0.7,
                    "max_variations_per_pattern": 5,
                    "workflow_detection": {
                        "min_steps": 2,
                        "max_steps": 10,
                        "common_verbs": ["create", "update", "delete", "test", "deploy", "review"]
                    },
                    "decision_detection": {
                        "decision_markers": ["decided", "chose", "selected", "option", "alternative"],
                        "rationale_markers": ["because", "since", "due to", "reason", "tradeoff"]
                    },
                    "code_detection": {
                        "min_lines": 5,
                        "languages": ["python", "javascript", "typescript", "rust", "sql"],
                        "frameworks": {
                            "python": ["fastapi", "flask", "django", "pytest"],
                            "javascript": ["react", "vue", "angular", "express", "next"],
                            "typescript": ["react", "nest", "angular"]
                        },
                        "design_patterns": ["singleton", "factory", "observer", "strategy", "decorator"]
                    },
                    "error_detection": {
                        "error_markers": ["error", "exception", "traceback", "failed", "bug"],
                        "solution_markers": ["fixed", "solved", "resolved", "workaround"]
                    },
                    "architecture_detection": {
                        "arch_markers": ["architecture", "design", "adr", "decision record"],
                        "component_markers": ["service", "module", "layer", "tier"]
                    },
                    "configuration_detection": {
                        "config_files": [".env", "config.yaml", "config.json", "docker-compose.yml", "Dockerfile"],
                        "env_markers": ["development", "staging", "production", "test"]
                    }
                }

                # Save default config with error handling
                try:
                    self.config_path.parent.mkdir(parents=True, exist_ok=True)
                    with open(self.config_path, 'w') as f:
                        json.dump(config, f, indent=2)
                    logger.info(f"Created default config: {self.config_path}")
                except OSError as e:
                    error_msg = f"Cannot create config file '{self.config_path}': {e}"
                    logger.error(error_msg)
                    raise ConfigurationError(error_msg) from e

                return config

        except ConfigurationError:
            raise
        except Exception as e:
            error_msg = f"Unexpected error loading configuration: {e}"
            logger.error(error_msg, exc_info=True)
            raise ConfigurationError(error_msg) from e

    def extract_patterns(self, session_data: Dict[str, Any]) -> List[Pattern]:
        """
        Extract patterns from session data.

        Args:
            session_data: Dictionary containing session information
                - conversation: List of messages
                - decisions: List of decisions made
                - file_changes: List of files changed
                - metadata: Session metadata

        Returns:
            List of extracted patterns
        """
        patterns = []

        try:
            # Extract workflow patterns
            if "conversation" in session_data:
                workflow_patterns = self.workflow_extractor.extract(
                    session_data["conversation"],
                    session_data.get("metadata", {})
                )
                patterns.extend(workflow_patterns)
                logger.info(f"Extracted {len(workflow_patterns)} workflow patterns")

            # Extract decision patterns
            if "decisions" in session_data:
                decision_patterns = self.decision_extractor.extract(
                    session_data["decisions"],
                    session_data.get("metadata", {})
                )
                patterns.extend(decision_patterns)
                logger.info(f"Extracted {len(decision_patterns)} decision patterns")

            # Extract code patterns
            if "file_changes" in session_data:
                code_patterns = self.code_extractor.extract(
                    session_data["file_changes"],
                    session_data.get("metadata", {})
                )
                patterns.extend(code_patterns)
                logger.info(f"Extracted {len(code_patterns)} code patterns")

            # Extract error patterns
            if "conversation" in session_data or "file_changes" in session_data:
                error_patterns = self.error_extractor.extract(
                    session_data.get("conversation", []),
                    session_data.get("file_changes", []),
                    session_data.get("metadata", {})
                )
                patterns.extend(error_patterns)
                logger.info(f"Extracted {len(error_patterns)} error patterns")

            # Extract architecture patterns
            if "decisions" in session_data or "file_changes" in session_data:
                arch_patterns = self.architecture_extractor.extract(
                    session_data.get("decisions", []),
                    session_data.get("file_changes", []),
                    session_data.get("metadata", {})
                )
                patterns.extend(arch_patterns)
                logger.info(f"Extracted {len(arch_patterns)} architecture patterns")

            # Extract configuration patterns
            if "file_changes" in session_data:
                config_patterns = self.configuration_extractor.extract(
                    session_data["file_changes"],
                    session_data.get("metadata", {})
                )
                patterns.extend(config_patterns)
                logger.info(f"Extracted {len(config_patterns)} configuration patterns")

            # Link session ID
            session_id = session_data.get("session_id")
            if session_id:
                for pattern in patterns:
                    pattern.source_session_id = session_id

            logger.info(f"Total patterns extracted: {len(patterns)}")
            return patterns

        except Exception as e:
            logger.error(f"Pattern extraction failed: {e}")
            return []

    def store_patterns(self, patterns: List[Pattern]) -> int:
        """
        Store patterns in database.

        Args:
            patterns: List of patterns to store

        Returns:
            Number of patterns stored

        Raises:
            PatternStorageError: If storage operation fails
        """
        if not patterns:
            logger.debug("No patterns to store")
            return 0

        conn = None
        try:
            # Validate database path
            if not self.db_path.parent.exists():
                self.db_path.parent.mkdir(parents=True, exist_ok=True)

            # Connect to database with timeout
            conn = sqlite3.connect(str(self.db_path), timeout=30.0)
            cursor = conn.cursor()

            stored_count = 0

            for pattern in patterns:
                try:
                    # Check if similar pattern exists
                    similar = self._find_similar_in_db(cursor, pattern)

                    if similar:
                        # Update existing pattern
                        self._merge_patterns(cursor, similar, pattern)
                        logger.debug(f"Merged pattern: {pattern.name}")
                    else:
                        # Insert new pattern
                        self._insert_pattern(cursor, pattern)
                        stored_count += 1
                        logger.debug(f"Inserted new pattern: {pattern.name}")

                except sqlite3.Error as e:
                    logger.warning(f"Failed to store pattern '{pattern.name}': {e}")
                    # Continue with next pattern
                    continue

            conn.commit()
            logger.info(f"Stored {stored_count} new patterns, merged {len(patterns) - stored_count}")
            return stored_count

        except sqlite3.Error as e:
            error_msg = f"Database error during pattern storage: {e}"
            logger.error(error_msg, exc_info=True)
            if conn:
                try:
                    conn.rollback()
                except:
                    pass
            raise PatternStorageError(error_msg) from e

        except Exception as e:
            error_msg = f"Unexpected error during pattern storage: {e}"
            logger.error(error_msg, exc_info=True)
            if conn:
                try:
                    conn.rollback()
                except:
                    pass
            raise PatternStorageError(error_msg) from e

        finally:
            # Ensure connection is closed
            if conn:
                try:
                    conn.close()
                except:
                    pass

    def track_pattern_usage(self, pattern_id: str, success: bool = True) -> bool:
        """
        Track pattern usage for incremental learning.

        Updates frequency, reuse_count, and success_rate metrics.

        Args:
            pattern_id: ID of the pattern being used
            success: Whether the pattern usage was successful

        Returns:
            True if tracking successful, False otherwise
        """
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()

            # Get current stats
            cursor.execute(
                """
                SELECT frequency, reuse_count, last_used, metadata
                FROM patterns
                WHERE pattern_id = ?
                """,
                (pattern_id,)
            )

            result = cursor.fetchone()
            if not result:
                logger.warning(f"Pattern {pattern_id} not found for usage tracking")
                conn.close()
                return False

            frequency, reuse_count, last_used, metadata_json = result
            metadata = json.loads(metadata_json) if metadata_json else {}

            # Update metrics
            new_frequency = frequency + 1
            new_reuse_count = reuse_count + 1

            # Track success rate
            successes = metadata.get('successes', 0)
            failures = metadata.get('failures', 0)

            if success:
                successes += 1
            else:
                failures += 1

            total_uses = successes + failures
            success_rate = successes / total_uses if total_uses > 0 else 0.0

            metadata['successes'] = successes
            metadata['failures'] = failures
            metadata['success_rate'] = success_rate

            # Update pattern
            cursor.execute(
                """
                UPDATE patterns
                SET frequency = ?,
                    reuse_count = ?,
                    last_used = ?,
                    metadata = ?
                WHERE pattern_id = ?
                """,
                (new_frequency, new_reuse_count, datetime.now().isoformat(),
                 json.dumps(metadata), pattern_id)
            )

            conn.commit()
            conn.close()

            # Update quality score based on new metrics
            self.update_pattern_quality(pattern_id)

            logger.debug(f"Tracked usage for pattern {pattern_id}: frequency={new_frequency}, success_rate={success_rate:.2f}")
            return True

        except Exception as e:
            logger.error(f"Pattern usage tracking failed: {e}")
            return False

    def update_pattern_quality(self, pattern_id: str) -> bool:
        """
        Update pattern quality score based on usage metrics.

        Quality score calculation:
        - 40% based on success_rate
        - 30% based on frequency (normalized)
        - 30% based on reuse_count (normalized)

        Args:
            pattern_id: ID of the pattern to update

        Returns:
            True if update successful, False otherwise
        """
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()

            # Get pattern metrics
            cursor.execute(
                """
                SELECT frequency, reuse_count, confidence, metadata
                FROM patterns
                WHERE pattern_id = ?
                """,
                (pattern_id,)
            )

            result = cursor.fetchone()
            if not result:
                logger.warning(f"Pattern {pattern_id} not found for quality update")
                conn.close()
                return False

            frequency, reuse_count, confidence, metadata_json = result
            metadata = json.loads(metadata_json) if metadata_json else {}

            # Get success rate from metadata
            success_rate = metadata.get('success_rate', 0.0)

            # Calculate normalized frequency score (cap at 20 uses)
            frequency_score = min(frequency / 20.0, 1.0)

            # Calculate normalized reuse score (cap at 10 reuses)
            reuse_score = min(reuse_count / 10.0, 1.0)

            # Calculate quality score (weighted average)
            quality_score = (
                0.40 * success_rate +
                0.30 * frequency_score +
                0.30 * reuse_score
            )

            # Update confidence score based on frequency (more uses = higher confidence)
            # Incremental learning: confidence increases with successful usage
            if success_rate > 0.7:
                # High success rate increases confidence
                new_confidence = min(confidence + (0.05 * (success_rate - 0.7)), 1.0)
            elif success_rate < 0.5:
                # Low success rate decreases confidence
                new_confidence = max(confidence - (0.05 * (0.5 - success_rate)), 0.0)
            else:
                # Moderate success rate maintains confidence
                new_confidence = confidence

            # Update pattern
            cursor.execute(
                """
                UPDATE patterns
                SET quality_score = ?,
                    confidence = ?
                WHERE pattern_id = ?
                """,
                (quality_score, new_confidence, pattern_id)
            )

            conn.commit()
            conn.close()

            logger.debug(f"Updated quality for pattern {pattern_id}: quality={quality_score:.2f}, confidence={new_confidence:.2f}")
            return True

        except Exception as e:
            logger.error(f"Pattern quality update failed: {e}")
            return False

    def get_pattern_evolution(self, pattern_id: str) -> List[Dict[str, Any]]:
        """
        Get evolution history for a pattern.

        Returns version history showing how pattern has evolved over time.

        Args:
            pattern_id: ID of the pattern

        Returns:
            List of version dictionaries with timestamps and changes
        """
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()

            # Get pattern metadata
            cursor.execute(
                """
                SELECT metadata FROM patterns WHERE pattern_id = ?
                """,
                (pattern_id,)
            )

            result = cursor.fetchone()
            conn.close()

            if not result:
                logger.warning(f"Pattern {pattern_id} not found")
                return []

            metadata = json.loads(result[0]) if result[0] else {}
            version_history = metadata.get('version_history', [])

            return version_history

        except Exception as e:
            logger.error(f"Failed to get pattern evolution: {e}")
            return []

    def deprecate_pattern(self, pattern_id: str, reason: str = "") -> bool:
        """
        Mark a pattern as deprecated.

        Deprecated patterns are not returned in searches but remain for historical reference.

        Args:
            pattern_id: ID of the pattern to deprecate
            reason: Reason for deprecation

        Returns:
            True if deprecation successful, False otherwise
        """
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()

            # Get current metadata
            cursor.execute(
                """
                SELECT metadata FROM patterns WHERE pattern_id = ?
                """,
                (pattern_id,)
            )

            result = cursor.fetchone()
            if not result:
                logger.warning(f"Pattern {pattern_id} not found for deprecation")
                conn.close()
                return False

            metadata = json.loads(result[0]) if result[0] else {}

            # Add deprecation info to metadata
            metadata['deprecated_at'] = datetime.now().isoformat()
            metadata['deprecation_reason'] = reason

            # Mark as deprecated
            cursor.execute(
                """
                UPDATE patterns
                SET deprecated = 1,
                    metadata = ?
                WHERE pattern_id = ?
                """,
                (json.dumps(metadata), pattern_id)
            )

            conn.commit()
            conn.close()

            logger.info(f"Deprecated pattern {pattern_id}: {reason}")
            return True

        except Exception as e:
            logger.error(f"Pattern deprecation failed: {e}")
            return False

    def recommend_patterns(
        self,
        context: str,
        pattern_type: Optional[PatternType] = None,
        limit: int = 5,
        min_quality: float = 0.5
    ) -> List[Dict[str, Any]]:
        """
        Recommend patterns relevant to current context.

        Uses combination of:
        - Context similarity (text matching)
        - Quality score (proven patterns)
        - Success rate (reliable patterns)
        - Recency (recently used patterns)

        Args:
            context: Current work context (description of what user is doing)
            pattern_type: Optional filter by pattern type
            limit: Maximum number of recommendations
            min_quality: Minimum quality score threshold

        Returns:
            List of recommended patterns with relevance scores
        """
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()

            # Build query
            query = """
                SELECT
                    pattern_id, pattern_type, name, description,
                    template, confidence, quality_score,
                    frequency, reuse_count, last_used, metadata
                FROM patterns
                WHERE deprecated = 0
                  AND quality_score >= ?
            """
            params = [min_quality]

            if pattern_type:
                query += " AND pattern_type = ?"
                params.append(pattern_type.value)

            query += " ORDER BY quality_score DESC, frequency DESC LIMIT 50"

            cursor.execute(query, params)
            candidates = cursor.fetchall()
            conn.close()

            # Calculate relevance score for each candidate
            recommendations = []

            for candidate in candidates:
                (pattern_id, p_type, name, description, template,
                 confidence, quality_score, frequency, reuse_count,
                 last_used, metadata_json) = candidate

                metadata = json.loads(metadata_json) if metadata_json else {}
                success_rate = metadata.get('success_rate', 0.0)

                # Calculate context similarity
                context_similarity = self._calculate_similarity(
                    context.lower(),
                    f"{name} {description} {template}".lower()
                )

                # Calculate recency score (patterns used in last 30 days score higher)
                recency_score = 0.0
                if last_used:
                    try:
                        last_used_dt = datetime.fromisoformat(last_used.replace('Z', '+00:00'))
                        days_since_use = (datetime.now(timezone.utc) - last_used_dt).days
                        recency_score = max(0.0, 1.0 - (days_since_use / 30.0))
                    except:
                        recency_score = 0.0

                # Calculate relevance score (weighted combination)
                relevance_score = (
                    0.40 * context_similarity +    # How well it matches current work
                    0.25 * quality_score +          # How good the pattern is
                    0.20 * success_rate +           # How reliable it is
                    0.15 * recency_score            # How recently used
                )

                recommendations.append({
                    'pattern_id': pattern_id,
                    'pattern_type': p_type,
                    'name': name,
                    'description': description,
                    'template': template,
                    'confidence': confidence,
                    'quality_score': quality_score,
                    'success_rate': success_rate,
                    'frequency': frequency,
                    'reuse_count': reuse_count,
                    'relevance_score': relevance_score,
                    'context_similarity': context_similarity,
                    'why_recommended': self._generate_recommendation_reason(
                        context_similarity, quality_score, success_rate, recency_score
                    )
                })

            # Sort by relevance score
            recommendations.sort(key=lambda x: x['relevance_score'], reverse=True)

            # Return top N
            return recommendations[:limit]

        except Exception as e:
            logger.error(f"Pattern recommendation failed: {e}")
            return []

    def _generate_recommendation_reason(
        self,
        context_similarity: float,
        quality_score: float,
        success_rate: float,
        recency_score: float
    ) -> str:
        """Generate human-readable reason for recommendation."""
        reasons = []

        if context_similarity > 0.7:
            reasons.append("highly relevant to current context")
        elif context_similarity > 0.5:
            reasons.append("relevant to current context")

        if quality_score > 0.8:
            reasons.append("high quality pattern")
        elif quality_score > 0.6:
            reasons.append("proven pattern")

        if success_rate > 0.8:
            reasons.append("very reliable ({}% success rate)".format(int(success_rate * 100)))
        elif success_rate > 0.6:
            reasons.append("reliable ({}% success rate)".format(int(success_rate * 100)))

        if recency_score > 0.7:
            reasons.append("recently used")

        if not reasons:
            return "matches criteria"

        return ", ".join(reasons)

    def _find_similar_in_db(self, cursor: sqlite3.Cursor, pattern: Pattern) -> Optional[Dict]:
        """Find similar pattern in database."""
        # Query patterns of same type
        cursor.execute(
            """
            SELECT pattern_id, name, template, confidence, quality_score
            FROM patterns
            WHERE pattern_type = ? AND deprecated = 0
            ORDER BY quality_score DESC
            LIMIT 10
            """,
            (pattern.pattern_type.value,)
        )

        candidates = cursor.fetchall()

        # Calculate similarity for each candidate
        for candidate in candidates:
            similarity = self._calculate_similarity(
                pattern.template,
                candidate[2]  # template
            )

            if similarity >= self.config.get("min_similarity_threshold", 0.7):
                return {
                    'pattern_id': candidate[0],
                    'name': candidate[1],
                    'template': candidate[2],
                    'confidence': candidate[3],
                    'quality_score': candidate[4],
                    'similarity': similarity
                }

        return None

    def _calculate_similarity(self, text1: str, text2: str) -> float:
        """
        Calculate similarity between two texts.

        Uses combination of:
        - Token overlap (Jaccard similarity)
        - Edit distance (normalized)

        Args:
            text1: First text
            text2: Second text

        Returns:
            Similarity score (0.0 to 1.0)
        """
        # Tokenize
        tokens1 = set(text1.lower().split())
        tokens2 = set(text2.lower().split())

        # Jaccard similarity
        if not tokens1 or not tokens2:
            return 0.0

        intersection = tokens1 & tokens2
        union = tokens1 | tokens2
        jaccard = len(intersection) / len(union) if union else 0.0

        # Edit distance (normalized)
        edit_dist = self._edit_distance(text1.lower(), text2.lower())
        max_len = max(len(text1), len(text2))
        normalized_edit = 1.0 - (edit_dist / max_len) if max_len > 0 else 0.0

        # Weighted combination
        similarity = 0.6 * jaccard + 0.4 * normalized_edit

        return similarity

    def _edit_distance(self, s1: str, s2: str) -> int:
        """Calculate Levenshtein edit distance."""
        if len(s1) < len(s2):
            return self._edit_distance(s2, s1)

        if len(s2) == 0:
            return len(s1)

        previous_row = range(len(s2) + 1)
        for i, c1 in enumerate(s1):
            current_row = [i + 1]
            for j, c2 in enumerate(s2):
                # Cost of insertions, deletions, or substitutions
                insertions = previous_row[j + 1] + 1
                deletions = current_row[j] + 1
                substitutions = previous_row[j] + (c1 != c2)
                current_row.append(min(insertions, deletions, substitutions))
            previous_row = current_row

        return previous_row[-1]

    def _merge_patterns(self, cursor: sqlite3.Cursor, existing: Dict, new_pattern: Pattern) -> None:
        """
        Merge new pattern into existing pattern.

        Tracks version history showing when patterns were merged.
        """
        # Get current metadata
        cursor.execute(
            """
            SELECT metadata FROM patterns WHERE pattern_id = ?
            """,
            (existing['pattern_id'],)
        )

        result = cursor.fetchone()
        metadata = json.loads(result[0]) if result and result[0] else {}

        # Add version history entry
        if 'version_history' not in metadata:
            metadata['version_history'] = []

        version_entry = {
            'timestamp': datetime.now(timezone.utc).isoformat(),
            'action': 'merged',
            'merged_from': new_pattern.pattern_id,
            'merged_template': new_pattern.template[:100],  # First 100 chars
            'confidence': new_pattern.confidence,
            'similarity': existing.get('similarity', 0.0)
        }

        metadata['version_history'].append(version_entry)

        # Keep only last 20 version entries
        if len(metadata['version_history']) > 20:
            metadata['version_history'] = metadata['version_history'][-20:]

        # Increment frequency and update metadata
        cursor.execute(
            """
            UPDATE patterns
            SET frequency = frequency + 1,
                updated_at = ?,
                metadata = ?
            WHERE pattern_id = ?
            """,
            (datetime.now(timezone.utc).isoformat(), json.dumps(metadata), existing['pattern_id'])
        )

    def _insert_pattern(self, cursor: sqlite3.Cursor, pattern: Pattern) -> None:
        """Insert new pattern into database."""
        # Convert pattern to JSON
        pattern_json = json.dumps({
            'name': pattern.name,
            'type': pattern.pattern_type.value,
            'template': pattern.template,
            'variations': pattern.variations,
        })

        # Initialize metadata with empty success tracking
        metadata = {
            'successes': 0,
            'failures': 0,
            'success_rate': 0.0,
            'version_history': []
        }

        # Insert
        cursor.execute(
            """
            INSERT INTO patterns (
                pattern_id, pattern_type, name, description,
                pattern_json, template, example,
                category, tags_csv, confidence, quality_score,
                frequency, reuse_count, success_rate, last_used,
                source_session_id, related_patterns_json,
                version, parent_pattern_id, deprecated,
                created_at, updated_at, metadata
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                pattern.pattern_id,
                pattern.pattern_type.value,
                pattern.name,
                pattern.description,
                pattern_json,
                pattern.template,
                pattern.example or '',
                pattern.category or '',
                ','.join(pattern.tags),
                pattern.confidence,
                pattern.quality_score,
                pattern.frequency,
                pattern.reuse_count,
                pattern.success_rate,
                pattern.last_used,
                pattern.source_session_id,
                json.dumps(pattern.related_patterns),
                pattern.version,
                pattern.parent_pattern_id,
                pattern.deprecated,
                pattern.created_at,
                pattern.updated_at,
                json.dumps(metadata),
            )
        )

    def find_similar_patterns(
        self,
        query: str,
        pattern_type: Optional[PatternType] = None,
        threshold: float = 0.7,
        limit: int = 10
    ) -> List[Tuple[Pattern, float]]:
        """
        Find patterns similar to query.

        Args:
            query: Query text
            pattern_type: Optional pattern type filter
            threshold: Minimum similarity threshold
            limit: Maximum results to return

        Returns:
            List of (pattern, similarity_score) tuples
        """
        try:
            conn = sqlite3.connect(str(self.db_path))
            cursor = conn.cursor()

            # Build query
            sql = """
                SELECT pattern_id, pattern_type, name, description, template,
                       confidence, quality_score, frequency
                FROM patterns
                WHERE deprecated = 0
            """
            params = []

            if pattern_type:
                sql += " AND pattern_type = ?"
                params.append(pattern_type.value)

            sql += " ORDER BY quality_score DESC, frequency DESC LIMIT ?"
            params.append(limit * 3)  # Get more candidates for filtering

            cursor.execute(sql, params)
            candidates = cursor.fetchall()

            # Calculate similarities
            results = []
            for row in candidates:
                template = row[4]
                similarity = self._calculate_similarity(query, template)

                if similarity >= threshold:
                    pattern = Pattern(
                        pattern_id=row[0],
                        pattern_type=PatternType(row[1]),
                        name=row[2],
                        description=row[3],
                        template=template,
                        confidence=row[5],
                        quality_score=row[6],
                        frequency=row[7]
                    )
                    results.append((pattern, similarity))

            # Sort by similarity
            results.sort(key=lambda x: x[1], reverse=True)

            conn.close()

            logger.info(f"Found {len(results)} similar patterns (threshold: {threshold})")
            return results[:limit]

        except Exception as e:
            logger.error(f"Pattern search failed: {e}")
            return []

    def get_pattern_statistics(self) -> Dict[str, Any]:
        """Get statistics about pattern library."""
        try:
            conn = sqlite3.connect(str(self.db_path))
            cursor = conn.cursor()

            # Total patterns by type
            cursor.execute("""
                SELECT pattern_type, COUNT(*), AVG(quality_score), AVG(frequency)
                FROM patterns
                WHERE deprecated = 0
                GROUP BY pattern_type
            """)

            by_type = {}
            for row in cursor.fetchall():
                by_type[row[0]] = {
                    'count': row[1],
                    'avg_quality': row[2],
                    'avg_frequency': row[3]
                }

            # Overall statistics
            cursor.execute("""
                SELECT
                    COUNT(*) as total,
                    AVG(quality_score) as avg_quality,
                    AVG(frequency) as avg_frequency,
                    SUM(reuse_count) as total_reuses
                FROM patterns
                WHERE deprecated = 0
            """)

            overall = cursor.fetchone()

            conn.close()

            return {
                'total_patterns': overall[0],
                'avg_quality_score': overall[1],
                'avg_frequency': overall[2],
                'total_reuses': overall[3],
                'by_type': by_type
            }

        except Exception as e:
            logger.error(f"Statistics retrieval failed: {e}")
            return {}


class WorkflowPatternExtractor:
    """Extracts workflow patterns from conversation."""

    def __init__(self, config: Dict[str, Any]):
        self.config = config.get("workflow_detection", {})
        self.common_verbs = set(self.config.get("common_verbs", []))

    def extract(self, conversation: List[Dict], metadata: Dict) -> List[WorkflowPattern]:
        """Extract workflow patterns from conversation."""
        patterns = []

        # Look for task sequences
        steps = self._extract_steps(conversation)

        if len(steps) >= self.config.get("min_steps", 2):
            # Create workflow pattern
            pattern = WorkflowPattern(
                pattern_id=f"workflow_{datetime.now().timestamp()}",
                pattern_type=PatternType.WORKFLOW,
                name=self._generate_workflow_name(steps),
                description=f"Workflow with {len(steps)} steps",
                template=" → ".join(steps),
                steps=steps,
                confidence=0.7,
                quality_score=0.6
            )
            patterns.append(pattern)

        return patterns

    def _extract_steps(self, conversation: List[Dict]) -> List[str]:
        """Extract task steps from conversation."""
        steps = []

        for message in conversation:
            content = message.get('content', '')

            # Look for action verbs
            for verb in self.common_verbs:
                if verb in content.lower():
                    # Extract sentence containing verb
                    sentences = re.split(r'[.!?]', content)
                    for sentence in sentences:
                        if verb in sentence.lower():
                            step = sentence.strip()
                            if step and step not in steps:
                                steps.append(step[:100])  # Truncate long steps
                                break

        return steps

    def _generate_workflow_name(self, steps: List[str]) -> str:
        """Generate descriptive name for workflow."""
        if not steps:
            return "Unnamed Workflow"

        # Use first and last step
        if len(steps) == 1:
            return f"Workflow: {steps[0][:50]}"
        else:
            return f"Workflow: {steps[0][:30]} ... {steps[-1][:30]}"


class DecisionPatternExtractor:
    """Extracts decision patterns from session."""

    def __init__(self, config: Dict[str, Any]):
        self.config = config.get("decision_detection", {})
        self.decision_markers = self.config.get("decision_markers", [])
        self.rationale_markers = self.config.get("rationale_markers", [])

    def extract(self, decisions: List[Dict], metadata: Dict) -> List[DecisionPattern]:
        """Extract decision patterns from decisions list."""
        patterns = []

        for decision in decisions:
            pattern = DecisionPattern(
                pattern_id=f"decision_{datetime.now().timestamp()}",
                pattern_type=PatternType.DECISION,
                name=decision.get('decision', 'Unnamed Decision')[:100],
                description=decision.get('rationale', '')[:200],
                template=self._create_decision_template(decision),
                rationale=decision.get('rationale'),
                alternatives_considered=decision.get('alternatives', []),
                outcome=decision.get('outcome'),
                confidence=0.8,
                quality_score=0.7
            )
            patterns.append(pattern)

        return patterns

    def _create_decision_template(self, decision: Dict) -> str:
        """Create template from decision."""
        template_parts = []

        if 'decision' in decision:
            template_parts.append(f"Decision: {decision['decision']}")

        if 'alternatives' in decision:
            template_parts.append(f"Alternatives: {', '.join(decision['alternatives'])}")

        if 'rationale' in decision:
            template_parts.append(f"Rationale: {decision['rationale']}")

        return " | ".join(template_parts)


class CodePatternExtractor:
    """Extracts code patterns from file changes."""

    def __init__(self, config: Dict[str, Any]):
        self.config = config.get("code_detection", {})
        self.languages = self.config.get("languages", [])

    def extract(self, file_changes: List[Dict], metadata: Dict) -> List[CodePattern]:
        """Extract code patterns from file changes."""
        patterns = []

        # Group by file type/language
        by_language = defaultdict(list)

        for change in file_changes:
            file_path = change.get('file', '')
            language = self._detect_language(file_path)

            if language in self.languages:
                by_language[language].append(change)

        # Create patterns for each language
        for language, changes in by_language.items():
            if len(changes) >= 1:
                # Detect framework and structure type from files
                framework = None
                structure_types = set()

                for change in changes:
                    file_path = change.get('file', '')

                    detected_framework = self._detect_framework(file_path, language)
                    if detected_framework:
                        framework = detected_framework

                    structure_type = self._detect_structure_type(file_path)
                    if structure_type:
                        structure_types.add(structure_type)

                # Generate better name based on framework/structure
                if framework:
                    name = f"{framework.capitalize()} {language} pattern"
                elif structure_types:
                    name = f"{language.capitalize()} {'/'.join(structure_types)} pattern"
                else:
                    name = f"{language.capitalize()} code pattern"

                pattern = CodePattern(
                    pattern_id=f"code_{language}_{datetime.now().timestamp()}",
                    pattern_type=PatternType.CODE,
                    name=name,
                    description=f"{framework or language.capitalize()} pattern from {len(changes)} files",
                    template=self._create_code_template(changes),
                    language=language,
                    framework=framework,
                    structure_type=', '.join(structure_types) if structure_types else None,
                    confidence=0.7 if framework else 0.6,
                    quality_score=0.6 if framework else 0.5
                )
                patterns.append(pattern)

        return patterns

    def _detect_language(self, file_path: str) -> Optional[str]:
        """Detect programming language from file extension."""
        ext_map = {
            '.py': 'python',
            '.js': 'javascript',
            '.jsx': 'javascript',
            '.ts': 'typescript',
            '.tsx': 'typescript',
            '.rs': 'rust',
            '.sql': 'sql',
            '.java': 'java',
            '.go': 'go',
            '.rb': 'ruby',
            '.php': 'php',
            '.cs': 'csharp',
            '.cpp': 'cpp',
            '.c': 'c',
        }

        ext = Path(file_path).suffix.lower()
        return ext_map.get(ext)

    def _detect_framework(self, file_path: str, language: str) -> Optional[str]:
        """Detect framework from file path and language."""
        path_lower = file_path.lower()

        frameworks = self.config.get('frameworks', {}).get(language, [])

        for framework in frameworks:
            if framework in path_lower:
                return framework

        # Additional heuristics
        if language == 'python':
            if 'fastapi' in path_lower or 'api/routes' in path_lower:
                return 'fastapi'
            elif 'flask' in path_lower or 'app.py' in path_lower:
                return 'flask'
            elif 'django' in path_lower or 'models.py' in path_lower:
                return 'django'
            elif 'test_' in path_lower or 'conftest.py' in path_lower:
                return 'pytest'
        elif language in ['javascript', 'typescript']:
            if 'component' in path_lower or '.tsx' in path_lower or '.jsx' in path_lower:
                return 'react'
            elif 'vue' in path_lower:
                return 'vue'
            elif 'app.module.ts' in path_lower:
                return 'angular'

        return None

    def _detect_structure_type(self, file_path: str) -> Optional[str]:
        """Detect code structure type from file path."""
        path_lower = file_path.lower()

        if 'test' in path_lower or 'spec' in path_lower:
            return 'test'
        elif 'api' in path_lower or 'routes' in path_lower or 'endpoints' in path_lower:
            return 'API'
        elif 'component' in path_lower or '.tsx' in path_lower or '.jsx' in path_lower:
            return 'component'
        elif 'model' in path_lower or 'schema' in path_lower:
            return 'model'
        elif 'service' in path_lower:
            return 'service'
        elif 'util' in path_lower or 'helper' in path_lower:
            return 'utility'
        elif 'config' in path_lower or 'setting' in path_lower:
            return 'configuration'
        else:
            return 'module'

    def _create_code_template(self, changes: List[Dict]) -> str:
        """Create template from code changes."""
        actions = [change.get('action', 'modified') for change in changes]
        action_counts = Counter(actions)

        template_parts = []
        for action, count in action_counts.most_common():
            template_parts.append(f"{action}: {count} files")

        return ", ".join(template_parts)


class ErrorPatternExtractor:
    """Extracts error patterns and their solutions from sessions."""

    def __init__(self, config: Dict[str, Any]):
        self.config = config.get("error_detection", {})
        self.error_markers = self.config.get("error_markers", [])
        self.solution_markers = self.config.get("solution_markers", [])

    def extract(self, conversation: List[Dict], file_changes: List[Dict], metadata: Dict) -> List[ErrorPattern]:
        """Extract error patterns from conversation and file changes."""
        patterns = []

        # Extract from conversation
        error_contexts = []
        current_error = None

        for message in conversation:
            content = message.get('content', '')

            # Check for error markers
            if any(marker in content.lower() for marker in self.error_markers):
                current_error = {
                    'content': content,
                    'timestamp': message.get('timestamp')
                }
                error_contexts.append(current_error)
            # Check for solution markers
            elif current_error and any(marker in content.lower() for marker in self.solution_markers):
                current_error['solution'] = content
                current_error = None

        # Create patterns from error contexts
        for error_ctx in error_contexts:
            # Extract error type and message
            error_type = self._extract_error_type(error_ctx['content'])
            error_message = self._extract_error_message(error_ctx['content'])

            pattern = ErrorPattern(
                pattern_id=f"error_{datetime.now().timestamp()}",
                pattern_type=PatternType.ERROR,
                name=f"Error: {error_type or 'Unknown'}",
                description=error_message[:200] if error_message else "Error pattern",
                template=f"Error: {error_type} - {error_message[:100]}" if error_type else error_message[:150],
                error_type=error_type,
                error_message=error_message,
                solution=error_ctx.get('solution'),
                confidence=0.75,
                quality_score=0.7 if error_ctx.get('solution') else 0.5
            )
            patterns.append(pattern)

        return patterns

    def _extract_error_type(self, content: str) -> Optional[str]:
        """Extract error type from content."""
        # Common error types
        error_types = ['TypeError', 'ValueError', 'KeyError', 'AttributeError', 'IndexError',
                       'RuntimeError', 'ImportError', 'SyntaxError', 'NameError',
                       '404', '500', '403', '401']

        for error_type in error_types:
            if error_type in content:
                return error_type

        return None

    def _extract_error_message(self, content: str) -> Optional[str]:
        """Extract error message from content."""
        # Try to extract error message
        lines = content.split('\n')
        for line in lines:
            if any(marker in line.lower() for marker in self.error_markers):
                return line.strip()[:200]

        return content[:200]


class ArchitecturePatternExtractor:
    """Extracts architecture patterns from decisions and file structure."""

    def __init__(self, config: Dict[str, Any]):
        self.config = config.get("architecture_detection", {})
        self.arch_markers = self.config.get("arch_markers", [])
        self.component_markers = self.config.get("component_markers", [])

    def extract(self, decisions: List[Dict], file_changes: List[Dict], metadata: Dict) -> List[ArchitecturePattern]:
        """Extract architecture patterns from decisions and file structure."""
        patterns = []

        # Extract from decisions
        for decision in decisions:
            decision_text = decision.get('decision', '') + ' ' + decision.get('rationale', '')

            # Check if it's an architectural decision
            if any(marker in decision_text.lower() for marker in self.arch_markers):
                # Detect architecture type
                arch_type = self._detect_architecture_type(decision_text, file_changes)

                # Extract components from file structure
                components = self._extract_components(file_changes)

                pattern = ArchitecturePattern(
                    pattern_id=f"arch_{datetime.now().timestamp()}",
                    pattern_type=PatternType.ARCHITECTURE,
                    name=decision.get('decision', 'Architecture Decision')[:100],
                    description=decision.get('rationale', '')[:200],
                    template=f"Architecture: {arch_type or 'Custom'} with {len(components)} components",
                    architecture_type=arch_type,
                    components=components[:10],  # Limit to 10 components
                    trade_offs={
                        'chosen': decision.get('decision', ''),
                        'alternatives': ', '.join(decision.get('alternatives', []))
                    },
                    confidence=0.8,
                    quality_score=0.75
                )
                patterns.append(pattern)

        return patterns

    def _detect_architecture_type(self, text: str, file_changes: List[Dict]) -> Optional[str]:
        """Detect architecture type from text and file structure."""
        text_lower = text.lower()

        # Common architecture patterns
        if 'microservice' in text_lower:
            return 'microservices'
        elif 'monolith' in text_lower:
            return 'monolith'
        elif 'serverless' in text_lower or 'lambda' in text_lower:
            return 'serverless'
        elif 'event-driven' in text_lower or 'event driven' in text_lower:
            return 'event-driven'
        elif 'layered' in text_lower or 'n-tier' in text_lower:
            return 'layered'
        elif 'mvc' in text_lower:
            return 'MVC'
        elif 'rest' in text_lower or 'api' in text_lower:
            return 'RESTful API'

        # Infer from file structure
        file_paths = [change.get('file', '') for change in file_changes]
        if any('service/' in path for path in file_paths):
            return 'service-oriented'
        elif any('lambda' in path.lower() for path in file_paths):
            return 'serverless'

        return None

    def _extract_components(self, file_changes: List[Dict]) -> List[str]:
        """Extract architectural components from file structure."""
        components = set()

        for change in file_changes:
            file_path = change.get('file', '')

            # Extract component from path
            parts = file_path.split('/')
            for i, part in enumerate(parts):
                part_lower = part.lower()
                # If this part contains a component marker, extract the next part as the component name
                if any(marker in part_lower for marker in self.component_markers):
                    # Add the next part if it exists (the actual component name)
                    if i + 1 < len(parts):
                        components.add(parts[i + 1])
                    # Also add the current part for backwards compatibility
                    components.add(part)

        return list(components)


class ConfigurationPatternExtractor:
    """Extracts configuration patterns from config files."""

    def __init__(self, config: Dict[str, Any]):
        self.config = config.get("configuration_detection", {})
        self.config_files = self.config.get("config_files", [])
        self.env_markers = self.config.get("env_markers", [])

    def extract(self, file_changes: List[Dict], metadata: Dict) -> List[ConfigurationPattern]:
        """Extract configuration patterns from config files."""
        patterns = []

        # Group config files by type
        config_changes = []
        for change in file_changes:
            file_path = change.get('file', '')
            if any(config_file in file_path for config_file in self.config_files):
                config_changes.append(change)

        if config_changes:
            # Detect config type and environment
            config_type = self._detect_config_type(config_changes)
            environment = self._detect_environment(config_changes, metadata)

            pattern = ConfigurationPattern(
                pattern_id=f"config_{datetime.now().timestamp()}",
                pattern_type=PatternType.CONFIGURATION,
                name=f"{config_type.upper() if config_type else 'Configuration'} setup",
                description=f"Configuration pattern for {len(config_changes)} files",
                template=f"{config_type or 'Configuration'}: {', '.join([c.get('file', '') for c in config_changes[:3]])}",
                config_type=config_type,
                environment=environment,
                confidence=0.7,
                quality_score=0.65
            )
            patterns.append(pattern)

        return patterns

    def _detect_config_type(self, config_changes: List[Dict]) -> Optional[str]:
        """Detect configuration file type."""
        for change in config_changes:
            file_path = change.get('file', '')

            if '.env' in file_path:
                return 'env'
            elif '.yaml' in file_path or '.yml' in file_path:
                return 'yaml'
            elif '.json' in file_path:
                return 'json'
            elif 'docker-compose' in file_path:
                return 'docker-compose'
            elif 'Dockerfile' in file_path:
                return 'dockerfile'

        return None

    def _detect_environment(self, config_changes: List[Dict], metadata: Dict) -> Optional[str]:
        """Detect target environment."""
        for change in config_changes:
            file_path = change.get('file', '').lower()

            for env in self.env_markers:
                if env in file_path:
                    return env

        return None


def main():
    """
    Main entry point for testing.

    Returns:
        Exit code (0 for success, 1 for failure)
    """
    try:
        print("="*80)
        print("NESTED LEARNING PROCESSOR - Test Mode")
        print("="*80)

        # Initialize processor
        print("\n1. Initializing processor...")
        processor = NestedLearningProcessor()
        print("✅ Processor initialized successfully")

        # Example session data
        session_data = {
            "session_id": "test_session_001",
            "conversation": [
                {"role": "user", "content": "Create a new Python class for authentication"},
                {"role": "assistant", "content": "I'll create the authentication class with proper error handling"},
            ],
            "decisions": [
                {
                    "decision": "Use JWT tokens for authentication",
                    "rationale": "JWT is stateless and scales well",
                    "alternatives": ["Session cookies", "OAuth2"],
                    "outcome": "Implemented successfully"
                }
            ],
            "file_changes": [
                {"file": "src/auth.py", "action": "created", "lines_added": 150}
            ],
            "metadata": {
                "duration_minutes": 45,
                "messages_count": 12
            }
        }

        # Extract patterns
        print("\n2. Extracting patterns from session data...")
        patterns = processor.extract_patterns(session_data)
        print(f"✅ Extracted {len(patterns)} patterns:")
        for pattern in patterns:
            print(f"   - {pattern.pattern_type.value}: {pattern.name}")

        # Store patterns
        print("\n3. Storing patterns in database...")
        stored = processor.store_patterns(patterns)
        print(f"✅ Stored {stored} new patterns")

        # Get statistics
        print("\n4. Retrieving pattern library statistics...")
        stats = processor.get_pattern_statistics()
        print("✅ Pattern library statistics:")
        print(f"   Total patterns: {stats.get('total_patterns', 0)}")
        print(f"   Avg quality: {stats.get('avg_quality_score', 0):.2f}")

        print("\n" + "="*80)
        print("✅ All tests completed successfully")
        print("="*80)
        return 0

    except ConfigurationError as e:
        print(f"\n❌ Configuration error: {e}", file=sys.stderr)
        logger.error("Configuration error in main", exc_info=True)
        return 1

    except PatternExtractionError as e:
        print(f"\n❌ Pattern extraction error: {e}", file=sys.stderr)
        logger.error("Pattern extraction error in main", exc_info=True)
        return 1

    except PatternStorageError as e:
        print(f"\n❌ Pattern storage error: {e}", file=sys.stderr)
        logger.error("Pattern storage error in main", exc_info=True)
        return 1

    except DatabaseError as e:
        print(f"\n❌ Database error: {e}", file=sys.stderr)
        logger.error("Database error in main", exc_info=True)
        return 1

    except NestedLearningError as e:
        print(f"\n❌ NESTED LEARNING error: {e}", file=sys.stderr)
        logger.error("NESTED LEARNING error in main", exc_info=True)
        return 1

    except KeyboardInterrupt:
        print("\n\n⚠️  Operation cancelled by user", file=sys.stderr)
        return 130

    except Exception as e:
        print(f"\n❌ Unexpected error: {e}", file=sys.stderr)
        logger.error("Unexpected error in main", exc_info=True)
        return 1


if __name__ == "__main__":
    sys.exit(main())
