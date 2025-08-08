from models.book import Book
from models.schemas import BookCreate
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from typing import List

class BookRepo:
    def __init__(self, db_session: AsyncSession):
        self.db_session = db_session

    async def add_book(self, book: BookCreate):
        db_book = Book(name=book.title, description=book.description)
        self.db_session.add(db_book)
        await self.db_session.commit()
        await self.db_session.refresh(db_book)
        return db_book

    async def get_book_by_id(self, book_id: int) -> Book | None:
        result = await self.db_session.execute(select(Book).where(Book.id == book_id))
        return result.scalars().first()

    async def get_books(self) -> List[Book]:
        result = await self.db_session.execute(select(Book))
        return result.scalars().all()
