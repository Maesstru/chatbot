from pydantic import BaseModel

class BookBase(BaseModel):
    title: str | None = None
    description: str | None = None

class BookCreate(BookBase):
    title: str
    description: str

class BookUpdate(BookBase):
    pass

class Book(BookBase):
    id: int
