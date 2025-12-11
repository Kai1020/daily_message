from flask import Flask, render_template, request, redirect, url_for, jsonify
from datetime import date
import os

app = Flask(__name__)

# daily messages (you can edit later)
messages = [
    "You make the ordinary feel magical.",
    "Every day with you becomes my favourite day.",
    "Your smile feels like home.",
    "You make my heart feel understood.",
    "I admire the strength and kindness in you.",
    "My world is softer because you're in it.",
    "You are a blessing I don’t take for granted."
]

STORAGE = "sent_messages.txt"  # simple local storage for messages she sends

@app.route("/")
def home():
    # pick today's message
    day = date.today().toordinal()
    daily_message = messages[day % len(messages)]
    return render_template("index.html", message=daily_message)

@app.route("/submit_message", methods=["POST"])
def submit_message():
    name = request.form.get("name", "Anonymous").strip()
    text = request.form.get("text", "").strip()
    if text:
        entry = f"{date.today().isoformat()} | {name} | {text}\n"
        with open(STORAGE, "a", encoding="utf-8") as f:
            f.write(entry)
    return redirect(url_for("home"))

@app.route("/api/messages", methods=["GET"])
def api_messages():
    # returns last 10 saved messages (optional, JSON)
    if not os.path.exists(STORAGE):
        return jsonify([])
    with open(STORAGE, "r", encoding="utf-8") as f:
        lines = [l for l in f.read().splitlines() if l.strip()]
    return jsonify(lines[-10:])

if __name__ == "__main__":
    # during local testing use debug=True; Render will use gunicorn in production
    app.run(host="0.0.0.0", debug=True)
