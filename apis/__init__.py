from fastapi import APIRouter
from apis.api import statistic_router


router = APIRouter()
router.include_router(statistic_router)
