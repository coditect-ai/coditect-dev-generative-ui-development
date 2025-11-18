#!/usr/bin/env python3
"""
Day 1 Integration Tests - Infrastructure Validation

Tests PostgreSQL, ChromaDB, and Redis connectivity and basic operations.

Author: AZ1.AI CODITECT Team
Project: CODITECT Rollout Master - MEMORY-CONTEXT Consolidation
Date: 2025-11-17
"""

import sys
import time
from typing import Dict, List, Tuple

# Test results tracking
test_results: List[Tuple[str, bool, str]] = []


def test_result(name: str, passed: bool, message: str = ""):
    """Record a test result."""
    test_results.append((name, passed, message))
    status = "✓ PASS" if passed else "✗ FAIL"
    color = "\033[0;32m" if passed else "\033[0;31m"
    reset = "\033[0m"
    print(f"{color}{status}{reset} {name}")
    if message:
        print(f"       {message}")


def test_postgresql():
    """Test PostgreSQL connectivity and schema."""
    print("\n" + "="*60)
    print("PostgreSQL Tests")
    print("="*60)

    try:
        import psycopg2
        from psycopg2 import sql
    except ImportError:
        test_result("PostgreSQL - Import psycopg2", False, "psycopg2 not installed")
        return

    # Connection test
    try:
        conn = psycopg2.connect(
            host="localhost",
            port=5432,
            database="coditect_memory_context",
            user="coditect_admin",
            password="changeme_dev_only"  # Default from .env
        )
        test_result("PostgreSQL - Connection", True, "Connected successfully")
    except Exception as e:
        test_result("PostgreSQL - Connection", False, str(e))
        return

    try:
        cursor = conn.cursor()

        # Test 1: Verify database exists
        cursor.execute("SELECT current_database();")
        db_name = cursor.fetchone()[0]
        test_result(
            "PostgreSQL - Database exists",
            db_name == "coditect_memory_context",
            f"Database: {db_name}"
        )

        # Test 2: Verify extensions
        cursor.execute("""
            SELECT extname FROM pg_extension
            WHERE extname IN ('uuid-ossp', 'pg_trgm', 'pgcrypto')
            ORDER BY extname;
        """)
        extensions = [row[0] for row in cursor.fetchall()]
        expected_extensions = ['pg_trgm', 'pgcrypto', 'uuid-ossp']
        test_result(
            "PostgreSQL - Extensions installed",
            all(ext in extensions for ext in expected_extensions),
            f"Extensions: {', '.join(extensions)}"
        )

        # Test 3: Verify tables exist
        cursor.execute("""
            SELECT table_name FROM information_schema.tables
            WHERE table_schema = 'public' AND table_type = 'BASE TABLE'
            ORDER BY table_name;
        """)
        tables = [row[0] for row in cursor.fetchall()]
        expected_tables = [
            'checkpoints', 'context_loads', 'db_metadata', 'pattern_tags',
            'patterns', 'privacy_audit', 'session_tags', 'sessions', 'tags'
        ]
        test_result(
            "PostgreSQL - Tables created",
            all(table in tables for table in expected_tables),
            f"Tables: {len(tables)}/9"
        )

        # Test 4: Verify views exist
        cursor.execute("""
            SELECT table_name FROM information_schema.views
            WHERE table_schema = 'public'
            ORDER BY table_name;
        """)
        views = [row[0] for row in cursor.fetchall()]
        expected_views = [
            'v_active_sessions', 'v_patterns_by_usage',
            'v_privacy_audit_summary', 'v_recent_checkpoints'
        ]
        test_result(
            "PostgreSQL - Views created",
            all(view in views for view in expected_views),
            f"Views: {len(views)}/4"
        )

        # Test 5: Verify metadata
        cursor.execute("SELECT key, value FROM db_metadata ORDER BY key;")
        metadata = {row[0]: row[1] for row in cursor.fetchall()}
        test_result(
            "PostgreSQL - Metadata initialized",
            'framework' in metadata and metadata['framework'] == 'CODITECT MEMORY-CONTEXT',
            f"Framework: {metadata.get('framework', 'N/A')}"
        )

        # Test 6: Test UUID generation
        cursor.execute("SELECT uuid_generate_v4();")
        uuid_value = cursor.fetchone()[0]
        test_result(
            "PostgreSQL - UUID generation",
            len(str(uuid_value)) == 36,
            f"UUID: {uuid_value}"
        )

        # Test 7: Test JSONB support
        cursor.execute("""
            CREATE TEMP TABLE test_jsonb (data JSONB);
            INSERT INTO test_jsonb (data) VALUES ('{"test": "value", "number": 42}');
            SELECT data->>'test' FROM test_jsonb;
        """)
        json_value = cursor.fetchone()[0]
        test_result(
            "PostgreSQL - JSONB support",
            json_value == "value",
            "JSONB queries working"
        )

        # Test 8: Test full-text search (pg_trgm)
        cursor.execute("""
            CREATE TEMP TABLE test_search (title TEXT);
            CREATE INDEX test_search_idx ON test_search USING GIN (title gin_trgm_ops);
            INSERT INTO test_search (title) VALUES ('authentication system'), ('authorization module');
            SELECT COUNT(*) FROM test_search WHERE title ILIKE '%auth%';
        """)
        search_count = cursor.fetchone()[0]
        test_result(
            "PostgreSQL - Full-text search",
            search_count == 2,
            f"Found {search_count} matches"
        )

        cursor.close()
        conn.close()

    except Exception as e:
        test_result("PostgreSQL - Schema verification", False, str(e))
        conn.close()


def test_chromadb():
    """Test ChromaDB connectivity and collections."""
    print("\n" + "="*60)
    print("ChromaDB Tests")
    print("="*60)

    try:
        import chromadb
        from chromadb.utils import embedding_functions
    except ImportError:
        test_result("ChromaDB - Import chromadb", False, "chromadb not installed")
        return

    # Connection test
    try:
        client = chromadb.HttpClient(host="localhost", port=8000)
        client.heartbeat()
        test_result("ChromaDB - Connection", True, "Connected successfully")
    except Exception as e:
        test_result("ChromaDB - Connection", False, str(e))
        return

    try:
        # Test 1: Verify collections exist
        collections = client.list_collections()
        collection_names = [col.name for col in collections]
        expected_collections = [
            'sessions_embeddings',
            'checkpoints_embeddings',
            'patterns_embeddings'
        ]
        test_result(
            "ChromaDB - Collections created",
            all(name in collection_names for name in expected_collections),
            f"Collections: {len(collection_names)}/3"
        )

        # Test 2: Get sessions collection
        sentence_transformer_ef = embedding_functions.SentenceTransformerEmbeddingFunction(
            model_name="sentence-transformers/all-MiniLM-L6-v2"
        )
        sessions_collection = client.get_collection(
            name="sessions_embeddings",
            embedding_function=sentence_transformer_ef
        )
        test_result(
            "ChromaDB - Get collection",
            sessions_collection.name == "sessions_embeddings",
            f"Collection: {sessions_collection.name}"
        )

        # Test 3: Verify test document exists (from setup script)
        count = sessions_collection.count()
        test_result(
            "ChromaDB - Test document exists",
            count >= 1,
            f"Documents: {count}"
        )

        # Test 4: Test embedding generation
        test_text = "Testing embedding generation for MEMORY-CONTEXT"
        embeddings = sentence_transformer_ef([test_text])
        test_result(
            "ChromaDB - Embedding generation",
            len(embeddings[0]) == 384,  # all-MiniLM-L6-v2 produces 384-dim embeddings
            f"Embedding dimensions: {len(embeddings[0])}"
        )

        # Test 5: Add a test document
        test_id = f"test-{int(time.time())}"
        sessions_collection.add(
            documents=[test_text],
            metadatas=[{"test": True, "timestamp": time.time()}],
            ids=[test_id]
        )
        test_result(
            "ChromaDB - Add document",
            True,
            f"Added document ID: {test_id}"
        )

        # Test 6: Search for test document
        results = sessions_collection.query(
            query_texts=["testing embedding"],
            n_results=1
        )
        found_id = results['ids'][0][0] if results['ids'][0] else None
        test_result(
            "ChromaDB - Semantic search",
            found_id == test_id,
            f"Found: {found_id}"
        )

        # Test 7: Get document by ID
        doc = sessions_collection.get(ids=[test_id])
        test_result(
            "ChromaDB - Get by ID",
            len(doc['ids']) == 1,
            f"Retrieved document: {test_id}"
        )

        # Clean up test document
        sessions_collection.delete(ids=[test_id])

    except Exception as e:
        test_result("ChromaDB - Operations", False, str(e))


def test_redis():
    """Test Redis connectivity."""
    print("\n" + "="*60)
    print("Redis Tests")
    print("="*60)

    try:
        import redis
    except ImportError:
        test_result("Redis - Import redis", False, "redis package not installed")
        print("       Install with: pip install redis")
        return

    # Connection test
    try:
        r = redis.Redis(
            host="localhost",
            port=6379,
            password="changeme_dev_only",  # Default from .env
            decode_responses=True
        )
        r.ping()
        test_result("Redis - Connection", True, "Connected successfully")
    except Exception as e:
        test_result("Redis - Connection", False, str(e))
        return

    try:
        # Test 1: Set and get value
        r.set("test:key", "test_value")
        value = r.get("test:key")
        test_result(
            "Redis - Set/Get",
            value == "test_value",
            f"Value: {value}"
        )

        # Test 2: Delete key
        r.delete("test:key")
        value = r.get("test:key")
        test_result(
            "Redis - Delete",
            value is None,
            "Key deleted successfully"
        )

        # Test 3: Set with expiration
        r.setex("test:expire", 10, "temporary")
        ttl = r.ttl("test:expire")
        test_result(
            "Redis - Expiration",
            0 < ttl <= 10,
            f"TTL: {ttl} seconds"
        )

        # Clean up
        r.delete("test:expire")

    except Exception as e:
        test_result("Redis - Operations", False, str(e))


def print_summary():
    """Print test summary."""
    print("\n" + "="*60)
    print("Test Summary")
    print("="*60)

    total_tests = len(test_results)
    passed_tests = sum(1 for _, passed, _ in test_results if passed)
    failed_tests = total_tests - passed_tests

    print(f"\nTotal Tests:  {total_tests}")
    print(f"Passed:       \033[0;32m{passed_tests}\033[0m")
    print(f"Failed:       \033[0;31m{failed_tests}\033[0m")
    print(f"Success Rate: {(passed_tests/total_tests*100):.1f}%")

    if failed_tests > 0:
        print("\nFailed Tests:")
        for name, passed, message in test_results:
            if not passed:
                print(f"  ✗ {name}")
                if message:
                    print(f"    {message}")

    print("\n" + "="*60)

    return failed_tests == 0


def main():
    """Run all tests."""
    print("\n" + "="*60)
    print("CODITECT MEMORY-CONTEXT - Day 1 Integration Tests")
    print("="*60)
    print(f"Date: {time.strftime('%Y-%m-%d %H:%M:%S')}")

    # Run all test suites
    test_postgresql()
    test_chromadb()
    test_redis()

    # Print summary
    all_passed = print_summary()

    if all_passed:
        print("\n\033[0;32m✓ All tests passed! Infrastructure is ready.\033[0m")
        print("\nNext steps:")
        print("1. Review connection information")
        print("2. Begin Context API development (Day 2-3)")
        print("3. See docs/MEMORY-CONTEXT-WEEK1-IMPLEMENTATION.md")
        return 0
    else:
        print("\n\033[0;31m✗ Some tests failed. Please fix issues before proceeding.\033[0m")
        print("\nTroubleshooting:")
        print("1. Ensure Docker Compose services are running: docker-compose ps")
        print("2. Check service logs: docker-compose logs [service-name]")
        print("3. Verify .env file has correct credentials")
        return 1


if __name__ == "__main__":
    sys.exit(main())
