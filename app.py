from fastapi import FastAPI
from apis import router
from uvicorn import run as uvicorn_run


app = FastAPI(title='LiLee Web Server APIs', docs_url='/')
app.include_router(router)


if __name__ == '__main__':
    uvicorn_run(app, host='127.0.0.1', port=9000, workers=1, reload=False)
