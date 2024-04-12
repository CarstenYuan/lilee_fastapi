from fastapi import APIRouter, HTTPException, Query, Body, Depends
from pydantic import BaseModel, Field
from typing import Optional
from models import Users, Groups
from sqlalchemy.orm import Session
from database import get_db

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


class AddUserInfoRequest(BaseModel):
    name: str = Field(description="The new name of the user.")
    group_id: Optional[int] = Field(None, description="The new group ID of the user.")


class UpdateUserInfoRequest(BaseModel):
    name: str = Field(None, description="The updated name of the user.")
    group_id: Optional[int] = Field(None, description="The updated group ID of the user.")
    is_activate: bool = Field(None, description="The updated activation status of the user.")


@users_statistic_router.post("/addUser", tags=users_tag)
def add_user(add_request: AddUserInfoRequest = Body(...), db_session: Session = Depends(get_db)):
    add_data = add_request.dict()
    if add_data['group_id'] == 0:
        add_data['group_id'] = None
    if add_data['group_id'] and not can_join_group(add_data['group_id'], db_session):
        raise HTTPException(status_code=400, detail="You cannot join a deactivated group.")
    user = add_item(Users, db_session, name=add_data['name'], group_id=add_data['group_id'])
    return user


@users_statistic_router.delete("/deleteUser/{id}", tags=users_tag)
def delete_user(id: int, db_session: Session = Depends(get_db)):
    user = delete_item(Users, id, db_session)
    if user:
        return user
    raise HTTPException(status_code=404, detail=f"User with id {id} does not exist.")


@users_statistic_router.get("/getSingleUser/{id}", tags=users_tag)
def get_single_user(id: int, db_session: Session = Depends(get_db)):
    user = get_single_item(Users, id, db_session)
    if user:
        return user
    raise HTTPException(status_code=404, detail=f"User with id {id} does not exist.")


@users_statistic_router.get("/getAllUsers", tags=users_tag)
def get_all_users(filter: Optional[str] = Query(None), db_session: Session = Depends(get_db)):
    users = get_all_items(Users, db_session, filter=filter)
    users_list = []
    for user in users:
        curr_id = user.id

        curr_name = user.name
        curr_group_id = user.group_id
        group = get_single_item(Groups, curr_group_id, db_session)
        curr_group_name = group.name if group else None

        curr_creator = user.creator
        curr_createdTime = user.createdTime
        curr_modifier = user.modifier
        curr_modifiedTime = user.modifiedTime
        curr_is_activate = user.is_activate

        users_list.append(
            {
            'id': curr_id,
            'name': curr_name,
            'group_id': curr_group_id,
            'group': curr_group_name,

            'creator': curr_creator,
            'createdTime': curr_createdTime,
            'modifier': curr_modifier,
            'modifiedTime': curr_modifiedTime,
            'is_activate': curr_is_activate
            }
        )
    return users_list


@users_statistic_router.patch("/updateIsUserActivate/{id}", tags=users_tag)
def update_is_user_activate(id: int, is_activate: bool, db_session: Session = Depends(get_db)):
    user = update_is_activate(Users, id, is_activate, db_session)
    if user:
        return user
    raise HTTPException(status_code=404, detail=f"User with id {id} does not exist.")


@users_statistic_router.put("/updateUserInfo/{id}", tags=users_tag)
def update_user_info(id: int, update_request: UpdateUserInfoRequest = Body(...), db_session: Session = Depends(get_db)):
    update_data = update_request.dict()

    if update_data['group_id'] == 0:
        update_data['group_id'] = None
    if update_data['group_id'] and not can_join_group(update_data['group_id'], db_session):
        raise HTTPException(status_code=400, detail="You cannot join a deactivated group.")

    user = update_items(Users, id, update_data, db_session)
    if user:
        return user
    raise HTTPException(status_code=404, detail=f"User with id {id} does not exist.")
