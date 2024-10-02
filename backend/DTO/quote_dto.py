from pydantic import BaseModel, ConfigDict

from DTO import ResponseCategoryDTO, ResponseSpeakerDTO, ResponseReferenceDTO, ResponseReferenceTypeDTO

class CreateQuoteDTO(BaseModel):
    
    ko_sentence : str
    en_sentence : str | None = None
    
    category_id : int
    speaker_id : int | None = None
    reference_id : int | None = None


class ResponseQuoteDTO(BaseModel):
    
    quote_id : int
    ko_sentence : str
    en_sentence : str | None = None
    
    category : ResponseCategoryDTO
    speaker : ResponseSpeakerDTO | None = None
    reference : ResponseReferenceDTO | None = None
    
    model_config = ConfigDict(from_attributes=True)
        
        
class ResponseQuoteKoSentenceDTO(BaseModel):
    
    quote_id : int
    ko_sentence : str
    
    model_config = ConfigDict(from_attributes=True)