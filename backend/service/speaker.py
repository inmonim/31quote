from sqlalchemy.orm import Session

from repository.speaker import SpeakerRepository
from DTO.speaker import SpeakerDTO

def get_speaker(db : Session, speaker_id : int) -> SpeakerDTO:
    
    speaker_repo = SpeakerRepository(db)
    
    speaker = speaker_repo.get_speaker(speaker_id)
    
    return speaker