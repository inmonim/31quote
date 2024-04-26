from fastapi import FastAPI

app = FastAPI()


@app.get('/')
async def home():
    return {'hello' : 'world'}

@app.get('/test')
async def test():
    
    return


if __name__ == '__main__':

    import uvicorn
    uvicorn.run('main:app', port=5051, host='127.0.0.1', reload=True)