from sqlalchemy.orm import Session

from util import dto_to_model

from model import Speaker
from DTO import CreateSpeakerDTO

class SpeakerRepository:
    
    def __init__(self, db: Session):
        self.db = db
        
    def create_speaker(self, data : CreateSpeakerDTO) -> Speaker:
        speaker = dto_to_model(data, Speaker)
        self.db.add(speaker)
        self.db.commit()
        return speaker
    
    def get_speaker(self, speaker_id : int) -> Speaker | None:
        speaker = self.db.query(Speaker).get(speaker_id)
        
        return speaker
    
    def find_speaker(self, search_text : str) -> list[Speaker]:
        result = self.db.query(Speaker).filter(Speaker.ko_name.like(f"%{search_text}%")).all()
        
        return result