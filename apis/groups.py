from fastapi import APIRouter, HTTPException
from apis.general import add_item, delete_item
from models import Groups

groups_statistic_router = APIRouter()
groups_tag = ['Groups APIs']


@groups_statistic_router.post("/addGroup", tags=groups_tag)
def add_group(name: str):
    group = add_item(Groups, name=name)
    return {"item_type": "Group", "name": group.name, "id": group.id}

@groups_statistic_router.post("/DeleteGroup", tags=groups_tag)
def delete_group(id: int):
    group = delete_item(Groups, id)
    if group:
        return {"item_type": "Group", "name": group.name, "id": group.id}
    raise HTTPException(status_code=404, detail=f"Group with id {id} does not exist.")
