import uvicorn
from agent import a2a_app

if __name__ == "__main__":
    uvicorn.run(a2a_app, host="127.0.0.1", port=8001)
