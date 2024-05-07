from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from view.quote import get_one_random_quote, get_one_quote_by_users_all_category
from auth.auth import get_current_user
from database import get_db

from DTO.quote import QuoteResultDTO

router = APIRouter()

@router.get('/getAllRandomQuote')
async def get_all_random_quote_ctr(db : Session = Depends(get_db)) -> QuoteResultDTO:
    
    quote_result = get_one_random_quote(db)

    return quote_result

@router.get('/getUsersAllCatergoryToOneQuote')
async def get_one_quote_by_users_all_category_ctr(db : Session = Depends(get_db),
                                                  user_id : int = Depends(get_current_user),
                                                  ) -> QuoteResultDTO:
    
    quote_result = get_one_quote_by_users_all_category(db, user_id)
    
    return quote_result