from fastapi import HTTPException
from sqlalchemy.orm import Session

from repository import SpeakerRepository, CategoryRepository, QuoteRepository, ReferenceRepository
from DTO import CreateSpeakerDTO, CreateCategoryDTO, CreateReferenceDTO, CreateReferenceTypeDTO, CreateQuoteDTO
from DTO import ResponseSpeakerDTO, ResponseCategoryDTO, ResponseQuoteDTO, ResponseReferenceDTO, ResponseReferenceTypeDTO, ResponseQuoteKoSentenceDTO, ResponseSpeakerKoNameDTO

class QuoteManageService:
    
    def __init__(self, db: Session):
        self.speaker_repo = SpeakerRepository(db)
        self.category_repo = CategoryRepository(db)
        self.quote_repo = QuoteRepository(db)
        self.reference_repo = ReferenceRepository(db)
    
    
    def create_speaker(self, data : CreateSpeakerDTO) -> ResponseSpeakerDTO:
        speaker = self.speaker_repo.create_speaker(data)
        speaker_response = ResponseSpeakerDTO.model_validate(speaker)
        return speaker_response
    
    
    def create_category(self, data : CreateCategoryDTO) -> ResponseCategoryDTO:
        category = self.category_repo.create_category(data)
        category_response = ResponseCategoryDTO.model_validate(category)
        return category_response
    
    
    def create_quote(self, data : CreateQuoteDTO) -> ResponseQuoteDTO:
        quote = self.quote_repo.create_quote(data)
        quote_response = ResponseQuoteDTO.model_validate(quote)
        return quote_response
    
    
    def create_reference(self, data : CreateReferenceDTO) -> ResponseReferenceDTO:
        reference = self.reference_repo.create_reference(data)
        reference_response = ResponseReferenceDTO.model_validate(reference)
        return reference_response
    
    
    def create_reference_type(self, data : CreateReferenceTypeDTO) -> ResponseReferenceTypeDTO:
        reference_type = self.reference_repo.create_reference_type(data)
        reference_type_response = ResponseReferenceTypeDTO.model_validate(reference_type)
        return reference_type_response
    
    
    def get_quote(self, quote_id : int) -> ResponseQuoteDTO:
        quote = self.quote_repo.get_quote(quote_id)
        quote_response = ResponseQuoteDTO.model_validate(quote)
        return quote_response
    
    
    def get_category(self, category_id : int) -> ResponseCategoryDTO:
        category = self.category_repo.get_category(category_id)
        category_dto = ResponseCategoryDTO.model_validate(category)
        return category_dto
    
    
    def get_speaker(self, speaker_id : int) -> ResponseSpeakerDTO:
        speaker = self.speaker_repo.get_speaker(speaker_id)
        speaker_dto = ResponseSpeakerDTO.model_validate(speaker)
        return speaker_dto
    
    def get_reference(self, reference_id : int) -> ResponseReferenceDTO:
        reference = self.reference_repo.get_reference(reference_id)
        reference_response = ResponseReferenceDTO.model_validate(reference)
        return reference_response

    def get_reference_type(self, reference_type_id : int) -> ResponseReferenceTypeDTO:
        reference_type = self.reference_repo.get_reference_type(reference_type_id)
        reference_type_response = ResponseReferenceTypeDTO.model_validate(reference_type)
        return reference_type_response
    
    
    def find_quote(self, search_text : str) -> list[ResponseQuoteKoSentenceDTO]:
        result = self.quote_repo.find_quote(search_text)
        
        if not result:
            raise HTTPException(404, "리소스 없음")
        
        quotes = [ResponseQuoteKoSentenceDTO.model_validate(quote) for quote in result]
        return quotes
    
    def find_speakers(self, search_text : str) -> list[ResponseSpeakerKoNameDTO]:
        result = self.speaker_repo.find_speaker(search_text)
        
        if not result:
            raise HTTPException(404, "발언자 없음")
        
        speakers = [ResponseSpeakerKoNameDTO.model_validate(speaker) for speaker in result]
        
        return speakers
    
    def find_categories(self, search_text : str) -> list[ResponseCategoryDTO]:
        result = self.category_repo.find_categories(search_text)
        
        if not result:
            raise HTTPException(404, "카테고리 없음")
        
        categories = [ResponseCategoryDTO.model_validate(category) for category in result]
        
        return categories
    
    def find_references(self, search_text : str) -> list[ResponseReferenceDTO]:
        result = self.reference_repo.find_references(search_text)
        
        if not result:
            raise HTTPException(404, "레퍼런스 없음")
        
        references = [ResponseReferenceDTO.model_validate(reference) for reference in result]
        
        return references
    
    def get_all_reference_types(self) -> list[ResponseReferenceTypeDTO]:
        result = self.reference_repo.get_all_reference_types()
        
        reference_types = [ResponseReferenceTypeDTO.model_validate(reference_type) for reference_type in result]
        
        return reference_types