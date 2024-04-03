from database import MySQLDB
from models import Users


def add_item(model_class, **kwargs):
    db_manager = MySQLDB()
    db_session = db_manager.SessionLocal()
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
    db_manager = MySQLDB()
    db_session = db_manager.SessionLocal()
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


def can_delete_group(group_id: int) -> bool:
    db_manager = MySQLDB()
    db_session = db_manager.SessionLocal()
    users_count = db_session.query(Users).filter(Users.group_id == group_id).count()
    return users_count == 0


def get_single_item(model_class, item_id):
    db_manager = MySQLDB()
    db_session = db_manager.SessionLocal()
    try:
        item = db_session.query(model_class).filter(model_class.id == item_id).one_or_none()
        if not item:
            return None
        return item
    finally:
        db_session.close()


def get_all_items(model_class, filter: str = None):
    db_manager = MySQLDB()
    db_session = db_manager.SessionLocal()
    try:
        query = db_session.query(model_class)
        if filter:
            query = query.filter(model_class.name.like(f"%{filter}%"))
        item = query.all()
        return item
    finally:
        db_session.close()
