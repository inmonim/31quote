from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from config import (DB_HOST, DB_PASSWORD, DB_PORT, DB_TABLE, DB_USERNAME)

_DB_URL = f'mysql+pymysql://{DB_USERNAME}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_TABLE}'

_engine = create_engine(url=_DB_URL, pool_recycle=3600, echo=True)

_SessionMaker = sessionmaker(bind=_engine)

async def get_db():
    print("새로운 세션 생성 시도")
    db = _SessionMaker()
    print("새로운 세션 생성 성공")
    try:
        print("세션 주입")
        yield db
    finally:
        print("세션 종료")
        db.close()

async def session_injection():
    return await anext(get_db())