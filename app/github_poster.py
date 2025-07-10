import httpx
import os

GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
GITHUB_API = "https://api.github.com"

def post_review_comments(pr_payload, comments):
    repo_full_name = pr_payload["repository"]["full_name"]
    pr_number = pr_payload["pull_request"]["number"]

    headers = {
    "Authorization": f"token {GITHUB_TOKEN}",
    "Accept": "application/vnd.github.v3+json"
}

    review_payload = {
        "body": "🤖 AutoReviewBot suggestions",
        "event": "COMMENT",
        "comments": []
    }

    for comment in comments:
        review_payload["comments"].append({
            "path": comment["path"],
            "body": comment["body"],
            "line": comment["line"],
            "side": "RIGHT"
        })

    url = f"{GITHUB_API}/repos/{repo_full_name}/pulls/{pr_number}/reviews"

    with httpx.Client() as client:
        response = client.post(url, json=review_payload, headers=headers)
        print("📨 Sending review to:", url)
        print("🧾 Payload:", json.dumps(review_payload, indent=2))
        print("🔐 Token starts with:", GITHUB_TOKEN[:6])
        print("📡 Response:", response.status_code, response.text)
        if response.status_code != 200 and response.status_code != 201:
            print(f"❌ Failed to post review: {response.status_code} {response.text}")
        else:
            print("✅ Review comments posted.")
