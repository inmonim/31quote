from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import DeclarativeBase

from env import ENV

HOST = ENV['HOST']
USER = ENV['USER']
PASSWORD = ENV['PASSWORD']
DATABASE = ENV['DATABASE']
PORT = ENV['PORT']

DB_URL = f'mysql+pymysql://{USER}:{PASSWORD}@{HOST}:{PORT}/{DATABASE}'

engine = create_engine(url=DB_URL)

SessionMaker = sessionmaker(bind=engine)

class Base(DeclarativeBase):
    pass

async def get_db():
    db = SessionMaker()
    try:
        yield db
    finally:
        db.close()