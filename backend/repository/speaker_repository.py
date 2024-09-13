from sqlalchemy.orm import Session

from util import dto_to_model

from model import Speaker
from DTO import CreateSpeakerDTO

class SpeakerRepository:
    
    def __init__(self, db: Session):
        self.db = db
        
    def create_speaker(self, data : CreateSpeakerDTO) -> Speaker:
        speaker: Speaker = dto_to_model(data, Speaker)
        self.db.add(speaker)
        self.db.commit()
        return speaker
    
    def get_speaker(self, speaker_id : int) -> Speaker:
        speaker: Speaker = self.db.query(Speaker).get(speaker_id)
        
        return speaker