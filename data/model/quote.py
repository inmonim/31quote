from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, func
from sqlalchemy.orm import relationship

from .base import Base

class Quote(Base):
    __tablename__ = 'quotes'
    
    quote_id = Column(Integer, primary_key=True, autoincrement=True)
    ko_sentence = Column(String(2047), nullable=False)
    en_sentence = Column(String(2047))
    
    created_at = Column(DateTime, default=func.current_timestamp())
    updated_at = Column(DateTime, default=func.current_timestamp(), onupdate=func.current_timestamp())
    
    category_id = Column(Integer, ForeignKey('categories.category_id'))
    speaker_id = Column(Integer, ForeignKey('speakers.speaker_id'), nullable=True)
    reference_id = Column(Integer, ForeignKey('references.reference_id'), nullable=True)
    
    category = relationship('Category')
    speaker = relationship('Speaker')
    reference = relationship('Reference')