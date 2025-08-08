import chromadb
from typing import Any

class ChromaBookRepo:
    def __init__(self):
        self.client = chromadb.Client()
        self.collection = self.client.get_or_create_collection("books")

    async def add_book(self, book: Any, embedding: list):
        doc = f"{book.name} {book.description}"
        self.collection.add(
            documents=[doc],
            embeddings=[embedding],
            ids=[str(book.id)]
        )

    def get_book_by_id(self, book_id: str):
        results = self.collection.get(ids=[book_id])
        return results
