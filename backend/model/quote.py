from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import mapped_column, Mapped

from database import Base


class Quote(Base):
    __tablename__ = 'quote_meta'
    
    quote_id : Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    quote_category_id : Mapped[int]
    quote_subtext_id : Mapped[int]
    quote_speaker_id : Mapped[int] = mapped_column(nullable=False)
    quote_source : Mapped[str] = mapped_column(String(30))

class QuoteSentence(Base):
    __tablename__ = 'quote_sentence'
    
    sentence_id : Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    ko_sentence : Mapped[str] = mapped_column(String(200), nullable=False)
    org_sentence : Mapped[str] = mapped_column(String(400))

class QuoteCategory(Base):
    __tablename__ = 'quote_category'
    
    category_id : Mapped[int] = mapped_column(primary_key=True)
    category : Mapped[str] = mapped_column(String(30))

class QuoteSubtext(Base):
    __tablename__ = 'quote_subtext'
    
    subtext_id : Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    subtext : Mapped[str] = mapped_column(nullable=False)

class UserCheckedCategory(Base):
    __tablename__ = 'user_checked_category'
    
    user_checked_category_id : Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    user_id : Mapped[int] = mapped_column(nullable=False)
    category_id : Mapped[int] = mapped_column(nullable=False)

