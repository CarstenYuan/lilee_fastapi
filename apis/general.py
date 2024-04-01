from database import MySQLDB
# from models.base import Base

db_manager = MySQLDB()
db_session = db_manager.SessionLocal()


def validate_name():
    pass


def add_item(model_class, **kwargs):
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


def delete_item(model_class, item_id):
    try:
        item = db_session.query(model_class).filter(model_class.id == item_id).one_or_none()
        if item:
            db_session.delete(item)
            db_session.commit()
            return item
        else:
            return None
    except Exception as e:
        db_session.rollback()
        raise e
    finally:
        db_session.close()
