from database import MySQLDB
from models.base import Base

db_manager = MySQLDB()
db_session = db_manager.SessionLocal()


def validate_name():
    pass


def add_item(model_class: Base, **kwargs):
    try:
        item = model_class(**kwargs)
        db_session.add(item)
        db_session.commit()
        db_session.refresh(item)
        return item
    except Exception as e:
        db_session.rollback()
        raise e
    finally:
        db_session.close()
