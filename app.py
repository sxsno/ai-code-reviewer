import os
import requests
from dotenv import load_dotenv
from flask import Flask, request, jsonify
from openai import OpenAI

# Load secrets from .env
load_dotenv()
OPENAI_KEY = os.getenv("OPENAI_API_KEY")
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")

if not OPENAI_KEY:
    raise RuntimeError("OPENAI_API_KEY is missing. Add it to .env or export it.")

client = OpenAI(api_key=OPENAI_KEY)
app = Flask(__name__)

#gitHub headers
GH_HEADERS = {
    "Authorization": f"token {GITHUB_TOKEN}" if GITHUB_TOKEN else "",
    "Accept": "application/vnd.github+json",
    "X-GitHub-Api-Version": "2022-11-28",
    "User-Agent": "ai-code-reviewer",
}

#server health Check
@app.route("/", methods=["GET"])
def health():
    return jsonify(ok=True)

#local Test Review
@app.route("/test-review", methods=["POST"])
def test_review():
    data = request.get_json(force=True) or {}
    snippet = data.get("code") or data.get("diff") or ""
    if not snippet:
        return {"error": "Send JSON with a 'code' or 'diff' field"}, 400

    prompt = f"""You are a strict senior code reviewer.
Review the following code (or git diff). Return 3-6 bullet points with:
- Critical issues (security/bugs)
- Performance concerns
- Style/maintainability suggestions
Then give a brief overall assessment.

Code/diff:
{snippet}"""

    resp = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.2,
    )
    feedback = resp.choices[0].message.content
    return {"feedback": feedback}, 200

#gitHub Webhook
@app.route("/webhook", methods=["POST"])
def webhook():
    payload = request.get_json(silent=True) or {}
    pr = payload.get("pull_request")
    if not pr or not pr.get("url"):
        return {"status": "ignored", "reason": "no pull_request in payload"}, 200

    files_url = pr["url"] + "/files"
    try:
        reviews = review_pr(files_url)
    except Exception as e:
        print("review_pr error:", e)
        return {"status": "error", "message": str(e)}, 200

    #for now just log reviews
    for r in reviews:
        print(f"\n=== Review for {r['file']} ===\n{r['review']}\n")

    return {"status": "ok", "count": len(reviews)}, 200

def review_pr(files_url: str):
    """Fetch PR files from GitHub and review each diff patch."""
    if not GITHUB_TOKEN:
        raise RuntimeError("GITHUB_TOKEN is missing. Add it to .env to read PR files.")

    resp = requests.get(files_url, headers=GH_HEADERS, timeout=30)
    resp.raise_for_status()
    files = resp.json()

    reviews = []
    for f in files:
        filename = f.get("filename")
        patch = f.get("patch")
        if not patch:
            continue

        prompt = f"""You are a senior code reviewer. Review the unified diff for {filename}.
Identify bugs, security issues, performance concerns, and style issues.
Give concrete, actionable suggestions with brief examples.

Diff:
{patch}"""

        ai = client.chat.completions.create(
            model="gpt-4o-mini",
            temperature=0.2,
            messages=[{"role": "user", "content": prompt}],
        )
        review_text = ai.choices[0].message.content.strip()
        reviews.append({"file": filename, "review": review_text})

    return reviews

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)
