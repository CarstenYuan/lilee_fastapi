from sqlalchemy import create_engine
from sqlalchemy_utils import database_exists, create_database

engine = create_engine("mysql+pymysql://<username>:<password>@<host>/<dbname>[?<options>]")

if not database_exists(engine.url):
    create_database(engine.url)
