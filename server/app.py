from server import app as fastapi_app
import uvicorn

def main():
    uvicorn.run(fastapi_app, host="0.0.0.0", port=8000)

if __name__ == "__main__":
    main()