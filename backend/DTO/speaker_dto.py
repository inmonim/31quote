from typing import Optional
from pydantic import BaseModel

class CreateSpeakerDTO(BaseModel):
    
    ko_name : str
    org_name : Optional[str | None] = None
    speaker_description : Optional[str | None] = None
    born_date : Optional[str | None] = None
    death_date : Optional[str | None] = None
    

class ResponseSpeakerDTO(BaseModel):
    
    ko_name : str
    org_name : Optional[str | None] = None
    speaker_description : Optional[str | None] = None
    born_date : Optional[str | None] = None
    death_date : Optional[str | None] = None