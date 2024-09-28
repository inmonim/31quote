from pydantic import BaseModel

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
    
    class Config:
        from_attributes = True
        
class ResponseSpeakerKoNameDTO(BaseModel):
    
    speaker_id : int
    ko_name : str
    
    class Config:
        from_attributes = True