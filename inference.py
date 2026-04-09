import requests
import time
import os
import re
from openai import OpenAI

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


def get_llm_score():
    try:
        client = OpenAI(
            base_url=os.environ.get("API_BASE_URL"),
            api_key=os.environ.get("API_KEY")
        )

        response = client.chat.completions.create(
            model=os.environ.get("MODEL_NAME", "gpt-3.5-turbo"),
            messages=[
                {
                    "role": "user",
                    "content": "Give a score from 0 to 100 for a resume matching a Python job. Just output a number."
                }
            ]
        )

        content = response.choices[0].message.content

        nums = re.findall(r"\d+", content)
        if nums:
            return int(nums[0])

    except Exception:
        pass

    return 75  # fallback


def run():
    task_name = "resume_scoring"

    print(f"[START] task={task_name}", flush=True)

    if not wait_for_server():
        print(f"[END] task={task_name} score=0 steps=0", flush=True)
        return

    try:
        # Reset environment
        requests.post(f"{BASE_URL}/reset")

        # Get score from LLM
        score = get_llm_score()

        # Call step
        step = requests.post(
            f"{BASE_URL}/step",
            json={"score": score}
        ).json()

        reward = step.get("reward", 0)

        print(f"[STEP] step=1 reward={reward}", flush=True)
        print(f"[END] task={task_name} score={reward} steps=1", flush=True)

    except Exception:
        print(f"[STEP] step=1 reward=0", flush=True)
        print(f"[END] task={task_name} score=0 steps=1", flush=True)


if __name__ == "__main__":
    run()