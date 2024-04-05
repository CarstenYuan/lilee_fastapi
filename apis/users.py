import random
from database import MySQLDB
from fastapi import APIRouter, HTTPException, Query
from typing import Optional
from apis.general import (
                            add_item,
                            delete_item,
                            get_single_item,
                            get_all_items,
                        )
from models import Users

users_statistic_router = APIRouter()
users_tag = ['Users APIs']


@users_statistic_router.post("/AddUser", tags=users_tag)
def add_user(name: str, group_id: int = None):
    # TODO: constraint group_id --> try except
    user = add_item(Users, name=name, group_id=group_id)
    return {"item_type": "User", "name": user.name, "id": user.id, "group_id": user.group_id, "is_activated": user.is_activated}


@users_statistic_router.delete("/DeleteUser", tags=users_tag)
def delete_user(id: int):
    user = delete_item(Users, id)
    if user:
        return {"item_type": "User", "name": user.name, "id": user.id, "group_id": user.group_id, "is_activated": user.is_activated}
    raise HTTPException(status_code=404, detail=f"User with id {id} does not exist.")


@users_statistic_router.get("/GetSingleUser/{user_id}", tags=users_tag)
def get_single_user(id: int):
    user = get_single_item(Users, id)
    if user:
        return {"item_type": "User", "name": user.name, "id": user.id, "group_id": user.group_id, "is_activated": user.is_activated}
    raise HTTPException(status_code=404, detail=f"User with id {id} does not exist.")


@users_statistic_router.get("/GetAllUsers", tags=users_tag)
def get_all_users(filter: Optional[str] = Query(None)):
    users = get_all_items(Users, filter=filter)
    return users


@users_statistic_router.patch("/UpdateIsActivate", tags=users_tag)
def update_is_activate(id: int, is_activate: bool):
    test_modifiers = ["Alice", "Bob", "Charlie", "David", "Eve"]
    db_manager = MySQLDB()
    db_session = db_manager.SessionLocal()

    try:
        user = db_session.query(Users).filter(Users.id == id).first()

        if not user:
            raise HTTPException(status_code=404, detail=f"User with id {id} does not exist.")

        user.is_activate = is_activate
        user.modifier = random.choice(test_modifiers)
        db_session.commit()
        return {"item_type": "User", "name": user.name, "id": user.id, "group_id": user.group_id, "is_activate": user.is_activate}
    except Exception as e:
        db_session.rollback()
        raise e
    finally:
        db_session.close()
