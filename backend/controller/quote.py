from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from view.quote import get_one_random_quote, get_security_quote
from auth.auth import get_current_user
from database import get_db

router = APIRouter()

@router.get('/test')
async def quote_hello(db : Session = Depends(get_db)):
    
    one_quote = get_one_random_quote(db)
        
    return one_quote

@router.get('/test/security')
async def security_quote(db : Session = Depends(get_db), user_id = Depends(get_current_user)):
    
    quote = get_security_quote(db)
    
    return quote