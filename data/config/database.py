from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from config.env import (DB_HOST, DB_PASSWORD, DB_PORT, DB_TABLE, DB_USERNAME)

_DB_URL = f'mysql+pymysql://{DB_USERNAME}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_TABLE}'

_engine = create_engine(url=_DB_URL, pool_recycle=3600, echo=True)

_SessionMaker = sessionmaker(bind=_engine)

def get_db():
    db = _SessionMaker()
    try:
        yield db
    finally:
        db.close()