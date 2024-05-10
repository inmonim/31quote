from fastapi import HTTPException
from sqlalchemy.orm import Session

from repository.speaker import SpeakerRepository
from DTO.speaker import SpeakerDTO, CreateSpeakerDTO
from model.speaker import Speaker


def get_speaker(db : Session, speaker_id : int) -> SpeakerDTO:
    
    speaker_repo = SpeakerRepository(db)
    
    speaker = speaker_repo.get_speaker(speaker_id)
    
    return speaker


def create_speaker(db : Session, speaker_data : CreateSpeakerDTO) -> SpeakerDTO:
    
    speaker_repo = SpeakerRepository(db)
    
    if speaker_repo.check_duplicated_speaker_name(speaker_data.speaker_name):
        raise HTTPException(409, "존재하는 이름")
    
    speaker_obj = Speaker(**vars(speaker_data))
    
    speaker_id = speaker_repo.create_speaker(speaker_obj)
    
    if not speaker_id:
        raise HTTPException(500, "speaker 생성 실패")
    
    speaker_obj.speaker_id = speaker_id
    
    speaker = SpeakerDTO(**vars(speaker_obj))
    
    return speaker