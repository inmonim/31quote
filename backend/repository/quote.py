from fastapi import HTTPException
from sqlalchemy import func
from sqlalchemy.orm import Session

from model.quote import (Quote, QuoteCategory, QuoteSentence, QuoteSubtext,
                         UserCheckedCategory)
from model.speaker import Speaker

from DTO.quote import QuoteResultDTO, SentenceDTO, SubtextDTO, CategoryDTO, QuoteMetaDTO, QuoteSpeakerDTO

class QuoteRepository:
    
    def __init__(self, db: Session):
        self.db = db
        
    
    def check_category_exists(self, category_id : int) -> bool:
        if not self.db.query(QuoteCategory).get(category_id):
            return False
        return True
    
    
    def get_quote_meta(self, quote_id : int) -> QuoteMetaDTO:
        quote_meta_obj = self.db.query(Quote).get(quote_id)
        
        quote_meta = QuoteMetaDTO(**quote_meta_obj.__dict__)
              
        return quote_meta

    # 코드 가독성 및 참조 편의를 위한 예외적 참조!
    def _get_speaker(self, speaker_id : int) -> QuoteSpeakerDTO:
        
        """" speaker 객체가 필요하면, speaker_repo 활용하기 """
        
        speaker_obj = self.db.query(Speaker).get(speaker_id)
        
        speaker = QuoteSpeakerDTO(**speaker_obj.__dict__)
        
        return speaker


    def get_category(self, category_id: int) -> CategoryDTO:
        category_obj = self.db.query(QuoteCategory).get(category_id)
        
        category = CategoryDTO(**category_obj.__dict__)

        return category


    def get_sentence(self, quote_id: int) -> SentenceDTO:  
        sentence_obj = self.db.query(QuoteSentence).get(quote_id)
        
        sentence = SentenceDTO(**sentence_obj.__dict__)
        
        return sentence


    def get_subtext(self, quote_id: int) -> SubtextDTO | None:
        subtext_obj = self.db.query(QuoteSubtext).get(quote_id)
        
        if not subtext_obj:
            return None
        
        subtext = SubtextDTO(**subtext_obj.__dict__)
        
        return subtext
    
    
    def get_random_quote(self) -> QuoteMetaDTO:
        quote_meta_obj = self.db.query(Quote).order_by(func.random()).first()
        
        quote_meta = QuoteMetaDTO(**quote_meta_obj.__dict__)
        
        return quote_meta
    
    
    def get_users_checked_category_list(self, user_id : int) -> list[QuoteCategory]:
        checked_category = self.db.query(UserCheckedCategory
                                         ).filter(UserCheckedCategory.user_id == user_id)
        
        return checked_category
    
    
    def get_quote_by_category(self, category_id : int) -> QuoteMetaDTO:
        
        quote = self.db.query(Quote).filter(Quote.quote_category_id == category_id
                                            ).order_by(func.random()
                                                       ).first()
        
        return quote


    def get_assemble_quote_by_meta(self, quote_meta : QuoteMetaDTO) -> QuoteResultDTO:
        
        quote_id = quote_meta.quote_id

        sentence = self.get_sentence(quote_id)
        subtext = self.get_subtext(quote_id)
        category = self.get_category(quote_meta.quote_category_id)
        speaker = self._get_speaker(quote_meta.quote_speaker_id)
        source = quote_meta.quote_source
        
        quote_result = QuoteResultDTO(
            quote_id = quote_id,
            quote_category = category,
            quote_sentence = sentence,
            quote_speaker = speaker,
            quote_source = source,
            quote_subtext = subtext
        )
        
        return quote_result
    
    
    def create_quote_meta(self, quote_obj : Quote) -> int:
        try:
            self.db.add(quote_obj)
            self.db.commit()
            
            quote_meta_id = quote_obj.quote_id
        except:
            return False
        
        return quote_meta_id
    
    
    def create_sentence(self, sentence_obj : QuoteSentence) -> int:
        
        try:
            self.db.add(sentence_obj)
            self.db.commit()
            
            sentence_id = sentence_obj.sentence_id
        except Exception as e:
            print(e)
            return False
        
        return sentence_id
    
    
    def create_subtext(self, subtext : QuoteSubtext) -> int:
        
        try:
            self.db.add(subtext)
            self.db.commit()
            
            subtext_id = subtext.subtext_id
        
        except:
            return False

        return subtext_id