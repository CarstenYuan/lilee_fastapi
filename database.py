import os
import configparser

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy_utils import database_exists, create_database


class MySQLDB:
    def __init__(self):
        # TODO: Dynamically assign config file to DB, ex: debug mode
        config_file = "./db.config"
        config = configparser.ConfigParser()
        config.read(config_file)

        self.username = config['database']['username']
        self.password = config['database']['password']
        self.host = config['database']['host']
        self.port = config['database']['port']
        self.dbname = config['database']['dbname']

        self.engine_url = f"mysql+pymysql://{self.username}:{self.password}@{self.host}:{self.port}/{self.dbname}"
        self.engine = create_engine(self.engine_url)
        self.SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=self.engine, expire_on_commit=False)
