#!/usr/bin/env python3
"""
Performance Benchmarks for MEMORY-CONTEXT System

Benchmarks key operations:
- Pattern extraction speed
- PII detection performance
- Database operations
- Session export performance
- Full pipeline throughput

Author: AZ1.AI CODITECT Team
Sprint: Sprint +1 Week 2 - Performance Testing
Date: 2025-11-16
"""

import os
import sys
import unittest
import tempfile
import time
import statistics
from pathlib import Path
from typing import List, Dict, Any
from datetime import datetime, timezone

# Add project root to path
PROJECT_ROOT = Path(__file__).parent.parent.parent
sys.path.insert(0, str(PROJECT_ROOT))
sys.path.insert(0, str(PROJECT_ROOT / "scripts" / "core"))

from nested_learning import NestedLearningProcessor
from privacy_manager import PrivacyManager, PrivacyLevel
from session_export import SessionExporter
from memory_context_integration import MemoryContextIntegration
from scripts.core.db_init import DatabaseInitializer


class PerformanceBenchmark:
    """Helper class for performance benchmarking."""

    @staticmethod
    def benchmark(func, iterations: int = 100) -> Dict[str, float]:
        """
        Run a function multiple times and collect performance metrics.

        Args:
            func: Function to benchmark (should take no arguments)
            iterations: Number of iterations to run

        Returns:
            Dictionary with performance metrics
        """
        times = []

        for _ in range(iterations):
            start = time.perf_counter()
            func()
            end = time.perf_counter()
            times.append((end - start) * 1000)  # Convert to milliseconds

        return {
            'iterations': iterations,
            'min_ms': min(times),
            'max_ms': max(times),
            'mean_ms': statistics.mean(times),
            'median_ms': statistics.median(times),
            'stdev_ms': statistics.stdev(times) if len(times) > 1 else 0,
            'total_ms': sum(times),
            'throughput_per_sec': 1000 / statistics.mean(times)  # Operations per second
        }


class TestPatternExtractionPerformance(unittest.TestCase):
    """Benchmark pattern extraction performance."""

    @classmethod
    def setUpClass(cls):
        """Set up test fixtures once for all tests."""
        cls.temp_dir = tempfile.mkdtemp()
        cls.db_path = Path(cls.temp_dir) / "perf_patterns.db"
        cls.config_path = Path(cls.temp_dir) / "config.json"

        # Initialize database
        initializer = DatabaseInitializer(cls.db_path, verbose=False)
        initializer.initialize()

        # Initialize processor
        cls.processor = NestedLearningProcessor(
            db_path=cls.db_path,
            config_path=cls.config_path
        )

        # Create test data
        cls.simple_session = {
            'conversation': [
                {'role': 'user', 'content': 'Create authentication function'},
                {'role': 'assistant', 'content': 'Created JWT auth function'}
            ],
            'decisions': [
                {'decision': 'Use JWT tokens', 'rationale': 'Stateless auth'}
            ],
            'file_changes': [
                {'file': 'src/auth.py', 'action': 'created'}
            ]
        }

        cls.complex_session = {
            'conversation': [
                {'role': 'user', 'content': f'Step {i}: Implement feature {i}'}
                for i in range(50)
            ] + [
                {'role': 'assistant', 'content': f'Completed step {i} successfully'}
                for i in range(50)
            ],
            'decisions': [
                {
                    'decision': f'Decision {i}: Use approach {i}',
                    'rationale': f'Rationale for decision {i}',
                    'alternatives': [f'Alt {j}' for j in range(3)]
                }
                for i in range(20)
            ],
            'file_changes': [
                {'file': f'src/module_{i}/file_{j}.py', 'action': 'modified'}
                for i in range(10) for j in range(5)
            ]
        }

    @classmethod
    def tearDownClass(cls):
        """Clean up test fixtures."""
        import shutil
        shutil.rmtree(cls.temp_dir, ignore_errors=True)

    def test_simple_pattern_extraction_speed(self):
        """Benchmark simple pattern extraction (baseline performance)."""
        metrics = PerformanceBenchmark.benchmark(
            lambda: self.processor.extract_patterns(self.simple_session),
            iterations=50
        )

        print(f"\n{'='*70}")
        print("SIMPLE PATTERN EXTRACTION PERFORMANCE")
        print(f"{'='*70}")
        print(f"Iterations:       {metrics['iterations']}")
        print(f"Mean time:        {metrics['mean_ms']:.2f} ms")
        print(f"Median time:      {metrics['median_ms']:.2f} ms")
        print(f"Min/Max:          {metrics['min_ms']:.2f} / {metrics['max_ms']:.2f} ms")
        print(f"Std deviation:    {metrics['stdev_ms']:.2f} ms")
        print(f"Throughput:       {metrics['throughput_per_sec']:.1f} ops/sec")
        print(f"{'='*70}\n")

        # Performance assertions
        self.assertLess(metrics['mean_ms'], 100, "Simple extraction should be under 100ms")

    def test_complex_pattern_extraction_speed(self):
        """Benchmark complex pattern extraction (100 messages, 20 decisions)."""
        metrics = PerformanceBenchmark.benchmark(
            lambda: self.processor.extract_patterns(self.complex_session),
            iterations=20
        )

        print(f"\n{'='*70}")
        print("COMPLEX PATTERN EXTRACTION PERFORMANCE")
        print(f"{'='*70}")
        print(f"Iterations:       {metrics['iterations']}")
        print(f"Mean time:        {metrics['mean_ms']:.2f} ms")
        print(f"Median time:      {metrics['median_ms']:.2f} ms")
        print(f"Min/Max:          {metrics['min_ms']:.2f} / {metrics['max_ms']:.2f} ms")
        print(f"Std deviation:    {metrics['stdev_ms']:.2f} ms")
        print(f"Throughput:       {metrics['throughput_per_sec']:.1f} ops/sec")
        print(f"{'='*70}\n")

        # Performance assertions
        self.assertLess(metrics['mean_ms'], 500, "Complex extraction should be under 500ms")

    def test_pattern_storage_speed(self):
        """Benchmark pattern storage to database."""
        # Generate patterns to store
        patterns = self.processor.extract_patterns(self.simple_session)

        metrics = PerformanceBenchmark.benchmark(
            lambda: self.processor.store_patterns(patterns),
            iterations=50
        )

        print(f"\n{'='*70}")
        print("PATTERN STORAGE PERFORMANCE")
        print(f"{'='*70}")
        print(f"Patterns stored:  {len(patterns)}")
        print(f"Iterations:       {metrics['iterations']}")
        print(f"Mean time:        {metrics['mean_ms']:.2f} ms")
        print(f"Median time:      {metrics['median_ms']:.2f} ms")
        print(f"Min/Max:          {metrics['min_ms']:.2f} / {metrics['max_ms']:.2f} ms")
        print(f"Throughput:       {metrics['throughput_per_sec']:.1f} ops/sec")
        print(f"{'='*70}\n")

        # Performance assertions
        self.assertLess(metrics['mean_ms'], 50, "Pattern storage should be under 50ms")


class TestPIIDetectionPerformance(unittest.TestCase):
    """Benchmark PII detection performance."""

    @classmethod
    def setUpClass(cls):
        """Set up test fixtures."""
        cls.privacy_manager = PrivacyManager()

        # Test data with various PII types
        cls.no_pii_text = "This is a normal conversation about implementing features."

        cls.simple_pii_text = "My email is john.doe@example.com and phone is 555-123-4567"

        cls.multiple_pii_text = """
        Contact info: john.doe@example.com, jane.smith@company.org
        Phone numbers: 555-123-4567, 555-987-6543, 555-555-5555
        API keys: sk-test-1234567890abcdef, ghp_abcdefghijklmnopqrstuvwxyz123456
        Credit cards: 4111-1111-1111-1111, 5500-0000-0000-0004
        SSN: 123-45-6789
        """

        cls.large_text_with_pii = "\n".join([
            f"Line {i}: Email user{i}@example.com, phone 555-{i:03d}-{i:04d}"
            for i in range(100)
        ])

    def test_no_pii_detection_speed(self):
        """Benchmark PII detection on text with no PII (baseline)."""
        metrics = PerformanceBenchmark.benchmark(
            lambda: self.privacy_manager.detect_pii(self.no_pii_text),
            iterations=100
        )

        print(f"\n{'='*70}")
        print("NO PII DETECTION PERFORMANCE (Baseline)")
        print(f"{'='*70}")
        print(f"Text length:      {len(self.no_pii_text)} chars")
        print(f"Iterations:       {metrics['iterations']}")
        print(f"Mean time:        {metrics['mean_ms']:.2f} ms")
        print(f"Median time:      {metrics['median_ms']:.2f} ms")
        print(f"Min/Max:          {metrics['min_ms']:.2f} / {metrics['max_ms']:.2f} ms")
        print(f"Throughput:       {metrics['throughput_per_sec']:.1f} ops/sec")
        print(f"{'='*70}\n")

        # Performance assertions
        self.assertLess(metrics['mean_ms'], 10, "No PII detection should be under 10ms")

    def test_simple_pii_detection_speed(self):
        """Benchmark PII detection with 2 PII instances."""
        metrics = PerformanceBenchmark.benchmark(
            lambda: self.privacy_manager.detect_pii(self.simple_pii_text),
            iterations=100
        )

        print(f"\n{'='*70}")
        print("SIMPLE PII DETECTION PERFORMANCE")
        print(f"{'='*70}")
        print(f"Text length:      {len(self.simple_pii_text)} chars")
        print(f"PII instances:    ~2")
        print(f"Iterations:       {metrics['iterations']}")
        print(f"Mean time:        {metrics['mean_ms']:.2f} ms")
        print(f"Median time:      {metrics['median_ms']:.2f} ms")
        print(f"Min/Max:          {metrics['min_ms']:.2f} / {metrics['max_ms']:.2f} ms")
        print(f"Throughput:       {metrics['throughput_per_sec']:.1f} ops/sec")
        print(f"{'='*70}\n")

        # Performance assertions
        self.assertLess(metrics['mean_ms'], 20, "Simple PII detection should be under 20ms")

    def test_multiple_pii_detection_speed(self):
        """Benchmark PII detection with 10+ PII instances."""
        metrics = PerformanceBenchmark.benchmark(
            lambda: self.privacy_manager.detect_pii(self.multiple_pii_text),
            iterations=100
        )

        print(f"\n{'='*70}")
        print("MULTIPLE PII DETECTION PERFORMANCE")
        print(f"{'='*70}")
        print(f"Text length:      {len(self.multiple_pii_text)} chars")
        print(f"PII instances:    ~10")
        print(f"Iterations:       {metrics['iterations']}")
        print(f"Mean time:        {metrics['mean_ms']:.2f} ms")
        print(f"Median time:      {metrics['median_ms']:.2f} ms")
        print(f"Min/Max:          {metrics['min_ms']:.2f} / {metrics['max_ms']:.2f} ms")
        print(f"Throughput:       {metrics['throughput_per_sec']:.1f} ops/sec")
        print(f"{'='*70}\n")

        # Performance assertions
        self.assertLess(metrics['mean_ms'], 50, "Multiple PII detection should be under 50ms")

    def test_large_text_pii_detection_speed(self):
        """Benchmark PII detection on large text (100+ PII instances)."""
        metrics = PerformanceBenchmark.benchmark(
            lambda: self.privacy_manager.detect_pii(self.large_text_with_pii),
            iterations=20
        )

        print(f"\n{'='*70}")
        print("LARGE TEXT PII DETECTION PERFORMANCE")
        print(f"{'='*70}")
        print(f"Text length:      {len(self.large_text_with_pii)} chars")
        print(f"PII instances:    ~200")
        print(f"Iterations:       {metrics['iterations']}")
        print(f"Mean time:        {metrics['mean_ms']:.2f} ms")
        print(f"Median time:      {metrics['median_ms']:.2f} ms")
        print(f"Min/Max:          {metrics['min_ms']:.2f} / {metrics['max_ms']:.2f} ms")
        print(f"Throughput:       {metrics['throughput_per_sec']:.1f} ops/sec")
        print(f"{'='*70}\n")

        # Performance assertions
        self.assertLess(metrics['mean_ms'], 200, "Large text PII detection should be under 200ms")

    def test_pii_redaction_speed(self):
        """Benchmark PII redaction performance."""
        metrics = PerformanceBenchmark.benchmark(
            lambda: self.privacy_manager.redact(self.multiple_pii_text, level=PrivacyLevel.PUBLIC),
            iterations=100
        )

        print(f"\n{'='*70}")
        print("PII REDACTION PERFORMANCE")
        print(f"{'='*70}")
        print(f"Text length:      {len(self.multiple_pii_text)} chars")
        print(f"PII instances:    ~10")
        print(f"Privacy level:    PUBLIC (most redaction)")
        print(f"Iterations:       {metrics['iterations']}")
        print(f"Mean time:        {metrics['mean_ms']:.2f} ms")
        print(f"Median time:      {metrics['median_ms']:.2f} ms")
        print(f"Min/Max:          {metrics['min_ms']:.2f} / {metrics['max_ms']:.2f} ms")
        print(f"Throughput:       {metrics['throughput_per_sec']:.1f} ops/sec")
        print(f"{'='*70}\n")

        # Performance assertions
        self.assertLess(metrics['mean_ms'], 50, "PII redaction should be under 50ms")


class TestDatabasePerformance(unittest.TestCase):
    """Benchmark database operation performance."""

    def setUp(self):
        """Set up test fixtures."""
        self.temp_dir = tempfile.mkdtemp()
        self.db_path = Path(self.temp_dir) / "perf_db.db"

        # Initialize database
        initializer = DatabaseInitializer(self.db_path, verbose=False)
        initializer.initialize()

        self.processor = NestedLearningProcessor(
            db_path=self.db_path,
            config_path=Path(self.temp_dir) / "config.json"
        )

    def tearDown(self):
        """Clean up test fixtures."""
        import shutil
        shutil.rmtree(self.temp_dir, ignore_errors=True)

    def test_single_pattern_insert_speed(self):
        """Benchmark single pattern insertion."""
        pattern = {
            'pattern_type': 'workflow',
            'name': 'Test workflow',
            'description': 'Test pattern',
            'pattern_data': {'steps': ['step1', 'step2']},
            'confidence': 0.8
        }

        metrics = PerformanceBenchmark.benchmark(
            lambda: self.processor.store_patterns([pattern]),
            iterations=100
        )

        print(f"\n{'='*70}")
        print("SINGLE PATTERN INSERT PERFORMANCE")
        print(f"{'='*70}")
        print(f"Iterations:       {metrics['iterations']}")
        print(f"Mean time:        {metrics['mean_ms']:.2f} ms")
        print(f"Median time:      {metrics['median_ms']:.2f} ms")
        print(f"Min/Max:          {metrics['min_ms']:.2f} / {metrics['max_ms']:.2f} ms")
        print(f"Throughput:       {metrics['throughput_per_sec']:.1f} inserts/sec")
        print(f"{'='*70}\n")

        # Performance assertions
        self.assertLess(metrics['mean_ms'], 20, "Single insert should be under 20ms")

    def test_bulk_pattern_insert_speed(self):
        """Benchmark bulk pattern insertion (100 patterns)."""
        patterns = [
            {
                'pattern_type': 'workflow',
                'name': f'Workflow {i}',
                'description': f'Pattern {i}',
                'pattern_data': {'steps': [f'step{j}' for j in range(5)]},
                'confidence': 0.8
            }
            for i in range(100)
        ]

        metrics = PerformanceBenchmark.benchmark(
            lambda: self.processor.store_patterns(patterns),
            iterations=10
        )

        print(f"\n{'='*70}")
        print("BULK PATTERN INSERT PERFORMANCE (100 patterns)")
        print(f"{'='*70}")
        print(f"Patterns/batch:   100")
        print(f"Iterations:       {metrics['iterations']}")
        print(f"Mean time:        {metrics['mean_ms']:.2f} ms")
        print(f"Median time:      {metrics['median_ms']:.2f} ms")
        print(f"Min/Max:          {metrics['min_ms']:.2f} / {metrics['max_ms']:.2f} ms")
        print(f"Patterns/sec:     {100 * metrics['throughput_per_sec']:.1f}")
        print(f"{'='*70}\n")

        # Performance assertions
        self.assertLess(metrics['mean_ms'], 1000, "Bulk insert should be under 1000ms")

    def test_pattern_query_speed(self):
        """Benchmark pattern query performance."""
        # First insert some patterns
        patterns = [
            {
                'pattern_type': 'workflow',
                'name': f'Pattern {i}',
                'description': 'Test',
                'pattern_data': {},
                'confidence': 0.8
            }
            for i in range(50)
        ]
        self.processor.store_patterns(patterns)

        metrics = PerformanceBenchmark.benchmark(
            lambda: self.processor.get_pattern_statistics(),
            iterations=100
        )

        print(f"\n{'='*70}")
        print("PATTERN QUERY PERFORMANCE")
        print(f"{'='*70}")
        print(f"Patterns in DB:   50")
        print(f"Iterations:       {metrics['iterations']}")
        print(f"Mean time:        {metrics['mean_ms']:.2f} ms")
        print(f"Median time:      {metrics['median_ms']:.2f} ms")
        print(f"Min/Max:          {metrics['min_ms']:.2f} / {metrics['max_ms']:.2f} ms")
        print(f"Throughput:       {metrics['throughput_per_sec']:.1f} queries/sec")
        print(f"{'='*70}\n")

        # Performance assertions
        self.assertLess(metrics['mean_ms'], 50, "Pattern query should be under 50ms")


class TestFullPipelinePerformance(unittest.TestCase):
    """Benchmark full MEMORY-CONTEXT pipeline performance."""

    def setUp(self):
        """Set up test fixtures."""
        self.temp_dir = tempfile.mkdtemp()
        self.db_path = Path(self.temp_dir) / "perf_pipeline.db"
        self.checkpoint_path = Path(self.temp_dir) / "checkpoint.md"

        # Initialize database
        initializer = DatabaseInitializer(self.db_path, verbose=False)
        initializer.initialize()

        # Create test checkpoint
        with open(self.checkpoint_path, 'w') as f:
            f.write("""# Test Checkpoint

## Work Completed
Implemented authentication system with JWT tokens.

## Decisions
- Use JWT for stateless auth
- Hash passwords with bcrypt

## Code Changes
- Created: src/auth.py
- Modified: src/api/routes.py
""")

        self.integration = MemoryContextIntegration(
            db_path=self.db_path,
            chroma_dir=Path(self.temp_dir) / "chroma"
        )

    def tearDown(self):
        """Clean up test fixtures."""
        import shutil
        shutil.rmtree(self.temp_dir, ignore_errors=True)

    def test_end_to_end_pipeline_speed(self):
        """Benchmark complete pipeline: checkpoint → database."""
        metrics = PerformanceBenchmark.benchmark(
            lambda: self.integration.process_checkpoint(
                checkpoint_path=self.checkpoint_path,
                privacy_level="TEAM",
                extract_patterns=True,
                store_in_db=True
            ),
            iterations=10
        )

        print(f"\n{'='*70}")
        print("END-TO-END PIPELINE PERFORMANCE")
        print(f"{'='*70}")
        print(f"Pipeline steps:   Export → Privacy → Patterns → Database")
        print(f"Iterations:       {metrics['iterations']}")
        print(f"Mean time:        {metrics['mean_ms']:.2f} ms")
        print(f"Median time:      {metrics['median_ms']:.2f} ms")
        print(f"Min/Max:          {metrics['min_ms']:.2f} / {metrics['max_ms']:.2f} ms")
        print(f"Std deviation:    {metrics['stdev_ms']:.2f} ms")
        print(f"Throughput:       {metrics['throughput_per_sec']:.1f} checkpoints/sec")
        print(f"{'='*70}\n")

        # Performance assertions
        self.assertLess(metrics['mean_ms'], 10000, "Full pipeline should be under 10 seconds")


if __name__ == '__main__':
    # Run with verbose output to see performance reports
    unittest.main(verbosity=2)
