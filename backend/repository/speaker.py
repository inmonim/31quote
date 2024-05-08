from sqlalchemy.orm import Session

from model.speaker import Speaker
from DTO.speaker import SpeakerDTO, CreateSpeakerDTO

class SpeakerRepository:
    
    def __init__(self, db : Session):
        self.db = db
    
    
    def get_speaker(self, speaker_id : int) -> SpeakerDTO:
        speaker_obj = self.db.query(Speaker).get(speaker_id)
        
        speaker = SpeakerDTO(**speaker_obj.__dict__)
        
        return speaker
    
    def create_speaker(self, create_speaker_data):
        pass