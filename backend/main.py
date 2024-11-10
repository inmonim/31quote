import asyncio
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from controller import quote_manage_router, quote_router, user_router

from util import r
from server_setup import ServerSetup

@asynccontextmanager
async def lifespan(app : FastAPI):
    await r._initalize()
    if r.connect:
        await r.flush_db()
        server_setup = ServerSetup(r)
        await server_setup.mount_redis_data()
        del server_setup
    
    yield  # FastAPI 서버 실행
    
    print("서버 종료")


app = FastAPI(lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=['GET', 'POST', 'PUT'],
    allow_headers=['*']
    )

app.include_router(quote_manage_router, prefix='/admin', tags=['admin'])
app.include_router(quote_router, prefix='/quote', tags=['quote'])
app.include_router(user_router, prefix='/user', tags=['users'])


@app.get('/')
async def home():
    try:
        return await r.get_quote_by_category(1)
    except:
        return "redis 연결이 해제되었습니다."

if __name__ == '__main__':

    import uvicorn
    uvicorn.run('main:app', port=5050, host='127.0.0.1')