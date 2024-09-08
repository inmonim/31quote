from fastapi import FastAPI

from fastapi.middleware.cors import CORSMiddleware

from controller import quote_manage_router

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=['GET', 'POST', 'PUT'],
    allow_headers=['*']
    )

app.include_router(quote_manage_router, prefix='/quote', tags=['quote'])

@app.get('/')
async def home():
    return {'hello' : '31quote'}

if __name__ == '__main__':

    import uvicorn
    uvicorn.run('main:app', port=5051, host='127.0.0.1', reload=True)