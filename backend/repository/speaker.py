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
    
    def check_duplicated_speaker_name(self, name) -> bool:
        
        if self.db.query(Speaker).filter(Speaker.speaker_name == name).count():
            return True
        return False
    
    def create_speaker(self, speaker_obj : Speaker) -> int:
        
        try:
            self.db.add(speaker_obj)
            self.db.commit()
            
            speaker_id = speaker_obj.speaker_id
        except:
            return False
        
        return speaker_id