import os
# Disable ChromaDB's default embedding function to avoid onnxruntime dependency
os.environ['CHROMA_NO_DEFAULT_EMBEDDING'] = '1'

import chromadb
from chromadb.utils import embedding_functions
from src.config import config

class VectorStore:
    _instance = None
    
    def __init__(self):
        try:
            self.client = chromadb.PersistentClient(path=config.VECTOR_DB_PATH)
            self.openai_ef = embedding_functions.OpenAIEmbeddingFunction(
                api_key=config.OPENAI_API_KEY,
                model_name="text-embedding-3-small"
            )
            self.collection = self.client.get_or_create_collection(
                name="mmic_collection",
                embedding_function=self.openai_ef
            )
            self.initialized = True
        except Exception as e:
            print(f"Warning: VectorStore initialization failed: {e}")
            self.initialized = False

    def add_document(self, doc_id: str, text: str, metadata: dict):
        if not self.initialized:
            print("VectorStore not initialized, skipping add_document")
            return
        try:
            self.collection.add(
                documents=[text],
                metadatas=[metadata],
                ids=[doc_id]
            )
        except Exception as e:
            print(f"Error adding document: {e}")

    def query_similar(self, query_text: str, n_results: int = 3):
        if not self.initialized:
            print("VectorStore not initialized, returning empty results")
            return {"documents": [[]], "metadatas": [[]], "distances": [[]]}
        try:
            results = self.collection.query(
                query_texts=[query_text],
                n_results=n_results
            )
            return results
        except Exception as e:
            print(f"Error querying: {e}")
            return {"documents": [[]], "metadatas": [[]], "distances": [[]]}

def get_vector_store():
    """Lazy initialization of vector store"""
    if VectorStore._instance is None:
        VectorStore._instance = VectorStore()
    return VectorStore._instance

# For backward compatibility
vector_store = get_vector_store()
