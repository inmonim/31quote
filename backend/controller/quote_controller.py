from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from config import get_db
from service import QuoteService
from DTO import ResponseQuoteDTO

router = APIRouter()

@router.get("/all_random", status_code=200)
def get_all_random_quote(db : Session = Depends(get_db)) -> ResponseQuoteDTO:
    
    random_quote = QuoteService(db).get_all_random_quote()
    
    return random_quote

@router.get("/category_random")
def get_category_random_quote(category_id : int, db : Session = Depends(get_db)) -> ResponseQuoteDTO:
    
    random_quote = QuoteService(db).get_category_random_quote(category_id)
    
    return random_quote

@router.get("/category_list_random")
def get_category_list_random_quote(category_ids : list[int] = Query(None), db : Session = Depends(get_db)) -> ResponseQuoteDTO:
    
    random_quote = QuoteService(db).get_category_list_random_quote(category_ids)
    
    return random_quote