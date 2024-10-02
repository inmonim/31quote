from sqlalchemy.orm import Session

from util import session_injection, dto_to_model

from model import Speaker
from DTO import CreateSpeakerDTO

class SpeakerRepository:
    
    def __init__(self):
        pass
        
    async def create_speaker(self, db: Session, data : CreateSpeakerDTO) -> Speaker:
        speaker = dto_to_model(data, Speaker)
        db.add(speaker)
        db.commit()
        return speaker
    
    async def get_speaker(self, db: Session,  speaker_id : int) -> Speaker | None:
        speaker = db.query(Speaker).get(speaker_id)
        
        return speaker
    
    async def find_speaker(self, db: Session,  search_text : str) -> list[Speaker]:
        result = db.query(Speaker).filter(Speaker.ko_name.like(f"%{search_text}%")).all()
        
        return result


speaker_repo = SpeakerRepository()