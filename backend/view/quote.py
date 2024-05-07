
from fastapi import HTTPException
from sqlalchemy import func
from sqlalchemy.orm import Session

from model.quote import (Quote, QuoteCategory, QuoteSentence, QuoteSubtext,
                         UserCheckedCategory)
from model.user import User
from model.speaker import Speaker

from DTO.quote import QuoteResultDTO, SentenceDTO, SpeakerDTO, SubtextDTO, CategoryDTO


def get_speaker(db : Session, speaker_id : int) -> SpeakerDTO:
    speaker_obj = db.query(Speaker).get(speaker_id)
    
    speaker = SpeakerDTO(speaker_id = speaker_id,
                        speaker_name = speaker_obj.speaker_name,
                        speaker_org_name = speaker_obj.speaker_org_name,
                        speaker_summary = speaker_obj.speaker_summary)
    
    return speaker


def get_category(db : Session, category_id: int) -> CategoryDTO:
    category_obj = db.query(QuoteCategory).get(category_id)
    
    category = CategoryDTO(category_id=category_obj.category_id,
                      category=category_obj.category)
    
    return category


def get_sentence(db : Session, quote_id: int) -> SentenceDTO:  
    sentence_obj = db.query(QuoteSentence).get(quote_id)
    
    sentence = SentenceDTO(sentence_id=sentence_obj.sentence_id,
                           ko_sentence=sentence_obj.ko_sentence,
                           org_sentence=sentence_obj.org_sentence)
    
    return sentence


def get_subtext(db : Session, quote_id: int) -> SubtextDTO:
    subtext_obj = db.query(QuoteSubtext).get(quote_id)
    
    if not subtext_obj:
        return None
    
    subtext = SubtextDTO(subtext_id=subtext_obj.subtext_id,
                         subtext=subtext_obj.subtext)
    
    return subtext


def get_assemble_quote_by_meta(db : Session, quote : Quote) -> QuoteResultDTO:
    
    sentence = get_sentence(db, quote.quote_id)
    subtext = get_subtext(db, quote.quote_id)
    category = get_category(db, quote.quote_category_id)
    speaker= get_speaker(db, quote.quote_speaker_id)
    source = quote.quote_source
    
    quote_result = QuoteResultDTO(
        quote_id = quote.quote_id,
        quote_category = category,
        quote_sentence = sentence,
        quote_speaker = speaker,
        quote_source = source,
        quote_subtext = subtext
    )
    
    return quote_result


def get_one_random_quote(db : Session):

    one_quote = db.query(Quote).order_by(func.random()).first()
    
    quote_result = get_assemble_quote_by_meta(db, one_quote)
    
    return quote_result


def get_one_quote_by_users_all_category(db: Session, user_id : int) -> QuoteResultDTO:
    
    checked_category_list = db.query(UserCheckedCategory).filter(UserCheckedCategory.user_id == user_id)
    checked_category_id_list = [obj.category_id for obj in checked_category_list]
    
    if not checked_category_id_list:
        raise HTTPException(404, '유저의 선택 카테고리가 없음')
    
    one_quote = db.query(Quote).filter(Quote.quote_category_id.in_(checked_category_id_list)).order_by(func.random()).first()
    
    quote_result = get_assemble_quote_by_meta(db, one_quote)
    
    return quote_result