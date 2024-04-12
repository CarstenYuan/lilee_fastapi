import random
from fastapi import HTTPException
from models import Users, Groups
from sqlalchemy.exc import NoResultFound


test_modifiers = ["Alice", "Bob", "Charlie", "David", "Eve"]
test_creators = ['root', 'carsten']


def add_item(model_class, db_session, **kwargs):
    try:
        item = model_class(**kwargs)
        item.creator = random.choice(test_creators)
        db_session.add(item)
        db_session.commit()
        db_session.refresh(item)
        return item
    except Exception as e:
        db_session.rollback()
        raise e
    finally:
        db_session.close()


def can_join_group(group_id: int, db_session) -> bool:
    group = get_single_item(Groups, group_id, db_session)
    if group:
        is_activate = group.is_activate
        return is_activate
    raise HTTPException(status_code=404, detail=f"Group with id {group_id} does not exist.")


def delete_item(model_class, item_id, db_session):
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


def has_member(group_id: int, db_session) -> bool:
    group = db_session.query(Groups).filter(Groups.id == group_id).one_or_none()
    if group:
        users_count = db_session.query(Users).filter(Users.group_id == group_id).count()
        return users_count != 0
    raise HTTPException(status_code=404, detail=f"Group with id {group_id} does not exist.")


def get_single_item(model_class, item_id, db_session):
    try:
        item = db_session.query(model_class).filter(model_class.id == item_id).one_or_none()
        if not item:
            return None
        return item
    finally:
        db_session.close()


def get_all_items(model_class, db_session, filter: str = None):
    try:
        query = db_session.query(model_class)
        if filter:
            query = query.filter(model_class.name.like(f"%{filter}%"))
        item = query.all()
        return item
    finally:
        db_session.close()


def update_is_activate(model_class, item_id, is_activate, db_session):
    modifier = random.choice(test_modifiers)

    try:
        item = db_session.query(model_class).filter(model_class.id == item_id).one_or_none()
        if item:
            item.is_activate = is_activate
            item.modifier = modifier
            db_session.commit()
            return item
        else:
            return None
    except Exception as e:
        db_session.rollback()
        raise e
    finally:
        db_session.close()


def update_items(model_class, item_id, kwargs: dict, db_session):
    try:
        item = db_session.query(model_class).filter_by(id=item_id).one_or_none()
        if item:
            has_changes = False

            for key, new_value in kwargs.items():
                if getattr(item, key) != new_value:
                    setattr(item, key, new_value)
                    has_changes = True
            if has_changes:
                modifier = random.choice(test_modifiers)
                item.modifier = modifier
                db_session.commit()
            else:
                db_session.rollback()
            return item
        return None
    except NoResultFound:
        # print(f"No item found with ID {item_id}")
        db_session.rollback()
    finally:
        db_session.close()
