from sqlalchemy.orm import Session


from repository import SpeakerRepository
from DTO import CreateSpeakerDTO

class QuoteManageService:
    
    def __init__(self, db: Session):
        self.speaker_repo = SpeakerRepository(db)
    
    def create_speaker(self, data : CreateSpeakerDTO) -> int:
        speaker_id = self.speaker_repo.create_speakr(data)
        return speaker_id