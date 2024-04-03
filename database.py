import os
import json
import random
import configparser

from models import Base, Groups, Users
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy_utils import database_exists, create_database


class MySQLDB:
    def __init__(self):
        config_file = os.getenv("DB_CONFIG_FILE")
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
            # populate data
            with open('example_data.json', 'r') as f:
                data = json.load(f)
                print(data)
            self.populate_data(data)
        
    def get_db(self):
        db = self.SessionLocal()
        try:
            yield db
        finally:
            db.close()

    def create_tables(self):
        Base.metadata.create_all(bind=self.engine)

    def populate_data(self, data):
        db = self.SessionLocal()

        for group in data['groups']:
            print(group)
            new_group = Groups(name=group)
            db.add(new_group)
        db.commit()

        groups = db.query(Groups).all()
        
        for i, user in enumerate(data['users']):
            if i % 3 == 0:
                group = None  # None == don't join any groups
            else:
                group = random.choice(groups)
            new_user = Users(name=user, group=group)
            db.add(new_user)
        db.commit()

        print("Successfully populated data!")
        db.close()
