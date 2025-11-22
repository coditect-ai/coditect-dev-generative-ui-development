# TOON Integration - Comprehensive Testing Strategy & Implementation

**Project:** CODITECT Rollout Master - TOON Format Integration
**Analysis Date:** 2025-11-17
**Author:** Test Engineering Specialist (AI-Assisted)
**Status:** Testing Strategy Complete - Ready for Implementation
**Priority:** P0 (Foundation for all TOON phases)

---

## Executive Summary

**Current State:** 0% test coverage for TOON integration (no tests exist)
**Target State:** 80%+ coverage with comprehensive test pyramid
**Risk Level:** HIGH - Production deployment without testing infrastructure
**Recommendation:** IMPLEMENT MINIMUM VIABLE TEST SUITE (Week 1) before Phase 2

### Critical Findings

| Category | Current | Target | Gap | Risk |
|----------|---------|--------|-----|------|
| **Unit Test Coverage** | 0% | 80%+ | 100% | 🔴 CRITICAL |
| **Integration Tests** | 0 tests | 50+ tests | 100% | 🔴 CRITICAL |
| **Security Tests** | 0 tests | 25+ tests | 100% | 🔴 CRITICAL |
| **Performance Tests** | 0 tests | 15+ tests | 100% | 🟡 HIGH |
| **E2E Tests** | 0 tests | 10+ tests | 100% | 🟡 HIGH |

### ROI Impact

**Without Testing:**
- ⚠️ Security vulnerabilities ship to production (path traversal, injection attacks)
- ⚠️ Performance regressions undetected (pre-commit hook delays)
- ⚠️ Data loss risk (checkpoint corruption)
- ⚠️ Integration failures between converters
- 💰 **Estimated cost of production failures:** $50K-$200K (downtime, data recovery, reputation)

**With Testing:**
- ✅ Catch 90%+ of bugs before production
- ✅ Prevent security vulnerabilities (OWASP Top 10)
- ✅ Validate token reduction claims (30-60%)
- ✅ Ensure data integrity across all converters
- 💰 **Testing investment:** $12K (Week 1-2), **ROI:** 4-16x return

---

## 1. Current State Analysis

### 1.1 Existing Testing Infrastructure

**coditect-framework (submodule):**
```
submodules/coditect-project-dot-claude/tests/
├── core/
│   ├── test_session_export.py (889 lines, comprehensive unit tests)
│   ├── test_privacy_manager.py
│   ├── test_memory_context_integration.py
│   ├── test_nested_learning.py
│   └── test_performance_benchmarks.py
├── conftest.py (missing - no fixtures defined)
└── pytest.ini (missing - no pytest configuration)
```

**Quality Assessment:**
- ✅ **Excellent example:** `test_session_export.py` demonstrates best practices
  - 100+ test cases
  - Edge case coverage
  - Mock usage (subprocess, file I/O)
  - Clear test naming
  - Proper setUp/tearDown
- ❌ **Missing infrastructure:**
  - No conftest.py with shared fixtures
  - No pytest.ini configuration
  - No CI/CD integration
  - No coverage reporting

**coditect-cloud-backend (submodule):**
```
submodules/coditect-cloud-backend/tests/
├── conftest.py (72 lines, good fixtures)
│   - db_session fixture (async)
│   - client fixture (HTTP client)
│   - Dependency injection for testing
└── pytest.ini (exists, basic configuration)
```

**Quality Assessment:**
- ✅ **Good infrastructure:** Async test fixtures, dependency injection
- ✅ **FastAPI patterns:** HTTP client testing ready
- ⚠️ **Limited scope:** Only 2 fixtures defined

### 1.2 TOON Integration Codebase

**Production Code:**
```
scripts/prototype_checkpoint_toon.py (248 lines)
├── TOONEncoder class (3 methods)
│   ├── encode_object() - nested dict encoding
│   ├── encode_array() - tabular array encoding
│   └── encode_primitive_array() - primitive list encoding
├── checkpoint_to_toon() - converter function
├── count_tokens() - token estimation (WRONG - uses char/4, not tiktoken)
└── demo_checkpoint_conversion() - CLI demonstration
```

**Test Code:**
```
None. Zero. Nada. 🚨
```

**Coverage Analysis:**
| Module | Lines | Complexity | Critical? | Tests | Coverage |
|--------|-------|------------|-----------|-------|----------|
| `TOONEncoder` | 73 | Medium | ✅ YES | 0 | 0% |
| `checkpoint_to_toon` | 5 | Low | ✅ YES | 0 | 0% |
| `count_tokens` | 8 | Low | ⚠️ WRONG | 0 | 0% |
| `demo_*` | 85 | Low | ❌ No | 0 | 0% |

### 1.3 Planned Components (Not Yet Implemented)

**Phase 1-8 Components (from TASKLIST):**
1. **TOON Utilities** (Week 1)
   - `scripts/utils/toon_encoder.py` - ⏸️ Not created
   - `scripts/utils/toon.ts` - ⏸️ Not created
   - `scripts/utils/token_counter.py` - ⏸️ Not created

2. **6 Converters** (Weeks 1-6)
   - `TOONMarkdownConverter` - ⏸️ Not created
   - `CheckpointConverter` - ⏸️ Not created
   - `TasklistConverter` - ⏸️ Not created
   - `SubmoduleStatusConverter` - ⏸️ Not created
   - `MemoryContextConverter` - ⏸️ Not created
   - `PDFToTOONConverter` - ⏸️ Not created

3. **Pre-commit Hook** (Week 2)
   - `.coditect/hooks/pre-commit-toon-sync.sh` - ⏸️ Not created

4. **API Integration** (Week 3-4)
   - Cloud backend TOON endpoints - ⏸️ Not created
   - Content negotiation (Accept: application/toon) - ⏸️ Not created

**Testing Gap:** 0% coverage for planned components = 100% risk

---

## 2. Test Pyramid Strategy

### 2.1 Test Pyramid Breakdown

**Recommended Distribution:**
```
        /\
       /10\     E2E Tests (10%)
      /    \    - Full workflow tests
     /------\   - User scenario tests
    /   20  \   Integration Tests (20%)
   /          \ - Converter integration
  /    70     \ - API + Database
 /--------------\ - Pre-commit hook
 Unit Tests (70%)  - TOON encoder/decoder
                   - Token counting
                   - Edge cases
```

**Target Metrics:**
- **Total Tests:** 150-200 tests
- **Unit Tests:** 105-140 tests (70%)
- **Integration Tests:** 30-40 tests (20%)
- **E2E Tests:** 15-20 tests (10%)
- **Coverage:** 80%+ for critical paths, 60%+ overall
- **Execution Time:** <30 seconds (unit), <5 minutes (integration), <15 minutes (E2E)

### 2.2 Test Categories and Priorities

| Category | Priority | Tests | Est. Hours | Deliverable Week |
|----------|----------|-------|------------|------------------|
| **Unit - TOON Encoding** | P0 | 35 | 8h | Week 1 |
| **Unit - Token Counting** | P0 | 15 | 3h | Week 1 |
| **Unit - Converters** | P0 | 40 | 10h | Week 1-2 |
| **Integration - Converters** | P0 | 20 | 6h | Week 2 |
| **Integration - API** | P1 | 15 | 5h | Week 3 |
| **Security - Injection** | P0 | 10 | 4h | Week 1 |
| **Security - Path Traversal** | P0 | 8 | 3h | Week 1 |
| **Performance - Benchmarks** | P1 | 12 | 6h | Week 2 |
| **E2E - Workflows** | P1 | 10 | 8h | Week 3 |
| **Regression - Existing** | P1 | 5 | 2h | Week 1 |
| **TOTAL** | | **170** | **55h** | **3 weeks** |

---

## 3. Unit Test Coverage Plan

### 3.1 TOONEncoder Test Suite

**File:** `tests/unit/test_toon_encoder.py`
**Target Coverage:** 95%+
**Estimated Tests:** 35 tests
**Priority:** P0 (foundation for all encoding)

#### Test Cases

**Basic Encoding:**
```python
class TestTOONEncoderBasic(unittest.TestCase):
    """Basic TOON encoding tests"""

    def test_encode_empty_object(self):
        """Test encoding empty dictionary"""
        result = TOONEncoder.encode_object({})
        self.assertEqual(result, "")

    def test_encode_simple_object(self):
        """Test encoding flat dictionary"""
        data = {"name": "test", "age": 30}
        result = TOONEncoder.encode_object(data)
        self.assertIn("name: test", result)
        self.assertIn("age: 30", result)

    def test_encode_nested_object(self):
        """Test encoding nested dictionaries"""
        data = {
            "person": {
                "name": "Alice",
                "address": {
                    "city": "NYC",
                    "zip": 10001
                }
            }
        }
        result = TOONEncoder.encode_object(data)
        self.assertIn("person:", result)
        self.assertIn("  name: Alice", result)
        self.assertIn("    city: NYC", result)

    def test_encode_array_empty(self):
        """Test encoding empty array"""
        result = TOONEncoder.encode_array("items", [])
        self.assertIn("items[0]: (empty)", result)

    def test_encode_array_single_item(self):
        """Test encoding single-item array"""
        items = [{"id": 1, "name": "Item1"}]
        result = TOONEncoder.encode_array("items", items)
        self.assertIn("items[1]{id,name}:", result)
        self.assertIn("1,Item1", result)

    def test_encode_array_multiple_items(self):
        """Test encoding multi-item array"""
        items = [
            {"id": 1, "name": "Item1"},
            {"id": 2, "name": "Item2"}
        ]
        result = TOONEncoder.encode_array("items", items)
        self.assertIn("items[2]{id,name}:", result)
        lines = result.split('\n')
        self.assertEqual(len(lines), 3)  # Header + 2 items

    def test_encode_primitive_array(self):
        """Test encoding primitive value arrays"""
        result = TOONEncoder.encode_primitive_array("tags", ["auth", "api", "test"])
        self.assertIn("tags[3]: auth,api,test", result)
```

**Edge Cases:**
```python
class TestTOONEncoderEdgeCases(unittest.TestCase):
    """Edge case handling"""

    def test_encode_special_characters(self):
        """Test encoding values with special characters"""
        data = {"message": "Hello, World!", "path": "/usr/bin"}
        result = TOONEncoder.encode_object(data)
        # Should quote values with commas
        self.assertIn('"Hello, World!"', result)

    def test_encode_unicode_characters(self):
        """Test encoding Unicode characters"""
        data = {"name": "José", "symbol": "€"}
        result = TOONEncoder.encode_object(data)
        self.assertIn("José", result)
        self.assertIn("€", result)

    def test_encode_very_long_string(self):
        """Test encoding strings longer than 1000 characters"""
        long_string = "x" * 2000
        data = {"content": long_string}
        result = TOONEncoder.encode_object(data)
        self.assertIn(long_string, result)

    def test_encode_deeply_nested_object(self):
        """Test encoding object nested 10+ levels deep"""
        data = {"a": {"b": {"c": {"d": {"e": {
            "f": {"g": {"h": {"i": {"j": "deep"}}}}
        }}}}}}
        result = TOONEncoder.encode_object(data)
        self.assertIn("deep", result)
        # Count indentation levels
        indent_count = result.count("  j:")
        self.assertGreater(indent_count, 0)

    def test_encode_mixed_array_types(self):
        """Test encoding array with mixed field sets"""
        items = [
            {"id": 1, "name": "Item1"},
            {"id": 2, "name": "Item2", "extra": "field"},  # Extra field
            {"id": 3}  # Missing name
        ]
        result = TOONEncoder.encode_array("items", items)
        # Should include all fields from all items
        self.assertIn("extra", result)
        # Should handle missing values
        self.assertIn(",,", result)  # Empty name for item 3

    def test_encode_null_values(self):
        """Test encoding None/null values"""
        data = {"value": None, "count": 0}
        result = TOONEncoder.encode_object(data)
        self.assertIn("value: ", result)  # Empty or "None"

    def test_encode_boolean_values(self):
        """Test encoding True/False values"""
        data = {"active": True, "deleted": False}
        result = TOONEncoder.encode_object(data)
        self.assertIn("active: True", result)
        self.assertIn("deleted: False", result)

    def test_encode_numeric_edge_cases(self):
        """Test encoding special numeric values"""
        data = {
            "zero": 0,
            "negative": -999,
            "float": 3.14159,
            "large": 999999999999999
        }
        result = TOONEncoder.encode_object(data)
        self.assertIn("zero: 0", result)
        self.assertIn("negative: -999", result)
```

**Error Handling:**
```python
class TestTOONEncoderErrors(unittest.TestCase):
    """Error handling tests"""

    def test_encode_invalid_input_type(self):
        """Test encoding non-dict raises TypeError"""
        with self.assertRaises(TypeError):
            TOONEncoder.encode_object("not a dict")

    def test_encode_circular_reference(self):
        """Test encoding circular reference raises error"""
        data = {"self": None}
        data["self"] = data  # Circular reference
        with self.assertRaises(RecursionError):
            TOONEncoder.encode_object(data)

    def test_encode_unserializable_object(self):
        """Test encoding non-serializable objects"""
        import datetime
        data = {"date": datetime.datetime.now()}
        # Should convert to string or raise error
        result = TOONEncoder.encode_object(data)
        # Verify it's handled somehow
        self.assertIsInstance(result, str)
```

**Assertion Density Target:** 2.5 assertions per test (87.5 assertions across 35 tests)

### 3.2 Token Counting Test Suite

**File:** `tests/unit/test_token_counter.py`
**Target Coverage:** 100%
**Estimated Tests:** 15 tests
**Priority:** P0 (validates ROI claims)

#### Critical Test Cases

```python
class TestTokenCounter(unittest.TestCase):
    """Token counting accuracy tests"""

    def setUp(self):
        """Set up token counter (using tiktoken)"""
        import tiktoken
        self.encoding = tiktoken.get_encoding("cl100k_base")  # Claude encoding

    def test_count_tokens_simple_text(self):
        """Test token counting for simple text"""
        text = "Hello, World!"
        expected = len(self.encoding.encode(text))
        actual = count_tokens(text)
        self.assertEqual(actual, expected)

    def test_count_tokens_json_format(self):
        """Test token counting for JSON"""
        json_text = '{"name": "test", "value": 123}'
        expected = len(self.encoding.encode(json_text))
        actual = count_tokens(json_text)
        self.assertEqual(actual, expected)

    def test_count_tokens_toon_format(self):
        """Test token counting for TOON"""
        toon_text = "name: test\nvalue: 123"
        expected = len(self.encoding.encode(toon_text))
        actual = count_tokens(toon_text)
        self.assertEqual(actual, expected)

    def test_token_reduction_checkpoint(self):
        """Test TOON achieves 30-60% reduction for checkpoint data"""
        checkpoint_data = create_sample_checkpoint_data()
        json_text = checkpoint_to_json(checkpoint_data)
        toon_text = checkpoint_to_toon(checkpoint_data)

        json_tokens = count_tokens(json_text)
        toon_tokens = count_tokens(toon_text)

        reduction = (json_tokens - toon_tokens) / json_tokens * 100

        # Validate ROI claim: 30-60% reduction
        self.assertGreaterEqual(reduction, 30, "TOON reduction below 30% target")
        self.assertLessEqual(reduction, 70, "TOON reduction suspiciously high")

    def test_token_reduction_tasklist(self):
        """Test TOON reduction for TASKLIST data"""
        # Create sample TASKLIST with 50 tasks
        tasks = [
            {"id": i, "status": "pending", "title": f"Task {i}"}
            for i in range(50)
        ]
        json_text = json.dumps(tasks, indent=2)
        toon_text = TOONEncoder.encode_array("tasks", tasks)

        reduction = (count_tokens(json_text) - count_tokens(toon_text)) / count_tokens(json_text) * 100
        self.assertGreater(reduction, 40, "TASKLIST reduction below expected")

    def test_count_tokens_empty_string(self):
        """Test token counting for empty string"""
        self.assertEqual(count_tokens(""), 0)

    def test_count_tokens_unicode(self):
        """Test token counting for Unicode text"""
        text = "Hello 世界 🌍"
        tokens = count_tokens(text)
        self.assertGreater(tokens, 0)

    def test_count_tokens_very_long_text(self):
        """Test token counting for 100K+ character text"""
        long_text = "x" * 100000
        tokens = count_tokens(long_text)
        # Should handle large text without error
        self.assertGreater(tokens, 10000)
```

**Performance Benchmarks:**
```python
class TestTokenCounterPerformance(unittest.TestCase):
    """Performance tests for token counting"""

    def test_token_counting_performance(self):
        """Test token counting completes in <100ms for 10KB text"""
        import time
        text = "test " * 2000  # ~10KB
        start = time.time()
        count_tokens(text)
        elapsed = time.time() - start
        self.assertLess(elapsed, 0.1, "Token counting too slow")

    def test_token_counting_scales_linearly(self):
        """Test token counting scales linearly with text size"""
        import time
        sizes = [1000, 5000, 10000, 50000]
        times = []
        for size in sizes:
            text = "x" * size
            start = time.time()
            count_tokens(text)
            times.append(time.time() - start)

        # Check linearity: time_ratio ≈ size_ratio
        time_ratio = times[-1] / times[0]
        size_ratio = sizes[-1] / sizes[0]
        # Allow 2x variance
        self.assertLess(time_ratio, size_ratio * 2)
```

### 3.3 Converter Unit Tests

**File:** `tests/unit/test_converters.py`
**Target Coverage:** 85%+
**Estimated Tests:** 40 tests (10 per converter x 4 converters)
**Priority:** P0

#### Test Structure (per converter)

```python
class TestCheckpointConverter(unittest.TestCase):
    """Checkpoint → TOON converter tests"""

    def setUp(self):
        self.temp_dir = tempfile.mkdtemp()
        self.converter = CheckpointConverter()

    def tearDown(self):
        shutil.rmtree(self.temp_dir)

    # 1. Happy Path Tests
    def test_convert_checkpoint_to_toon(self):
        """Test converting checkpoint.md to checkpoint.toon"""
        # Create sample checkpoint
        checkpoint_path = Path(self.temp_dir) / "checkpoint.md"
        checkpoint_path.write_text(SAMPLE_CHECKPOINT_MARKDOWN)

        # Convert
        toon_path = self.converter.convert_to_toon(checkpoint_path)

        # Verify
        self.assertTrue(toon_path.exists())
        self.assertEqual(toon_path.suffix, ".toon")
        toon_content = toon_path.read_text()
        self.assertIn("checkpoint:", toon_content)

    def test_convert_toon_to_markdown(self):
        """Test converting checkpoint.toon to checkpoint.md"""
        # Create sample TOON checkpoint
        toon_path = Path(self.temp_dir) / "checkpoint.toon"
        toon_path.write_text(SAMPLE_CHECKPOINT_TOON)

        # Convert
        md_path = self.converter.convert_to_markdown(toon_path)

        # Verify
        self.assertTrue(md_path.exists())
        md_content = md_path.read_text()
        self.assertIn("# Checkpoint", md_content)

    # 2. Data Integrity Tests
    def test_roundtrip_conversion_preserves_data(self):
        """Test MD → TOON → MD preserves all data"""
        original_md = Path(self.temp_dir) / "original.md"
        original_md.write_text(SAMPLE_CHECKPOINT_MARKDOWN)

        # Convert MD → TOON → MD
        toon_path = self.converter.convert_to_toon(original_md)
        restored_md = self.converter.convert_to_markdown(toon_path)

        # Compare (should be semantically equivalent)
        original_data = parse_checkpoint_md(original_md)
        restored_data = parse_checkpoint_md(restored_md)
        self.assertEqual(original_data, restored_data)

    def test_conversion_preserves_task_count(self):
        """Test conversion preserves all tasks"""
        checkpoint_data = {
            "tasks_completed": [{"task": f"Task {i}"} for i in range(100)]
        }
        toon = checkpoint_to_toon(checkpoint_data)
        restored_data = toon_to_checkpoint(toon)
        self.assertEqual(len(restored_data["tasks_completed"]), 100)

    # 3. Edge Case Tests
    def test_convert_empty_checkpoint(self):
        """Test converting checkpoint with no tasks"""
        checkpoint_path = Path(self.temp_dir) / "empty.md"
        checkpoint_path.write_text("# Checkpoint\n\nNo work completed.")
        toon_path = self.converter.convert_to_toon(checkpoint_path)
        self.assertTrue(toon_path.exists())

    def test_convert_checkpoint_with_special_chars(self):
        """Test checkpoint with special characters in commit messages"""
        # Commit messages with quotes, commas, pipes
        pass

    # 4. Error Handling Tests
    def test_convert_nonexistent_file_raises_error(self):
        """Test converting non-existent file raises FileNotFoundError"""
        with self.assertRaises(FileNotFoundError):
            self.converter.convert_to_toon(Path("/nonexistent.md"))

    def test_convert_invalid_markdown_raises_error(self):
        """Test converting malformed markdown raises ValueError"""
        invalid_md = Path(self.temp_dir) / "invalid.md"
        invalid_md.write_text("Not a valid checkpoint")
        with self.assertRaises(ValueError):
            self.converter.convert_to_toon(invalid_md)

    # 5. Metrics Validation
    def test_conversion_returns_metrics(self):
        """Test conversion returns token reduction metrics"""
        checkpoint_path = Path(self.temp_dir) / "checkpoint.md"
        checkpoint_path.write_text(SAMPLE_CHECKPOINT_MARKDOWN)

        metrics = self.converter.convert_to_toon(checkpoint_path, return_metrics=True)

        self.assertIn("tokens_before", metrics)
        self.assertIn("tokens_after", metrics)
        self.assertIn("reduction_percent", metrics)
        self.assertGreater(metrics["reduction_percent"], 0)

    # 6. Performance Tests
    def test_convert_large_checkpoint_performance(self):
        """Test converting large checkpoint (1000+ tasks) completes in <5s"""
        import time
        large_checkpoint = create_large_checkpoint(1000)
        checkpoint_path = Path(self.temp_dir) / "large.md"
        checkpoint_path.write_text(large_checkpoint)

        start = time.time()
        self.converter.convert_to_toon(checkpoint_path)
        elapsed = time.time() - start

        self.assertLess(elapsed, 5.0, "Conversion too slow for large checkpoint")
```

**Repeat similar structure for:**
- `TestTasklistConverter` (40 tests)
- `TestSubmoduleStatusConverter` (10 tests)
- `TestMemoryContextConverter` (15 tests)

---

## 4. Integration Test Plan

### 4.1 Converter Integration Tests

**File:** `tests/integration/test_converter_integration.py`
**Target Coverage:** Full converter pipeline
**Estimated Tests:** 20 tests
**Priority:** P0

#### Test Scenarios

```python
class TestConverterIntegration(unittest.TestCase):
    """Integration tests for converter pipeline"""

    def test_checkpoint_creation_with_toon_output(self):
        """Test create-checkpoint.py generates both .toon and .md files"""
        # Run create-checkpoint.py
        result = subprocess.run(
            ["python3", "scripts/create-checkpoint.py", "Test checkpoint", "--auto-commit"],
            cwd=repo_root,
            capture_output=True
        )

        # Verify both formats created
        checkpoints_dir = repo_root / "CHECKPOINTS"
        toon_files = list(checkpoints_dir.glob("*.toon"))
        md_files = list(checkpoints_dir.glob("*.md"))

        self.assertGreater(len(toon_files), 0, "No .toon file created")
        self.assertGreater(len(md_files), 0, "No .md file created")

        # Verify files have same basename
        toon_basename = toon_files[0].stem
        md_basename = md_files[0].stem
        self.assertEqual(toon_basename, md_basename)

    def test_checkpoint_loading_prefers_toon(self):
        """Test checkpoint loading prefers .toon over .md when both exist"""
        # Create both formats
        checkpoint_data = create_sample_checkpoint_data()
        checkpoint_path = Path("test-checkpoint")

        toon_path = checkpoint_path.with_suffix(".toon")
        md_path = checkpoint_path.with_suffix(".md")

        toon_path.write_text(checkpoint_to_toon(checkpoint_data))
        md_path.write_text(checkpoint_to_markdown(checkpoint_data))

        # Load (should prefer .toon)
        loaded_data = load_checkpoint(checkpoint_path)

        # Verify loaded from TOON (check metadata or format-specific marker)
        self.assertEqual(loaded_data["format"], "toon")

    def test_tasklist_generation_dual_format(self):
        """Test TASKLIST generation creates both formats"""
        # Similar to checkpoint test
        pass

    def test_converter_dependency_chain(self):
        """Test converters can chain: MD → TOON → JSON → HTML"""
        # Create markdown file
        md_path = Path("test.md")
        md_path.write_text("# Test\n\nContent")

        # Convert MD → TOON
        toon_path = markdown_to_toon(md_path)
        self.assertTrue(toon_path.exists())

        # Convert TOON → JSON
        json_path = toon_to_json(toon_path)
        self.assertTrue(json_path.exists())

        # Verify data integrity across conversions
        original_data = parse_markdown(md_path)
        final_data = json.loads(json_path.read_text())
        self.assertEqual(original_data, final_data)
```

### 4.2 API Integration Tests

**File:** `tests/integration/test_api_toon_endpoints.py`
**Target Coverage:** TOON content negotiation
**Estimated Tests:** 15 tests
**Priority:** P1 (Week 3)

#### Test Cases

```python
class TestAPITOONEndpoints(unittest.TestCase):
    """API TOON content negotiation tests"""

    @pytest.fixture
    async def client(self):
        """FastAPI test client with database"""
        # Use existing conftest.py fixture
        pass

    async def test_api_accepts_toon_content_type(self):
        """Test API accepts Accept: application/toon header"""
        response = await client.get(
            "/api/v1/checkpoints/latest",
            headers={"Accept": "application/toon"}
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.headers["Content-Type"], "application/toon")

    async def test_api_returns_toon_format(self):
        """Test API returns valid TOON format"""
        response = await client.get(
            "/api/v1/checkpoints/latest",
            headers={"Accept": "application/toon"}
        )
        content = response.text

        # Verify TOON format characteristics
        self.assertRegex(content, r"checkpoint:")
        self.assertNotIn("{", content)  # No JSON braces
        self.assertNotIn("}", content)

    async def test_api_fallback_to_json(self):
        """Test API falls back to JSON when TOON not accepted"""
        response = await client.get(
            "/api/v1/checkpoints/latest",
            headers={"Accept": "application/json"}
        )
        self.assertEqual(response.headers["Content-Type"], "application/json")

    async def test_api_dual_format_session_export(self):
        """Test session export endpoint returns both formats"""
        response = await client.post("/api/v1/sessions/export")
        data = response.json()

        self.assertIn("toon_url", data)
        self.assertIn("markdown_url", data)

        # Verify both files downloadable
        toon_response = await client.get(data["toon_url"])
        md_response = await client.get(data["markdown_url"])

        self.assertEqual(toon_response.status_code, 200)
        self.assertEqual(md_response.status_code, 200)
```

### 4.3 Pre-commit Hook Integration Tests

**File:** `tests/integration/test_precommit_hook.py`
**Target Coverage:** Git workflow integration
**Estimated Tests:** 10 tests
**Priority:** P0 (critical path)

```python
class TestPrecommitHook(unittest.TestCase):
    """Pre-commit hook tests"""

    def setUp(self):
        """Create temporary git repo"""
        self.temp_repo = tempfile.mkdtemp()
        subprocess.run(["git", "init"], cwd=self.temp_repo)
        # Install pre-commit hook
        shutil.copy(
            ".coditect/hooks/pre-commit-toon-sync.sh",
            f"{self.temp_repo}/.git/hooks/pre-commit"
        )
        os.chmod(f"{self.temp_repo}/.git/hooks/pre-commit", 0o755)

    def test_precommit_syncs_toon_to_markdown(self):
        """Test pre-commit hook generates .md from .toon"""
        # Create .toon file
        checkpoint_toon = Path(self.temp_repo) / "checkpoint.toon"
        checkpoint_toon.write_text("checkpoint:\n  status: complete")

        # Stage .toon file
        subprocess.run(["git", "add", "checkpoint.toon"], cwd=self.temp_repo)

        # Commit (triggers hook)
        result = subprocess.run(
            ["git", "commit", "-m", "Test commit"],
            cwd=self.temp_repo,
            capture_output=True
        )

        # Verify .md file generated and staged
        checkpoint_md = Path(self.temp_repo) / "checkpoint.md"
        self.assertTrue(checkpoint_md.exists(), "Pre-commit hook didn't generate .md")

        # Verify .md file staged
        git_status = subprocess.run(
            ["git", "status", "--porcelain"],
            cwd=self.temp_repo,
            capture_output=True,
            text=True
        )
        self.assertIn("checkpoint.md", git_status.stdout)

    def test_precommit_hook_performance(self):
        """Test pre-commit hook completes in <3 seconds"""
        import time
        # Create 10 .toon files
        for i in range(10):
            toon_file = Path(self.temp_repo) / f"checkpoint_{i}.toon"
            toon_file.write_text(f"checkpoint:\n  id: {i}")
            subprocess.run(["git", "add", str(toon_file)], cwd=self.temp_repo)

        # Time commit
        start = time.time()
        subprocess.run(["git", "commit", "-m", "Test"], cwd=self.temp_repo)
        elapsed = time.time() - start

        self.assertLess(elapsed, 3.0, "Pre-commit hook too slow")

    def test_precommit_hook_fails_on_invalid_toon(self):
        """Test pre-commit hook rejects invalid TOON syntax"""
        # Create invalid .toon file
        invalid_toon = Path(self.temp_repo) / "invalid.toon"
        invalid_toon.write_text("{{invalid TOON syntax}}")

        subprocess.run(["git", "add", "invalid.toon"], cwd=self.temp_repo)

        # Commit should fail
        result = subprocess.run(
            ["git", "commit", "-m", "Test"],
            cwd=self.temp_repo,
            capture_output=True
        )
        self.assertNotEqual(result.returncode, 0, "Pre-commit hook didn't reject invalid TOON")
```

---

## 5. Security Testing

### 5.1 Injection Attack Tests

**File:** `tests/security/test_injection_attacks.py`
**Target Coverage:** OWASP Top 10 - Injection
**Estimated Tests:** 10 tests
**Priority:** P0 (CRITICAL)

```python
class TestTOONInjectionAttacks(unittest.TestCase):
    """Test TOON parser against injection attacks"""

    def test_toon_parser_sql_injection_attempt(self):
        """Test TOON parser rejects SQL injection in field names"""
        malicious_toon = """
        tasks[1]{id,name,'; DROP TABLE tasks; --}:
         1,Task1,malicious
        """
        with self.assertRaises(ValueError):
            parse_toon(malicious_toon)

    def test_toon_parser_command_injection_attempt(self):
        """Test TOON parser rejects command injection in values"""
        malicious_toon = """
        file: $(rm -rf /)
        """
        parsed = parse_toon(malicious_toon)
        # Should be treated as literal string, not executed
        self.assertEqual(parsed["file"], "$(rm -rf /)")

    def test_toon_parser_xss_attempt(self):
        """Test TOON parser escapes XSS payloads"""
        malicious_toon = """
        message: <script>alert('XSS')</script>
        """
        parsed = parse_toon(malicious_toon)
        # When converted to HTML, should be escaped
        html = toon_to_html(malicious_toon)
        self.assertNotIn("<script>", html)
        self.assertIn("&lt;script&gt;", html)

    def test_toon_parser_path_traversal_attempt(self):
        """Test TOON parser rejects path traversal in field names"""
        malicious_toon = """
        ../../../etc/passwd: hacked
        """
        with self.assertRaises(ValueError):
            parse_toon(malicious_toon)

    def test_toon_encoder_sanitizes_untrusted_input(self):
        """Test TOON encoder sanitizes untrusted user input"""
        untrusted_data = {
            "user_input": "<script>alert('XSS')</script>",
            "file_path": "../../etc/passwd"
        }
        toon_output = TOONEncoder.encode_object(untrusted_data)
        # Should escape or reject dangerous characters
        self.assertNotIn("<script>", toon_output)
```

### 5.2 Path Traversal Tests

**File:** `tests/security/test_path_traversal.py`
**Target Coverage:** File system security
**Estimated Tests:** 8 tests
**Priority:** P0

```python
class TestPathTraversal(unittest.TestCase):
    """Test protection against path traversal attacks"""

    def test_checkpoint_loader_rejects_parent_directory_traversal(self):
        """Test checkpoint loader rejects ../ in path"""
        malicious_path = "../../etc/passwd"
        with self.assertRaises(ValueError):
            load_checkpoint(malicious_path)

    def test_converter_validates_output_path(self):
        """Test converter rejects output paths outside allowed directories"""
        converter = CheckpointConverter()
        with self.assertRaises(ValueError):
            converter.convert_to_toon(
                input_path="checkpoint.md",
                output_path="../../../etc/passwd"
            )

    def test_file_operations_restricted_to_repo_root(self):
        """Test file operations cannot access files outside repo"""
        # Attempt to read /etc/passwd
        with self.assertRaises(PermissionError):
            read_checkpoint("/etc/passwd")

    def test_symlink_attack_prevention(self):
        """Test system rejects symlinks pointing outside repo"""
        # Create symlink to /etc/passwd
        symlink_path = Path("checkpoint.toon")
        symlink_path.symlink_to("/etc/passwd")

        # Attempt to read via symlink
        with self.assertRaises(SecurityError):
            load_checkpoint(symlink_path)
```

### 5.3 Multi-Tenant Isolation Tests

**File:** `tests/security/test_multi_tenant_isolation.py`
**Target Coverage:** Cloud backend multi-tenancy
**Estimated Tests:** 7 tests
**Priority:** P1 (cloud backend integration)

```python
class TestMultiTenantIsolation(unittest.TestCase):
    """Test tenant data isolation in cloud backend"""

    async def test_tenant_cannot_access_other_tenant_checkpoints(self):
        """Test tenant A cannot access tenant B's checkpoints"""
        # Create checkpoint for tenant A
        tenant_a_token = get_auth_token(tenant_id="tenant-a")
        response_a = await client.post(
            "/api/v1/checkpoints",
            json={"data": "Tenant A checkpoint"},
            headers={"Authorization": f"Bearer {tenant_a_token}"}
        )
        checkpoint_id = response_a.json()["id"]

        # Attempt to access from tenant B
        tenant_b_token = get_auth_token(tenant_id="tenant-b")
        response_b = await client.get(
            f"/api/v1/checkpoints/{checkpoint_id}",
            headers={"Authorization": f"Bearer {tenant_b_token}"}
        )

        self.assertEqual(response_b.status_code, 403, "Tenant isolation violated")

    async def test_sql_injection_cannot_bypass_tenant_filter(self):
        """Test SQL injection cannot bypass tenant_id filtering"""
        malicious_token = get_auth_token(tenant_id="tenant-a' OR '1'='1")
        response = await client.get(
            "/api/v1/checkpoints",
            headers={"Authorization": f"Bearer {malicious_token}"}
        )
        # Should only return tenant-a's checkpoints, not all checkpoints
        data = response.json()
        self.assertLessEqual(len(data), 10)  # Not all tenants' data
```

---

## 6. Performance Testing

### 6.1 Performance Benchmarks

**File:** `tests/performance/test_toon_performance.py`
**Target Coverage:** Performance SLAs
**Estimated Tests:** 12 tests
**Priority:** P1

```python
class TestTOONPerformance(unittest.TestCase):
    """Performance benchmark tests"""

    def test_toon_encoding_performance_small_dataset(self):
        """Test TOON encoding 1KB data completes in <10ms"""
        import time
        data = create_sample_data(size_kb=1)

        start = time.time()
        toon_output = checkpoint_to_toon(data)
        elapsed = time.time() - start

        self.assertLess(elapsed, 0.01, "TOON encoding too slow for small dataset")

    def test_toon_encoding_performance_large_dataset(self):
        """Test TOON encoding 100KB data completes in <500ms"""
        import time
        data = create_sample_data(size_kb=100)

        start = time.time()
        toon_output = checkpoint_to_toon(data)
        elapsed = time.time() - start

        self.assertLess(elapsed, 0.5, "TOON encoding too slow for large dataset")

    def test_token_counting_performance_baseline(self):
        """Test token counting 10KB text completes in <100ms"""
        import time
        text = "test " * 2000  # ~10KB

        start = time.time()
        count_tokens(text)
        elapsed = time.time() - start

        self.assertLess(elapsed, 0.1, "Token counting performance regression")

    def test_precommit_hook_performance_10_files(self):
        """Test pre-commit hook processes 10 files in <3 seconds"""
        # Measured in integration tests (see section 4.3)
        pass

    def test_memory_usage_large_checkpoint(self):
        """Test memory usage for 10MB checkpoint stays under 100MB"""
        import tracemalloc
        tracemalloc.start()

        large_checkpoint = create_large_checkpoint(size_mb=10)
        toon_output = checkpoint_to_toon(large_checkpoint)

        current, peak = tracemalloc.get_traced_memory()
        tracemalloc.stop()

        # Peak memory should be reasonable (< 100MB for 10MB input)
        self.assertLess(peak / 1024 / 1024, 100, "Memory usage too high")

    def test_toon_decoding_performance(self):
        """Test TOON → JSON decoding performance"""
        import time
        toon_text = create_large_toon(size_kb=100)

        start = time.time()
        json_data = toon_to_json(toon_text)
        elapsed = time.time() - start

        self.assertLess(elapsed, 0.3, "TOON decoding too slow")
```

### 6.2 Load Testing

**File:** `tests/performance/test_load.py`
**Target Coverage:** Concurrent request handling
**Estimated Tests:** 5 tests
**Priority:** P2 (post-MVP)

```python
class TestLoadTesting(unittest.TestCase):
    """Load testing for API endpoints"""

    async def test_api_handles_100_concurrent_requests(self):
        """Test API handles 100 concurrent checkpoint requests"""
        import asyncio

        async def fetch_checkpoint():
            return await client.get("/api/v1/checkpoints/latest")

        # Send 100 concurrent requests
        tasks = [fetch_checkpoint() for _ in range(100)]
        responses = await asyncio.gather(*tasks)

        # All should succeed
        success_count = sum(1 for r in responses if r.status_code == 200)
        self.assertGreater(success_count, 95, "Too many failures under load")

    def test_converter_throughput(self):
        """Test converter processes 1000 checkpoints in <5 minutes"""
        import time
        converter = CheckpointConverter()

        start = time.time()
        for i in range(1000):
            checkpoint_path = create_temp_checkpoint(f"checkpoint_{i}")
            converter.convert_to_toon(checkpoint_path)
        elapsed = time.time() - start

        self.assertLess(elapsed, 300, "Converter throughput too low")
```

---

## 7. End-to-End Testing

### 7.1 E2E Workflow Tests

**File:** `tests/e2e/test_workflows.py`
**Target Coverage:** User scenarios
**Estimated Tests:** 10 tests
**Priority:** P1

```python
class TestE2EWorkflows(unittest.TestCase):
    """End-to-end user workflow tests"""

    def test_create_checkpoint_workflow(self):
        """Test complete checkpoint creation workflow"""
        # Step 1: User creates checkpoint
        result = subprocess.run(
            ["python3", "scripts/create-checkpoint.py", "E2E Test", "--auto-commit"],
            cwd=repo_root,
            capture_output=True
        )
        self.assertEqual(result.returncode, 0)

        # Step 2: Verify .toon and .md files created
        checkpoints_dir = repo_root / "CHECKPOINTS"
        latest_toon = max(checkpoints_dir.glob("*.toon"), key=lambda p: p.stat().st_mtime)
        latest_md = max(checkpoints_dir.glob("*.md"), key=lambda p: p.stat().st_mtime)

        self.assertTrue(latest_toon.exists())
        self.assertTrue(latest_md.exists())

        # Step 3: Claude Code reads .toon file
        checkpoint_data = load_checkpoint(latest_toon)
        self.assertIn("checkpoint", checkpoint_data)

        # Step 4: Human views .md file on GitHub
        md_content = latest_md.read_text()
        self.assertIn("# Checkpoint", md_content)

    def test_tasklist_generation_workflow(self):
        """Test TASKLIST generation and agent consumption workflow"""
        # Step 1: Generate TASKLIST
        result = subprocess.run(
            ["python3", "scripts/generate-tasklist.py", "Project X"],
            cwd=repo_root,
            capture_output=True
        )

        # Step 2: Verify dual formats
        tasklist_toon = repo_root / "TASKLIST.toon"
        tasklist_md = repo_root / "TASKLIST.md"
        self.assertTrue(tasklist_toon.exists())
        self.assertTrue(tasklist_md.exists())

        # Step 3: Agent reads TOON
        tasks = parse_toon_tasklist(tasklist_toon)
        self.assertGreater(len(tasks), 0)

        # Step 4: Human edits .md on GitHub
        # Simulate edit
        md_content = tasklist_md.read_text()
        md_content += "\n- [ ] New task from human"
        tasklist_md.write_text(md_content)

        # Step 5: Pre-commit hook syncs .md → .toon
        subprocess.run(["git", "add", "TASKLIST.md"], cwd=repo_root)
        subprocess.run(["git", "commit", "-m", "Update TASKLIST"], cwd=repo_root)

        # Step 6: Verify .toon updated
        updated_tasks = parse_toon_tasklist(tasklist_toon)
        task_titles = [t["title"] for t in updated_tasks]
        self.assertIn("New task from human", task_titles)

    def test_session_export_workflow(self):
        """Test MEMORY-CONTEXT session export workflow"""
        # Step 1: Export session from checkpoint
        checkpoint_path = create_test_checkpoint()
        result = subprocess.run(
            ["python3", "scripts/export-session.py", str(checkpoint_path)],
            cwd=repo_root,
            capture_output=True
        )

        # Step 2: Verify TOON and JSON exports created
        exports_dir = repo_root / "MEMORY-CONTEXT" / "exports"
        toon_exports = list(exports_dir.glob("*.toon"))
        json_exports = list(exports_dir.glob("*.json"))

        self.assertGreater(len(toon_exports), 0)
        self.assertGreater(len(json_exports), 0)

        # Step 3: Claude Code loads session context from TOON
        session_data = load_session_export(toon_exports[0])
        self.assertIn("conversation", session_data)

    def test_cloud_dashboard_workflow(self):
        """Test cloud dashboard displays TOON data"""
        # Step 1: Upload checkpoint to cloud backend
        with open(create_test_checkpoint(), "rb") as f:
            response = await client.post(
                "/api/v1/checkpoints/upload",
                files={"file": f}
            )
        self.assertEqual(response.status_code, 200)

        # Step 2: Request TOON format from API
        checkpoint_id = response.json()["id"]
        toon_response = await client.get(
            f"/api/v1/checkpoints/{checkpoint_id}",
            headers={"Accept": "application/toon"}
        )
        self.assertEqual(toon_response.headers["Content-Type"], "application/toon")

        # Step 3: Request Markdown format for web UI
        md_response = await client.get(
            f"/api/v1/checkpoints/{checkpoint_id}",
            headers={"Accept": "text/markdown"}
        )
        self.assertEqual(md_response.headers["Content-Type"], "text/markdown")
```

---

## 8. Test Infrastructure Setup

### 8.1 pytest Configuration

**File:** `pytest.ini`

```ini
[pytest]
# Test discovery
testpaths = tests
python_files = test_*.py
python_classes = Test*
python_functions = test_*

# Output
addopts =
    -v
    --strict-markers
    --tb=short
    --cov=scripts
    --cov=src
    --cov-report=html:htmlcov
    --cov-report=term-missing:skip-covered
    --cov-fail-under=60

# Markers
markers =
    unit: Unit tests (fast, isolated)
    integration: Integration tests (slower, requires infrastructure)
    e2e: End-to-end tests (slowest, full system)
    security: Security tests (injection, path traversal)
    performance: Performance benchmark tests
    slow: Slow-running tests (>5 seconds)

# Async support
asyncio_mode = auto

# Coverage
[coverage:run]
source = scripts,src
omit =
    */tests/*
    */venv/*
    */__pycache__/*

[coverage:report]
precision = 2
skip_covered = False
show_missing = True
```

### 8.2 conftest.py (Shared Fixtures)

**File:** `tests/conftest.py`

```python
"""
Shared pytest fixtures for TOON integration tests
"""

import pytest
import tempfile
import shutil
from pathlib import Path
import subprocess

@pytest.fixture(scope="session")
def repo_root():
    """Get repository root directory"""
    return Path(__file__).parent.parent

@pytest.fixture(scope="function")
def temp_dir():
    """Create temporary directory for test files"""
    temp_dir = tempfile.mkdtemp()
    yield Path(temp_dir)
    shutil.rmtree(temp_dir)

@pytest.fixture(scope="function")
def temp_git_repo(temp_dir):
    """Create temporary git repository"""
    subprocess.run(["git", "init"], cwd=temp_dir)
    subprocess.run(["git", "config", "user.name", "Test User"], cwd=temp_dir)
    subprocess.run(["git", "config", "user.email", "test@example.com"], cwd=temp_dir)
    yield temp_dir

@pytest.fixture(scope="session")
def toon_encoder():
    """TOON encoder instance"""
    from scripts.utils.toon_encoder import TOONEncoder
    return TOONEncoder()

@pytest.fixture(scope="session")
def token_counter():
    """Token counter with tiktoken"""
    from scripts.utils.token_counter import count_tokens
    return count_tokens

@pytest.fixture
def sample_checkpoint_data():
    """Sample checkpoint data for testing"""
    return {
        "checkpoint": {
            "timestamp": "2025-11-17T10:00:00Z",
            "sprint": "Test Sprint",
            "status": "Complete"
        },
        "tasks_completed": [
            {"id": 1, "title": "Task 1", "status": "done"},
            {"id": 2, "title": "Task 2", "status": "done"}
        ],
        "submodules_updated": [
            {"name": "backend", "commit": "abc123", "status": "Active"}
        ]
    }

@pytest.fixture
def sample_checkpoint_markdown():
    """Sample checkpoint in Markdown format"""
    return """# Checkpoint

**Sprint:** Test Sprint
**Status:** Complete

## Tasks Completed

- [x] Task 1
- [x] Task 2

## Submodules Updated

- backend (abc123) - Active
"""

@pytest.fixture
def sample_checkpoint_toon():
    """Sample checkpoint in TOON format"""
    return """checkpoint:
  timestamp: 2025-11-17T10:00:00Z
  sprint: Test Sprint
  status: Complete

tasks_completed[2]{id,title,status}:
 1,Task 1,done
 2,Task 2,done

submodules_updated[1]{name,commit,status}:
 backend,abc123,Active
"""

# Security test fixtures
@pytest.fixture
def malicious_payloads():
    """Common security payloads for injection testing"""
    return {
        "sql_injection": [
            "'; DROP TABLE users; --",
            "1' OR '1'='1",
            "admin'--"
        ],
        "xss": [
            "<script>alert('XSS')</script>",
            "<img src=x onerror=alert('XSS')>",
            "javascript:alert('XSS')"
        ],
        "command_injection": [
            "; rm -rf /",
            "| cat /etc/passwd",
            "`whoami`"
        ],
        "path_traversal": [
            "../../etc/passwd",
            "..\\..\\windows\\system32",
            "/etc/passwd"
        ]
    }
```

### 8.3 CI/CD Integration

**File:** `.github/workflows/toon-tests.yml`

```yaml
name: TOON Integration Tests

on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main]

jobs:
  unit-tests:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        python-version: [3.9, 3.10, 3.11]

    steps:
      - uses: actions/checkout@v3

      - name: Set up Python ${{ matrix.python-version }}
        uses: actions/setup-python@v4
        with:
          python-version: ${{ matrix.python-version }}

      - name: Install dependencies
        run: |
          python -m pip install --upgrade pip
          pip install -r requirements.txt
          pip install pytest pytest-cov pytest-asyncio

      - name: Run unit tests
        run: |
          pytest tests/unit -v --cov --cov-report=xml

      - name: Upload coverage
        uses: codecov/codecov-action@v3
        with:
          file: ./coverage.xml

  integration-tests:
    runs-on: ubuntu-latest
    needs: unit-tests

    steps:
      - uses: actions/checkout@v3

      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: 3.11

      - name: Install dependencies
        run: |
          pip install -r requirements.txt
          pip install pytest pytest-asyncio

      - name: Run integration tests
        run: |
          pytest tests/integration -v

  security-tests:
    runs-on: ubuntu-latest
    needs: unit-tests

    steps:
      - uses: actions/checkout@v3

      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: 3.11

      - name: Install dependencies
        run: |
          pip install -r requirements.txt
          pip install pytest

      - name: Run security tests
        run: |
          pytest tests/security -v

      - name: Run SAST (Bandit)
        run: |
          pip install bandit
          bandit -r scripts/ src/ -f json -o bandit-report.json

      - name: Upload SAST results
        uses: actions/upload-artifact@v3
        with:
          name: bandit-report
          path: bandit-report.json

  performance-tests:
    runs-on: ubuntu-latest
    needs: integration-tests

    steps:
      - uses: actions/checkout@v3

      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: 3.11

      - name: Install dependencies
        run: |
          pip install -r requirements.txt
          pip install pytest

      - name: Run performance tests
        run: |
          pytest tests/performance -v --benchmark-only
```

---

## 9. Test Quality Metrics

### 9.1 Coverage Report (Target State)

| Module | Statements | Missing | Coverage | Critical? |
|--------|------------|---------|----------|-----------|
| `toon_encoder.py` | 120 | 8 | 93% | ✅ |
| `token_counter.py` | 35 | 2 | 94% | ✅ |
| `checkpoint_converter.py` | 180 | 25 | 86% | ✅ |
| `tasklist_converter.py` | 210 | 30 | 86% | ✅ |
| `submodule_converter.py` | 95 | 12 | 87% | ⚠️ |
| `memory_context_converter.py` | 140 | 22 | 84% | ⚠️ |
| `pdf_to_toon_converter.py` | 250 | 60 | 76% | ⚠️ |
| `api/toon_endpoints.py` | 160 | 28 | 82% | ✅ |
| `hooks/pre-commit-sync.py` | 80 | 14 | 82% | ✅ |
| **TOTAL** | **1,270** | **201** | **84%** | ✅ TARGET MET |

### 9.2 Assertion Density

**Target:** 2-3 assertions per test
**Current:** N/A (no tests)
**Recommended:**

| Test Suite | Tests | Assertions | Density | Quality |
|------------|-------|------------|---------|---------|
| Unit - TOON Encoding | 35 | 87 | 2.5 | ✅ Good |
| Unit - Token Counting | 15 | 45 | 3.0 | ✅ Excellent |
| Unit - Converters | 40 | 100 | 2.5 | ✅ Good |
| Integration | 20 | 50 | 2.5 | ✅ Good |
| Security | 18 | 54 | 3.0 | ✅ Excellent |
| Performance | 12 | 24 | 2.0 | ⚠️ Acceptable |
| E2E | 10 | 30 | 3.0 | ✅ Excellent |
| **TOTAL** | **150** | **390** | **2.6** | ✅ GOOD |

### 9.3 Test Isolation Score

**Target:** 100% (no shared state between tests)
**Measurement:**
- ✅ Use `setUp()` and `tearDown()` for test fixtures
- ✅ Use `@pytest.fixture(scope="function")` for isolated fixtures
- ✅ Clean up temp files/directories after each test
- ❌ Avoid global state or class-level variables

**Recommended Pattern:**
```python
class TestExample(unittest.TestCase):
    def setUp(self):
        """Create fresh state for each test"""
        self.temp_dir = tempfile.mkdtemp()
        self.encoder = TOONEncoder()

    def tearDown(self):
        """Clean up after each test"""
        shutil.rmtree(self.temp_dir)

    def test_something(self):
        """Test is isolated - uses setUp() state"""
        # Test logic here
        pass
```

### 9.4 Mock Usage Analysis

**Appropriate Mocking:**
- ✅ External API calls (GitHub API, Claude API)
- ✅ File system I/O (when testing logic, not file operations)
- ✅ Database queries (for unit tests, not integration tests)
- ✅ Subprocess calls (git commands)

**Excessive Mocking (avoid):**
- ❌ Simple getter/setter methods
- ❌ Data structure operations
- ❌ Converters (test real conversions, not mocked logic)

**Example:**
```python
# ✅ Good: Mock subprocess for git status
@patch('subprocess.run')
def test_git_status(self, mock_run):
    mock_run.return_value = MagicMock(stdout="M file.py")
    status = get_git_status()
    self.assertIn("file.py", status)

# ❌ Bad: Mock TOON encoder (defeats purpose of test)
@patch('toon_encoder.encode_object')
def test_checkpoint_to_toon(self, mock_encode):
    mock_encode.return_value = "mocked toon"
    result = checkpoint_to_toon(data)
    # This doesn't test anything!
```

### 9.5 Test Flakiness Prevention

**Sources of Flakiness:**
1. **Timing issues** - Tests that depend on time.sleep() or system time
2. **Filesystem race conditions** - Tests that don't clean up properly
3. **Network dependencies** - Tests that make real HTTP requests
4. **Random data** - Tests with non-deterministic inputs

**Prevention Strategies:**
```python
# ✅ Use deterministic data
def test_something(self):
    # Fixed seed for reproducibility
    random.seed(42)
    data = generate_random_data()
    # Test logic...

# ✅ Mock time-dependent code
@patch('datetime.datetime')
def test_timestamp(self, mock_datetime):
    mock_datetime.now.return_value = datetime(2025, 11, 17, 10, 0, 0)
    result = generate_timestamp()
    self.assertEqual(result, "2025-11-17T10:00:00Z")

# ✅ Use temporary directories for file tests
def test_file_operations(self):
    with tempfile.TemporaryDirectory() as temp_dir:
        file_path = Path(temp_dir) / "test.txt"
        file_path.write_text("test")
        # Test logic...
        # Cleanup automatic when exiting context
```

---

## 10. Security Testing Checklist

### 10.1 OWASP Top 10 Coverage

| Vulnerability | Tests | Coverage | Status |
|---------------|-------|----------|--------|
| **A01: Broken Access Control** | 7 | Multi-tenant isolation | ✅ Covered |
| **A02: Cryptographic Failures** | 3 | N/A (no encryption yet) | ⏸️ Future |
| **A03: Injection** | 10 | SQL, XSS, Command | ✅ Covered |
| **A04: Insecure Design** | - | Architecture review | ✅ Covered |
| **A05: Security Misconfiguration** | 5 | Default configs | ⚠️ Partial |
| **A06: Vulnerable Components** | - | Dependency scanning | ⚠️ Bandit only |
| **A07: Auth/AuthZ Failures** | 8 | API authentication | ✅ Covered |
| **A08: Data Integrity Failures** | 5 | Roundtrip conversion | ✅ Covered |
| **A09: Logging Failures** | 3 | Audit logging | ⚠️ Partial |
| **A10: SSRF** | 2 | URL validation | ⏸️ Future |

### 10.2 Security Test Matrix

| Attack Vector | Test Case | Expected Behavior |
|---------------|-----------|-------------------|
| SQL Injection | `'; DROP TABLE` in field name | ValueError raised |
| XSS | `<script>alert()</script>` in value | Escaped in HTML output |
| Command Injection | `$(rm -rf /)` in value | Treated as literal string |
| Path Traversal | `../../etc/passwd` in path | ValueError raised |
| CSRF | Missing CSRF token | 403 Forbidden |
| Insecure Deserialization | Malicious pickle payload | ValueError raised |
| XXE | XML external entity in TOON | N/A (TOON is not XML) |

---

## 11. Performance Testing Plan

### 11.1 Performance SLAs

| Operation | Target | Measurement | Test |
|-----------|--------|-------------|------|
| TOON Encode (1KB) | <10ms | 95th percentile | `test_toon_encoding_performance_small_dataset` |
| TOON Encode (100KB) | <500ms | 95th percentile | `test_toon_encoding_performance_large_dataset` |
| Token Count (10KB) | <100ms | Average | `test_token_counting_performance_baseline` |
| Pre-commit Hook (10 files) | <3s | Max | `test_precommit_hook_performance` |
| API Response (TOON) | <200ms | 95th percentile | `test_api_response_time_toon` |
| Checkpoint Creation | <2s | Average | `test_checkpoint_creation_performance` |

### 11.2 Scalability Testing

**Test Scenarios:**
1. **10x Scale:** 100KB checkpoint, 500 tasks, 20 submodules
2. **100x Scale:** 1MB checkpoint, 5000 tasks, 100 submodules
3. **Concurrent Load:** 100 simultaneous API requests

**Expected Results:**
| Scenario | Target Time | Memory Usage | Status |
|----------|-------------|--------------|--------|
| 10x Scale | <5s | <200MB | TBD |
| 100x Scale | <30s | <500MB | TBD |
| Concurrent Load | <5s (95th %ile) | <1GB total | TBD |

### 11.3 Performance Regression Detection

**Baseline:**
```python
# Establish performance baseline
def test_establish_performance_baseline(self):
    """Record baseline performance metrics"""
    import json
    metrics = {
        "toon_encode_1kb": benchmark_toon_encoding(size_kb=1),
        "toon_encode_100kb": benchmark_toon_encoding(size_kb=100),
        "token_count_10kb": benchmark_token_counting(size_kb=10),
        "checkpoint_creation": benchmark_checkpoint_creation()
    }

    # Save baseline
    with open("performance_baseline.json", "w") as f:
        json.dump(metrics, f)

# Detect regressions
def test_performance_regression(self):
    """Detect performance regressions vs baseline"""
    import json
    with open("performance_baseline.json") as f:
        baseline = json.load(f)

    current = {
        "toon_encode_1kb": benchmark_toon_encoding(size_kb=1),
        "toon_encode_100kb": benchmark_toon_encoding(size_kb=100),
        "token_count_10kb": benchmark_token_counting(size_kb=10),
        "checkpoint_creation": benchmark_checkpoint_creation()
    }

    for metric, current_value in current.items():
        baseline_value = baseline[metric]
        regression_percent = (current_value - baseline_value) / baseline_value * 100

        # Fail if >20% regression
        self.assertLess(
            regression_percent, 20,
            f"Performance regression detected in {metric}: {regression_percent:.1f}%"
        )
```

---

## 12. Test Execution Plan

### 12.1 Minimum Viable Test Suite (Week 1)

**Goal:** Prevent critical bugs from shipping
**Priority:** P0 only
**Estimated Effort:** 24 hours
**Deliverable:** Week 1 (parallel with Phase 1)

**Scope:**
1. ✅ **Unit - TOON Encoding** (8h)
   - 20 tests (reduced from 35)
   - Core encoding logic only
   - Edge cases: empty, nested, special chars

2. ✅ **Unit - Token Counting** (3h)
   - 8 tests (reduced from 15)
   - Accuracy validation
   - ROI claim verification (30-60% reduction)

3. ✅ **Security - Injection** (4h)
   - 6 tests (reduced from 10)
   - SQL injection, XSS, command injection

4. ✅ **Security - Path Traversal** (3h)
   - 5 tests (reduced from 8)
   - Path validation, symlink protection

5. ✅ **Integration - Checkpoint Workflow** (6h)
   - 5 tests (reduced from 20)
   - Create checkpoint, load checkpoint, dual-format

**Total:** 44 tests, 24 hours, Week 1

### 12.2 Comprehensive Test Suite (Week 2-3)

**Goal:** Full test pyramid coverage
**Priority:** P0 + P1
**Estimated Effort:** 31 hours (additional)
**Deliverable:** Week 2-3

**Additional Scope:**
1. ✅ **Unit - Converters** (10h)
   - 40 tests for all converters
   - Roundtrip conversion tests
   - Data integrity validation

2. ✅ **Integration - API** (5h)
   - 15 tests for TOON endpoints
   - Content negotiation
   - Dual-format responses

3. ✅ **Integration - Pre-commit Hook** (6h)
   - 10 tests for Git workflow
   - Sync .toon ↔ .md
   - Performance validation

4. ✅ **Performance - Benchmarks** (6h)
   - 12 tests for SLAs
   - Scalability tests
   - Regression detection

5. ✅ **E2E - Workflows** (4h)
   - 10 tests for user scenarios
   - Checkpoint creation → loading
   - TASKLIST generation → agent parsing

**Total:** 87 additional tests, 31 hours, Week 2-3

### 12.3 Test Execution Schedule

**Week 1 (Days 1-5):**
```
Day 1-2: Unit - TOON Encoding (20 tests)
Day 2-3: Unit - Token Counting (8 tests)
Day 3-4: Security - Injection + Path Traversal (11 tests)
Day 4-5: Integration - Checkpoint Workflow (5 tests)
---
Milestone: Minimum Viable Test Suite Complete (44 tests)
```

**Week 2 (Days 6-10):**
```
Day 6-7: Unit - Converters (40 tests)
Day 8: Integration - API (15 tests)
Day 9: Integration - Pre-commit Hook (10 tests)
Day 10: Performance - Benchmarks (12 tests)
---
Milestone: Comprehensive Unit & Integration Tests Complete
```

**Week 3 (Days 11-15):**
```
Day 11-12: E2E - Workflows (10 tests)
Day 13: CI/CD Integration
Day 14: Documentation & Training
Day 15: Final validation & sign-off
---
Milestone: Complete Test Suite Operational (170 tests)
```

---

## 13. Testing Tools & Dependencies

### 13.1 Required Libraries

**File:** `requirements-test.txt`

```txt
# Core testing
pytest==7.4.3
pytest-cov==4.1.0
pytest-asyncio==0.21.1
pytest-mock==3.12.0
pytest-benchmark==4.0.0

# Coverage reporting
coverage==7.3.2
codecov==2.1.13

# Security testing
bandit==1.7.5
safety==2.3.5

# Performance testing
memory-profiler==0.61.0
pytest-timeout==2.2.0

# HTTP testing
httpx==0.25.2
requests-mock==1.11.0

# Token counting
tiktoken==0.5.2

# Test data generation
faker==20.1.0
factory-boy==3.3.0

# Linting (for test quality)
pylint==3.0.3
mypy==1.7.1
black==23.12.1
isort==5.13.2
```

### 13.2 Development Setup

```bash
# Install test dependencies
pip install -r requirements-test.txt

# Run all tests
pytest

# Run specific test suite
pytest tests/unit/test_toon_encoder.py -v

# Run with coverage
pytest --cov=scripts --cov-report=html

# Run only fast tests (skip slow)
pytest -m "not slow"

# Run only security tests
pytest -m security

# Run with performance benchmarking
pytest tests/performance --benchmark-only
```

---

## 14. Test Gap Analysis

### 14.1 Current vs. Target State

| Metric | Current | Week 1 Target | Week 3 Target | Gap |
|--------|---------|---------------|---------------|-----|
| **Total Tests** | 0 | 44 | 170 | 170 |
| **Unit Tests** | 0 | 28 | 105 | 105 |
| **Integration Tests** | 0 | 5 | 30 | 30 |
| **Security Tests** | 0 | 11 | 18 | 18 |
| **Performance Tests** | 0 | 0 | 12 | 12 |
| **E2E Tests** | 0 | 0 | 10 | 10 |
| **Coverage** | 0% | 65% | 84% | 84% |
| **Execution Time** | 0s | <30s | <5m | - |

### 14.2 Priority Gaps

**P0 - Critical (Must have Week 1):**
1. ❌ **TOON Encoding Tests** - Zero coverage for core encoding logic
2. ❌ **Token Counting Validation** - ROI claims unverified
3. ❌ **Security Injection Tests** - SQL, XSS, command injection unchecked
4. ❌ **Path Traversal Protection** - File system vulnerabilities unchecked
5. ❌ **Checkpoint Workflow Tests** - End-to-end creation/loading untested

**P1 - High (Should have Week 2-3):**
1. ❌ **Converter Unit Tests** - All 6 converters untested
2. ❌ **API Integration Tests** - TOON endpoints untested
3. ❌ **Pre-commit Hook Tests** - Git workflow integration untested
4. ❌ **Performance Benchmarks** - SLAs undefined and unvalidated
5. ❌ **E2E User Workflows** - No user scenario coverage

**P2 - Medium (Nice to have post-MVP):**
1. ❌ **Load Testing** - Concurrent request handling untested
2. ❌ **Chaos Engineering** - Failure scenario testing
3. ❌ **Mutation Testing** - Test quality validation
4. ❌ **Property-Based Testing** - Hypothesis testing for edge cases

### 14.3 Risk Assessment

**Without Testing (Current State):**
| Risk | Probability | Impact | Mitigation Cost |
|------|-------------|--------|-----------------|
| Security breach (injection) | 60% | $50K-$200K | $100K+ |
| Data loss (checkpoint corruption) | 40% | $20K-$100K | $50K+ |
| Performance degradation | 70% | $10K-$50K | $30K+ |
| Integration failures | 50% | $15K-$75K | $40K+ |
| **Total Expected Loss** | - | **$95K-$425K** | **$220K+** |

**With Testing (Week 3 State):**
| Risk | Probability | Impact | Mitigation Cost |
|------|-------------|--------|-----------------|
| Security breach | 5% | $5K-$20K | $10K |
| Data loss | 2% | $2K-$10K | $5K |
| Performance degradation | 10% | $1K-$5K | $3K |
| Integration failures | 5% | $1K-$10K | $5K |
| **Total Expected Loss** | - | **$9K-$45K** | **$23K** |

**ROI Calculation:**
```
Testing Investment: $12K (55 hours @ $150/hr engineer + $3K infrastructure)
Risk Reduction: $86K-$380K (expected loss prevented)
ROI: 7-32x return on investment
```

**Recommendation:** **INVEST IN TESTING IMMEDIATELY** (95% confidence)

---

## 15. Recommendations

### 15.1 Immediate Actions (This Week)

**Day 1-2:**
1. ✅ **Create test infrastructure** (pytest.ini, conftest.py)
2. ✅ **Set up CI/CD pipeline** (.github/workflows/toon-tests.yml)
3. ✅ **Implement TOON encoding tests** (20 tests, 8 hours)

**Day 3-4:**
4. ✅ **Implement token counting tests** (8 tests, 3 hours)
5. ✅ **Implement security injection tests** (11 tests, 7 hours)

**Day 5:**
6. ✅ **Implement checkpoint workflow tests** (5 tests, 6 hours)
7. ✅ **Run full test suite, measure coverage**
8. ✅ **Generate coverage report, identify gaps**

**Milestone:** Minimum Viable Test Suite (44 tests, 65% coverage)

### 15.2 Week 2-3 Actions

**Week 2:**
1. ✅ **Implement converter unit tests** (40 tests, 10 hours)
2. ✅ **Implement API integration tests** (15 tests, 5 hours)
3. ✅ **Implement pre-commit hook tests** (10 tests, 6 hours)
4. ✅ **Implement performance benchmarks** (12 tests, 6 hours)

**Week 3:**
5. ✅ **Implement E2E workflow tests** (10 tests, 4 hours)
6. ✅ **Optimize test execution time** (<5 minutes total)
7. ✅ **Document test patterns and best practices**
8. ✅ **Train team on testing strategy**

**Milestone:** Comprehensive Test Suite (170 tests, 84% coverage)

### 15.3 Long-term Improvements (Post-MVP)

**Month 2:**
1. ⏸️ **Load testing** - Validate 100+ concurrent requests
2. ⏸️ **Mutation testing** - Verify test quality with mutmut
3. ⏸️ **Property-based testing** - Hypothesis library for edge cases
4. ⏸️ **Visual regression testing** - Percy for UI changes

**Month 3+:**
5. ⏸️ **Chaos engineering** - Netflix Chaos Monkey integration
6. ⏸️ **Fuzzing** - AFL/libFuzzer for parser robustness
7. ⏸️ **Accessibility testing** - axe-core for WCAG compliance
8. ⏸️ **Internationalization testing** - Unicode edge cases

---

## 16. Success Metrics

### 16.1 Week 1 Success Criteria

**Quantitative:**
- ✅ 44+ tests implemented
- ✅ 65%+ code coverage
- ✅ <30 second test execution time
- ✅ 0 P0 security vulnerabilities detected
- ✅ CI/CD pipeline operational

**Qualitative:**
- ✅ All P0 test cases passing
- ✅ Team trained on pytest usage
- ✅ Test documentation complete
- ✅ Coverage report generated

### 16.2 Week 3 Success Criteria

**Quantitative:**
- ✅ 170+ tests implemented
- ✅ 84%+ code coverage
- ✅ <5 minute test execution time
- ✅ 0 P0/P1 security vulnerabilities
- ✅ 100% P0 feature coverage

**Qualitative:**
- ✅ Full test pyramid implemented
- ✅ All user workflows validated
- ✅ Performance SLAs validated
- ✅ Security testing comprehensive

### 16.3 Production Readiness Checklist

**Before Phase 2 Deployment:**
- [ ] Minimum Viable Test Suite passing (44 tests)
- [ ] Security injection tests passing (11 tests)
- [ ] Checkpoint workflow validated
- [ ] CI/CD integration complete
- [ ] Coverage report >65%

**Before Phase 8 Deployment:**
- [ ] Comprehensive Test Suite passing (170 tests)
- [ ] All security tests passing (18 tests)
- [ ] Performance benchmarks validated
- [ ] E2E workflows validated
- [ ] Coverage report >84%
- [ ] Load testing complete (100 concurrent requests)

---

## 17. Appendix

### 17.1 Test File Structure

```
tests/
├── conftest.py                      # Shared fixtures
├── pytest.ini                       # Pytest configuration
├── unit/
│   ├── test_toon_encoder.py        # 35 tests
│   ├── test_token_counter.py       # 15 tests
│   ├── test_checkpoint_converter.py # 10 tests
│   ├── test_tasklist_converter.py  # 10 tests
│   ├── test_submodule_converter.py # 10 tests
│   ├── test_memory_context_converter.py # 10 tests
│   └── test_pdf_to_toon_converter.py # 5 tests
├── integration/
│   ├── test_converter_integration.py # 20 tests
│   ├── test_api_toon_endpoints.py   # 15 tests
│   └── test_precommit_hook.py       # 10 tests
├── security/
│   ├── test_injection_attacks.py    # 10 tests
│   ├── test_path_traversal.py       # 8 tests
│   └── test_multi_tenant_isolation.py # 7 tests (cloud backend)
├── performance/
│   ├── test_toon_performance.py     # 12 tests
│   └── test_load.py                 # 5 tests
└── e2e/
    └── test_workflows.py            # 10 tests
```

### 17.2 Sample Test Execution Output

```bash
$ pytest -v

================================ test session starts =================================
platform darwin -- Python 3.11.5, pytest-7.4.3, pluggy-1.3.0
cachedir: .pytest_cache
rootdir: /Users/halcasteel/PROJECTS/coditect-rollout-master
configfile: pytest.ini
plugins: cov-4.1.0, asyncio-0.21.1, mock-3.12.0
collected 170 items

tests/unit/test_toon_encoder.py::TestTOONEncoderBasic::test_encode_empty_object PASSED [  1%]
tests/unit/test_toon_encoder.py::TestTOONEncoderBasic::test_encode_simple_object PASSED [  2%]
tests/unit/test_toon_encoder.py::TestTOONEncoderBasic::test_encode_nested_object PASSED [  3%]
...
tests/security/test_injection_attacks.py::TestTOONInjectionAttacks::test_sql_injection PASSED [ 98%]
tests/e2e/test_workflows.py::TestE2EWorkflows::test_create_checkpoint_workflow PASSED [ 99%]
tests/e2e/test_workflows.py::TestE2EWorkflows::test_cloud_dashboard_workflow PASSED [100%]

---------- coverage: platform darwin, python 3.11.5 -----------
Name                                  Stmts   Miss  Cover   Missing
-------------------------------------------------------------------
scripts/utils/toon_encoder.py          120      8    93%   45-52
scripts/utils/token_counter.py          35      2    94%   28-29
scripts/converters/checkpoint.py       180     25    86%   67-89, 155-157
scripts/converters/tasklist.py         210     30    86%   78-105, 190-195
...
-------------------------------------------------------------------
TOTAL                                 1270    201    84%

========================= 170 passed in 245.23s (0:04:05) =========================
```

### 17.3 References

**Testing Best Practices:**
- [Pytest Documentation](https://docs.pytest.org/)
- [Google Testing Blog](https://testing.googleblog.com/)
- [Martin Fowler - Test Pyramid](https://martinfowler.com/bliki/TestPyramid.html)

**Security Testing:**
- [OWASP Testing Guide](https://owasp.org/www-project-web-security-testing-guide/)
- [OWASP Top 10](https://owasp.org/www-project-top-ten/)

**Performance Testing:**
- [Python Performance Testing](https://docs.python.org/3/library/timeit.html)
- [pytest-benchmark](https://pytest-benchmark.readthedocs.io/)

---

**Document Version:** 1.0
**Last Updated:** 2025-11-17
**Next Review:** Week 1 completion (post-Minimum Viable Test Suite)
**Owner:** CODITECT Platform Team
**Status:** Ready for Implementation ✅
