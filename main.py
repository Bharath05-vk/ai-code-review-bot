from fastapi import FastAPI, Request
import requests

app = FastAPI()

@app.get("/")
def home():
    return {"message": "Server Running FINAL"}

@app.post("/webhook")
async def github_webhook(request: Request):
    event = request.headers.get("X-GitHub-Event")

    if event != "pull_request":
        print("Ignored event:", event)
        return {"status": "ignored"}

    data = await request.json()

    action = data.get("action")

    # Only handle PR opened or updated
    if action not in ["opened", "synchronize"]:
        return {"status": "ignored action"}

    pull_request = data.get("pull_request", {})
    pr_number = pull_request.get("number")

    repo = data.get("repository", {}).get("full_name")

    print(f"\nFetching files for PR #{pr_number} in {repo}")

    # 🔥 GitHub API call
    url = f"https://api.github.com/repos/{repo}/pulls/{pr_number}/files"

    response = requests.get(url)
    files = response.json()

    print("\nChanged Files:")

    for file in files:
        print(f"File: {file['filename']}")
        print(f"Changes: +{file['additions']} -{file['deletions']}")
        print("Patch (code diff):")
        print(file.get("patch", "No patch available"))
        print("-" * 40)

    return {"status": "processed"}