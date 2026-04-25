from fastapi import FastAPI, Request

app = FastAPI()

@app.get("/")
def home():
    return {"message": "Server Running FINAL"}

@app.post("/webhook")
async def github_webhook(request: Request):
    data = await request.json()

    print("\n===== Webhook Received =====")

    # Extract important fields safely
    action = data.get("action")

    pull_request = data.get("pull_request", {})
    pr_title = pull_request.get("title")
    pr_number = pull_request.get("number")

    repository = data.get("repository", {})
    repo_name = repository.get("full_name")

    sender = data.get("sender", {}).get("login")

    # Print structured info
    print(f"Action       : {action}")
    print(f"Repository   : {repo_name}")
    print(f"PR Number    : {pr_number}")
    print(f"PR Title     : {pr_title}")
    print(f"Triggered by : {sender}")

    print("================================\n")

    return {"message": "Webhook Trigger FINAL v2"}