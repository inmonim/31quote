from fastapi import APIRouter, Depends, Query

from service import QuoteService
from DTO import ResponseQuoteDTO

router = APIRouter()

quote_service = QuoteService()

@router.get("/all_random", status_code=200, summary="랜덤 쿼트")
async def get_all_random_quote() -> ResponseQuoteDTO:
    """
    모든 quotes 중 하나를 랜덤으로 조회하여 반환
    
    Returns:
        랜덤 quote 한 개
    """
    
    random_quote = await quote_service.get_all_random_quote()
    
    return random_quote

@router.get("/category_random", status_code=200, summary="1개 카테고리 랜덤 쿼트")
async def get_category_random_quote(category_id : int) -> ResponseQuoteDTO:
    """
    1개의 카테고리 id에 해당하는 quote 랜덤 조회하여 반환
    
    Args:
        category_id : 카테고리 id
    
    Returns:
        1개 카테고리 내 랜덤 quote 한 개
    """
    
    random_quote = await quote_service.get_category_random_quote(category_id)
    
    return random_quote

@router.get("/category_list_random", status_code=200, summary="n개 카테고리 랜덤 쿼트")
async def get_category_list_random_quote(category_ids : list[int] = Query(None)) -> ResponseQuoteDTO:
    """
    n개의 카테고리 id에 해당gk는 quote 랜덤 조회하여 반환
    
    Args:
        list[category] : 카테고리 id가 담긴 리스트
    
    Returns:
        n개 카테고리 내 랜덤 quote 한 개
    """
     
    random_quote = await quote_service.get_category_list_random_quote(category_ids)
    
    return random_quote