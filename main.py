from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi_restful.tasks import repeat_every
from routers import contestRouter, runsRouter
from globalVars import global_vars
from enum import Enum
import time

class DATA_ACESS_POS(Enum):
    TID = 0
    COLLEGE = 1
    NAME = 2
    REGION = 3

def init_vars():
    CONTEST = './data/contest'
    RUNS = './data/runs'
    FILE_SEPARATOR = 28
    data = []
    with open(RUNS, 'r') as fp:
        data = fp.readlines()
    for run in data:
        [uid, t, tid, quest, acc] = run.split(chr(FILE_SEPARATOR))
        global_vars.total_runs.append({"runId": int(uid), "time": int(t), "teamUid": tid, "problem": quest, "verdict": acc[0]})
    global_vars.total_runs.reverse()
    with open(CONTEST, 'r') as fp:
        global_vars.contest["name"]= fp.readline()[:-1]
        [duration, frozen, blind, penalty] = fp.readline().split(chr(FILE_SEPARATOR))
        global_vars.contest["duration"] = int(duration)
        global_vars.contest["frozen"] = int(frozen)
        global_vars.contest["blind"] = int(blind)
        global_vars.contest["penalty"] = int(penalty[:-1])
        [n_teams, n_quest] = fp.readline().split(chr(FILE_SEPARATOR))
        global_vars.contest["n_teams"] = int(n_teams)
        global_vars.contest["n_questions"] = int(n_quest[:-1])
        teams = []
        for i in range(int(n_teams)):
            arr_team = fp.readline()[:-1].split(chr(FILE_SEPARATOR))
            # [tid, region, college, name] = fp.readline().split(chr(FILE_SEPARATOR))
            
            team = {
                "teamId": arr_team[DATA_ACESS_POS.TID.value], 
                "college": arr_team[DATA_ACESS_POS.COLLEGE.value], 
                "name": arr_team[DATA_ACESS_POS.NAME.value]
            }
            if(len(arr_team) > 3):
                team["region"] = arr_team[DATA_ACESS_POS.REGION.value]

            teams.append((team))
        global_vars.contest["teams"] = teams

init_vars()

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(contestRouter.router)
app.include_router(runsRouter.router)

@app.on_event("startup")
@repeat_every(seconds=1, wait_first=True, max_repetitions=global_vars.contest["duration"]/10)
def periodic():
    global_vars.t += 10
    print(global_vars.t, len(global_vars.runs))
    for index, run in enumerate(global_vars.total_runs):
        if(run['time'] > global_vars.t):
            global_vars.runs =  global_vars.total_runs[:index]
            return
        
    global_vars.runs = global_vars.total_runs