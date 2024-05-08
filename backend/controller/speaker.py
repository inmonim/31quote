from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

from service import speaker
from auth.auth import get_current_user
from database import get_db

from DTO.quote import QuoteResultDTO, CreateQuoteDTO

router = APIRouter()

@router.get('/getSpeaker/{speaker_id}')
async def get_speaker_ctr(speaker_id : int, db : Session = Depends(get_db)):
    
    speaker_data = speaker.get_speaker(db, speaker_id)
    
    return JSONResponse(speaker_data.__dict__,
                        200)