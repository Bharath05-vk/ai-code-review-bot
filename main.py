from fastapi import FastAPI, Request

app = FastAPI()

@app.get("/")
def home():
    return {"message": "Server Running"}

@app.post("/webhook")
async def github_webhook(request: Request):
    data = await request.json()
    print("Webhook received:")
    print(data)
    return {"message": "Server Running v2"}