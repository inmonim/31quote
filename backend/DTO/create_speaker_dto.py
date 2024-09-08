from pydantic import BaseModel

from model import Speaker

class CreateSpeakerDTO(BaseModel):
    
    ko_name : str
    org_name : str = None
    speaker_description : str = None
    
    
    def to_model(self) -> Speaker:
        return Speaker(ko_name = self.ko_name,
                       org_name = self.org_name,
                       speaker_description = self.speaker_description)