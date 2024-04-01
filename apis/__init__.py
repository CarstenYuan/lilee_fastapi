from fastapi import APIRouter
from apis.users import users_statistic_router
from apis.groups import groups_statistic_router

router = APIRouter()
router.include_router(users_statistic_router)
router.include_router(groups_statistic_router)
