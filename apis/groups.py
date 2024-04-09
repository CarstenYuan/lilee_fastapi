from fastapi import APIRouter, HTTPException, Body
from pydantic import BaseModel, Field
from typing import Optional
from models import Groups

from apis.general import (
                            add_item,
                            delete_item,
                            has_member,
                            get_single_item,
                            get_all_items,
                            update_is_activate,
                            update_items,
                        )


groups_statistic_router = APIRouter()
groups_tag = ['Groups APIs']


class AddGroupInfoRequest(BaseModel):
    name: str = Field(description="The new name of the group.")


class UpdateGroupInfoRequest(BaseModel):
    name: Optional[str] = Field(None, description="The new name of the group.")
    is_activate: Optional[bool] = Field(None, description="The new activation status of the group.")


@groups_statistic_router.post("/addGroup", tags=groups_tag)
def add_group(add_request: AddGroupInfoRequest = Body(...)):
    add_data = add_request.dict()
    group = add_item(Groups, name=add_data['name'])
    return group


@groups_statistic_router.delete("/deleteGroup/{id}", tags=groups_tag)
def delete_group(id: int):
    if has_member(id):
        raise HTTPException(status_code=400, detail="Group cannot be deleted because it has members.")
    
    group = delete_item(Groups, id)
    if group:
        return group
    raise HTTPException(status_code=404, detail=f"Group with id {id} does not exist.")


@groups_statistic_router.get("/getSingleGroup/{id}", tags=groups_tag)
def get_single_group(id: int):
    group = get_single_item(Groups, id)
    if group:
        return group
    raise HTTPException(status_code=404, detail=f"Group with id {id} does not exist.")


@groups_statistic_router.get("/getAllGroups", tags=groups_tag)
def get_all_groups():
    groups = get_all_items(Groups)
    return groups


@groups_statistic_router.get("/getActiveGroups", tags=groups_tag)
def get_active_groups():
    groups = get_all_items(Groups)
    active_groups = []
    for group in groups:
        if group.is_activate:
            active_groups.append(
                {
                'id': group.id,
                'name': group.name
                }
            )
    return active_groups


@groups_statistic_router.patch("/updateIsGroupActivate/{id}", tags=groups_tag)
def update_is_group_activate(id: int, is_activate: bool):
    if (not is_activate) and (has_member(id)):
        raise HTTPException(status_code=400, detail="Group cannot be deactivated because it has members.")
    group = update_is_activate(Groups, id, is_activate)
    if group:
        return group
    raise HTTPException(status_code=404, detail=f"Group with id {id} does not exist.")


@groups_statistic_router.put("/updateGroupInfo/{id}", tags=groups_tag)
def update_group_info(id: int, update_request: UpdateGroupInfoRequest = Body(...)):
    update_data = update_request.dict(exclude_none=True)

    if update_data['is_activate'] == False and has_member(id):
        raise HTTPException(status_code=400, detail="Group cannot be deactivated because it has members.")

    group = update_items(Groups, id, update_data)
    if group:
        return group
    raise HTTPException(status_code=404, detail=f"Group with id {id} does not exist.")