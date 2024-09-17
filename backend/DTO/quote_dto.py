from typing import Optional

from pydantic import BaseModel

from util import model_to_dto
from model import Quote
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
    
    class Config:
        from_attributes = True
        
        
class ResponseQuoteKoSentenceDTO(BaseModel):
    
    quote_id : int
    ko_sentence : str
    
    class Config:
        from_attributes = True