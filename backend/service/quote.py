import random

from fastapi import HTTPException
from sqlalchemy.orm import Session

from DTO.quote import QuoteResultDTO, SentenceDTO, SubtextDTO, CategoryDTO, CreateQuoteDTO
from repository.quote import QuoteRepository
from model.quote import QuoteSentence, QuoteSubtext, Quote

class QuoteService:
    
    def __init__(self, db: Session):
        self.db = db
        self.quote_repo = QuoteRepository(db)
        
    def get_quote_by_id(self, quote_id : int) -> QuoteResultDTO:
        
        quote_meta = self.quote_repo.get_quote_meta(quote_id)
        
        quote_result = self.quote_repo.get_assemble_quote_by_meta(quote_meta)
        
        return quote_result
    

    def get_random_quote(self) -> QuoteResultDTO:
        
        quote = self.quote_repo.get_random_quote()
        
        quote_result = self.quote_repo.get_assemble_quote_by_meta(quote)
        
        return quote_result


    def get_quote_by_users_all_category(self, user_id : int) -> QuoteResultDTO:
        
        checked_category_list = self.quote_repo.get_users_checked_category_list(user_id)
        
        category_id_list = [obj.category_id for obj in checked_category_list]
        
        if not category_id_list:
            raise HTTPException(404, '유저의 선택 카테고리가 없음')
        
        random_category_id = random.choice(category_id_list)
        
        quote_meta = self.quote_repo.get_quote_by_category(random_category_id)
        
        quote_result = self.quote_repo.get_assemble_quote_by_meta(quote_meta)
        
        return quote_result


    def get_quote_by_category(self, category_id : int) -> QuoteResultDTO:
        
        quote_meta = self.quote_repo.get_quote_by_category(category_id)
        
        if not quote_meta:
            raise HTTPException(404, '존재하지 않는 카테고리')
        
        quote_result = self.quote_repo.get_assemble_quote_by_meta(quote_meta)
        
        return quote_result


    # DTO의 데이터를 정리 및 검증 후 생성
    def create_quote(self, quote_data : CreateQuoteDTO) -> int:
        
        if not quote_data.quote_speaker:
            raise HTTPException(404, "speaker is empty")
        
        sentence_obj = QuoteSentence(ko_sentence = quote_data.quote_ko_sentence,
                                    org_sentence = quote_data.quote_org_sentence)
        sentence_id = self.quote_repo.create_sentence(sentence_obj)
        
        if not sentence_id:
            raise HTTPException(500, "fail to create sentence obj")
        
        if not self.quote_repo.check_category_exists(quote_data.quote_category):
            raise HTTPException(404, "not found quote's category")
        
        subtext_id = None
        if quote_data.quote_subtext:
            subtext_id = self.create_subtext(db, quote_data.quote_subtext)
            if not subtext_id:
                raise HTTPException(500, "fail to create subtext obj")
        
        quote_source = quote_data.quote_source
        
        quote_obj = Quote(quote_id = sentence_id,
                        quote_category_id = quote_data.quote_category,
                        quote_speaker_id = quote_data.quote_speaker,
                        quote_subtext_id = subtext_id,
                        quote_source = quote_source)
        
        quote_meta_id = self.quote_repo.create_quote_meta(quote_obj)
        
        return quote_meta_id


    def create_subtext(db : Session, subtext : str) -> int:
        
        quote_repo = QuoteRepository(db)
        
        subtext_obj = QuoteSubtext(subtext = subtext)
        
        subtext_id = quote_repo.create_subtext(subtext_obj)
        
        return subtext_id