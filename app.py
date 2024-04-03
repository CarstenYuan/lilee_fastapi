import os
import argparse
from fastapi import FastAPI
from uvicorn import run as uvicorn_run



if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--config', type=str, default='./db.config',
                        help='Select a db config file. Default: db.config')
    
    args = parser.parse_args()
    os.environ["DB_CONFIG_FILE"] = args.config

    # apis will import database and create/use MySQLDB,
    # so move down here in order to get the desired file path
    from apis import router
    
    app = FastAPI(title='LiLee Web Server APIs', docs_url='/swagger')
    app.include_router(router)
    uvicorn_run(app, host='127.0.0.1', port=9000, workers=1, reload=False)
