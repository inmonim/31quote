import time, logging

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware

from controller import quote, user_manage, speaker, user_setting

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=['GET', 'POST', 'PUT'],
    allow_headers=['*']
    )

app.include_router(quote.router, prefix='/api/v1/quote', tags=['quote'])
app.include_router(user_manage.router, prefix='/api/v1/user', tags=['user_manage', 'users_account'])
app.include_router(speaker.router, prefix='/api/v1/speaker', tags=['speaker'])
app.include_router(user_setting.router, prefix='/api/v1/user_setting', tags=['user_setting'])

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@app.middleware("http")
async def log_request_time(request: Request, call_next):

    start_time = time.time()
    
    # 요청 처리
    response = await call_next(request)
    
    end_time = time.time()

    duration = end_time - start_time
    
    # 상세 표기
    # logger.info(f"Request: {request.method} {request.url} completed in {duration:.4f} seconds")
    
    # 시간 표기
    logger.info(f"completed in {duration:.4f} seconds")
    
    return response


@app.get('/')
async def home():
    return {'hello' : '31quote'}

if __name__ == '__main__':

    import uvicorn
    uvicorn.run('main:app', port=5051, host='127.0.0.1', reload=True)