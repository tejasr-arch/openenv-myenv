from fastapi import FastAPI
from models import Action

app = FastAPI()

# 3 tasks (easy → medium → hard)
tasks = [
    {"resume": "Python developer", "job": "Python job", "answer": 80},
    {"resume": "Java fresher", "job": "Senior Python job", "answer": 30},
    {"resume": "ML engineer", "job": "AI role", "answer": 90},
]

current_task = {"index": 0}


@app.post("/reset")
def reset():
    task = tasks[current_task["index"]]
    return {
        "resume": task["resume"],
        "job": task["job"]
    }


@app.post("/step")
def step(action: Action):
    task = tasks[current_task["index"]]
    correct_score = task["answer"]

    # difference
    diff = abs(action.score - correct_score)

    # improved smooth reward (0–1)
    reward = max(0, 1 - (diff / 100))

    # move to next task
    current_task["index"] = (current_task["index"] + 1) % len(tasks)

    return {
        "reward": reward,
        "done": True
    }


@app.get("/state")
def state():
    return {
        "current_task_index": current_task["index"],
        "total_tasks": len(tasks)
    }