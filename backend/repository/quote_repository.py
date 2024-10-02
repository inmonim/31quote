from sqlalchemy import func
from sqlalchemy.orm import joinedload, Session

from model import Quote, Reference
from util import dto_to_model
from DTO import CreateQuoteDTO

quote_reo = None

class QuoteRepository:
    
    def __init__(self):
        print("Quote 레포지토리 생성")
        pass

    async def get_quote(self, db : Session, quote_id : int) -> Quote | None:
        quote = db.query(Quote).options(joinedload(Quote.category),
                                             joinedload(Quote.speaker),
                                             joinedload(Quote.reference).joinedload(Reference.reference_type),
                                             ).get(quote_id)
    
        return quote
    
    async def get_all_random_quote(self, db : Session) -> Quote | None:
        quote = db.query(Quote).options(joinedload(Quote.category),
                                             joinedload(Quote.speaker),
                                             joinedload(Quote.reference).joinedload(Reference.reference_type),
                                             ).order_by(func.random()).first()
        return quote
    
    async def get_category_random_quote(self, db : Session, category_id) -> Quote | None:
        quote = db.query(Quote).filter(Quote.category_id == category_id
                                            ).options(joinedload(Quote.category),
                                                      joinedload(Quote.speaker),
                                                      joinedload(Quote.reference).joinedload(Reference.reference_type),
                                                      ).order_by(func.random()).first()
        return quote
    
    async def find_quote(self, db : Session, search_text : str) -> list[Quote] | None:
        result = db.query(Quote).filter(Quote.ko_sentence.like(f"%{search_text}%")).all()
        return result
    
    async def create_quote(self, db : Session, data : CreateQuoteDTO) -> Quote:
        quote = dto_to_model(data, Quote)
        db.add(quote)
        db.commit()
        return quote

if __name__ != "__main__":
    quote_repo = QuoteRepository()