from sqlalchemy.orm import Session

from model import Speaker

from DTO import CreateSpeakerDTO

class SpeakerRepository:
    
    def __init__(self, db: Session):
        self.db = db
        
    
    def create_speakr(self, data : CreateSpeakerDTO):
        
        speaker: Speaker = CreateSpeakerDTO.to_model(data)
        self.db.add(speaker)
        self.db.commit()
        return speaker.speaker_id