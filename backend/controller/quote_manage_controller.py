from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

from config import get_db
from service import QuoteManageService

from DTO import CreateCategoryDTO, CreateQuoteDTO, CreateSpeakerDTO, ResponseCategoryDTO

router = APIRouter()

@router.post("/category", status_code=201)
def create_category(data : CreateCategoryDTO, db: Session = Depends(get_db)) -> ResponseCategoryDTO:
    new_category = QuoteManageService(db).create_category(data)
    
    return new_category

@router.post("/quote")
def create_quote(data : CreateQuoteDTO, db: Session = Depends(get_db)):
    new_quote = QuoteManageService(db).create_quote(data)
    
    return new_quote
    
@router.post("/speaker")
def create_speaker(data : CreateSpeakerDTO, db: Session = Depends(get_db)):
    speaker_id = QuoteManageService(db).create_speaker(data)
    
    return {"speaker_id" : speaker_id}

@router.get("/quote")
def get_quote(quote_id : int, db : Session = Depends(get_db)):
    quote = QuoteManageService(db).get_quote(quote_id)
    
    return quote