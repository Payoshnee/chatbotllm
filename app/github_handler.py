import json
from fastapi import Request
from app.diff_parser import get_changed_java_files
from app.llm_reviewer import review_with_llm
from app.comment_generator import generate_comments
from app.github_poster import post_review_comments
from app.utils import extract_pr_info, load_config

async def handle_github_webhook(request: Request):
    try:
        payload = await request.json()
        event = request.headers.get('X-GitHub-Event')

        if event != "pull_request":
            return {"status": "ignored: not a pull request event"}

        action = payload.get("action")
        if action not in ["opened", "synchronize", "reopened"]:
            return {"status": f"ignored: unsupported PR action '{action}'"}

        pr_info = extract_pr_info(payload)
        if not pr_info:
            return {"status": "error: invalid PR payload"}

        changed_files = get_changed_java_files(pr_info)
        if not changed_files:
            return {"status": "no Java files changed"}

        print("🔍 Changed files:", changed_files)
        config = load_config()
        review_results = review_with_llm(changed_files, config)
        print("🧠 LLM raw review output:", review_results)
        comments = generate_comments(review_results)
        print("✍️ Final comments to post:", comments)
        post_review_comments(payload, comments)
        
        return {"status": "review completed", "comments_count": len(comments)}

    except Exception as e:
        return {"status": "error", "message": str(e)}
