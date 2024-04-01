import configparser
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy_utils import database_exists, create_database
from models import Base

config = configparser.ConfigParser()
config.read('db.config')

username = config['database']['username']
password = config['database']['password']
host = config['database']['host']
port = config['database']['port']
dbname = config['database']['dbname']


class MySQLDB:
    def __init__(self):
        engine_url = f"mysql+pymysql://{username}:{password}@{host}:{port}/{dbname}"
        self.engine = create_engine(engine_url)
        # check if db exists
        if not database_exists(self.engine.url):
            create_database(self.engine.url)
            self.create_tables()
        self.SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=self.engine)

    def get_db(self):
        db = self.SessionLocal()
        try:
            yield db
        finally:
            db.close()

    def create_tables(self):
        Base.metadata.create_all(bind=self.engine)
