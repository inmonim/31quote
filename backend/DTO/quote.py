from pydantic import BaseModel

class CategoryDTO(BaseModel):
    category_id : int
    category : str

class SentenceDTO(BaseModel):
    sentence_id : int
    ko_sentence : str
    org_sentence : str
    
class SubtextDTO(BaseModel):
    subtext_id : int
    subtext : str

class QuoteMetaDTO(BaseModel):
    quote_id : int
    quote_category_id : int
    quote_speaker_id : int
    quote_source : str | None = None
    quote_sbutext_id : int | None = None

class QuoteSpeakerDTO(BaseModel):
    speaker_id : int
    speaker_name : str
    speaker_org_name : str
    speaker_summary : str | None = None

class QuoteResultDTO(BaseModel):
    
    quote_id : int
    quote_sentence : SentenceDTO
    quote_category : CategoryDTO
    quote_speaker : QuoteSpeakerDTO
    quote_source : str | None = None
    quote_subtext : SubtextDTO | None = None    

class CreateQuoteDTO(BaseModel):
    
    quote_ko_sentence : str
    quote_org_sentence : str
    quote_speaker : str | int
    quote_source : str
    quote_subtext : str