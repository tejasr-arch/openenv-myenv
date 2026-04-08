import requests

url = "http://127.0.0.1:8000"

for i in range(3):
    res = requests.post(f"{url}/reset").json()
    print("RESET:", res)

    action = {"score": 75}
    step = requests.post(f"{url}/step", json=action).json()

    print("STEP:", step)