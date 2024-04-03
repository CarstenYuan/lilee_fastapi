import os
import argparse
import subprocess
from apis import router
from fastapi import FastAPI
from uvicorn import run as uvicorn_run

app = FastAPI(title='LiLee Web Server APIs', docs_url='/swagger')
app.include_router(router)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--config', type=str, default='./db.config',
                        help='Select a db config file. Default: db.config')
    parser.add_argument('-p', '--populate', action='store_true',
                        help='Populate data for testing Default: False')
    args = parser.parse_args()

    os.environ["DB_CONFIG_FILE"] = args.config
    os.system("alembic upgrade head")

    if args.populate:
        os.system("python populate_data.py")

    # uvicorn_run(app, host='127.0.0.1', port=9000, workers=1, reload=False)
    uvicorn_run('app:app', host='127.0.0.1', port=9000, reload=True)
