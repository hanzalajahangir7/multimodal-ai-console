import os
from typing import List, Dict
from openai import OpenAI
from src.config import config

class SimpleVectorStore:
    """Lightweight in-memory vector store for Vercel deployment"""
    _instance = None
    
    def __init__(self):
        try:
            self.client = OpenAI(api_key=config.OPENAI_API_KEY)
            self.documents = []  # List of {id, text, metadata, embedding}
            self.initialized = True
        except Exception as e:
            print(f"Warning: VectorStore initialization failed: {e}")
            self.initialized = False

    def _get_embedding(self, text: str) -> List[float]:
        """Get embedding from OpenAI"""
        try:
            response = self.client.embeddings.create(
                model="text-embedding-3-small",
                input=text
            )
            return response.data[0].embedding
        except Exception as e:
            print(f"Error getting embedding: {e}")
            return []

    def _cosine_similarity(self, a: List[float], b: List[float]) -> float:
        """Calculate cosine similarity between two vectors"""
        if not a or not b:
            return 0.0
        dot_product = sum(x * y for x, y in zip(a, b))
        magnitude_a = sum(x * x for x in a) ** 0.5
        magnitude_b = sum(x * x for x in b) ** 0.5
        if magnitude_a == 0 or magnitude_b == 0:
            return 0.0
        return dot_product / (magnitude_a * magnitude_b)

    def add_document(self, doc_id: str, text: str, metadata: dict):
        """Add document to vector store"""
        if not self.initialized:
            print("VectorStore not initialized, skipping add_document")
            return
        try:
            embedding = self._get_embedding(text)
            self.documents.append({
                "id": doc_id,
                "text": text,
                "metadata": metadata,
                "embedding": embedding
            })
        except Exception as e:
            print(f"Error adding document: {e}")

    def query_similar(self, query_text: str, n_results: int = 3) -> Dict:
        """Query similar documents"""
        if not self.initialized or not self.documents:
            return {"documents": [[]], "metadatas": [[]], "distances": [[]]}
        
        try:
            query_embedding = self._get_embedding(query_text)
            
            # Calculate similarities
            similarities = []
            for doc in self.documents:
                similarity = self._cosine_similarity(query_embedding, doc["embedding"])
                similarities.append((doc, similarity))
            
            # Sort by similarity (highest first)
            similarities.sort(key=lambda x: x[1], reverse=True)
            
            # Get top n results
            top_results = similarities[:n_results]
            
            # Format results to match ChromaDB format
            documents = [[doc["text"] for doc, _ in top_results]]
            metadatas = [[doc["metadata"] for doc, _ in top_results]]
            distances = [[1 - sim for _, sim in top_results]]  # Convert similarity to distance
            
            return {
                "documents": documents,
                "metadatas": metadatas,
                "distances": distances
            }
        except Exception as e:
            print(f"Error querying: {e}")
            return {"documents": [[]], "metadatas": [[]], "distances": [[]]}

def get_vector_store():
    """Lazy initialization of vector store"""
    if SimpleVectorStore._instance is None:
        SimpleVectorStore._instance = SimpleVectorStore()
    return SimpleVectorStore._instance

# For backward compatibility
vector_store = get_vector_store()
