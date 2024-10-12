from sqlalchemy.orm import Session

from util import dto_to_model

from model import Speaker
from DTO import CreateSpeakerDTO

class SpeakerRepository:
    
    def __init__(self):
        print("Speaker repository 생성")
        pass
        
    async def create_speaker(self, data : CreateSpeakerDTO, db: Session) -> Speaker:
        speaker = dto_to_model(data, Speaker)
        db.add(speaker)
        db.commit()
        return speaker
    
    async def get_speaker(self, speaker_id : int, db: Session) -> Speaker | None:
        speaker = db.query(Speaker).get(speaker_id)
        
        return speaker
    
    async def find_speaker(self, search_text : str, db: Session) -> list[Speaker]:
        result = db.query(Speaker).filter(Speaker.ko_name.like(f"%{search_text}%")).all()
        
        return result


speaker_repo = SpeakerRepository()