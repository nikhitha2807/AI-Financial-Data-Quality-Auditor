import chromadb
from chromadb.utils import embedding_functions
import os

class VectorStore:
    def __init__(self, db_path="./chroma_db"):
        self.client = chromadb.PersistentClient(path=db_path)
        self.ef = embedding_functions.DefaultEmbeddingFunction()
        self.collection = self.client.get_or_create_collection(
            name="dataset_metadata", 
            embedding_function=self.ef
        )

    def add_dataset_context(self, dataset_id: str, context_text: str):
        """
        Store dataset summary/profile text as chunks for RAG.
        """
        # Clear existing context for this dataset if necessary or just append
        # To keep it simple, we'll use a single collection and ID prefixes
        chunks = self._split_text(context_text)
        ids = [f"{dataset_id}_{i}" for i in range(len(chunks))]
        self.collection.add(
            documents=chunks,
            ids=ids,
            metadatas=[{"dataset_id": dataset_id} for _ in chunks]
        )

    def query_context(self, dataset_id: str, query: str, n_results: int = 3):
        results = self.collection.query(
            query_texts=[query],
            n_results=n_results,
            where={"dataset_id": dataset_id}
        )
        return results['documents'][0] if results['documents'] else []

    def _split_text(self, text: str, chunk_size: int = 500):
        # Basic character splitting for now
        return [text[i:i+chunk_size] for i in range(0, len(text), chunk_size)]

    def clear_collection(self):
        self.client.delete_collection("dataset_metadata")
        self.collection = self.client.get_or_create_collection("dataset_metadata")
