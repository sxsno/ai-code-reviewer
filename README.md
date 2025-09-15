# AI Code Reviewer Bot 

An AI-powered GitHub bot that automatically reviews pull requests using OpenAI models, providing inline feedback on code quality, bugs, and best practices.

---

##  Features
- Automatic pull request reviews triggered via GitHub Webhooks
- Inline AI feedback using OpenAI GPT models
- Configurable severity levels (Critical, Warning, Suggestion)
- Dockerized for easy deployment

---

## Tech Stack
- Python, Flask
- GitHub REST API & Webhooks
- OpenAI API
- Docker

---

## Setup Instructions
1. Clone the repo:
   ```bash
   git clone https://github.com/sxsno/ai-code-reviewer.git
   cd ai-code-reviewer
   pip install -r requirement.txt
   python app.py
   For demo open another terminal and type the following:
   curl -X POST http://127.0.0.1:5000/test-review \
   -H "Content-Type: application/json" \
   -d '{"code":"def add(a,b): return a+b\nprint(add(2,\"3\"))"}'


