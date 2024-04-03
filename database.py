import os
import configparser

from models import Base, Groups, Users
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy_utils import database_exists, create_database


class MySQLDB:
    def __init__(self):
        config_file = os.getenv("DB_CONFIG_FILE", "./db.config")
        config = configparser.ConfigParser()
        config.read(config_file)

        self.username = config['database']['username']
        self.password = config['database']['password']
        self.host = config['database']['host']
        self.port = config['database']['port']
        self.dbname = config['database']['dbname']

        self.engine_url = f"mysql+pymysql://{self.username}:{self.password}@{self.host}:{self.port}/{self.dbname}"
        self.engine = create_engine(self.engine_url)
        self.SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=self.engine)

        # check if db exists
        if not database_exists(self.engine.url):
            create_database(self.engine.url)
            # create users and groups tables
            self.create_tables() 
        
    def get_db(self):
        db = self.SessionLocal()
        try:
            yield db
        finally:
            db.close()

    def create_tables(self):
        Base.metadata.create_all(bind=self.engine)
