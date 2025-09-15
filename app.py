from flask import Flask, request
import requests, os
from openai import OpenAI

app = Flask(__name__)
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

@app.route("/webhook", methods=["POST"])
def webhook():
    data = request.json
    if "pull_request" in data:
        files_url = data["pull_request"]["url"] + "/files"
        review_pr(files_url)
    return {"status": "ok"}, 200

def review_pr(files_url):
    headers = {"Authorization": f"token {os.getenv('GITHUB_TOKEN')}"}
    files = requests.get(files_url, headers=headers).json()
    for file in files:
        patch = file.get("patch", "")
        if patch:
            feedback = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[{"role": "system", "content": "You are a senior code reviewer."},
                          {"role": "user", "content": f"Review this code diff:\n{patch}"}]
            )
            print(f"Review for {file['filename']}:\n", feedback.choices[0].message.content)

if __name__ == "__main__":
    app.run(port=5000)
