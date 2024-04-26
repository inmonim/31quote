from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from dotenv import dotenv_values

ENV = dotenv_values('./.env')

HOST = ENV['HOST']
USER = ENV['USER']
PASSWORD = ENV['PASSWORD']
DATABASE = ENV['DATABASE']
PORT = ENV['PORT']

DB_URL = f'mysql+pymysql://{USER}:{PASSWORD}@{HOST}:{PORT}/{DATABASE}'

engine = create_engine(url=DB_URL)

Session = sessionmaker(bind=engine)

with Session() as session:
    session.execute('SELECT * FROM quote_meta')