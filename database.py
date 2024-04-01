import configparser
from sqlalchemy import create_engine
from sqlalchemy_utils import database_exists, create_database


config = configparser.ConfigParser()
config.read('db.config')

username = config['database']['username']
password = config['database']['password']
host = config['database']['host']
port = config['database']['port']
dbname = config['database']['dbname']

engine = create_engine(f"mysql+pymysql://{username}:{password}@{host}:{port}/{dbname}")

if not database_exists(engine.url):
    create_database(engine.url)
