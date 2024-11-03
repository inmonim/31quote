from sqlalchemy import BigInteger, Integer, String, SmallInteger, ForeignKey
from sqlalchemy.orm import relationship, mapped_column, Mapped

from .base import Base


class Role(Base):
    __tablename__ = 'roles'
    
    role_id : Mapped[int] = mapped_column(Integer, primary_key=True)
    role: Mapped[str] = mapped_column(String(45), nullable=False)

class User(Base):
    __tablename__ = 'users'
    
    user_id : Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    nickname : Mapped[str] = mapped_column(String(45), default="Test")
    login_id : Mapped[str] = mapped_column(String(255))
    password : Mapped[str] = mapped_column(String(255))
    is_activate : Mapped[int] = mapped_column(SmallInteger, default=1)
    
    role_id : Mapped[int] = mapped_column(Integer, ForeignKey('roles.role_id'))
    role = relationship('Role')