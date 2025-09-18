from flask import Flask, request, jsonify
import json, os
from datetime import datetime
import git

app = Flask(__name__)

REPO_PATH = os.getcwd()
README_FILE = os.path.join(REPO_PATH, "README.md")
DATA_FILE = os.path.join(REPO_PATH, "activity.json")
MAX_ACTIVITIES = 5

def load_activities():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    return []

def save_activities(acts):
    with open(DATA_FILE, "w") as f:
        json.dump(acts, f, indent=2)

def favicon_url(domain):
    return f"https://www.google.com/s2/favicons?sz=64&domain={domain}"

def short_text(s, n=40):
    return s if len(s) <= n else s[:n-1]+"…"

def build_markdown_table(activities):
    rows = []
    for act in activities:
        fav = favicon_url(act['site'])
        rows.append(
            f"| {act['time']} | <img src='{fav}' width='16' height='16'> **{act['site']}** | "
            f"[{short_text(act['title'], 50)}]({act['url']}) |"
        )
    table = "\n".join(rows)
    md = f"""
| Time | Site | Link |
|------|------|------|
{table}
"""
    return md

def update_readme_with(activities):
    with open(README_FILE, "r", encoding="utf-8") as f:
        content = f.read()
    start_marker = "<!--ACTIVITY-START-->"
    end_marker = "<!--ACTIVITY-END-->"
    block_md = build_markdown_table(activities)
    if start_marker in content and end_marker in content:
        before = content.split(start_marker)[0]
        after = content.split(end_marker)[1]
        new_content = before + start_marker + "\n" + block_md + "\n" + end_marker + after
    else:
        new_content = content + "\n" + start_marker + "\n" + block_md + "\n" + end_marker
    with open(README_FILE, "w", encoding="utf-8") as f:
        f.write(new_content)

def commit_and_push():
    repo = git.Repo(REPO_PATH)
    repo.git.add(["README.md", "activity.json"])
    try:
        repo.index.commit("chore(activity): update activity table")
    except Exception:
        pass
    repo.git.push()

@app.route('/api/update', methods=['POST'])
def update_activity():
    data = request.json
    if not data:
        return jsonify({"status": "error"}), 400

    timestamp = datetime.now().strftime("%I:%M %p")
    new_item = {"time": timestamp, "site": data["site"], "title": data["title"], "url": data["url"]}

    activities = load_activities()
    if not activities or activities[0].get("url") != data["url"]:
        activities.insert(0, new_item)
    activities = activities[:MAX_ACTIVITIES]

    save_activities(activities)
    update_readme_with(activities)
    commit_and_push()

    return jsonify({"status": "ok", "activities": activities})

if __name__ == "__main__":
    app.run(port=5000)
