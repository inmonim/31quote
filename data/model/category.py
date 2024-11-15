from sqlalchemy import Column, Integer, String, DateTime, func
from sqlalchemy.orm import mapped_column, Mapped

from .base import Base


class Category(Base):
    __tablename__ = 'categories'
    
    category_id = Column(Integer, primary_key=True, autoincrement=True)
    category : Mapped[str] = mapped_column(String(45))
    
    created_at = Column(DateTime, default=func.current_timestamp())
    updated_at = Column(DateTime, default=func.current_timestamp(), onupdate=func.current_timestamp())