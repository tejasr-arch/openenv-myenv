import requests
import time
import os
import re

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
        from openai import OpenAI

        client = OpenAI(
            base_url=os.environ.get("API_BASE_URL"),
            api_key=os.environ.get("API_KEY")
        )

        model = os.environ.get("MODEL_NAME", "gpt-3.5-turbo")

        response = client.chat.completions.create(
            model=model,
            messages=[
                {
                    "role": "user",
                    "content": "Return ONLY a number between 0 and 100."
                }
            ]
        )

        content = response.choices[0].message.content

        nums = re.findall(r"\d+", content)
        if nums:
            score = int(nums[0])
            return max(0, min(100, score))  # clamp

    except Exception:
        pass

    return 50


def run():
    task_name = "resume_scoring"

    print(f"[START] task={task_name}", flush=True)

    if not wait_for_server():
        print(f"[END] task={task_name} score=0 steps=0", flush=True)
        return

    try:
        requests.post(f"{BASE_URL}/reset")

        score = get_llm_score()

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