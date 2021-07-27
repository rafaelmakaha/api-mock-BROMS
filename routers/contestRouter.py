from fastapi import APIRouter
from fastapi.responses import JSONResponse
from globalVars import global_vars
from utils import utils
import json

router = APIRouter(
    prefix="/contest",
    tags=["contest"]
)

@router.get("/", tags=["contest"])
async def get_contest():
    return global_vars.contest

@router.get("/finish", tags=["contest"])
async def get_contest():
    if global_vars.t > global_vars.contest["duration"]:
        return True
    return False