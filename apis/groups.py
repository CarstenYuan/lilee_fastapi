from fastapi import APIRouter
from apis.general import add_item
from models import Groups

groups_statistic_router = APIRouter()
groups_tag = ['Groups APIs']


@groups_statistic_router.post("/addGroup", tags=groups_tag)
def add_group(name: str):
    group = add_item(Groups, name=name)
    return {"item_type": "Group", "name": group.name, "id": group.id}
