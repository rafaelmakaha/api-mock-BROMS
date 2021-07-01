from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers import contestRouter
from globalVars import global_vars

def init_vars():
    CONTEST = './data/contest'
    RUNS = './data/runs'
    FILE_SEPARATOR = 28
    data = []
    with open(RUNS, 'r') as fp:
        data = fp.readlines()
    for run in data:
        [uid, t, tid, quest, acc] = run.split(chr(FILE_SEPARATOR))
        global_vars.runs.append({"uid": uid, "time": t, "teamId": tid, "question": quest, "acc": acc[0]})
    with open(CONTEST, 'r') as fp:
        global_vars.contest["name"]= fp.readline()[:-1]
        [duration, frozen, blind, penality] = fp.readline().split(chr(FILE_SEPARATOR))
        global_vars.contest["duration"] = int(duration)
        global_vars.contest["frozen"] = int(frozen)
        global_vars.contest["blind"] = int(blind)
        global_vars.contest["penality"] = int(penality[:-1])
        [n_teams, n_quest] = fp.readline().split(chr(FILE_SEPARATOR))
        global_vars.contest["n_teams"] = int(n_teams)
        global_vars.contest["n_questions"] = int(n_quest[:-1])
        teams = []
        for i in range(int(n_teams)-1):
            [tid, college, name] = fp.readline().split(chr(FILE_SEPARATOR))
            team = {"teamId": tid, "college": college, "name": name[:-1]}
            teams.append((team))
        global_vars.contest["teams"] = teams

init_vars()

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(contestRouter.router)
