from repos.chroma_repo import ChromaBookRepo
from repos.book_repo import BookRepo
from models.schemas import BookCreate
from utils.embedding_util import EmbeddingUtil
import string

class BookService:
    def __init__(self, chroma_repo: ChromaBookRepo, book_repo: BookRepo, embedding_util: EmbeddingUtil):
        self.chroma_repo = chroma_repo
        self.book_repo = book_repo
        self.embedding_util = embedding_util

    async def add_book(self, book: BookCreate):
        # Add to SQL repo first
        db_book = await self.book_repo.add_book(book)
        # Generate embedding and add to Chroma repo
        embedding = await self.embedding_util.generate_embedding(f"{db_book.title} {db_book.description}")
        await self.chroma_repo.add_book(
            book=db_book,
            embedding=embedding
        )
        return db_book
    
    async def get_book_by_prompt(self, prompt: string):
        
