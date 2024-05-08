import random

from fastapi import HTTPException
from sqlalchemy.orm import Session

from DTO.quote import QuoteResultDTO, SentenceDTO, SubtextDTO, CategoryDTO, CreateQuoteDTO
from repository.quote import QuoteRepository



def get_random_quote(db : Session) -> QuoteResultDTO:

    quote_repo = QuoteRepository(db)
    
    quote = quote_repo.get_random_quote()
    
    quote_result = quote_repo.get_assemble_quote_by_meta(quote)
    
    return quote_result


def get_quote_by_users_all_category(db: Session, user_id : int) -> QuoteResultDTO:
    
    quote_repo = QuoteRepository(db)
    
    checked_category_list = quote_repo.get_users_checked_category_list(user_id)
    
    category_id_list = [obj.category_id for obj in checked_category_list]
    
    if not category_id_list:
        raise HTTPException(404, '유저의 선택 카테고리가 없음')
    
    random_category_id = random.choice(category_id_list)
    
    quote_meta = quote_repo.get_quote_by_category(random_category_id)
    
    quote_result = quote_repo.get_assemble_quote_by_meta(quote_meta)
    
    return quote_result


def get_quote_by_category(db: Session, category_id : int) -> QuoteResultDTO:
    
    quote_repo = QuoteRepository(db)
    
    quote_meta = quote_repo.get_quote_by_category(category_id)
    
    if not quote_meta:
        raise HTTPException(404, '존재하지 않는 카테고리')
    
    quote_result = quote_repo.get_assemble_quote_by_meta(quote_meta)
    
    return quote_result


def create_new_quote(db: Session, create_quote_data : CreateQuoteDTO):
    
    pass