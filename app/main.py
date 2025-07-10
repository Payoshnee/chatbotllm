from fastapi import FastAPI, Request
from app.github_handler import handle_github_webhook
import uvicorn
from dotenv import load_dotenv
load_dotenv()

app = FastAPI()

@app.post("/webhook")
async def webhook(request: Request):
    return await handle_github_webhook(request)


if __name__ == "__main__":
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
