from fastapi import APIRouter, HTTPException
from apis.general import add_item, delete_item, can_delete_group, get_single_item, get_all_items
from models import Groups

groups_statistic_router = APIRouter()
groups_tag = ['Groups APIs']


@groups_statistic_router.post("/addGroup", tags=groups_tag)
def add_group(name: str):
    group = add_item(Groups, name=name)
    return {"item_type": "Group", "name": group.name, "id": group.id}


@groups_statistic_router.delete("/DeleteGroup", tags=groups_tag)
def delete_group(id: int):
    if not can_delete_group(id):
        raise HTTPException(status_code=400, detail="Group cannot be deleted because it has members.")
    
    group = delete_item(Groups, id)
    if group:
        return {"item_type": "Group", "name": group.name, "id": group.id}
    raise HTTPException(status_code=404, detail=f"Group with id {id} does not exist.")


@groups_statistic_router.get("/GetSingleGroup/{group_id}", tags=groups_tag)
def get_single_group(id: int):
    group = get_single_item(Groups, id)
    if group:
        return {"item_type": "Group", "name": group.name, "id": group.id}
    raise HTTPException(status_code=404, detail=f"Group with id {id} does not exist.")


@groups_statistic_router.get("/GetAllGroups", tags=groups_tag)
def get_all_groups():
    groups = get_all_items(Groups)
    return groups
