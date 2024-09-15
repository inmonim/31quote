from typing import Optional
from pydantic import BaseModel

from util import model_to_dto

from model import Speaker

class CreateSpeakerDTO(BaseModel):
    
    ko_name : str
    org_name : str | None = None
    speaker_description : str | None = None
    born_date : str | None = None
    death_date : str | None = None
    

class ResponseSpeakerDTO(BaseModel):
    
    ko_name : str
    org_name : str | None = None
    speaker_description : str | None = None
    born_date : str | None = None
    death_date : str | None = None
    
    class Config:
        from_attributes = True