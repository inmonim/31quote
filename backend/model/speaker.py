from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import mapped_column, Mapped

from config import Base

class Speaker(Base):
    
    __tablename__ = 'speaker'
    
    speaker_id : Mapped[int] = mapped_column(primary_key=True)
    speaker_name : Mapped[str] = mapped_column(String(30))
    speaker_org_name : Mapped[str] = mapped_column(String(50))
    speaker_summary : Mapped[str] = mapped_column(String(500))