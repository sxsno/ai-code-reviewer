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

