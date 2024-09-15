from typing import Optional

from pydantic import BaseModel

from util import model_to_dto
from model import Quote
from DTO import ResponseCategoryDTO, ResponseSpeakerDTO, ResponseReferenceDTO, ResponseReferenceTypeDTO

class CreateQuoteDTO(BaseModel):
    
    ko_sentence : str
    en_sentence : Optional[str | None] = None
    
    category_id : int
    speaker_id : int
    reference_id : int


class ResponseQuoteDTO(BaseModel):
    
    quote_id : int
    ko_sentence : str
    en_sentence : Optional[str | None] = None
    
    category : ResponseCategoryDTO
    speaker : Optional[ResponseSpeakerDTO | None] = None
    reference : Optional[ResponseReferenceDTO | None] = None
    
    class Config:
        from_attributes = True
        
        
class ResponseQuoteKoSentenceDTO(BaseModel):
    
    quote_id : int
    ko_sentence : str
    
    class Config:
        from_attributes = True