from fastapi import APIRouter, Depends, UploadFile, File

from service import QuoteManageService

from DTO import CreateCategoryDTO, CreateQuoteDTO, CreateSpeakerDTO, CreateReferenceDTO, CreateReferenceTypeDTO
from DTO import ResponseCategoryDTO, ResponseQuoteDTO, ResponseReferenceDTO, ResponseReferenceTypeDTO, ResponseSpeakerDTO, ResponseQuoteKoSentenceDTO, ResponseSpeakerKoNameDTO

router = APIRouter()

quote_manage_service = QuoteManageService()

@router.post("/category", status_code=201)
async def create_category(data : CreateCategoryDTO) -> ResponseCategoryDTO:
    new_category = await quote_manage_service.create_category(data)
    
    return new_category

@router.post("/quote")
async def create_quote(data : CreateQuoteDTO) -> ResponseQuoteDTO:
    new_quote = await quote_manage_service.create_quote(data)
    
    return new_quote
    
@router.post("/speaker")
async def create_speaker(data : CreateSpeakerDTO) -> ResponseSpeakerDTO:
    new_speaker = await quote_manage_service.create_speaker(data)
    
    return new_speaker

@router.post("/reference")
async def create_reference(data : CreateReferenceDTO) -> ResponseReferenceDTO:
    new_reference = await quote_manage_service.create_reference(data)
    
    return new_reference

@router.post("/reference_type")
async def create_reference_type(data : CreateReferenceTypeDTO) -> ResponseReferenceTypeDTO:
    new_reference_type = await quote_manage_service.create_reference_type(data)
    
    return new_reference_type
    

@router.get("/quote")
async def get_quote(quote_id : int ) -> ResponseQuoteDTO:
    quote = await quote_manage_service.get_quote(quote_id)
    
    return quote

@router.get("/category")
async def get_category(category_id : int ) -> ResponseCategoryDTO:
    category = await quote_manage_service.get_category(category_id)
    
    return category

@router.get("/speaker")
async def get_speaker(speaker_id : int ) -> ResponseSpeakerDTO:
    speaker = await quote_manage_service.get_speaker(speaker_id)
    
    return speaker

@router.get("/reference")
async def get_reference(reference_id : int ) -> ResponseReferenceDTO:
    reference = await quote_manage_service.get_reference(reference_id)
    
    return reference

@router.get("/reference_type")
async def get_reference_type(reference_type_id : int ) -> ResponseReferenceTypeDTO:
    reference_type = await quote_manage_service.get_reference_type(reference_type_id)
    
    return reference_type


@router.get("/find_quotes")
async def find_quote(search_text : str ) -> list[ResponseQuoteKoSentenceDTO]:
    quotes = await quote_manage_service.find_quote(search_text)
    
    return quotes

@router.get("/find_speakers")
async def find_speakers(search_text : str ) -> list[ResponseSpeakerKoNameDTO]:
    speakers = await quote_manage_service.find_speakers(search_text)
    
    return speakers

@router.get("/find_categories")
async def find_categories(search_text : str ) -> list[ResponseCategoryDTO]:
    categories = await quote_manage_service.find_categories(search_text)
    
    return categories

@router.get("/find_references")
async def find_references(search_text : str ) -> list[ResponseReferenceDTO]:
    references = await quote_manage_service.find_references(search_text)
    
    return references

@router.get("/all_reference_types")
async def get_all_reference_types() -> list[ResponseReferenceTypeDTO]:
    reference_types = await quote_manage_service.get_all_reference_types()
    
    return reference_types


@router.post("/input_xlsx")
async def input_quote_to_xlsx(xlsx_file : UploadFile = File(...) ) -> int:
    
    fail_cnt = await quote_manage_service.input_quote_xlsx(xlsx_file)
    
    return fail_cnt