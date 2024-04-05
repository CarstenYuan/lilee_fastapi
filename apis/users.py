from fastapi import APIRouter, HTTPException, Query
from typing import Optional
from apis.general import (
                            add_item,
                            delete_item,
                            get_single_item,
                            get_all_items,
                            update_is_activate,
                            can_join_group,
                        )
from models import Users

users_statistic_router = APIRouter()
users_tag = ['Users APIs']


@users_statistic_router.post("/AddUser", tags=users_tag)
def add_user(name: str, group_id: int = None):
    if not can_join_group(group_id):
        raise HTTPException(status_code=400, detail="You cannot join a deactivated group.")
    user = add_item(Users, name=name, group_id=group_id)
    return {"item_type": "User", "name": user.name, "id": user.id, "group_id": user.group_id, "is_activate": user.is_activate}


@users_statistic_router.delete("/DeleteUser", tags=users_tag)
def delete_user(id: int):
    user = delete_item(Users, id)
    if user:
        return {"item_type": "User", "name": user.name, "id": user.id, "group_id": user.group_id, "is_activate": user.is_activate}
    raise HTTPException(status_code=404, detail=f"User with id {id} does not exist.")


@users_statistic_router.get("/GetSingleUser/{user_id}", tags=users_tag)
def get_single_user(id: int):
    user = get_single_item(Users, id)
    if user:
        return {"item_type": "User", "name": user.name, "id": user.id, "group_id": user.group_id, "is_activate": user.is_activate}
    raise HTTPException(status_code=404, detail=f"User with id {id} does not exist.")


@users_statistic_router.get("/GetAllUsers", tags=users_tag)
def get_all_users(filter: Optional[str] = Query(None)):
    users = get_all_items(Users, filter=filter)
    return users


@users_statistic_router.patch("/UpdateIsUserActivate", tags=users_tag)
def update_is_user_activate(id: int, is_activate: bool):
    user = update_is_activate(Users, id, is_activate)
    if user:
        return {"item_type": "User", "name": user.name, "id": user.id, "group_id": user.group_id, "is_activate": user.is_activate}
    raise HTTPException(status_code=404, detail=f"User with id {id} does not exist.")
