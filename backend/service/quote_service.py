from random import choice

from fastapi import HTTPException

from repository import QuoteRepository
from DTO import ResponseQuoteDTO

class QuoteService:
    
    def __init__(self, db):
        self.quote_repo = QuoteRepository(db)
        
    
    def get_all_random_quote(self) -> ResponseQuoteDTO:
        quote = self.quote_repo.get_all_random_quote()
        
        if not quote:
            raise HTTPException(404, "Quotes table is empty")
        
        quote_response = ResponseQuoteDTO.model_validate(quote)
        
        return quote_response
    
    
    def get_category_random_quote(self, category_id : int) -> ResponseQuoteDTO:
        quote = self.quote_repo.get_category_random_quote(category_id)
        
        quote_response = ResponseQuoteDTO.model_validate(quote)
        
        return quote_response
    
    
    def get_category_list_random_quote(self, category_ids : list[int]) -> ResponseQuoteDTO:
        category_id = choice(category_ids)
        quote = self.quote_repo.get_category_random_quote(category_id)
        
        quote_response = ResponseQuoteDTO.model_validate(quote)
        
        return quote_response