from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

from config import get_db
from service import QuoteManageService

from DTO import CreateCategoryDTO, CreateQuoteDTO, CreateSpeakerDTO, CreateReferenceDTO, CreateReferenceTypeDTO
from DTO import ResponseCategoryDTO, ResponseQuoteDTO, ResponseReferenceDTO, ResponseReferenceTypeDTO, ResponseSpeakerDTO, ResponseQuoteKoSentenceDTO, ResponseSpeakerKoNameDTO

router = APIRouter()

@router.post("/category", status_code=201)
def create_category(data : CreateCategoryDTO, db: Session = Depends(get_db)) -> ResponseCategoryDTO:
    new_category = QuoteManageService(db).create_category(data)
    
    return new_category

@router.post("/quote")
def create_quote(data : CreateQuoteDTO, db: Session = Depends(get_db)) -> ResponseQuoteDTO:
    new_quote = QuoteManageService(db).create_quote(data)
    
    return new_quote
    
@router.post("/speaker")
def create_speaker(data : CreateSpeakerDTO, db: Session = Depends(get_db)) -> ResponseSpeakerDTO:
    new_speaker = QuoteManageService(db).create_speaker(data)
    
    return new_speaker

@router.post("/reference")
def create_reference(data : CreateReferenceDTO, db: Session = Depends(get_db)) -> ResponseReferenceDTO:
    new_reference = QuoteManageService(db).create_reference(data)
    
    return new_reference

@router.post("/reference_type")
def create_reference_type(data : CreateReferenceTypeDTO, db: Session = Depends(get_db)) -> ResponseReferenceTypeDTO:
    new_reference_type = QuoteManageService(db).create_reference_type(data)
    
    return new_reference_type
    

@router.get("/quote")
def get_quote(quote_id : int, db : Session = Depends(get_db)) -> ResponseQuoteDTO:
    quote = QuoteManageService(db).get_quote(quote_id)
    
    return quote

@router.get("/category")
def get_category(category_id : int, db : Session = Depends(get_db)) -> ResponseCategoryDTO:
    category = QuoteManageService(db).get_category(category_id)
    
    return category

@router.get("/speaker")
def get_speaker(speaker_id : int, db : Session = Depends(get_db)) -> ResponseSpeakerDTO:
    speaker = QuoteManageService(db).get_speaker(speaker_id)
    
    return speaker

@router.get("/reference")
def get_reference(reference_id : int, db : Session = Depends(get_db)) -> ResponseReferenceDTO:
    reference = QuoteManageService(db).get_reference(reference_id)
    
    return reference

@router.get("/reference_type")
def get_reference_type(reference_type_id : int, db : Session = Depends(get_db)) -> ResponseReferenceTypeDTO:
    reference_type = QuoteManageService(db).get_reference_type(reference_type_id)
    
    return reference_type


@router.get("/find_quotes")
def find_quote(search_text : str, db : Session = Depends(get_db)) -> list[ResponseQuoteKoSentenceDTO]:
    quotes = QuoteManageService(db).find_quote(search_text)
    
    return quotes

@router.get("/find_speakers")
def find_speakers(search_text : str, db : Session = Depends(get_db)) -> list[ResponseSpeakerKoNameDTO]:
    speakers = QuoteManageService(db).find_speakers(search_text)
    
    return speakers

@router.get("/find_categories")
def find_categories(search_text : str, db : Session = Depends(get_db)) -> list[ResponseCategoryDTO]:
    categories = QuoteManageService(db).find_categories(search_text)
    
    return categories

@router.get("/find_references")
def find_references(search_text : str, db : Session = Depends(get_db)) -> list[ResponseReferenceDTO]:
    references = QuoteManageService(db).find_references(search_text)
    
    return references

@router.get("/all_reference_types")
def get_all_reference_types(db : Session = Depends(get_db)) -> list[ResponseReferenceTypeDTO]:
    reference_types = QuoteManageService(db).get_all_reference_types()
    
    return reference_types