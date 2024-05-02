from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from view.quote import get_one_random_quote
from database import get_db

router = APIRouter()

@router.get('/test')
async def quote_hello(db : Session = Depends(get_db)):
    
    one_quote = get_one_random_quote(db)
        
    return one_quote