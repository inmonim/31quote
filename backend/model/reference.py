from sqlalchemy import Column, String, DateTime, BigInteger, Integer, ForeignKey, func
from sqlalchemy.orm import relationship

from .base import Base


class ReferenceType(Base):
    __tablename__ = "reference_types"

    reference_type_id = Column(Integer, primary_key=True)
    reference_tyep = Column(String(45))


class Reference(Base):
    __tablename__ = "references"
    
    reference_id = Column(BigInteger, primary_key=True, autoincrement=True)
    reference_name = Column(String(255), nullable=False)
    year = Column(Integer, nullable=True)
    
    created_at = Column(DateTime, default=func.current_timestamp())
    updated_at = Column(DateTime, default=func.current_timestamp(), onupdate=func.current_timestamp())
    
    reference_type_id = Column(Integer, ForeignKey('reference_types.reference_type_id'))
    reference_type = relationship('ReferenceType')