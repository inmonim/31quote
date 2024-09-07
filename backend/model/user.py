from datetime import datetime

from sqlalchemy import Integer, String, func
from sqlalchemy.orm import mapped_column, Mapped

from config import Base

class UserProfile(Base):
    __tablename__ = 'user_profile'
    
    user_id : Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    nickname : Mapped[str] = mapped_column(String(20), unique=True, nullable=False)
    login_id : Mapped[str] = mapped_column(String(30), unique=True, nullable=False)
    password : Mapped[str] = mapped_column(String(200), nullable=False)
    create_at : Mapped[datetime] = mapped_column(insert_default=func.now(), nullable=False)
    update_at : Mapped[datetime]
    is_available : Mapped[int] = mapped_column(default=1)

class User(Base):
    __tablename__ = 'user'
    
    user_id : Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    nickname : Mapped[str] = mapped_column(String(20), unique=True, nullable=False)