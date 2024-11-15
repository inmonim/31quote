from fastapi import HTTPException
from sqlalchemy.orm import Session
import pandas as pd
from io import BytesIO

from repository import reference_repo, user_repo, quote_repo, speaker_repo, category_repo
from DTO import CreateSpeakerDTO, CreateCategoryDTO, CreateReferenceDTO, CreateReferenceTypeDTO, CreateQuoteDTO
from DTO import ResponseSpeakerDTO, ResponseCategoryDTO, ResponseQuoteDTO, ResponseReferenceDTO, ResponseReferenceTypeDTO, ResponseQuoteKoSentenceDTO, ResponseSpeakerKoNameDTO

class QuoteManageService:
    
    def __init__(self):
        print("Quote Manage Service 생성")
        self.speaker_repo = speaker_repo
        self.category_repo = category_repo
        self.quote_repo = quote_repo
        self.reference_repo = reference_repo
    
    
    async def create_speaker(self, data : CreateSpeakerDTO, db: Session) -> ResponseSpeakerDTO:
        speaker = await self.speaker_repo.create_speaker(data, db)
        speaker_response = ResponseSpeakerDTO.model_validate(speaker)
        return speaker_response
    
    
    async def create_category(self, data : CreateCategoryDTO, db: Session) -> ResponseCategoryDTO:

        category = await self.category_repo.create_category(data, db)
        category_response = ResponseCategoryDTO.model_validate(category)
        return category_response
    
    
    async def create_quote(self, data : CreateQuoteDTO, db: Session) -> ResponseQuoteDTO:

        quote = await self.quote_repo.create_quote(data, db)
        quote_response = ResponseQuoteDTO.model_validate(quote)
        return quote_response
    
    
    async def create_reference(self, data : CreateReferenceDTO, db: Session) -> ResponseReferenceDTO:

        reference = await self.reference_repo.create_reference(data, db)
        reference_response = ResponseReferenceDTO.model_validate(reference)
        return reference_response
    
    
    async def create_reference_type(self, data : CreateReferenceTypeDTO, db: Session) -> ResponseReferenceTypeDTO:

        reference_type = await self.reference_repo.create_reference_type(data, db)
        reference_type_response = ResponseReferenceTypeDTO.model_validate(reference_type)
        return reference_type_response
    
    
    async def get_quote(self, quote_id : int, db: Session) -> ResponseQuoteDTO:

        quote = await self.quote_repo.get_quote(quote_id, db)
        quote_response = ResponseQuoteDTO.model_validate(quote)
        return quote_response
    
    
    async def get_category(self, category_id : int, db: Session) -> ResponseCategoryDTO:

        category = await self.category_repo.get_category(category_id, db)
        category_dto = ResponseCategoryDTO.model_validate(category)
        return category_dto
    
    
    async def get_speaker(self, speaker_id : int, db: Session) -> ResponseSpeakerDTO:

        speaker = await self.speaker_repo.get_speaker(speaker_id, db)
        speaker_dto = ResponseSpeakerDTO.model_validate(speaker)
        return speaker_dto
    
    async def get_reference(self, reference_id : int, db: Session) -> ResponseReferenceDTO:

        reference = await self.reference_repo.get_reference(reference_id, db)
        reference_response = ResponseReferenceDTO.model_validate(reference)
        return reference_response

    async def get_reference_type(self, reference_type_id : int, db: Session) -> ResponseReferenceTypeDTO:

        reference_type = await self.reference_repo.get_reference_type(reference_type_id, db)
        reference_type_response = ResponseReferenceTypeDTO.model_validate(reference_type)
        return reference_type_response
    
    
    async def find_quote(self, search_text : str, db: Session) -> list[ResponseQuoteKoSentenceDTO]:

        result = await self.quote_repo.find_quote(search_text, db)
        
        if not result:
            raise HTTPException(404, "리소스 없음")
        
        quotes = [ResponseQuoteKoSentenceDTO.model_validate(quote) for quote in result]
        return quotes
    
    async def find_speakers(self, search_text : str, db: Session) -> list[ResponseSpeakerKoNameDTO]:

        result = await self.speaker_repo.find_speaker(search_text, db)
        
        if not result:
            raise HTTPException(404, "발언자 없음")
        
        speakers = [ResponseSpeakerKoNameDTO.model_validate(speaker) for speaker in result]
        
        return speakers
    
    async def find_categories(self, search_text : str, db: Session) -> list[ResponseCategoryDTO]:

        result = await self.category_repo.find_categories(search_text, db)
        
        if not result:
            raise HTTPException(404, "카테고리 없음")
        
        categories = [ResponseCategoryDTO.model_validate(category) for category in result]
        
        return categories
    
    async def find_references(self, search_text : str, db: Session) -> list[ResponseReferenceDTO]:

        result = await self.reference_repo.find_references(search_text, db)
        
        if not result:
            raise HTTPException(404, "레퍼런스 없음")
        
        references = [ResponseReferenceDTO.model_validate(reference) for reference in result]
        
        return references
    
    async def get_all_reference_types(self, db: Session) -> list[ResponseReferenceTypeDTO]:

        result = await self.reference_repo.get_all_reference_types(db)
        
        reference_types = [ResponseReferenceTypeDTO.model_validate(reference_type) for reference_type in result]
        
        return reference_types
    
    
    async def input_quote_xlsx(self, xlsx, db: Session):
        
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
            
            if await self.quote_repo.find_quote(ko_sentence, db):
                continue
            
            category_id = await self.category_repo.find_categories(category, db)[0].category_id
            
            speaker_id = None
            if not pd.isna(speaker_ko_name):
                speakers = await self.speaker_repo.find_speaker(speaker_ko_name, db)
                if not speakers:
                    create_speaker = CreateSpeakerDTO(ko_name=str(speaker_ko_name),
                                    org_name=str(speaker_org_name))
                    speaker_id = await self.speaker_repo.create_speaker(create_speaker, db).speaker_id
                else:
                    speaker_id = speakers[0].speaker_id
            
            reference_id = None
            if not pd.isna(reference):
                references = await self.reference_repo.find_references(reference, db)
                
                if not references:
                    reference_types = await self.reference_repo.get_all_reference_types(db)
                    for rt in reference_types:
                        if rt.reference_type == reference_type:
                            reference_type_id = rt.reference_type_id
                    
                    reference_create = CreateReferenceDTO(reference_name=str(reference),
                                                        reference_type_id=reference_type_id)
                    reference_id = await self.reference_repo.create_reference(reference_create, db).reference_id
                else:
                    reference_id = references[0].reference_id
            
            quote_create = CreateQuoteDTO(ko_sentence=str(ko_sentence),
                        en_sentence=str(org_sentence),
                        category_id=category_id,
                        speaker_id=speaker_id,
                        reference_id=reference_id)
            
            await self.quote_repo.create_quote(quote_create, db)
                
        return fail_cnt