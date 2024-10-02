from random import choice

from fastapi import HTTPException

from util import session_injection
from repository import quote_repo
from DTO import ResponseQuoteDTO

class QuoteService:
    
    def __init__(self, quote_repo=quote_repo):
        print("Quote 서비스 생성")
        self.quote_repo = quote_repo
        
    
    async def get_all_random_quote(self) -> ResponseQuoteDTO:
        db = await session_injection()
        quote = await self.quote_repo.get_all_random_quote(db)
        
        if not quote:
            raise HTTPException(404, "Quotes table is empty")
        
        quote_response = ResponseQuoteDTO.model_validate(quote)
        
        return quote_response
    
    
    async def get_category_random_quote(self, category_id : int) -> ResponseQuoteDTO:
        db = await session_injection()
        quote = await self.quote_repo.get_category_random_quote(db, category_id)
        
        quote_response = ResponseQuoteDTO.model_validate(quote)
        
        return quote_response
    
    
    async def get_category_list_random_quote(self, category_ids : list[int]) -> ResponseQuoteDTO:
        db = await session_injection()
        category_id = choice(category_ids)
        
        quote = await self.quote_repo.get_category_random_quote(db, category_id)
        
        quote_response = ResponseQuoteDTO.model_validate(quote)
        
        return quote_response