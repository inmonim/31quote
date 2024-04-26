from fastapi import FastAPI

from controller import quote

app = FastAPI()

app.include_router(quote.router, prefix='/api/v1/quote', tags=['quote'])

@app.get('/')
async def home():
    return {'hello' : 'world'}

if __name__ == '__main__':

    import uvicorn
    uvicorn.run('main:app', port=5051, host='127.0.0.1', reload=True)