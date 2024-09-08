from pydantic import BaseModel


class CreateQuoteDTO(BaseModel):
    
    ko_sentence : str
    en_sentence : str
    
    category_id : int
    speaker_id : int
    reference_id : int