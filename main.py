from fastapi import FastAPI, Request
import requests
import os
from openai import OpenAI

app = FastAPI()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")

@app.post("/webhook")
async def github_webhook(request: Request):
    data = await request.json()

    # Only handle PR events
    if "pull_request" not in data:
        print("Ignored event: push")
        return {"status": "ignored"}

    repo = data["repository"]["full_name"]
    pr_number = data["pull_request"]["number"]

    print(f"\nFetching files for PR #{pr_number} in {repo}")

    # Get PR files
    files_url = f"https://api.github.com/repos/{repo}/pulls/{pr_number}/files"
    headers = {"Authorization": f"token {GITHUB_TOKEN}"}

    files = requests.get(files_url, headers=headers).json()

    review_text = ""

    for file in files:
        filename = file["filename"]
        patch = file.get("patch", "")

        print(f"Analyzing file: {filename}")

        prompt = f"""
        Review this code change and give suggestions:

        {patch}
        """

        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}]
        )

        ai_review = response.choices[0].message.content
        review_text += f"\n### {filename}\n{ai_review}\n"

    print("\nAI Review Generated:\n", review_text)

    # 🔥 POST COMMENT TO PR
    comment_url = f"https://api.github.com/repos/{repo}/issues/{pr_number}/comments"

    comment_data = {
        "body": f"🤖 AI Code Review:\n{review_text}"
    }

    requests.post(comment_url, headers=headers, json=comment_data)

    print("✅ Comment posted to PR")

    return {"status": "review posted"}