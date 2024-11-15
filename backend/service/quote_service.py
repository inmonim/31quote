import random

from util import r
from repository import quote_repo
from DTO import ResponseQuoteDTO

class QuoteService:
    
    def __init__(self, quote_repo=quote_repo, redis=r):
        print("Quote Service 생성")
        self.quote_repo = quote_repo
        self.r = redis
        
    
    async def get_all_random_quote(self, db) -> ResponseQuoteDTO:
        
        try:
            random_category_id = random.randint(1, await self.r.get_category_id_range())
            quote_response = await self.r.get_quote_by_category(random_category_id)
            return quote_response
        
        except:
            quote = await self.quote_repo.get_all_random_quote(db)
            quote_response = ResponseQuoteDTO.model_validate(quote)
            
            return quote_response
    
    
    async def get_category_random_quote(self, category_id : int, db) -> ResponseQuoteDTO:
        
        try:
            quote_response = await self.r.get_quote_by_category(category_id)
            return quote_response
        
        except:
            quote = await self.quote_repo.get_category_random_quote(category_id, db)
            quote_response = ResponseQuoteDTO.model_validate(quote)
            return quote_response
    
    
    async def get_category_list_random_quote(self, category_ids : list[int], db) -> ResponseQuoteDTO:

        category_id = random.choice(category_ids)
        
        return await self.get_category_random_quote(category_id, db)