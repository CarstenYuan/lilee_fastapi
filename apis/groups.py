from fastapi import APIRouter, HTTPException, Body, Depends
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session
from typing import Optional
from models import Groups
from database import get_db

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
def add_group(add_request: AddGroupInfoRequest = Body(...), db_session: Session = Depends(get_db)):
    add_data = add_request.dict()
    group = add_item(Groups, db_session, name=add_data['name'])
    return group


@groups_statistic_router.delete("/deleteGroup/{id}", tags=groups_tag)
def delete_group(id: int, db_session: Session = Depends(get_db)):
    if has_member(id, db_session):
        raise HTTPException(status_code=400, detail="Group cannot be deleted because it has members.")
    
    group = delete_item(Groups, id, db_session)
    if group:
        return group
    raise HTTPException(status_code=404, detail=f"Group with id {id} does not exist.")


@groups_statistic_router.get("/getSingleGroup/{id}", tags=groups_tag)
def get_single_group(id: int, db_session: Session = Depends(get_db)):
    group = get_single_item(Groups, id, db_session)
    if group:
        return group
    raise HTTPException(status_code=404, detail=f"Group with id {id} does not exist.")


@groups_statistic_router.get("/getAllGroups", tags=groups_tag)
def get_all_groups(db_session: Session = Depends(get_db)):
    groups = get_all_items(Groups, db_session)
    return groups


@groups_statistic_router.get("/getActiveGroups", tags=groups_tag)
def get_active_groups(db_session: Session = Depends(get_db)):
    groups = get_all_items(Groups, db_session)
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
def update_is_group_activate(id: int, is_activate: bool, db_session: Session = Depends(get_db)):
    if (not is_activate) and (has_member(id, db_session)):
        raise HTTPException(status_code=400, detail="Group cannot be deactivated because it has members.")
    group = update_is_activate(Groups, id, is_activate, db_session)
    if group:
        return group
    raise HTTPException(status_code=404, detail=f"Group with id {id} does not exist.")


@groups_statistic_router.put("/updateGroupInfo/{id}", tags=groups_tag)
def update_group_info(id: int, update_request: UpdateGroupInfoRequest = Body(...), db_session: Session = Depends(get_db)):
    update_data = update_request.dict(exclude_none=True)

    if update_data['is_activate'] == False and has_member(id, db_session):
        raise HTTPException(status_code=400, detail="Group cannot be deactivated because it has members.")

    group = update_items(Groups, id, update_data, db_session)
    if group:
        return group
    raise HTTPException(status_code=404, detail=f"Group with id {id} does not exist.")