from sqlalchemy.orm import Session, joinedload

from model import Quote, Reference
from util import dto_to_model
from DTO import CreateQuoteDTO

class QuoteRepository:
    
    def __init__(self, db : Session):
        self.db = db
    
    def create_quote(self, data : CreateQuoteDTO) -> Quote:
        quote = dto_to_model(data, Quote)
        self.db.add(quote)
        self.db.commit()
        return quote

    def get_quote(self, quote_int : int) -> Quote | None:
        quote = self.db.query(Quote).options(joinedload(Quote.category), joinedload(Quote.reference).joinedload(Reference.reference_type), joinedload(Quote.speaker)).get(quote_int)
    
        return quote