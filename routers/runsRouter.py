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
    return global_vars.runs

@router.post("/diff", tags=["runs"])
async def get_diff_runs(request: Request):
    uid = await request.json()
    i = 0
    for index,run in enumerate(global_vars.runs):
        if run["runId"] == uid:
            i = index
            break
    if i > 0:
        return global_vars.runs[i+1:]
    return []
    
