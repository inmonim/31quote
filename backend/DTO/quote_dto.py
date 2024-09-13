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
    
    @classmethod
    def from_model(cls, quote : Quote):
        category_dto = model_to_dto(quote.category, ResponseCategoryDTO)
        
        speaker_dto = None
        if (speaker := quote.speaker):
            speaker_dto = model_to_dto(speaker, ResponseSpeakerDTO)
        
        reference = None
        if (reference := quote.reference):
            reference_dto = ResponseReferenceDTO.from_model(reference)
        
        return cls(quote_id = quote.quote_id,
                   ko_sentence = quote.ko_sentence,
                   en_sentence = quote.en_sentence,
                   category = category_dto,
                   speaker = speaker_dto,
                   reference = reference_dto)