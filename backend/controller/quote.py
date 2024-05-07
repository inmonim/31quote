from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from service import quote
from auth.auth import get_current_user
from database import get_db

from DTO.quote import QuoteResultDTO

router = APIRouter()

@router.get('/getAllRandomQuote')
async def get_all_random_quote_ctr(db : Session = Depends(get_db)) -> QuoteResultDTO:
    
    quote_result = quote.get_random_quote(db)

    return quote_result

@router.get('/getUsersAllCatergoryByOneQuote')
async def get_quote_by_users_all_category(db : Session = Depends(get_db),
                                                  user_id : int = Depends(get_current_user),
                                                  ) -> QuoteResultDTO:
    
    quote_result = quote.get_quote_by_users_all_category(db, user_id)
    
    return quote_result


@router.get('/getQuoteByCategory/{category_id}')
async def get_quote_by_category_id(category_id: int, db : Session = Depends(get_db)) -> QuoteResultDTO:
    
    quote_result = quote.get_quote_by_category(db, category_id)
    
    return quote_result