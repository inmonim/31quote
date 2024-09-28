from fastapi import HTTPException
import pandas as pd
from io import BytesIO

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
        speaker = await self.speaker_repo.create_speaker(data)
        speaker_response = ResponseSpeakerDTO.model_validate(speaker)
        return speaker_response
    
    
    async def create_category(self, data : CreateCategoryDTO) -> ResponseCategoryDTO:
        category = await self.category_repo.create_category(data)
        category_response = ResponseCategoryDTO.model_validate(category)
        return category_response
    
    
    async def create_quote(self, data : CreateQuoteDTO) -> ResponseQuoteDTO:
        quote = await self.quote_repo.create_quote(data)
        quote_response = ResponseQuoteDTO.model_validate(quote)
        return quote_response
    
    
    async def create_reference(self, data : CreateReferenceDTO) -> ResponseReferenceDTO:
        reference = await self.reference_repo.create_reference(data)
        reference_response = ResponseReferenceDTO.model_validate(reference)
        return reference_response
    
    
    async def create_reference_type(self, data : CreateReferenceTypeDTO) -> ResponseReferenceTypeDTO:
        reference_type = await self.reference_repo.create_reference_type(data)
        reference_type_response = ResponseReferenceTypeDTO.model_validate(reference_type)
        return reference_type_response
    
    
    async def get_quote(self, quote_id : int) -> ResponseQuoteDTO:
        quote = await self.quote_repo.get_quote(quote_id)
        quote_response = ResponseQuoteDTO.model_validate(quote)
        return quote_response
    
    
    async def get_category(self, category_id : int) -> ResponseCategoryDTO:
        category = await self.category_repo.get_category(category_id)
        category_dto = ResponseCategoryDTO.model_validate(category)
        return category_dto
    
    
    async def get_speaker(self, speaker_id : int) -> ResponseSpeakerDTO:
        speaker = await self.speaker_repo.get_speaker(speaker_id)
        speaker_dto = ResponseSpeakerDTO.model_validate(speaker)
        return speaker_dto
    
    async def get_reference(self, reference_id : int) -> ResponseReferenceDTO:
        reference = await self.reference_repo.get_reference(reference_id)
        reference_response = ResponseReferenceDTO.model_validate(reference)
        return reference_response

    async def get_reference_type(self, reference_type_id : int) -> ResponseReferenceTypeDTO:
        reference_type = await self.reference_repo.get_reference_type(reference_type_id)
        reference_type_response = ResponseReferenceTypeDTO.model_validate(reference_type)
        return reference_type_response
    
    
    async def find_quote(self, search_text : str) -> list[ResponseQuoteKoSentenceDTO]:
        result = await self.quote_repo.find_quote(search_text)
        
        if not result:
            raise HTTPException(404, "리소스 없음")
        
        quotes = [ResponseQuoteKoSentenceDTO.model_validate(quote) for quote in result]
        return quotes
    
    async def find_speakers(self, search_text : str) -> list[ResponseSpeakerKoNameDTO]:
        result = await self.speaker_repo.find_speaker(search_text)
        
        if not result:
            raise HTTPException(404, "발언자 없음")
        
        speakers = [ResponseSpeakerKoNameDTO.model_validate(speaker) for speaker in result]
        
        return speakers
    
    async def find_categories(self, search_text : str) -> list[ResponseCategoryDTO]:
        result = await self.category_repo.find_categories(search_text)
        
        if not result:
            raise HTTPException(404, "카테고리 없음")
        
        categories = [ResponseCategoryDTO.model_validate(category) for category in result]
        
        return categories
    
    async def find_references(self, search_text : str) -> list[ResponseReferenceDTO]:
        result = await self.reference_repo.find_references(search_text)
        
        if not result:
            raise HTTPException(404, "레퍼런스 없음")
        
        references = [ResponseReferenceDTO.model_validate(reference) for reference in result]
        
        return references
    
    async def get_all_reference_types(self) -> list[ResponseReferenceTypeDTO]:
        result = await self.reference_repo.get_all_reference_types()
        
        reference_types = [ResponseReferenceTypeDTO.model_validate(reference_type) for reference_type in result]
        
        return reference_types
    
    
    async def input_quote_xlsx(self, xlsx):
        
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
            
            if await self.quote_repo.find_quote(ko_sentence):
                continue
            
            category_id = await self.category_repo.find_categories(category)[0].category_id
            
            speaker_id = None
            if not pd.isna(speaker_ko_name):
                speakers = await self.speaker_repo.find_speaker(speaker_ko_name)
                if not speakers:
                    create_speaker = CreateSpeakerDTO(ko_name=speaker_ko_name,
                                    org_name=speaker_org_name)
                    speaker_id = await self.speaker_repo.create_speaker(create_speaker).speaker_id
                else:
                    speaker_id = speakers[0].speaker_id
            
            reference_id = None
            if not pd.isna(reference):
                references = await self.reference_repo.find_references(reference)
                
                if not references:
                    reference_types = await self.reference_repo.get_all_reference_types()
                    for rt in reference_types:
                        if rt.reference_type == reference_type:
                            reference_type_id = rt.reference_type_id
                    
                    reference_create = CreateReferenceDTO(reference_name=reference,
                                                        reference_type_id=reference_type_id)
                    reference_id = await self.reference_repo.create_reference(reference_create).reference_id
                else:
                    reference_id = references[0].reference_id
            
            quote_create = CreateQuoteDTO(ko_sentence=ko_sentence,
                        en_sentence=org_sentence,
                        category_id=category_id,
                        speaker_id=speaker_id,
                        reference_id=reference_id)
            
            await self.quote_repo.create_quote(quote_create)
                
        return fail_cnt