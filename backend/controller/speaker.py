from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

from service import speaker
from auth.auth import get_current_user
from database import get_db

from DTO.speaker import CreateSpeakerDTO

router = APIRouter()

@router.get('/getSpeaker/{speaker_id}')
async def get_speaker_ctr(speaker_id : int, db : Session = Depends(get_db)):
    
    speaker_data = speaker.get_speaker(db, speaker_id)
    
    return JSONResponse(speaker_data.__dict__,
                        200)


@router.post('/createSpeaker')
async def create_speaker(create_speaker_data : CreateSpeakerDTO, db : Session = Depends(get_db)):
    
    speaker_data = speaker.create_speaker(db, create_speaker_data)
    
    return JSONResponse(vars(speaker_data),
                        201)