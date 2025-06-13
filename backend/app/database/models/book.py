from sqlalchemy import Column, String, Text, DateTime, Integer
from app.database.models.base import Base
from datetime import datetime


class Book(Base):
    """Model for storing psychological books"""

    __tablename__ = "books"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False, index=True)
    author = Column(String(255), nullable=False, index=True)
    content = Column(Text, nullable=False)
    file_path = Column(String(512), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __repr__(self):
        return f"<Book {self.id}: {self.title} by {self.author}>"
