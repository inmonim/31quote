from datetime import datetime

from sqlalchemy import Column, BigInteger, Integer, String, SmallInteger, ForeignKey, func
from sqlalchemy.orm import relationship

from .base import Base


class Role(Base):
    __tablename__ = 'roles'
    
    role_id = Column(Integer, primary_key=True)
    role = Column(String(45), nullable=False)

class User(Base):
    __tablename__ = 'users'
    
    user_id = Column(BigInteger, primary_key=True, autoincrement=True)
    nickname = Column(String(45), nullable=False)
    login_id = Column(String(255))
    password = Column(String(255))
    is_activate = Column(SmallInteger, default=1)
    
    role_id = Column(Integer, ForeignKey('roles.role_id'))
    role = relationship('Role')