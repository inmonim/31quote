from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from config import get_db
from service import QuoteManageService

from DTO import CreateCategoryDTO, CreateQuoteDTO, CreateSpeakerDTO

router = APIRouter()

@router.post("/category")
def create_category(data : CreateCategoryDTO, db: Session = Depends(get_db)):
    pass

@router.post("/quote")
def create_quote(data : CreateQuoteDTO, db: Session = Depends(get_db)):
    pass
    
@router.post("/speaker")
def create_speaker(data : CreateSpeakerDTO, db: Session = Depends(get_db)):
    speaker_id = QuoteManageService(db).create_speaker(data)
    
    return {"speaker_id" : speaker_id}