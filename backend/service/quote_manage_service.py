from fastapi import HTTPException
import pandas as pd
from io import BytesIO

from util import session_injection
from repository import reference_repo, user_repo, quote_repo, speaker_repo, category_repo
from DTO import CreateSpeakerDTO, CreateCategoryDTO, CreateReferenceDTO, CreateReferenceTypeDTO, CreateQuoteDTO
from DTO import ResponseSpeakerDTO, ResponseCategoryDTO, ResponseQuoteDTO, ResponseReferenceDTO, ResponseReferenceTypeDTO, ResponseQuoteKoSentenceDTO, ResponseSpeakerKoNameDTO

class QuoteManageService:
    
    def __init__(self):
        self.speaker_repo = speaker_repo
        self.category_repo = category_repo
        self.quote_repo = quote_repo
        self.reference_repo = reference_repo
    
    
    async def create_speaker(self, data : CreateSpeakerDTO) -> ResponseSpeakerDTO:
        db = await session_injection()
        speaker = await self.speaker_repo.create_speaker(db, data)
        speaker_response = ResponseSpeakerDTO.model_validate(speaker)
        return speaker_response
    
    
    async def create_category(self, data : CreateCategoryDTO) -> ResponseCategoryDTO:
        db = await session_injection()
        category = await self.category_repo.create_category(db, data)
        category_response = ResponseCategoryDTO.model_validate(category)
        return category_response
    
    
    async def create_quote(self, data : CreateQuoteDTO) -> ResponseQuoteDTO:
        db = await session_injection()
        quote = await self.quote_repo.create_quote(db, data)
        quote_response = ResponseQuoteDTO.model_validate(quote)
        return quote_response
    
    
    async def create_reference(self, data : CreateReferenceDTO) -> ResponseReferenceDTO:
        db = await session_injection()
        reference = await self.reference_repo.create_reference(db, data)
        reference_response = ResponseReferenceDTO.model_validate(reference)
        return reference_response
    
    
    async def create_reference_type(self, data : CreateReferenceTypeDTO) -> ResponseReferenceTypeDTO:
        db = await session_injection()
        reference_type = await self.reference_repo.create_reference_type(db, data)
        reference_type_response = ResponseReferenceTypeDTO.model_validate(reference_type)
        return reference_type_response
    
    
    async def get_quote(self, quote_id : int) -> ResponseQuoteDTO:
        db = await session_injection()
        quote = await self.quote_repo.get_quote(db, quote_id)
        quote_response = ResponseQuoteDTO.model_validate(quote)
        return quote_response
    
    
    async def get_category(self, category_id : int) -> ResponseCategoryDTO:
        db = await session_injection()
        category = await self.category_repo.get_category(db, category_id)
        category_dto = ResponseCategoryDTO.model_validate(category)
        return category_dto
    
    
    async def get_speaker(self, speaker_id : int) -> ResponseSpeakerDTO:
        db = await session_injection()
        speaker = await self.speaker_repo.get_speaker(db, speaker_id)
        speaker_dto = ResponseSpeakerDTO.model_validate(speaker)
        return speaker_dto
    
    async def get_reference(self, reference_id : int) -> ResponseReferenceDTO:
        db = await session_injection()
        reference = await self.reference_repo.get_reference(db, reference_id)
        reference_response = ResponseReferenceDTO.model_validate(reference)
        return reference_response

    async def get_reference_type(self, reference_type_id : int) -> ResponseReferenceTypeDTO:
        db = await session_injection()
        reference_type = await self.reference_repo.get_reference_type(db, reference_type_id)
        reference_type_response = ResponseReferenceTypeDTO.model_validate(reference_type)
        return reference_type_response
    
    
    async def find_quote(self, search_text : str) -> list[ResponseQuoteKoSentenceDTO]:
        db = await session_injection()
        result = await self.quote_repo.find_quote(db, search_text)
        
        if not result:
            raise HTTPException(404, "리소스 없음")
        
        quotes = [ResponseQuoteKoSentenceDTO.model_validate(quote) for quote in result]
        return quotes
    
    async def find_speakers(self, search_text : str) -> list[ResponseSpeakerKoNameDTO]:
        db = await session_injection()
        result = await self.speaker_repo.find_speaker(db, search_text)
        
        if not result:
            raise HTTPException(404, "발언자 없음")
        
        speakers = [ResponseSpeakerKoNameDTO.model_validate(speaker) for speaker in result]
        
        return speakers
    
    async def find_categories(self, search_text : str) -> list[ResponseCategoryDTO]:
        db = await session_injection()
        result = await self.category_repo.find_categories(db, search_text)
        
        if not result:
            raise HTTPException(404, "카테고리 없음")
        
        categories = [ResponseCategoryDTO.model_validate(category) for category in result]
        
        return categories
    
    async def find_references(self, search_text : str) -> list[ResponseReferenceDTO]:
        db = await session_injection()
        result = await self.reference_repo.find_references(db, search_text)
        
        if not result:
            raise HTTPException(404, "레퍼런스 없음")
        
        references = [ResponseReferenceDTO.model_validate(reference) for reference in result]
        
        return references
    
    async def get_all_reference_types(self) -> list[ResponseReferenceTypeDTO]:
        db = await session_injection()
        result = await self.reference_repo.get_all_reference_types(db)
        
        reference_types = [ResponseReferenceTypeDTO.model_validate(reference_type) for reference_type in result]
        
        return reference_types
    
    
    async def input_quote_xlsx(self, xlsx):
        db = await session_injection()
        
        contents = await xlsx.read()
        excel_data = BytesIO(contents)
        
        df = pd.read_excel(excel_data, engine="openpyxl")
        
        df = df.replace({float('nan') : None})
        
        fail_cnt = 0
        
        for i in range(len(df)):
            category = df.iloc[i, 0]
            ko_sentence = df.iloc[i, 1]
            org_sentence = df.iloc[i, 2]
            speaker_ko_name = df.iloc[i, 3]
            reference = df.iloc[i, 4]
            reference_type = df.iloc[i, 5]
            speaker_org_name = df.iloc[i, 6]
            
            if await self.quote_repo.find_quote(db, ko_sentence):
                continue
            
            category_id = await self.category_repo.find_categories(db, category)[0].category_id
            
            speaker_id = None
            if not pd.isna(speaker_ko_name):
                speakers = await self.speaker_repo.find_speaker(db, speaker_ko_name)
                if not speakers:
                    create_speaker = CreateSpeakerDTO(ko_name=speaker_ko_name,
                                    org_name=speaker_org_name)
                    speaker_id = await self.speaker_repo.create_speaker(db, create_speaker).speaker_id
                else:
                    speaker_id = speakers[0].speaker_id
            
            reference_id = None
            if not pd.isna(reference):
                references = await self.reference_repo.find_references(db, reference)
                
                if not references:
                    reference_types = await self.reference_repo.get_all_reference_types(db)
                    for rt in reference_types:
                        if rt.reference_type == reference_type:
                            reference_type_id = rt.reference_type_id
                    
                    reference_create = CreateReferenceDTO(reference_name=reference,
                                                        reference_type_id=reference_type_id)
                    reference_id = await self.reference_repo.create_reference(db, reference_create).reference_id
                else:
                    reference_id = references[0].reference_id
            
            quote_create = CreateQuoteDTO(ko_sentence=ko_sentence,
                        en_sentence=org_sentence,
                        category_id=category_id,
                        speaker_id=speaker_id,
                        reference_id=reference_id)
            
            await self.quote_repo.create_quote(db, quote_create)
                
        return fail_cnt