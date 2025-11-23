#!/usr/bin/env python3
"""
CODITECT MEMORY-CONTEXT ChromaDB Setup

Configures ChromaDB for vector storage and semantic search.
Creates collections for sessions and patterns with embeddings.

Usage:
    python3 scripts/core/chromadb_setup.py [--reset] [--verbose]

Options:
    --reset     Delete existing collections before creating
    --verbose   Show detailed progress

Dependencies:
    pip install chromadb sentence-transformers

Author: AZ1.AI CODITECT Team
Sprint: Sprint +1 - MEMORY-CONTEXT Implementation Day 3
Date: 2025-11-16
"""

import os
import sys
import argparse
import logging
from pathlib import Path
from typing import List, Dict, Optional

# Add project root to path
PROJECT_ROOT = Path(__file__).parent.parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class ChromaDBSetup:
    """Setup ChromaDB for CODITECT MEMORY-CONTEXT."""

    def __init__(self, chroma_dir: Path, verbose: bool = False):
        """
        Initialize ChromaDB setup.

        Args:
            chroma_dir: Directory for ChromaDB storage
            verbose: Enable verbose logging
        """
        self.chroma_dir = Path(chroma_dir)
        self.verbose = verbose

        if self.verbose:
            logger.setLevel(logging.DEBUG)

        # Ensure directory exists
        self.chroma_dir.mkdir(parents=True, exist_ok=True)

        # Import ChromaDB (late import to provide clear error if not installed)
        try:
            import chromadb
            from chromadb.config import Settings
            self.chromadb = chromadb
            self.Settings = Settings
        except ImportError:
            raise ImportError(
                "ChromaDB not installed. Install with:\n"
                "  pip install chromadb sentence-transformers"
            )

    def get_client(self):
        """
        Create ChromaDB client.

        Returns:
            ChromaDB client instance
        """
        client = self.chromadb.PersistentClient(
            path=str(self.chroma_dir),
            settings=self.Settings(
                anonymized_telemetry=False,
                allow_reset=True,
            )
        )

        logger.info(f"Connected to ChromaDB: {self.chroma_dir}")
        return client

    def create_sessions_collection(self, client, reset: bool = False):
        """
        Create collection for session embeddings.

        Args:
            client: ChromaDB client
            reset: Delete existing collection before creating

        Returns:
            ChromaDB collection
        """
        collection_name = "sessions"

        # Delete if resetting
        if reset:
            try:
                client.delete_collection(collection_name)
                logger.info(f"Deleted existing collection: {collection_name}")
            except:
                pass  # Collection didn't exist

        # Create collection
        collection = client.get_or_create_collection(
            name=collection_name,
            metadata={
                "description": "Session conversation embeddings for semantic search",
                "hnsw:space": "cosine",  # Use cosine similarity
            }
        )

        logger.info(f"Created collection: {collection_name}")
        logger.info(f"  Embedding model: sentence-transformers/all-MiniLM-L6-v2 (default)")
        logger.info(f"  Similarity metric: cosine")

        return collection

    def create_patterns_collection(self, client, reset: bool = False):
        """
        Create collection for pattern embeddings.

        Args:
            client: ChromaDB client
            reset: Delete existing collection before creating

        Returns:
            ChromaDB collection
        """
        collection_name = "patterns"

        # Delete if resetting
        if reset:
            try:
                client.delete_collection(collection_name)
                logger.info(f"Deleted existing collection: {collection_name}")
            except:
                pass  # Collection didn't exist

        # Create collection
        collection = client.get_or_create_collection(
            name=collection_name,
            metadata={
                "description": "Pattern embeddings for similarity search and reuse",
                "hnsw:space": "cosine",  # Use cosine similarity
            }
        )

        logger.info(f"Created collection: {collection_name}")
        logger.info(f"  Embedding model: sentence-transformers/all-MiniLM-L6-v2 (default)")
        logger.info(f"  Similarity metric: cosine")

        return collection

    def add_sample_embeddings(self, sessions_collection, patterns_collection):
        """
        Add sample embeddings for testing.

        Args:
            sessions_collection: Sessions collection
            patterns_collection: Patterns collection
        """
        # Sample session embeddings
        sample_sessions = [
            {
                'id': 'session_001',
                'document': 'Implemented privacy manager with 4-level privacy model. Added PII detection using regex patterns for emails, phones, SSN, credit cards, and GitHub tokens.',
                'metadata': {
                    'title': 'Privacy Manager Implementation',
                    'privacy_level': 'TEAM',
                    'timestamp': '2025-11-16T12:00:00Z',
                }
            },
            {
                'id': 'session_002',
                'document': 'Designed SQLite database schema for MEMORY-CONTEXT system. Created tables for sessions, patterns, tags, checkpoints, and privacy audit.',
                'metadata': {
                    'title': 'Database Schema Design',
                    'privacy_level': 'PUBLIC',
                    'timestamp': '2025-11-16T15:00:00Z',
                }
            },
            {
                'id': 'session_003',
                'document': 'Fixed bug in session export engine where edge cases in conversation extraction were not handled properly.',
                'metadata': {
                    'title': 'Session Export Bug Fix',
                    'privacy_level': 'TEAM',
                    'timestamp': '2025-11-15T10:00:00Z',
                }
            },
        ]

        # Add to sessions collection
        sessions_collection.add(
            ids=[s['id'] for s in sample_sessions],
            documents=[s['document'] for s in sample_sessions],
            metadatas=[s['metadata'] for s in sample_sessions],
        )

        logger.info(f"Added {len(sample_sessions)} sample session embeddings")

        # Sample pattern embeddings
        sample_patterns = [
            {
                'id': 'pattern_001',
                'document': 'Workflow pattern: Create Python class with unit tests. Steps: 1) Create class skeleton, 2) Write comprehensive unit tests, 3) Implement functionality, 4) Run tests and verify.',
                'metadata': {
                    'type': 'workflow',
                    'name': 'Create Python Class with Tests',
                    'category': 'python-development',
                    'frequency': 15,
                }
            },
            {
                'id': 'pattern_002',
                'document': 'Decision pattern: Choose PII detection method. Evaluate regex vs ML vs LLM approaches. Consider accuracy, complexity, and performance tradeoffs. For v1.0, regex is sufficient for MVP.',
                'metadata': {
                    'type': 'decision',
                    'name': 'Choose PII Detection Method',
                    'category': 'security',
                    'frequency': 3,
                }
            },
            {
                'id': 'pattern_003',
                'document': 'Code pattern: Use Python Enum for type-safe configuration. Define configuration options as Enum members for compile-time type checking and autocomplete support.',
                'metadata': {
                    'type': 'code',
                    'name': 'Enum-based Configuration',
                    'category': 'python-patterns',
                    'frequency': 20,
                }
            },
        ]

        # Add to patterns collection
        patterns_collection.add(
            ids=[p['id'] for p in sample_patterns],
            documents=[p['document'] for p in sample_patterns],
            metadatas=[p['metadata'] for p in sample_patterns],
        )

        logger.info(f"Added {len(sample_patterns)} sample pattern embeddings")

    def test_similarity_search(self, sessions_collection, patterns_collection):
        """
        Test similarity search functionality.

        Args:
            sessions_collection: Sessions collection
            patterns_collection: Patterns collection
        """
        logger.info("Testing similarity search...")

        # Test session search
        query = "privacy and security implementation"
        results = sessions_collection.query(
            query_texts=[query],
            n_results=2,
        )

        logger.info(f"Session search results for: '{query}'")
        for i, (doc_id, distance, metadata) in enumerate(zip(
            results['ids'][0],
            results['distances'][0],
            results['metadatas'][0]
        )):
            logger.info(f"  {i+1}. {metadata['title']} (similarity: {1 - distance:.3f})")

        # Test pattern search
        query = "how to create a python class"
        results = patterns_collection.query(
            query_texts=[query],
            n_results=2,
        )

        logger.info(f"Pattern search results for: '{query}'")
        for i, (doc_id, distance, metadata) in enumerate(zip(
            results['ids'][0],
            results['distances'][0],
            results['metadatas'][0]
        )):
            logger.info(f"  {i+1}. {metadata['name']} (similarity: {1 - distance:.3f})")

    def get_collection_stats(self, client):
        """
        Get statistics for all collections.

        Args:
            client: ChromaDB client
        """
        collections = client.list_collections()

        logger.info(f"ChromaDB Statistics:")
        logger.info(f"  Total collections: {len(collections)}")

        for collection in collections:
            count = collection.count()
            logger.info(f"  - {collection.name}: {count} documents")

    def setup(self, reset: bool = False, add_samples: bool = True):
        """
        Setup ChromaDB collections.

        Args:
            reset: Delete existing collections before creating
            add_samples: Add sample embeddings for testing
        """
        try:
            # Get client
            client = self.get_client()

            # Create collections
            logger.info("Creating collections...")
            sessions_collection = self.create_sessions_collection(client, reset=reset)
            patterns_collection = self.create_patterns_collection(client, reset=reset)

            # Add sample data
            if add_samples:
                logger.info("Adding sample embeddings...")
                self.add_sample_embeddings(sessions_collection, patterns_collection)

                # Test search
                self.test_similarity_search(sessions_collection, patterns_collection)

            # Get stats
            self.get_collection_stats(client)

            # Success
            logger.info("✅ ChromaDB setup complete")

        except Exception as e:
            logger.error(f"❌ ChromaDB setup failed: {e}")
            raise


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description='Setup ChromaDB for CODITECT MEMORY-CONTEXT'
    )
    parser.add_argument(
        '--reset',
        action='store_true',
        help='Delete existing collections before creating'
    )
    parser.add_argument(
        '--verbose',
        action='store_true',
        help='Show detailed progress'
    )
    parser.add_argument(
        '--no-samples',
        action='store_true',
        help='Skip adding sample embeddings'
    )
    parser.add_argument(
        '--chroma-dir',
        type=str,
        default=None,
        help='Custom ChromaDB directory (default: MEMORY-CONTEXT/chromadb)'
    )

    args = parser.parse_args()

    # Determine ChromaDB directory
    if args.chroma_dir:
        chroma_dir = Path(args.chroma_dir)
    else:
        chroma_dir = PROJECT_ROOT.parent.parent.parent / "MEMORY-CONTEXT" / "chromadb"

    # Setup ChromaDB
    setup = ChromaDBSetup(
        chroma_dir=chroma_dir,
        verbose=args.verbose
    )

    try:
        setup.setup(
            reset=args.reset,
            add_samples=not args.no_samples
        )

        print()
        print("=" * 70)
        print("CHROMADB SETUP COMPLETE")
        print("=" * 70)
        print()
        print(f"ChromaDB directory: {chroma_dir}")
        print()
        print("Collections created:")
        print("  - sessions: Conversation embeddings for semantic search")
        print("  - patterns: Pattern embeddings for similarity and reuse")
        print()
        print("Embedding model: sentence-transformers/all-MiniLM-L6-v2")
        print("Similarity metric: cosine")
        print()
        print("Next steps:")
        print("  1. Integrate with session export: scripts/core/session_export.py")
        print("  2. Integrate with context loader: scripts/core/context_loader.py")
        print("  3. Test similarity search with real sessions")
        print()

    except ImportError as e:
        print()
        print("=" * 70)
        print("CHROMADB NOT INSTALLED")
        print("=" * 70)
        print()
        print("ChromaDB requires additional dependencies.")
        print()
        print("Install with:")
        print("  pip install chromadb sentence-transformers")
        print()
        print("Or install all MEMORY-CONTEXT dependencies:")
        print("  pip install -r requirements.txt")
        print()
        sys.exit(1)

    except Exception as e:
        print()
        print("=" * 70)
        print("CHROMADB SETUP FAILED")
        print("=" * 70)
        print()
        print(f"Error: {e}")
        print()
        sys.exit(1)


if __name__ == "__main__":
    main()
