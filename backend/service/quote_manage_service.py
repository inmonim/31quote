from sqlalchemy.orm import Session

from util import model_to_json, model_to_dto, _to_dict

from repository import SpeakerRepository, CategoryRepository, QuoteRepository, ReferenceRepository
from DTO import CreateSpeakerDTO, CreateCategoryDTO, ResponseCategoryDTO, ResponseSpeakerDTO, CreateQuoteDTO, ResponseQuoteDTO, ResponseReferenceDTO, ResponseReferenceTypeDTO

class QuoteManageService:
    
    def __init__(self, db: Session):
        self.speaker_repo = SpeakerRepository(db)
        self.category_repo = CategoryRepository(db)
        self.quote_repo = QuoteRepository(db)
        self.reference_repo = ReferenceRepository(db)
    
    
    def create_speaker(self, data : CreateSpeakerDTO) -> ResponseSpeakerDTO:
        speaker = self.speaker_repo.create_speaker(data)
        speaker_response = model_to_dto(speaker, ResponseSpeakerDTO)
        return speaker_response
    
    
    def create_category(self, data : CreateCategoryDTO) -> ResponseCategoryDTO:
        category = self.category_repo.create_category(data)
        category_response = model_to_dto(category, ResponseCategoryDTO)
        return category_response
    
    
    def create_quote(self, data : CreateQuoteDTO) -> ResponseQuoteDTO:
        quote = self.quote_repo.create_quote(data)
        
        quote_response = ResponseQuoteDTO.from_model(quote)
        
        return quote_response
    
    def get_quote(self, quote_id : int) -> ResponseQuoteDTO:
        quote = self.quote_repo.get_quote(quote_id)
        
        if quote:
            quote_response = ResponseQuoteDTO.from_model(quote)
    
        return quote_response