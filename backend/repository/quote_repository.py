import asyncio

from sqlalchemy import func
from sqlalchemy.orm import Session, joinedload
from sqlalchemy.pool import QueuePool

from config import get_db, _engine
from model import Quote, Reference
from util import dto_to_model
from DTO import CreateQuoteDTO

class QuoteRepository:
    
    def __init__(self):
        print("레포지토리 생성")
        pass

    async def session_injection(self):
        return await anext(get_db())

    async def get_quote(self, quote_id : int) -> Quote | None:
        db : Session = await anext(get_db())
        quote = db.query(Quote).options(joinedload(Quote.category),
                                             joinedload(Quote.speaker),
                                             joinedload(Quote.reference).joinedload(Reference.reference_type),
                                             ).get(quote_id)
    
        return quote
    
    async def get_all_random_quote(self) -> Quote | None:
        db = await self.session_injection()
        quote = db.query(Quote).options(joinedload(Quote.category),
                                             joinedload(Quote.speaker),
                                             joinedload(Quote.reference).joinedload(Reference.reference_type),
                                             ).order_by(func.random()).first()
        return quote
    
    async def get_category_random_quote(self, category_id) -> Quote | None:
        db : Session = await anext(get_db())
        quote = db.query(Quote).filter(Quote.category_id == category_id
                                            ).options(joinedload(Quote.category),
                                                      joinedload(Quote.speaker),
                                                      joinedload(Quote.reference).joinedload(Reference.reference_type),
                                                      ).order_by(func.random()).first()
        return quote
    
    def find_quote(self, search_text : str) -> list[Quote] | None:
        result = self.db.query(Quote).filter(Quote.ko_sentence.like(f"%{search_text}%")).all()
        return result
    

    def create_quote(self, data : CreateQuoteDTO) -> Quote:
        quote = dto_to_model(data, Quote)
        self.db.add(quote)
        self.db.commit()
        return quote