from fastapi import APIRouter, Depends, UploadFile, File, HTTPException

from config import ADMIN_ID
from service import QuoteManageService
from auth import get_current_user
from DTO import CreateCategoryDTO, CreateQuoteDTO, CreateSpeakerDTO, CreateReferenceDTO, CreateReferenceTypeDTO
from DTO import ResponseCategoryDTO, ResponseQuoteDTO, ResponseReferenceDTO, ResponseReferenceTypeDTO, ResponseSpeakerDTO, ResponseQuoteKoSentenceDTO, ResponseSpeakerKoNameDTO

router = APIRouter()

quote_manage_service = QuoteManageService()

@router.post("/category", status_code=201)
async def create_category(data : CreateCategoryDTO, user = Depends(get_current_user)) -> ResponseCategoryDTO:
    if user[1] != ADMIN_ID:
        raise HTTPException(403, "You are not ADMIN")
    new_category = await quote_manage_service.create_category(data)
    
    return new_category

@router.post("/quote")
async def create_quote(data : CreateQuoteDTO, user = Depends(get_current_user)) -> ResponseQuoteDTO:
    if user[1] != ADMIN_ID:
        raise HTTPException(403, "You are not ADMIN")
    new_quote = await quote_manage_service.create_quote(data)
    
    return new_quote
    
@router.post("/speaker")
async def create_speaker(data : CreateSpeakerDTO, user = Depends(get_current_user)) -> ResponseSpeakerDTO:
    if user[1] != ADMIN_ID:
        raise HTTPException(403, "You are not ADMIN")
    new_speaker = await quote_manage_service.create_speaker(data)
    
    return new_speaker

@router.post("/reference")
async def create_reference(data : CreateReferenceDTO, user = Depends(get_current_user)) -> ResponseReferenceDTO:
    if user[1] != ADMIN_ID:
        raise HTTPException(403, "You are not ADMIN")
    new_reference = await quote_manage_service.create_reference(data)
    
    return new_reference

@router.post("/reference_type")
async def create_reference_type(data : CreateReferenceTypeDTO, user = Depends(get_current_user)) -> ResponseReferenceTypeDTO:
    if user[1] != ADMIN_ID:
        raise HTTPException(403, "You are not ADMIN")
    new_reference_type = await quote_manage_service.create_reference_type(data)
    
    return new_reference_type
    

@router.get("/quote")
async def get_quote(quote_id : int, user = Depends(get_current_user)) -> ResponseQuoteDTO:
    if user[1] != ADMIN_ID:
        raise HTTPException(403, "You are not ADMIN")
    quote = await quote_manage_service.get_quote(quote_id)
    
    return quote

@router.get("/category")
async def get_category(category_id : int, user = Depends(get_current_user)) -> ResponseCategoryDTO:
    if user[1] != ADMIN_ID:
        raise HTTPException(403, "You are not ADMIN")
    category = await quote_manage_service.get_category(category_id)
    
    return category

@router.get("/speaker")
async def get_speaker(speaker_id : int, user = Depends(get_current_user)) -> ResponseSpeakerDTO:
    if user[1] != ADMIN_ID:
        raise HTTPException(403, "You are not ADMIN")
    speaker = await quote_manage_service.get_speaker(speaker_id)
    
    return speaker

@router.get("/reference")
async def get_reference(reference_id : int, user = Depends(get_current_user)) -> ResponseReferenceDTO:
    if user[1] != ADMIN_ID:
        raise HTTPException(403, "You are not ADMIN")
    reference = await quote_manage_service.get_reference(reference_id)
    
    return reference

@router.get("/reference_type")
async def get_reference_type(reference_type_id : int, user = Depends(get_current_user)) -> ResponseReferenceTypeDTO:
    if user[1] != ADMIN_ID:
        raise HTTPException(403, "You are not ADMIN")
    reference_type = await quote_manage_service.get_reference_type(reference_type_id)
    
    return reference_type


@router.get("/find_quotes")
async def find_quote(search_text : str, user = Depends(get_current_user)) -> list[ResponseQuoteKoSentenceDTO]:
    if user[1] != ADMIN_ID:
        raise HTTPException(403, "You are not ADMIN")
    quotes = await quote_manage_service.find_quote(search_text)
    
    return quotes

@router.get("/find_speakers")
async def find_speakers(search_text : str, user = Depends(get_current_user)) -> list[ResponseSpeakerKoNameDTO]:
    if user[1] != ADMIN_ID:
        raise HTTPException(403, "You are not ADMIN")
    speakers = await quote_manage_service.find_speakers(search_text)
    
    return speakers

@router.get("/find_categories")
async def find_categories(search_text : str, user = Depends(get_current_user)) -> list[ResponseCategoryDTO]:
    if user[1] != ADMIN_ID:
        raise HTTPException(403, "You are not ADMIN")
    categories = await quote_manage_service.find_categories(search_text)
    
    return categories

@router.get("/find_references")
async def find_references(search_text : str, user = Depends(get_current_user)) -> list[ResponseReferenceDTO]:
    if user[1] != ADMIN_ID:
        raise HTTPException(403, "You are not ADMIN")
    references = await quote_manage_service.find_references(search_text)
    
    return references

@router.get("/all_reference_types")
async def get_all_reference_types(user = Depends(get_current_user)) -> list[ResponseReferenceTypeDTO]:
    if user[1] != ADMIN_ID:
        raise HTTPException(403, "You are not ADMIN")
    reference_types = await quote_manage_service.get_all_reference_types()
    
    return reference_types


@router.post("/input_xlsx")
async def input_quote_to_xlsx(xlsx_file : UploadFile = File(...), user = Depends(get_current_user)) -> int:
    if user[1] != ADMIN_ID:
        raise HTTPException(403, "You are not ADMIN")
    fail_cnt = await quote_manage_service.input_quote_xlsx(xlsx_file)
    
    return fail_cnt