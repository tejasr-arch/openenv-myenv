import requests
import time

BASE_URL = "http://127.0.0.1:8000"

def wait_for_server():
    for _ in range(10):
        try:
            res = requests.get(f"{BASE_URL}/docs")
            if res.status_code == 200:
                return True
        except:
            pass
        time.sleep(1)
    return False

def run():
    task_name = "resume_scoring"

    if not wait_for_server():
        print("[START] task=resume_scoring", flush=True)
        print("[END] task=resume_scoring score=0 steps=0", flush=True)
        return

    print(f"[START] task={task_name}", flush=True)

    try:
        reset = requests.post(f"{BASE_URL}/reset").json()

        step = requests.post(f"{BASE_URL}/step", json={"score": 75}).json()
        reward = step.get("reward", 0)

        print(f"[STEP] step=1 reward={reward}", flush=True)

        print(f"[END] task={task_name} score={reward} steps=1", flush=True)

    except Exception:
        print(f"[STEP] step=1 reward=0", flush=True)
        print(f"[END] task={task_name} score=0 steps=1", flush=True)


if __name__ == "__main__":
    run()