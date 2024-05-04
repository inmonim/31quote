
from sqlalchemy import func
from sqlalchemy.orm import Session

from model.quote import Quote, QuoteCategory, QuoteSentence
from model.speaker import Speaker

def get_quote_speaker(db : Session, speaker_id : int):
    speaker = db.query(Speaker).get(speaker_id)
    
    return speaker

def get_one_category(db : Session, category_id: int):
    category = db.query(QuoteCategory).get(category_id)
    return category.quote_category

def get_one_random_quote(db : Session):

    one_quote = db.query(Quote).order_by(func.random()).first()
    quote_id = one_quote.quote_id
    quote_sentence = db.query(QuoteSentence).get(quote_id)
    quote_category = get_one_category(db, one_quote.quote_category_id)
    quote_speaker = get_quote_speaker(db, one_quote.quote_speaker_id)
    
    result = {'quote_id': quote_id,
              'quote_sentence': quote_sentence,
              'quote_category': quote_category,
              'quote_speaker': quote_speaker}
    
    return result

