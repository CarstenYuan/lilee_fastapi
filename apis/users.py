from fastapi import APIRouter, HTTPException
from apis.general import add_item, delete_item, get_single_item, get_all_item
from models import Users

users_statistic_router = APIRouter()
users_tag = ['Users APIs']


@users_statistic_router.post("/AddUser", tags=users_tag)
def add_user(name: str, group_id: int = None):
    # TODO: constraint group_id --> try except
    user = add_item(Users, name=name, group_id=group_id)
    return {"item_type": "User", "name": user.name, "id": user.id, "group_id": user.group_id}


@users_statistic_router.delete("/DeleteUser", tags=users_tag)
def delete_user(id: int):
    user = delete_item(Users, id)
    if user:
        return {"item_type": "User", "name": user.name, "id": user.id, "group_id": user.group_id}
    raise HTTPException(status_code=404, detail=f"User with id {id} does not exist.")


@users_statistic_router.get("/GetSingleUser/{user_id}", tags=users_tag)
def get_single_user(id: int):
    user = get_single_item(Users, id)
    if user:
        return {"item_type": "User", "name": user.name, "id": user.id, "group_id": user.group_id}
    raise HTTPException(status_code=404, detail=f"User with id {id} does not exist.")


@users_statistic_router.get("/GetAllUsers", tags=users_tag)
def get_all_users():
    users = get_all_item(Users)
    return users