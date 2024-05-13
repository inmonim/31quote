from pydantic import BaseModel

class SpeakerDTO(BaseModel):
    speaker_id : int
    speaker_name : str
    speaker_org_name : str
    speaker_summary : str | None = None

class CreateSpeakerDTO(BaseModel):
    
    speaker_name : str
    speaker_org_name : str | None
    speaker_summary : str | None