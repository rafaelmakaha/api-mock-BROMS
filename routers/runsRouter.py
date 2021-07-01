from fastapi import APIRouter
from fastapi.responses import JSONResponse
from starlette.requests import Request
from globalVars import global_vars

router = APIRouter(
    prefix="/runs",
    tags=["runs"]
)

@router.get("/", tags=["runs"])
async def get_runs():
    return global_vars.total_runs

@router.post("/diff", tags=["runs"])
async def get_diff_runs(request: Request):
    uid = await request.json()
    uid = uid["uid"]
    for index,run in enumerate(global_vars.runs):
        if run["uid"] == uid:
            i = index
            break
    if index > 0:
        return global_vars.runs[i:]
    return []
    
