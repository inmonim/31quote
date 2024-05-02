from datetime import datetime

from sqlalchemy import Integer, String, func
from sqlalchemy.orm import mapped_column, Mapped

from database import Base

class User(Base):
    __tablename__ = 'user'
    
    user_id : Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    nickname : Mapped[str] = mapped_column(String(20), unique=True, nullable=False)
    login_id : Mapped[str] = mapped_column(String(30), unique=True, nullable=False)
    password : Mapped[str] = mapped_column(String(200), nullable=False)
    create_at : Mapped[datetime] = mapped_column(insert_default=func.now())
    update_at : Mapped[datetime]