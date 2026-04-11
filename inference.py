import requests
import time
import os
import re
import openai

BASE_URL = "http://127.0.0.1:8000"


def wait_for_server():
    for _ in range(15):
        try:
            if requests.get(f"{BASE_URL}/docs").status_code == 200:
                return True
        except:
            pass
        time.sleep(1)
    return False


def run():
    task_name = "resume_scoring"

    print(f"[START] task={task_name}", flush=True)

    if not wait_for_server():
        print(f"[END] task={task_name} score=0 steps=0", flush=True)
        return

    try:
        requests.post(f"{BASE_URL}/reset")

        # 🔥 FORCE ENV (NO fallback)
        openai.api_key = os.environ["API_KEY"]
        openai.base_url = os.environ["API_BASE_URL"]
        model = os.environ["MODEL_NAME"]

        print("[DEBUG] Calling LLM...", flush=True)

        # 🔥 DIRECT LLM CALL (no wrapper)
        response = openai.ChatCompletion.create(
            model=model,
            messages=[
                {"role": "user", "content": "Return a number between 0 and 100."}
            ]
        )

        print("[DEBUG] LLM response received", flush=True)

        content = response["choices"][0]["message"]["content"]

        nums = re.findall(r"\d+", content)
        score = int(nums[0]) if nums else 50
        score = max(0, min(100, score))

        step = requests.post(
            f"{BASE_URL}/step",
            json={"score": score}
        ).json()

        reward = step.get("reward", 0)

        print(f"[STEP] step=1 reward={reward}", flush=True)
        print(f"[END] task={task_name} score={reward} steps=1", flush=True)

    except Exception as e:
        print(f"[DEBUG ERROR] {e}", flush=True)
        print(f"[STEP] step=1 reward=0", flush=True)
        print(f"[END] task={task_name} score=0 steps=1", flush=True)


if __name__ == "__main__":
    run()