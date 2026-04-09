import requests
import time

BASE_URL = "http://127.0.0.1:8000"

def wait_for_server():
    for _ in range(10):  # retry 10 times
        try:
            res = requests.get(f"{BASE_URL}/docs")
            if res.status_code == 200:
                return True
        except:
            pass
        time.sleep(1)
    return False

def run():
    if not wait_for_server():
        print("Server not ready")
        return

    try:
        reset = requests.post(f"{BASE_URL}/reset").json()
        print("RESET:", reset)

        step = requests.post(f"{BASE_URL}/step", json={"score": 75}).json()
        print("STEP:", step)

    except Exception as e:
        print("Error:", str(e))


if __name__ == "__main__":
    run()