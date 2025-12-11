from flask import Flask, render_template, request, jsonify
import requests
from datetime import date

app = Flask(__name__)

# 🚨 REPLACE THESE WITH YOUR VALUES
TELEGRAM_TOKEN = "8541424045:AAGJz5sMje4EjyHzDLR_AFgAE7hwfsd8BQo"
CHAT_ID = "6942307057"

def send_telegram(msg):
    try:
        url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
        data = {"chat_id": CHAT_ID, "text": msg}
        requests.post(url, json=data)
    except Exception as e:
        print("Telegram error:", e)

messages = [
    "You make the ordinary feel magical.",
    "Every day with you becomes my favourite day.",
    "Your smile feels like home.",
    "You make my heart feel understood.",
    "I admire the strength and kindness in you.",
    "You are a blessing I don’t take for granted."
]

@app.route("/")
def home():
    day = date.today().toordinal()
    msg = messages[day % len(messages)]
    return render_template("index.html", message=msg)

@app.route("/game")
def game():
    return render_template("game.html")

@app.route("/send_message", methods=["POST"])
def get_message():
    name = request.form.get("name", "Unknown")
    message = request.form.get("message", "(No message)")

    send_telegram(f"💌 New message from your girlfriend:\n\nName: {name}\nMessage: {message}")

    return jsonify({"status": "sent"})

@app.route("/meter_update", methods=["POST"])
def meter_update():
    value = request.json.get("value")
    mood = request.json.get("mood")

    send_telegram(f"💗 Love meter update:\nValue: {value}%\nMood: {mood}")

    return jsonify({"status": "ok"})

if __name__ == "__main__":
    app.run()
