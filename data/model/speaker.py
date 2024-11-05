from sqlalchemy import Column, Integer, String, DateTime, func, ForeignKey
from sqlalchemy.orm import relationship

from .base import Base

class SpeakerCareer(Base):
    __tablename__ = 'speaker_careers'
    
    speaker_career_id = Column(Integer, primary_key=True, autoincrement=True)
    speaker_career = Column(String(45), nullable=False)

class Speaker(Base):
    __tablename__ = 'speakers'
    
    speaker_id = Column(Integer, primary_key=True, autoincrement=True)
    ko_name = Column(String(45), nullable=False)
    org_name = Column(String(45))
    speaker_description = Column(String(2047))
    born_date = Column(String(45))
    death_date = Column(String(45))
    
    speaker_career_id = Column(Integer, ForeignKey('speaker_careers.speaker_career_id'))
    speaker_career = relationship("SpeakerCareer")
    
    created_at = Column(DateTime, default=func.current_timestamp())
    updated_at = Column(DateTime, default=func.current_timestamp(), onupdate=func.current_timestamp())