from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, func
from sqlalchemy.orm import relationship

from .base import Base
from model import Category, Speaker, Reference

class Quote(Base):
    __tablename__ = 'quotes'
    
    quote_id = Column(Integer, primary_key=True, autoincrement=True)
    ko_sentence = Column(String(2047), nullable=False)
    en_sentence = Column(String(2047))
    
    created_at = Column(DateTime, default=func.now)
    updated_at = Column(DateTime, default=func.now, onupdate=func.now)
    
    category_id = Column(Integer, ForeignKey('categories.category_id'))
    speaker_id = Column(Integer, ForeignKey('speakers.speaker_id'))
    reference_id = Column(Integer, ForeignKey('references.reference_id'))
    
    category = relationship('Category')
    speaker = relationship('Speaker')
    reference = relationship('Reference')