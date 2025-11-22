#!/usr/bin/env python3
"""
Unit Tests for NESTED LEARNING Processor

Tests pattern extraction, similarity scoring, and pattern library management.

Author: AZ1.AI CODITECT Team
Sprint: Sprint +1 - MEMORY-CONTEXT Implementation Day 4
Date: 2025-11-16
"""

import os
import sys
import unittest
import tempfile
import sqlite3
import json
from pathlib import Path
from datetime import datetime, timezone

# Add project root to path
PROJECT_ROOT = Path(__file__).parent.parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from scripts.core.nested_learning import (
    NestedLearningProcessor,
    WorkflowPatternExtractor,
    DecisionPatternExtractor,
    CodePatternExtractor,
    ErrorPatternExtractor,
    ArchitecturePatternExtractor,
    ConfigurationPatternExtractor,
    Pattern,
    WorkflowPattern,
    DecisionPattern,
    CodePattern,
    ErrorPattern,
    ArchitecturePattern,
    ConfigurationPattern,
    PatternType
)
from scripts.core.db_init import DatabaseInitializer


class TestNestedLearningProcessor(unittest.TestCase):
    """Test cases for NESTED LEARNING processor."""

    @classmethod
    def setUpClass(cls):
        """Set up test database."""
        cls.temp_dir = tempfile.mkdtemp()
        cls.db_path = Path(cls.temp_dir) / "test_memory.db"
        cls.config_path = Path(cls.temp_dir) / "test_config.json"

        # Initialize database
        schema_path = PROJECT_ROOT / "MEMORY-CONTEXT" / "database-schema.sql"
        if schema_path.exists():
            initializer = DatabaseInitializer(cls.db_path, verbose=False)
            initializer.initialize()

    def setUp(self):
        """Set up each test."""
        self.processor = NestedLearningProcessor(
            db_path=self.db_path,
            config_path=self.config_path
        )

    def test_processor_initialization(self):
        """Test processor initializes correctly."""
        self.assertIsNotNone(self.processor)
        self.assertEqual(self.processor.db_path, self.db_path)
        self.assertTrue(self.config_path.exists())
        self.assertIn("workflow_detection", self.processor.config)
        self.assertIn("decision_detection", self.processor.config)
        self.assertIn("code_detection", self.processor.config)

    def test_workflow_pattern_extraction(self):
        """Test workflow pattern extraction from conversation."""
        conversation = [
            {"role": "user", "content": "Create a new authentication system"},
            {"role": "assistant", "content": "I'll create the auth module"},
            {"role": "assistant", "content": "Next, I'll test the authentication flow"},
            {"role": "assistant", "content": "Finally, I'll deploy to staging"}
        ]

        session_data = {
            "session_id": "test_001",
            "conversation": conversation,
            "metadata": {}
        }

        patterns = self.processor.extract_patterns(session_data)

        # Should extract at least one workflow pattern
        workflow_patterns = [p for p in patterns if p.pattern_type == PatternType.WORKFLOW]
        self.assertGreater(len(workflow_patterns), 0)

        # Check workflow has steps
        workflow = workflow_patterns[0]
        self.assertIsInstance(workflow, WorkflowPattern)
        self.assertGreater(len(workflow.steps), 0)

    def test_decision_pattern_extraction(self):
        """Test decision pattern extraction."""
        decisions = [
            {
                "decision": "Use PostgreSQL for database",
                "rationale": "Better JSON support and performance",
                "alternatives": ["MySQL", "SQLite", "MongoDB"],
                "outcome": "Implemented successfully"
            }
        ]

        session_data = {
            "session_id": "test_002",
            "decisions": decisions,
            "metadata": {}
        }

        patterns = self.processor.extract_patterns(session_data)

        # Should extract decision pattern
        decision_patterns = [p for p in patterns if p.pattern_type == PatternType.DECISION]
        self.assertEqual(len(decision_patterns), 1)

        # Check decision details
        decision = decision_patterns[0]
        self.assertIsInstance(decision, DecisionPattern)
        self.assertEqual(decision.name, "Use PostgreSQL for database")
        self.assertEqual(decision.rationale, "Better JSON support and performance")
        self.assertEqual(len(decision.alternatives_considered), 3)

    def test_code_pattern_extraction(self):
        """Test code pattern extraction from file changes."""
        file_changes = [
            {"file": "src/auth.py", "action": "created", "lines_added": 150},
            {"file": "src/models.py", "action": "modified", "lines_added": 50},
            {"file": "tests/test_auth.py", "action": "created", "lines_added": 80}
        ]

        session_data = {
            "session_id": "test_003",
            "file_changes": file_changes,
            "metadata": {}
        }

        patterns = self.processor.extract_patterns(session_data)

        # Should extract code pattern
        code_patterns = [p for p in patterns if p.pattern_type == PatternType.CODE]
        self.assertGreater(len(code_patterns), 0)

        # Check code pattern details
        code = code_patterns[0]
        self.assertIsInstance(code, CodePattern)
        self.assertEqual(code.language, "python")

    def test_pattern_storage(self):
        """Test storing patterns in database."""
        pattern = Pattern(
            pattern_id="test_pattern_001",
            pattern_type=PatternType.WORKFLOW,
            name="Test Workflow",
            description="Test workflow pattern",
            template="Step 1 → Step 2 → Step 3",
            confidence=0.8,
            quality_score=0.7
        )

        stored = self.processor.store_patterns([pattern])
        self.assertEqual(stored, 1)

        # Verify in database
        conn = sqlite3.connect(str(self.db_path))
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM patterns WHERE pattern_id = ?", (pattern.pattern_id,))
        count = cursor.fetchone()[0]
        conn.close()

        self.assertEqual(count, 1)

    def test_similarity_calculation(self):
        """Test similarity scoring between patterns."""
        text1 = "Create authentication system with JWT tokens"
        text2 = "Create authentication module using JWT"
        text3 = "Deploy database backup script"

        # Similar texts should have higher similarity than different texts
        sim_high = self.processor._calculate_similarity(text1, text2)
        sim_low = self.processor._calculate_similarity(text1, text3)

        self.assertGreater(sim_high, 0.4)  # Realistic threshold for similar texts
        self.assertLess(sim_low, 0.3)  # Different texts should be lower
        self.assertGreater(sim_high, sim_low)  # Similar should be higher than different

    def test_edit_distance(self):
        """Test edit distance calculation."""
        # Identical strings
        self.assertEqual(self.processor._edit_distance("test", "test"), 0)

        # One character difference
        self.assertEqual(self.processor._edit_distance("test", "text"), 1)

        # Multiple differences
        dist = self.processor._edit_distance("kitten", "sitting")
        self.assertEqual(dist, 3)

    def test_find_similar_patterns(self):
        """Test finding similar patterns."""
        # Store some patterns first
        patterns = [
            Pattern(
                pattern_id="pattern_001",
                pattern_type=PatternType.WORKFLOW,
                name="Auth Setup",
                description="Authentication setup workflow",
                template="Setup OAuth → Configure JWT → Test authentication",
                confidence=0.8,
                quality_score=0.75
            ),
            Pattern(
                pattern_id="pattern_002",
                pattern_type=PatternType.WORKFLOW,
                name="Database Setup",
                description="Database configuration workflow",
                template="Install PostgreSQL → Create schema → Run migrations",
                confidence=0.9,
                quality_score=0.85
            )
        ]

        self.processor.store_patterns(patterns)

        # Search for similar patterns
        query = "Setup authentication with OAuth"
        results = self.processor.find_similar_patterns(
            query=query,
            pattern_type=PatternType.WORKFLOW,
            threshold=0.3,
            limit=5
        )

        # Should find at least one result
        self.assertGreater(len(results), 0)

        # First result should be auth pattern (higher similarity)
        best_match, similarity = results[0]
        self.assertIn("Auth", best_match.name)
        self.assertGreater(similarity, 0.3)

    def test_pattern_merging(self):
        """Test merging similar patterns."""
        # Create base pattern
        base_pattern = Pattern(
            pattern_id="merge_test_001",
            pattern_type=PatternType.WORKFLOW,
            name="Test Workflow",
            description="Test workflow",
            template="Create class → Write tests → Deploy",
            confidence=0.7,
            quality_score=0.6,
            frequency=1
        )

        # Store base pattern
        self.processor.store_patterns([base_pattern])

        # Create similar pattern (should merge)
        similar_pattern = Pattern(
            pattern_id="merge_test_002",
            pattern_type=PatternType.WORKFLOW,
            name="Test Workflow Similar",
            description="Similar test workflow",
            template="Create class → Write tests → Deploy application",
            confidence=0.8,
            quality_score=0.7,
            frequency=1
        )

        # Store similar pattern
        stored = self.processor.store_patterns([similar_pattern])

        # Should merge (0 new patterns stored)
        self.assertEqual(stored, 0)

        # Verify frequency incremented
        conn = sqlite3.connect(str(self.db_path))
        cursor = conn.cursor()
        cursor.execute("SELECT frequency FROM patterns WHERE pattern_id = ?", (base_pattern.pattern_id,))
        frequency = cursor.fetchone()[0]
        conn.close()

        self.assertEqual(frequency, 2)

    def test_pattern_statistics(self):
        """Test getting pattern library statistics."""
        # Add some test patterns
        patterns = [
            Pattern(
                pattern_id=f"stat_test_{i}",
                pattern_type=PatternType.WORKFLOW if i % 2 == 0 else PatternType.DECISION,
                name=f"Pattern {i}",
                description=f"Test pattern {i}",
                template=f"Template {i}",
                confidence=0.7 + (i * 0.05),
                quality_score=0.6 + (i * 0.05),
                frequency=i + 1,
                reuse_count=i
            )
            for i in range(5)
        ]

        self.processor.store_patterns(patterns)

        # Get statistics
        stats = self.processor.get_pattern_statistics()

        self.assertIn('total_patterns', stats)
        self.assertIn('avg_quality_score', stats)
        self.assertIn('by_type', stats)
        self.assertGreater(stats['total_patterns'], 0)

    def test_complex_session_extraction(self):
        """Test extracting multiple pattern types from complex session."""
        session_data = {
            "session_id": "complex_001",
            "conversation": [
                {"role": "user", "content": "Create a new API endpoint for user management"},
                {"role": "assistant", "content": "I'll create the endpoint with proper validation"},
                {"role": "assistant", "content": "Next, I'll test the endpoint"},
                {"role": "assistant", "content": "Finally, update the API documentation"}
            ],
            "decisions": [
                {
                    "decision": "Use FastAPI for the API",
                    "rationale": "Better async support and automatic docs",
                    "alternatives": ["Flask", "Django REST"],
                    "outcome": "Working well"
                }
            ],
            "file_changes": [
                {"file": "src/api/users.py", "action": "created", "lines_added": 120},
                {"file": "tests/api/test_users.py", "action": "created", "lines_added": 80},
                {"file": "docs/api.md", "action": "modified", "lines_added": 30}
            ],
            "metadata": {
                "duration_minutes": 60,
                "messages_count": 15
            }
        }

        patterns = self.processor.extract_patterns(session_data)

        # Should extract multiple types
        workflow_count = sum(1 for p in patterns if p.pattern_type == PatternType.WORKFLOW)
        decision_count = sum(1 for p in patterns if p.pattern_type == PatternType.DECISION)
        code_count = sum(1 for p in patterns if p.pattern_type == PatternType.CODE)

        self.assertGreater(workflow_count, 0)
        self.assertGreater(decision_count, 0)
        self.assertGreater(code_count, 0)

        # All patterns should have session ID
        for pattern in patterns:
            self.assertEqual(pattern.source_session_id, "complex_001")


class TestWorkflowPatternExtractor(unittest.TestCase):
    """Test cases for workflow pattern extractor."""

    def setUp(self):
        """Set up test."""
        config = {
            "workflow_detection": {
                "min_steps": 2,
                "max_steps": 10,
                "common_verbs": ["create", "update", "delete", "test", "deploy", "review"]
            }
        }
        self.extractor = WorkflowPatternExtractor(config)

    def test_step_extraction(self):
        """Test extracting steps from conversation."""
        conversation = [
            {"content": "Create a new database schema"},
            {"content": "Update the user model"},
            {"content": "Test the authentication flow"},
            {"content": "Deploy to production"}
        ]

        steps = self.extractor._extract_steps(conversation)

        self.assertGreater(len(steps), 0)
        self.assertTrue(any("create" in step.lower() or "database" in step.lower() for step in steps))

    def test_workflow_name_generation(self):
        """Test generating workflow names."""
        steps = ["Create schema", "Add migrations", "Test database"]

        name = self.extractor._generate_workflow_name(steps)

        self.assertIn("Create schema", name)
        self.assertIn("Test database", name)


class TestDecisionPatternExtractor(unittest.TestCase):
    """Test cases for decision pattern extractor."""

    def setUp(self):
        """Set up test."""
        config = {
            "decision_detection": {
                "decision_markers": ["decided", "chose", "selected"],
                "rationale_markers": ["because", "since", "due to"]
            }
        }
        self.extractor = DecisionPatternExtractor(config)

    def test_decision_template_creation(self):
        """Test creating decision templates."""
        decision = {
            "decision": "Use PostgreSQL",
            "rationale": "Better JSON support",
            "alternatives": ["MySQL", "SQLite"]
        }

        template = self.extractor._create_decision_template(decision)

        self.assertIn("Use PostgreSQL", template)
        self.assertIn("Better JSON support", template)
        self.assertIn("MySQL", template)


class TestCodePatternExtractor(unittest.TestCase):
    """Test cases for code pattern extractor."""

    def setUp(self):
        """Set up test."""
        config = {
            "code_detection": {
                "min_lines": 5,
                "languages": ["python", "javascript", "typescript"]
            }
        }
        self.extractor = CodePatternExtractor(config)

    def test_language_detection(self):
        """Test detecting programming language."""
        self.assertEqual(self.extractor._detect_language("test.py"), "python")
        self.assertEqual(self.extractor._detect_language("app.js"), "javascript")
        self.assertEqual(self.extractor._detect_language("component.ts"), "typescript")
        self.assertIsNone(self.extractor._detect_language("readme.md"))

    def test_code_template_creation(self):
        """Test creating code templates."""
        changes = [
            {"action": "created", "file": "a.py"},
            {"action": "created", "file": "b.py"},
            {"action": "modified", "file": "c.py"}
        ]

        template = self.extractor._create_code_template(changes)

        self.assertIn("created: 2", template)
        self.assertIn("modified: 1", template)


class TestErrorPatternExtractor(unittest.TestCase):
    """Test cases for Error Pattern Extractor (Day 6)."""

    def setUp(self):
        """Set up each test."""
        self.extractor = ErrorPatternExtractor({
            "error_detection": {
                "error_markers": ["error", "exception", "traceback", "failed"],
                "solution_markers": ["fixed", "solved", "resolved"]
            }
        })

    def test_error_extraction_from_conversation(self):
        """Test extracting error patterns from conversation."""
        conversation = [
            {"content": "Error: TypeError: Cannot read property 'map' of undefined"},
            {"content": "Fixed by adding null check before map operation"}
        ]

        patterns = self.extractor.extract(conversation, [], {})

        self.assertGreater(len(patterns), 0)
        self.assertIsInstance(patterns[0], ErrorPattern)
        self.assertIn("TypeError", patterns[0].name)

    def test_error_type_detection(self):
        """Test error type detection."""
        content = "ValueError: invalid literal for int() with base 10"
        error_type = self.extractor._extract_error_type(content)
        self.assertEqual(error_type, "ValueError")

    def test_solution_capture(self):
        """Test solution capture from conversation."""
        conversation = [
            {"content": "Error: Connection timeout", "timestamp": "2025-11-16T10:00:00Z"},
            {"content": "Fixed by increasing timeout to 30 seconds", "timestamp": "2025-11-16T10:01:00Z"}
        ]

        patterns = self.extractor.extract(conversation, [], {})

        self.assertGreater(len(patterns), 0)
        if patterns[0].solution:
            self.assertIn("Fixed", patterns[0].solution)


class TestArchitecturePatternExtractor(unittest.TestCase):
    """Test cases for Architecture Pattern Extractor (Day 6)."""

    def setUp(self):
        """Set up each test."""
        self.extractor = ArchitecturePatternExtractor({
            "architecture_detection": {
                "arch_markers": ["architecture", "design", "adr"],
                "component_markers": ["service", "module", "layer"]
            }
        })

    def test_architecture_extraction(self):
        """Test extracting architecture patterns from decisions."""
        decisions = [
            {
                "decision": "Use microservices architecture",
                "rationale": "Better scalability and independent deployment",
                "alternatives": ["Monolith", "Serverless"]
            }
        ]

        file_changes = [
            {"file": "services/auth/app.py"},
            {"file": "services/api/app.py"}
        ]

        patterns = self.extractor.extract(decisions, file_changes, {})

        self.assertGreater(len(patterns), 0)
        self.assertIsInstance(patterns[0], ArchitecturePattern)
        self.assertEqual(patterns[0].architecture_type, "microservices")

    def test_component_extraction(self):
        """Test extracting components from file structure."""
        file_changes = [
            {"file": "services/auth/app.py"},
            {"file": "services/api/routes.py"},
            {"file": "services/database/models.py"}
        ]

        components = self.extractor._extract_components(file_changes)

        self.assertGreater(len(components), 0)
        self.assertIn("auth", components)


class TestConfigurationPatternExtractor(unittest.TestCase):
    """Test cases for Configuration Pattern Extractor (Day 6)."""

    def setUp(self):
        """Set up each test."""
        self.extractor = ConfigurationPatternExtractor({
            "configuration_detection": {
                "config_files": [".env", "config.yaml", "docker-compose.yml"],
                "env_markers": ["development", "staging", "production"]
            }
        })

    def test_config_extraction(self):
        """Test extracting configuration patterns."""
        file_changes = [
            {"file": ".env.example"},
            {"file": "config.yaml"},
            {"file": "docker-compose.yml"}
        ]

        patterns = self.extractor.extract(file_changes, {"environment": "production"})

        self.assertGreater(len(patterns), 0)
        self.assertIsInstance(patterns[0], ConfigurationPattern)

    def test_config_type_detection(self):
        """Test config type detection."""
        file_changes = [
            {"file": ".env"},
            {"file": ".env.example"}
        ]

        config_type = self.extractor._detect_config_type(file_changes)
        self.assertEqual(config_type, "env")

    def test_environment_detection(self):
        """Test environment detection."""
        file_changes = [{"file": "config.production.yaml"}]
        metadata = {"tags": ["production", "deployment"]}

        env = self.extractor._detect_environment(file_changes, metadata)
        self.assertEqual(env, "production")


class TestIncrementalLearning(unittest.TestCase):
    """Test cases for Incremental Learning features (Day 6)."""

    def setUp(self):
        """Set up each test with fresh database."""
        self.temp_dir = tempfile.mkdtemp()
        self.db_path = Path(self.temp_dir) / "test_incremental.db"
        self.config_path = Path(self.temp_dir) / "test_config.json"

        # Initialize database
        schema_path = PROJECT_ROOT / "MEMORY-CONTEXT" / "database-schema.sql"
        if schema_path.exists():
            initializer = DatabaseInitializer(self.db_path, verbose=False)
            initializer.initialize()

        self.processor = NestedLearningProcessor(
            db_path=self.db_path,
            config_path=self.config_path
        )

        # Create a test pattern
        self.test_pattern = CodePattern(
            pattern_id="test_pattern_001",
            pattern_type=PatternType.CODE,
            name="Test Pattern",
            description="Test pattern for incremental learning",
            template="def test(): pass",
            language="python",
            confidence=0.7,
            quality_score=0.6
        )

        # Store it
        self.processor.store_patterns([self.test_pattern])

    def test_track_pattern_usage(self):
        """Test tracking pattern usage."""
        result = self.processor.track_pattern_usage("test_pattern_001", success=True)
        self.assertTrue(result)

        # Verify frequency increased
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT frequency FROM patterns WHERE pattern_id = ?", ("test_pattern_001",))
        frequency = cursor.fetchone()[0]
        conn.close()

        self.assertEqual(frequency, 2)  # Initial 1 + 1 usage

    def test_update_pattern_quality(self):
        """Test updating pattern quality score."""
        # Track several successful uses
        for _ in range(5):
            self.processor.track_pattern_usage("test_pattern_001", success=True)

        # Get updated pattern
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute(
            "SELECT quality_score, confidence FROM patterns WHERE pattern_id = ?",
            ("test_pattern_001",)
        )
        quality_score, confidence = cursor.fetchone()
        conn.close()

        # Quality should increase with successful usage
        self.assertGreater(quality_score, 0.6)
        self.assertGreater(confidence, 0.7)

    def test_success_rate_calculation(self):
        """Test success rate calculation."""
        # Track mixed success/failure
        self.processor.track_pattern_usage("test_pattern_001", success=True)
        self.processor.track_pattern_usage("test_pattern_001", success=True)
        self.processor.track_pattern_usage("test_pattern_001", success=False)

        # Get metadata
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT metadata FROM patterns WHERE pattern_id = ?", ("test_pattern_001",))
        metadata_json = cursor.fetchone()[0]
        conn.close()

        metadata = json.loads(metadata_json)
        success_rate = metadata.get('success_rate', 0.0)

        # Should be 2/3 ≈ 0.67
        self.assertAlmostEqual(success_rate, 0.67, places=2)


class TestPatternEvolution(unittest.TestCase):
    """Test cases for Pattern Evolution Tracking (Day 6)."""

    def setUp(self):
        """Set up each test with fresh database."""
        self.temp_dir = tempfile.mkdtemp()
        self.db_path = Path(self.temp_dir) / "test_evolution.db"
        self.config_path = Path(self.temp_dir) / "test_config.json"

        # Initialize database
        schema_path = PROJECT_ROOT / "MEMORY-CONTEXT" / "database-schema.sql"
        if schema_path.exists():
            initializer = DatabaseInitializer(self.db_path, verbose=False)
            initializer.initialize()

        self.processor = NestedLearningProcessor(
            db_path=self.db_path,
            config_path=self.config_path
        )

    def test_version_history_on_merge(self):
        """Test version history tracking when patterns are merged."""
        # Create and store original pattern
        pattern1 = CodePattern(
            pattern_id="pattern_001",
            pattern_type=PatternType.CODE,
            name="Original Pattern",
            description="Original",
            template="def original(): pass",
            language="python",
            confidence=0.7,
            quality_score=0.6
        )

        self.processor.store_patterns([pattern1])

        # Create similar pattern that will be merged
        pattern2 = CodePattern(
            pattern_id="pattern_002",
            pattern_type=PatternType.CODE,
            name="Similar Pattern",
            description="Similar",
            template="def original(): pass",  # Same template = high similarity
            language="python",
            confidence=0.7,
            quality_score=0.6
        )

        self.processor.store_patterns([pattern2])

        # Get version history
        history = self.processor.get_pattern_evolution("pattern_001")

        # Should have version history from merge
        self.assertGreater(len(history), 0)
        self.assertEqual(history[0]['action'], 'merged')

    def test_deprecate_pattern(self):
        """Test pattern deprecation."""
        # Create and store pattern
        pattern = CodePattern(
            pattern_id="deprecated_001",
            pattern_type=PatternType.CODE,
            name="Old Pattern",
            description="To be deprecated",
            template="def old(): pass",
            language="python",
            confidence=0.7,
            quality_score=0.6
        )

        self.processor.store_patterns([pattern])

        # Deprecate it
        result = self.processor.deprecate_pattern("deprecated_001", "Replaced by new pattern")
        self.assertTrue(result)

        # Verify it's marked as deprecated
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT deprecated FROM patterns WHERE pattern_id = ?", ("deprecated_001",))
        deprecated = cursor.fetchone()[0]
        conn.close()

        self.assertEqual(deprecated, 1)

    def test_get_pattern_evolution_empty(self):
        """Test getting evolution for pattern with no history."""
        # Create and store pattern
        pattern = CodePattern(
            pattern_id="new_pattern_001",
            pattern_type=PatternType.CODE,
            name="New Pattern",
            description="No history yet",
            template="def new(): pass",
            language="python",
            confidence=0.7,
            quality_score=0.6
        )

        self.processor.store_patterns([pattern])

        # Get version history
        history = self.processor.get_pattern_evolution("new_pattern_001")

        # Should be empty
        self.assertEqual(len(history), 0)


class TestPatternRecommendation(unittest.TestCase):
    """Test cases for Pattern Recommendation Engine (Day 6)."""

    def setUp(self):
        """Set up each test with fresh database."""
        self.temp_dir = tempfile.mkdtemp()
        self.db_path = Path(self.temp_dir) / "test_recommendation.db"
        self.config_path = Path(self.temp_dir) / "test_config.json"

        # Initialize database
        schema_path = PROJECT_ROOT / "MEMORY-CONTEXT" / "database-schema.sql"
        if schema_path.exists():
            initializer = DatabaseInitializer(self.db_path, verbose=False)
            initializer.initialize()

        self.processor = NestedLearningProcessor(
            db_path=self.db_path,
            config_path=self.config_path
        )

        # Create test patterns with different quality scores
        patterns = [
            CodePattern(
                pattern_id="high_quality_001",
                pattern_type=PatternType.CODE,
                name="High Quality Authentication Pattern",
                description="Well-tested authentication using JWT",
                template="JWT authentication pattern",
                language="python",
                confidence=0.9,
                quality_score=0.9
            ),
            CodePattern(
                pattern_id="medium_quality_001",
                pattern_type=PatternType.CODE,
                name="Database Connection Pattern",
                description="Standard database connection",
                template="Database connection pattern",
                language="python",
                confidence=0.7,
                quality_score=0.6
            ),
            WorkflowPattern(
                pattern_id="workflow_001",
                pattern_type=PatternType.WORKFLOW,
                name="Testing Workflow",
                description="Standard testing workflow",
                template="Write tests then deploy",
                steps=["Write tests", "Run tests", "Deploy"],
                confidence=0.8,
                quality_score=0.7
            )
        ]

        self.processor.store_patterns(patterns)

    def test_recommend_patterns_basic(self):
        """Test basic pattern recommendation."""
        recommendations = self.processor.recommend_patterns(
            context="I need to add user authentication to my API",
            limit=3
        )

        self.assertGreater(len(recommendations), 0)
        self.assertLessEqual(len(recommendations), 3)

        # Check structure
        self.assertIn('pattern_id', recommendations[0])
        self.assertIn('relevance_score', recommendations[0])
        self.assertIn('why_recommended', recommendations[0])

    def test_recommend_by_pattern_type(self):
        """Test recommendation filtered by pattern type."""
        recommendations = self.processor.recommend_patterns(
            context="Need authentication",
            pattern_type=PatternType.CODE,
            limit=5
        )

        # All recommendations should be CODE type
        for rec in recommendations:
            self.assertEqual(rec['pattern_type'], PatternType.CODE.value)

    def test_recommend_quality_threshold(self):
        """Test recommendation with quality threshold."""
        recommendations = self.processor.recommend_patterns(
            context="authentication",
            min_quality=0.8,
            limit=5
        )

        # All recommendations should have quality >= 0.8
        for rec in recommendations:
            self.assertGreaterEqual(rec['quality_score'], 0.8)

    def test_recommendation_relevance_scoring(self):
        """Test relevance scoring prefers high-quality patterns."""
        recommendations = self.processor.recommend_patterns(
            context="authentication JWT secure login",
            limit=5
        )

        if len(recommendations) > 0:
            # First recommendation should have highest relevance
            for i in range(1, len(recommendations)):
                self.assertGreaterEqual(
                    recommendations[i-1]['relevance_score'],
                    recommendations[i]['relevance_score']
                )

    def test_recommendation_reason_generation(self):
        """Test recommendation reason is meaningful."""
        recommendations = self.processor.recommend_patterns(
            context="authentication",
            limit=1
        )

        if len(recommendations) > 0:
            reason = recommendations[0]['why_recommended']
            self.assertIsInstance(reason, str)
            self.assertGreater(len(reason), 0)


def run_tests():
    """Run all tests."""
    # Create test suite
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()

    # Add test cases
    suite.addTests(loader.loadTestsFromTestCase(TestNestedLearningProcessor))
    suite.addTests(loader.loadTestsFromTestCase(TestWorkflowPatternExtractor))
    suite.addTests(loader.loadTestsFromTestCase(TestDecisionPatternExtractor))
    suite.addTests(loader.loadTestsFromTestCase(TestCodePatternExtractor))

    # Day 6 test cases
    suite.addTests(loader.loadTestsFromTestCase(TestErrorPatternExtractor))
    suite.addTests(loader.loadTestsFromTestCase(TestArchitecturePatternExtractor))
    suite.addTests(loader.loadTestsFromTestCase(TestConfigurationPatternExtractor))
    suite.addTests(loader.loadTestsFromTestCase(TestIncrementalLearning))
    suite.addTests(loader.loadTestsFromTestCase(TestPatternEvolution))
    suite.addTests(loader.loadTestsFromTestCase(TestPatternRecommendation))

    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)

    # Return success/failure
    return result.wasSuccessful()


if __name__ == "__main__":
    success = run_tests()
    sys.exit(0 if success else 1)
