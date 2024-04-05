from fastapi import APIRouter, HTTPException, Body
from pydantic import BaseModel, Field
from typing import Optional
from models import Groups

from apis.general import (
                            add_item,
                            delete_item,
                            can_delete_group,
                            get_single_item,
                            get_all_items,
                            update_is_activate,
                            update_items,
                        )


groups_statistic_router = APIRouter()
groups_tag = ['Groups APIs']


class UpdateGroupInfoRequest(BaseModel):
    name: Optional[str] = Field(None, description="The new name of the group.")
    is_activate: Optional[bool] = Field(None, description="The new activation status of the group.")


@groups_statistic_router.post("/addGroup", tags=groups_tag)
def add_group(name: str):
    group = add_item(Groups, name=name)
    return {"item_type": "Group", "name": group.name, "id": group.id}


@groups_statistic_router.delete("/deleteGroup/{id}", tags=groups_tag)
def delete_group(id: int):
    if not can_delete_group(id):
        raise HTTPException(status_code=400, detail="Group cannot be deleted because it has members.")
    
    group = delete_item(Groups, id)
    if group:
        return {"item_type": "Group", "name": group.name, "id": group.id}
    raise HTTPException(status_code=404, detail=f"Group with id {id} does not exist.")


@groups_statistic_router.get("/getSingleGroup/{id}", tags=groups_tag)
def get_single_group(id: int):
    group = get_single_item(Groups, id)
    if group:
        return {"item_type": "Group", "name": group.name, "id": group.id}
    raise HTTPException(status_code=404, detail=f"Group with id {id} does not exist.")


@groups_statistic_router.get("/getAllGroups", tags=groups_tag)
def get_all_groups():
    groups = get_all_items(Groups)
    return groups


@groups_statistic_router.patch("/updateIsGroupActivate/{id}", tags=groups_tag)
def update_is_group_activate(id: int, is_activate: bool):
    if (not is_activate) and (not can_delete_group(id)):
        raise HTTPException(status_code=400, detail="Group cannot be deactivated because it has members.")
    group = update_is_activate(Groups, id, is_activate)
    if group:
        return {"item_type": "Group", "name": group.name, "id": group.id, "is_activate": group.is_activate}
    raise HTTPException(status_code=404, detail=f"Group with id {id} does not exist.")


@groups_statistic_router.put("/updateGroupInfo/{id}", tags=groups_tag)
def update_group_info(id: int, update_request: UpdateGroupInfoRequest = Body(...)):
    update_data = update_request.dict(exclude_none=True)
    group = update_items(Groups, id, update_data)
    if group:
        return group
    raise HTTPException(status_code=404, detail=f"Group with id {id} does not exist.")