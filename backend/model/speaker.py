from sqlalchemy import Column, Integer, String, DateTime, func

from .base import Base


class Speaker(Base):
    __tablename__ = 'speakers'
    
    speaker_id = Column(Integer, primary_key=True, autoincrement=True)
    ko_name = Column(String(45), nullable=False)
    org_name = Column(String(45))
    speaker_description = Column(String(2047))
    
    created_at = Column(DateTime, default=func.now)
    updated_at = Column(DateTime, default=func.now, onupdate=func.now)