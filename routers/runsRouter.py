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
    index = await request.json()
    if index < len(global_vars.runs):
        return global_vars.runs[index:]
    return []
    
