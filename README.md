# 🤖 AutoReviewBot – LLM-Powered Java Code Reviewer

AutoReviewBot is a GitHub-integrated, LLM-powered tool that automatically reviews Java pull requests based on your firm's internal guidelines. It detects code quality issues, suggests fixes, and posts inline comments — reducing manual review time by 60%+.

---

## 🚀 Features

- 🔍 Detects pull request events via GitHub webhook
- 🤖 Uses GPT-4 or open-source LLMs to analyze code
- 🛡️ Enforces custom firm Java code guidelines
- 💬 Posts inline suggestions and summary comments on GitHub
- ⚙️ Containerized, configurable, CI-ready

---

## 🧱 Project Structure

autoreviewbot/
├── app/
│ ├── main.py # FastAPI entrypoint
│ ├── github_handler.py # Webhook logic
│ ├── diff_parser.py # Git PR diff logic
│ ├── llm_reviewer.py # Calls LLM
│ ├── comment_generator.py # Formats comments
│ ├── github_poster.py # Posts review to GitHub
│ ├── utils.py
│ └── config.yaml # Rule weights, LLM model config![WhatsApp Image 2025-07-10 at 21 02 30_1c356b5b](https://github.com/user-attachments/assets/6618ea47-2327-4bd5-999f-d361ba3b9cef)

├── rules/
│ ├── guideline_ids.md # Rule IDs + descriptions
│ └── prompt_template.txt # Reusable LLM prompt
├── .env # API keys (not checked into git)
├── Dockerfile
├── requirements.txt
├── .github/workflows/deploy.yml
└── README.md

---
![WhatsApp Image 2025-07-10 at 21 02 30_1c356b5b](https://github.com/user-attachments/assets/1eac492e-28b9-420e-a92c-8b6700c3273b)

## ⚙️ Setup Instructions

### 1. Clone & Install

```bash
git clone https://github.com/your-username/AutoReviewBot.git
cd AutoReviewBot
pip install -r requirements.txt
2. Create .env File
env
Copy
Edit
OPENAI_API_KEY=sk-xxxxxxxxxxxxxxxxxxxxxxxx
GITHUB_TOKEN=ghp_xxxxxxxxxxxxxxxxxxxxxxxxx
3. Run the Server
bash
Copy
Edit
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
🌐 GitHub Integration
🔗 1. Create a GitHub App
Go to GitHub Developer Settings → Apps

Set Webhook URL to: https://<your-ngrok-id>.ngrok.io/webhook

Permissions:

✅ Pull Requests: Read & Write

✅ Contents: Read-only

Events: Pull request

Install the App on your forked repo

🔐 2. Expose Server with Ngrok
bash
Copy
Edit
ngrok http 8000
Copy the HTTPS URL to use as your webhook endpoint.

💡 Usage
Open a pull request in your forked repo (must modify .java files)

AutoReviewBot:

Clones the repo

Analyzes changes with GPT-4

Posts inline GitHub comments and recommendations

GitHub shows feedback directly in the PR

📊 Java Review Rules Enforced
Rule ID	Description
STYLE-001	Use Java naming conventions
STYLE-002	Prefer lambdas and streams
NULL-001	Avoid NullPointerException
SEC-001	Don’t expose mutable state
EXC-001	Catch specific exceptions first
DS-001	Use correct data structures
OOP-001	Keep internal methods private
OOP-002	Code to interfaces
OOP-003	Avoid unnecessary interfaces
OOP-004	Override hashCode with equals

🐞 Troubleshooting
Issue	Fix
Webhook returns 405	Webhook URL must end in /webhook
401 Bad credentials	Use token not Bearer with GitHub PAT
No comments posted	Ensure .java files are changed
LLM returns nothing	Check OpenAI key and prompt formatting
Git fails on SHAs	Use real PR base/head SHAs from active PR

🧪 Testing Locally (No GitHub)
You can stub the LLM and diff to test locally without webhooks:

python
Copy
Edit
# llm_reviewer.py
return [{
  "file": "Test.java",
  "raw_response": "⚠️ STYLE-001: Use camelCase\nSuggestion:\nint myVariable = 5;"
}]
🐳 Docker Support
bash
Copy
Edit
docker build -t autoreviewbot .
docker run --env-file .env -p 8000:8000 autoreviewbot
