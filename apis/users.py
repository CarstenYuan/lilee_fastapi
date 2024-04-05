from fastapi import APIRouter, HTTPException, Query, Body
from pydantic import BaseModel, Field
from typing import Optional
from models import Users

from apis.general import (
                            add_item,
                            delete_item,
                            get_single_item,
                            get_all_items,
                            update_is_activate,
                            can_join_group,
                            update_items,
                        )


users_statistic_router = APIRouter()
users_tag = ['Users APIs']


class UpdateUserInfoRequest(BaseModel):
    name: Optional[str] = Field(None, description="The new name of the user.")
    group_id: Optional[int] = Field(None, description="The new group ID of the user.")
    is_activate: Optional[bool] = Field(None, description="The new activation status of the user.")


@users_statistic_router.post("/addUser", tags=users_tag)
def add_user(name: str, group_id: int = None):
    if not can_join_group(group_id):
        raise HTTPException(status_code=400, detail="You cannot join a deactivated group.")
    user = add_item(Users, name=name, group_id=group_id)
    return {"item_type": "User", "name": user.name, "id": user.id, "group_id": user.group_id, "is_activate": user.is_activate}


@users_statistic_router.delete("/deleteUser/{id}", tags=users_tag)
def delete_user(id: int):
    user = delete_item(Users, id)
    if user:
        return {"item_type": "User", "name": user.name, "id": user.id, "group_id": user.group_id, "is_activate": user.is_activate}
    raise HTTPException(status_code=404, detail=f"User with id {id} does not exist.")


@users_statistic_router.get("/getSingleUser/{id}", tags=users_tag)
def get_single_user(id: int):
    user = get_single_item(Users, id)
    if user:
        return {"item_type": "User", "name": user.name, "id": user.id, "group_id": user.group_id, "is_activate": user.is_activate}
    raise HTTPException(status_code=404, detail=f"User with id {id} does not exist.")


@users_statistic_router.get("/getAllUsers", tags=users_tag)
def get_all_users(filter: Optional[str] = Query(None)):
    users = get_all_items(Users, filter=filter)
    return users


@users_statistic_router.patch("/updateIsUserActivate/{id}", tags=users_tag)
def update_is_user_activate(id: int, is_activate: bool):
    user = update_is_activate(Users, id, is_activate)
    if user:
        return {"item_type": "User", "name": user.name, "id": user.id, "group_id": user.group_id, "is_activate": user.is_activate}
    raise HTTPException(status_code=404, detail=f"User with id {id} does not exist.")


@users_statistic_router.put("/updateUserInfo/{id}", tags=users_tag)
def update_user_info(id: int, update_request: UpdateUserInfoRequest = Body(...)):
    update_data = update_request.dict(exclude_none=True)
    user = update_items(Users, id, update_data)
    if user:
        return user
    raise HTTPException(status_code=404, detail=f"User with id {id} does not exist.")
