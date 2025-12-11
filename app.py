from flask import Flask, render_template, request, jsonify, redirect, url_for
import requests
from datetime import date

app = Flask(__name__)

# ------------ CONFIG (REPLACE) ------------
TELEGRAM_TOKEN = "YOUR_TELEGRAM_BOT_TOKEN"
CHAT_ID = "YOUR_CHAT_ID"
# -------------------------------------------

def send_telegram(text):
    try:
        url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
        requests.post(url, json={"chat_id": CHAT_ID, "text": text})
    except Exception as e:
        print("Telegram error:", e)

# daily messages
messages = [
    "You make the ordinary feel magical.",
    "Every day with you becomes my favourite day.",
    "Your smile feels like home.",
    "You make my heart feel understood.",
    "I admire the strength and kindness in you.",
    "My world is softer because you're in it.",
    "You are a blessing I don’t take for granted."
]

@app.route("/")
def home():
    return render_template("home.html")

@app.route("/daily")
def daily():
    d = date.today().toordinal()
    msg = messages[d % len(messages)]
    return render_template("daily.html", message=msg)

@app.route("/cards")
def cards():
    return render_template("cards.html")

@app.route("/meter")
def meter():
    return render_template("meter.html")

@app.route("/message")
def message():
    return render_template("message.html")

@app.route("/game")
def game():
    return render_template("game.html")

# receive text message (from form)
@app.route("/send_message", methods=["POST"])
def send_message():
    name = request.form.get("name", "Someone")
    text = request.form.get("message", "").strip()
    if text:
        entry = f"💌 New message\nFrom: {name}\nMessage: {text}"
        send_telegram(entry)
    return redirect(url_for("message"))

# meter updates (JSON)
@app.route("/meter_update", methods=["POST"])
def meter_update():
    payload = request.get_json(force=True, silent=True) or {}
    value = payload.get("value")
    mood = payload.get("mood")
    if value is not None and mood is not None:
        send_telegram(f"💗 Love meter update\nValue: {value}%\nMood: {mood}")
        return jsonify(status="ok")
    return jsonify(status="missing"), 400

if __name__ == "__main__":
    app.run(host="0.0.0.0")
