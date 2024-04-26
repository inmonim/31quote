
from sqlalchemy import func

from model.quote import Quote, QuoteCategory, QuoteSentence
from model.speaker import Speaker

from db_connect import Session

def get_quote_speaker(speaker_id, session):
    speaker = session.query(Speaker).get(speaker_id)
    return speaker

def get_one_category(category_id, session):
    category = session.query(QuoteCategory).get(category_id)
    return category.quote_category

def get_one_random_quote():
    
    with Session() as session:
        one_quote = session.query(Quote).order_by(func.random()).first()
        quote_id = one_quote.quote_id
        quote_sentence = session.query(QuoteSentence).get(quote_id)
        quote_category = get_one_category(one_quote.quote_category_id, session)
        quote_speaker = get_quote_speaker(one_quote.quote_speaker_id, session)
    
    result = {'quote_id': quote_id,
              'quote_sentence': quote_sentence,
              'quote_category': quote_category,
              'quote_speaker': quote_speaker}
    
    return result