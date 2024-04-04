from apis import router
from fastapi import FastAPI
from uvicorn import run as uvicorn_run


app = FastAPI(title='LiLee Web Server APIs', docs_url='/swagger')
app.include_router(router)


if __name__ == '__main__':
    uvicorn_run('app:app', host='0.0.0.0', port=9000, reload=True)
