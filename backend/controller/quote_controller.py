from fastapi import APIRouter, Depends, Query

from service import QuoteService
from DTO import ResponseQuoteDTO

router = APIRouter()

quote_service = QuoteService()

@router.get("/all_random", status_code=200)
async def get_all_random_quote() -> ResponseQuoteDTO:
    
    random_quote = await quote_service.get_all_random_quote()
    
    return random_quote

@router.get("/category_random")
async def get_category_random_quote(category_id : int) -> ResponseQuoteDTO:
    
    random_quote = await quote_service.get_category_random_quote(category_id)
    
    return random_quote

@router.get("/category_list_random")
async def get_category_list_random_quote(category_ids : list[int] = Query(None)) -> ResponseQuoteDTO:
    
    random_quote = await quote_service.get_category_list_random_quote(category_ids)
    
    return random_quote