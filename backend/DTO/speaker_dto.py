from pydantic import BaseModel, ConfigDict

class CreateSpeakerDTO(BaseModel):
    
    ko_name : str
    org_name : str | None = None
    speaker_description : str | None = None
    born_date : str | None = None
    death_date : str | None = None
    

class ResponseSpeakerDTO(BaseModel):
    
    speaker_id : int
    ko_name : str
    org_name : str | None = None
    speaker_description : str | None = None
    born_date : str | None = None
    death_date : str | None = None
    
    model_config = ConfigDict(from_attributes=True)
        
class ResponseSpeakerKoNameDTO(BaseModel):
    
    speaker_id : int
    ko_name : str
    
    model_config = ConfigDict(from_attributes=True)