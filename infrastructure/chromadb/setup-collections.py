#!/usr/bin/env python3
"""
ChromaDB Collections Setup Script

Creates and configures ChromaDB collections for CODITECT MEMORY-CONTEXT
semantic search.

Author: AZ1.AI CODITECT Team
Project: CODITECT Rollout Master - MEMORY-CONTEXT Consolidation
Date: 2025-11-17
"""

import sys
import time
from typing import Optional

try:
    import chromadb
    from chromadb.config import Settings
    from chromadb.utils import embedding_functions
except ImportError:
    print("ERROR: chromadb package not installed")
    print("Install with: pip install chromadb")
    sys.exit(1)


def wait_for_chromadb(host: str = "localhost", port: int = 8000, max_retries: int = 30) -> bool:
    """Wait for ChromaDB to be ready."""
    print(f"Waiting for ChromaDB at {host}:{port}...")

    for i in range(max_retries):
        try:
            client = chromadb.HttpClient(host=host, port=port)
            client.heartbeat()  # Check if server is alive
            print(f"✓ ChromaDB is ready (attempt {i+1}/{max_retries})")
            return True
        except Exception as e:
            if i < max_retries - 1:
                print(f"  Waiting... (attempt {i+1}/{max_retries})")
                time.sleep(2)
            else:
                print(f"✗ ChromaDB not ready after {max_retries} attempts")
                print(f"  Error: {e}")
                return False

    return False


def setup_chromadb_collections(
    host: str = "localhost",
    port: int = 8000,
    embedding_model: str = "sentence-transformers/all-MiniLM-L6-v2"
) -> bool:
    """
    Set up ChromaDB collections for MEMORY-CONTEXT.

    Args:
        host: ChromaDB server host
        port: ChromaDB server port
        embedding_model: Sentence transformer model to use

    Returns:
        True if successful, False otherwise
    """

    try:
        # Initialize ChromaDB client
        print("="*60)
        print("CODITECT MEMORY-CONTEXT - ChromaDB Collections Setup")
        print("="*60)
        print(f"\nConnecting to ChromaDB at {host}:{port}...")

        client = chromadb.HttpClient(host=host, port=port)

        # Test connection
        client.heartbeat()
        print("✓ Connected to ChromaDB successfully")

        # Initialize embedding function
        print(f"\nInitializing embedding function: {embedding_model}")
        sentence_transformer_ef = embedding_functions.SentenceTransformerEmbeddingFunction(
            model_name=embedding_model
        )
        print(f"✓ Embedding function initialized")
        print(f"  Model: {embedding_model}")
        print(f"  Embedding dimensions: 384")

        # Collection configurations
        collections_config = [
            {
                "name": "sessions_embeddings",
                "metadata": {
                    "description": "Session context summaries for semantic search",
                    "hnsw:space": "cosine",
                    "hnsw:construction_ef": 200,
                    "hnsw:M": 16
                }
            },
            {
                "name": "checkpoints_embeddings",
                "metadata": {
                    "description": "Checkpoint descriptions for semantic search",
                    "hnsw:space": "cosine",
                    "hnsw:construction_ef": 200,
                    "hnsw:M": 16
                }
            },
            {
                "name": "patterns_embeddings",
                "metadata": {
                    "description": "Extracted patterns for semantic search",
                    "hnsw:space": "cosine",
                    "hnsw:construction_ef": 200,
                    "hnsw:M": 16
                }
            }
        ]

        # Create or get collections
        print("\nCreating collections...")
        created_collections = []

        for config in collections_config:
            collection_name = config["name"]

            try:
                # Try to get existing collection
                collection = client.get_collection(
                    name=collection_name,
                    embedding_function=sentence_transformer_ef
                )
                print(f"✓ Collection '{collection_name}' already exists")
                print(f"  Document count: {collection.count()}")

            except Exception:
                # Collection doesn't exist, create it
                collection = client.create_collection(
                    name=collection_name,
                    metadata=config["metadata"],
                    embedding_function=sentence_transformer_ef
                )
                print(f"✓ Collection '{collection_name}' created")
                print(f"  Metadata: {config['metadata']}")

            created_collections.append(collection)

        # Test embedding generation
        print("\nTesting embedding generation...")
        test_text = "This is a test session about implementing user authentication with JWT tokens"
        test_embedding = sentence_transformer_ef([test_text])
        print(f"✓ Embedding generated successfully")
        print(f"  Input text: '{test_text}'")
        print(f"  Embedding dimensions: {len(test_embedding[0])}")
        print(f"  First 5 values: {test_embedding[0][:5]}")

        # Add test document to sessions_embeddings
        print("\nAdding test document to sessions_embeddings...")
        sessions_collection = created_collections[0]
        sessions_collection.add(
            documents=[test_text],
            metadatas=[{
                "session_id": "test-session-001",
                "privacy_level": "PUBLIC",
                "timestamp": "2025-11-17T00:00:00Z",
                "test": True
            }],
            ids=["test-embedding-001"]
        )
        print(f"✓ Test document added")
        print(f"  Document ID: test-embedding-001")

        # Test search functionality
        print("\nTesting semantic search...")
        query_text = "authentication and JWT"
        results = sessions_collection.query(
            query_texts=[query_text],
            n_results=1
        )
        print(f"✓ Search completed")
        print(f"  Query: '{query_text}'")
        print(f"  Results found: {len(results['ids'][0])}")
        if results['ids'][0]:
            print(f"  Top result ID: {results['ids'][0][0]}")
            print(f"  Distance: {results['distances'][0][0]:.4f}")
            print(f"  Document: {results['documents'][0][0][:100]}...")

        # Summary
        print("\n" + "="*60)
        print("Setup Complete!")
        print("="*60)
        print("\nCollections created:")
        for i, config in enumerate(collections_config):
            collection = created_collections[i]
            print(f"  {i+1}. {config['name']}")
            print(f"     Documents: {collection.count()}")
            print(f"     Description: {config['metadata']['description']}")

        print("\nNext steps:")
        print("1. Start migrating existing sessions and checkpoints")
        print("2. Generate embeddings for all existing content")
        print("3. Integrate with Context API (Day 2-3)")
        print("")

        return True

    except Exception as e:
        print(f"\n✗ Error during setup: {e}")
        import traceback
        traceback.print_exc()
        return False


def main():
    """Main entry point."""
    import argparse

    parser = argparse.ArgumentParser(
        description="Set up ChromaDB collections for CODITECT MEMORY-CONTEXT"
    )
    parser.add_argument(
        "--host",
        default="localhost",
        help="ChromaDB host (default: localhost)"
    )
    parser.add_argument(
        "--port",
        type=int,
        default=8000,
        help="ChromaDB port (default: 8000)"
    )
    parser.add_argument(
        "--embedding-model",
        default="sentence-transformers/all-MiniLM-L6-v2",
        help="Sentence transformer model to use"
    )
    parser.add_argument(
        "--no-wait",
        action="store_true",
        help="Don't wait for ChromaDB to be ready"
    )

    args = parser.parse_args()

    # Wait for ChromaDB to be ready (unless --no-wait)
    if not args.no_wait:
        if not wait_for_chromadb(args.host, args.port):
            print("\nERROR: ChromaDB is not ready")
            print("Make sure ChromaDB is running:")
            print("  docker-compose up -d chromadb")
            sys.exit(1)

    # Set up collections
    success = setup_chromadb_collections(
        host=args.host,
        port=args.port,
        embedding_model=args.embedding_model
    )

    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
