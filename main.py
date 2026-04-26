from fastapi import FastAPI, Request
import requests
import os
from openai import OpenAI

app = FastAPI()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

@app.post("/webhook")
async def github_webhook(request: Request):
    event = request.headers.get("X-GitHub-Event")

    if event != "pull_request":
        print("Ignored event:", event)
        return {"status": "ignored"}

    data = await request.json()
    action = data.get("action")

    if action not in ["opened", "synchronize"]:
        return {"status": "ignored action"}

    pr_number = data["pull_request"]["number"]
    repo = data["repository"]["full_name"]

    print(f"\nFetching files for PR #{pr_number} in {repo}")

    # 🔹 Get changed files
    url = f"https://api.github.com/repos/{repo}/pulls/{pr_number}/files"
    response = requests.get(url)
    files = response.json()

    for file in files:
        filename = file["filename"]
        patch = file.get("patch")

        if not patch:
            continue

        print(f"\nAnalyzing file: {filename}")

        # 🔥 Send to AI
        prompt = f"""
        You are a senior code reviewer.

        Review the following code changes:
        {patch}

        Give:
        - Bugs (if any)
        - Improvements
        - Best practices
        """

        ai_response = client.chat.completions.create(
            model="gpt-4.1-mini",
            messages=[{"role": "user", "content": prompt}]
        )

        review = ai_response.choices[0].message.content

        print("\nAI Review:")
        print(review)
        print("=" * 50)

    return {"message": "AI FINAL TEST"}