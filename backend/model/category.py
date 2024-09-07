from sqlalchemy import Column, Integer, String, DateTime, func

from .base import Base


class Category(Base):
    __tablename__ = 'categories'
    
    category_id = Column(Integer, primary_key=True, autoincrement=True)
    category = Column(String(45))
    
    created_at = Column(DateTime, default=func.now)
    updated_at = Column(DateTime, default=func.now, onupdate=func.now)