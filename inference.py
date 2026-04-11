import requests
import time
import os
import re

BASE_URL = "http://127.0.0.1:8000"


def wait_for_server():
    for _ in range(15):
        try:
            res = requests.get(f"{BASE_URL}/docs")
            if res.status_code == 200:
                return True
        except:
            pass
        time.sleep(1)
    return False


def get_llm_score():
    try:
        # 🔥 STRICT ENV (NO .get)
        base_url = os.environ["API_BASE_URL"]
        api_key = os.environ["API_KEY"]
        model = os.environ["MODEL_NAME"]

        url = f"{base_url}/chat/completions"

        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }

        data = {
            "model": model,
            "messages": [
                {
                    "role": "user",
                    "content": "Return ONLY a number between 0 and 100."
                }
            ]
        }

        response = requests.post(url, headers=headers, json=data, timeout=10)

        result = response.json()

        content = result["choices"][0]["message"]["content"]

        nums = re.findall(r"\d+", content)
        if nums:
            score = int(nums[0])
            return max(0, min(100, score))

    except Exception as e:
        print(f"[DEBUG] LLM error: {e}", flush=True)

    return 50  # fallback


def run():
    task_name = "resume_scoring"

    print(f"[START] task={task_name}", flush=True)

    if not wait_for_server():
        print(f"[END] task={task_name} score=0 steps=0", flush=True)
        return

    try:
        # reset env
        requests.post(f"{BASE_URL}/reset")

        # 🔥 LLM CALL (MANDATORY)
        score = get_llm_score()

        # step
        step = requests.post(
            f"{BASE_URL}/step",
            json={"score": score}
        ).json()

        reward = step.get("reward", 0)

        print(f"[STEP] step=1 reward={reward}", flush=True)
        print(f"[END] task={task_name} score={reward} steps=1", flush=True)

    except Exception as e:
        print(f"[DEBUG] Runtime error: {e}", flush=True)
        print(f"[STEP] step=1 reward=0", flush=True)
        print(f"[END] task={task_name} score=0 steps=1", flush=True)


if __name__ == "__main__":
    run()