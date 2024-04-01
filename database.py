import configparser
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy_utils import database_exists, create_database
from models.user import Base


config = configparser.ConfigParser()
config.read('db.config')

username = config['database']['username']
password = config['database']['password']
host = config['database']['host']
port = config['database']['port']
dbname = config['database']['dbname']

engine_url = f"mysql+pymysql://{username}:{password}@{host}:{port}/{dbname}"
engine = create_engine(engine_url)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def init_db():
    if not database_exists(engine.url):
        create_database(engine.url)
    Base.metadata.create_all(bind=engine)