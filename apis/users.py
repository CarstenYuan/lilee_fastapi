from fastapi import APIRouter
from apis.general import add_item
from models import Users

users_statistic_router = APIRouter()
users_tag = ['Users APIs']


@users_statistic_router.post("/Adduser", tags=users_tag)
def add_user(name: str, group_id: int = None):
    user = add_item(Users, name=name, group_id=group_id)
    return {"item_type": "User", "name": user.name, "id": user.id, "group_id": user.group_id}
