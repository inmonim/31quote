from fastapi import FastAPI

from fastapi.middleware.cors import CORSMiddleware

from controller import quote, user_manage, speaker

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=['GET', 'POST', 'PUT'],
    allow_headers=['*']
    )

app.include_router(quote.router, prefix='/api/v1/quote', tags=['quote'])
app.include_router(user_manage.router, prefix='/api/v1/user', tags=['user'])
app.include_router(speaker.router, prefix='/api/v1/speaker', tags=['speaker'])

@app.get('/')
async def home():
    return {'hello' : '31quote'}

if __name__ == '__main__':

    import uvicorn
    uvicorn.run('main:app', port=5051, host='127.0.0.1', reload=True)