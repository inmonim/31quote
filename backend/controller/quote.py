from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder as jse
from sqlalchemy.orm import Session

from service import quote
from auth.auth import get_current_user
from config import get_db

from DTO.quote import QuoteResultDTO, CreateQuoteDTO

router = APIRouter()

@router.get('/getAllRandomQuote')
async def get_all_random_quote(db : Session = Depends(get_db)) -> QuoteResultDTO:
    
    quote_result = quote.get_random_quote(db) 

    return JSONResponse(jse(quote_result), 200)


@router.get('/getUsersAllCatergoryByOneQuote')
async def get_quote_by_users_all_category(db : Session = Depends(get_db),
                                                  user_id : int = Depends(get_current_user),
                                                  ) -> QuoteResultDTO:
    
    quote_result = quote.get_quote_by_users_all_category(db, user_id)
    
    return JSONResponse(jse(quote_result),
                        200)


@router.get('/getQuoteByCategory/{category_id}')
async def get_quote_by_category_id(category_id: int, db : Session = Depends(get_db)) -> QuoteResultDTO:
    
    quote_result = quote.get_quote_by_category(db, category_id)
    
    return JSONResponse(jse(quote_result),
                        200)


@router.post('/createNewQuote')
async def create_new_quote(create_quote_data : CreateQuoteDTO, db : Session = Depends(get_db)) -> QuoteResultDTO:
    
    quote_meta_id = quote.create_quote(db, create_quote_data)
    
    quote_result = quote.get_quote_by_id(db, quote_meta_id)
    
    return JSONResponse(jse(quote_result),
                        201)