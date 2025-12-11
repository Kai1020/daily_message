from flask import Flask, render_template, request, redirect, url_for, jsonify
from datetime import date
import json
import os
import requests

app = Flask(__name__)

# ----------------------------
# CONFIG - REPLACE THESE
# ----------------------------
TELEGRAM_TOKEN = "8541424045:AAGJz5sMje4EjyHzDLR_AFgAE7hwfsd8BQo"   # replace with your token
CHAT_ID = "6942307057"                     # replace with your chat id (string or number)
ADMIN_KEY = "tanyam123"          # pick a secret string and keep it private
# ----------------------------

DATA_FILE = "messages.json"  # persistent storage for messages

# default messages (120+) — initial dataset
DEFAULT_MESSAGES = [
"Good morning, Shahad — may your day be soft and bright.",
"You make ordinary moments feel like magic.",
"Thinking about your smile right now.",
"You're the warmest part of my day.",
"Each day with you is a favorite chapter.",
"Your laugh is my favorite sound.",
"You make my world gentle and kind.",
"I love the little ways you show you care.",
"You're a quiet miracle in my life.",
"My heart knows home when you're near.",
"Your presence makes everything lighter.",
"Every message from you is a treasure.",
"You carry sunshine in your pocket.",
"I admire your kindness every day.",
"Your voice feels like an embrace.",
"I'm grateful for every little moment with you.",
"Your smile is my favorite view.",
"You are more beautiful than you know.",
"In your eyes I find home and adventure.",
"You're my soft place on loud days.",
"I think about the way you tilt your head.",
"You bring calm to my busiest days.",
"Your courage is quietly inspiring.",
"Small things you do mean the world to me.",
"I could listen to you forever.",
"You're a poem I love rereading.",
"Your laugh is a warm, bright light.",
"Every day with you is sweeter than before.",
"Your kindness makes strangers kinder.",
"Being with you feels wonderfully easy.",
"I love the way you notice the small things.",
"You make ordinary days sparkle.",
"You're the best part of my plans.",
"Your warmth lingers like perfume.",
"I like the way you say my name.",
"You make even silence feel comfortable.",
"I love how you see the world.",
"You're my favorite hello and my hardest goodbye.",
"You're a beautiful reason to smile today.",
"With you, even small things feel grand.",
"Your hands are a safe place.",
"You are gentler than a summer breeze.",
"I wish I could wrap you in all my care.",
"Just a thought of you makes my day better.",
"You make simple moments unforgettable.",
"Your kindness is quietly powerful.",
"I miss your smile right now.",
"You have a soft, steady strength.",
"There's a galaxy in your eyes.",
"Your presence is my daily comfort.",
"I love the way you make things better.",
"You deserve every bit of happiness today.",
"Your giggle could fix any bad day.",
"You are a constant, lovely surprise.",
"Your heart is made of the best things.",
"I think the stars conspired to make you.",
"You are sweeter than the kindest thing I know.",
"Your voice is my favorite melody.",
"Your courage makes me proud.",
"You are warmer than winter sunlight.",
"Everything's better when I imagine you smiling.",
"You make normal moments feel romantic.",
"I'm still smiling just thinking about you.",
"The world feels kinder with you in it.",
"Your smile is like a small sunrise.",
"You're calm, clever, and endlessly kind.",
"You make my day feel complete.",
"I treasure every silly, small memory with you.",
"You are loved more than you know.",
"Your eyes hold wonderful stories.",
"I'd choose you in every lifetime.",
"Your hugs are my shelter.",
"You have the gentlest strength.",
"The way you care is quietly heroic.",
"I love you more than yesterday.",
"Your voice is a soft, perfect song.",
"You make my ordinary world extraordinary.",
"You are brave, beautiful, and true.",
"Your laugh is a pocket of sunshine.",
"Just you being you is enough.",
"You make even gloomy days feel softer.",
"You're a gallery of the gentlest things.",
"I adore the person you are becoming.",
"Your light makes me feel safer.",
"I love the tiny details about you.",
"Your kindness is the kind the world needs.",
"You are my calm in the storm.",
"Your smile outshines the rest of the day.",
"I’m grateful for every message from you.",
"Your presence turns grey skies pink.",
"You're the gentlest kind of amazing.",
"Each day I find another reason to adore you.",
"You make love feel like the simplest thing.",
"I'm proud of the little things you do.",
"You have the kindest heart I know.",
"Your warmth could melt mountains.",
"You are my favorite comforting thought.",
"You make every minute feel cozy.",
"I keep a soft place for you in my thoughts.",
"You are a beautiful, soft constant.",
"Your care is my favorite gift.",
"You're sweeter than the sweetest song.",
"You're my favorite story to return to.",
"Your laugh is a treasured soundtrack.",
"You are the calm I look for.",
"Your thoughtfulness is endlessly lovely.",
"Every message from you is a soft gift.",
"You're the spark that brightens routine days."
]

# -------------------------------------------------------
# Persistent messages handling (load/save)
# -------------------------------------------------------
def load_messages():
    if os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
            # ensure list
            if isinstance(data, list) and data:
                return data
        except Exception:
            pass
    # fallback: write defaults
    save_messages(DEFAULT_MESSAGES)
    return DEFAULT_MESSAGES

def save_messages(lst):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(lst, f, ensure_ascii=False, indent=2)

# load at startup
MESSAGES = load_messages()

# special dates config: map (month,day) -> message (personalized)
SPECIAL_DATES = {
    (1, 7): f"Happy Birthday, Shahad! 🎉 May your day be as beautiful as your heart ❤️"   # Jan 7
    # add more special-dates here if you want later
}

# -------------------------------------------------------
# Utility: pick today's message (birthday override)
# -------------------------------------------------------
def today_message():
    t = date.today()
    # special date?
    special = SPECIAL_DATES.get((t.month, t.day))
    if special:
        return special
    # deterministic rotation: use ordinal to choose index
    idx = t.toordinal() % len(MESSAGES)
    return MESSAGES[idx]

# -------------------------------------------------------
# Telegram helper (used for messages / meter updates)
# -------------------------------------------------------
def send_telegram(text):
    if not TELEGRAM_TOKEN or not CHAT_ID:
        print("Telegram not configured")
        return False
    try:
        url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
        requests.post(url, json={"chat_id": CHAT_ID, "text": text})
        return True
    except Exception as e:
        print("Telegram error:", e)
        return False

# -------------------------------------------------------
# Routes
# -------------------------------------------------------
@app.route("/")
def home():
    return render_template("home.html")

@app.route("/daily")
def daily():
    msg = today_message()
    return render_template("daily.html", message=msg)

@app.route("/send_message", methods=["POST"])
def send_message():
    name = request.form.get("name", "Someone").strip()
    text = request.form.get("message", "").strip()
    if text:
        send_telegram(f"💌 New message for you\nFrom: {name}\n\n{text}")
    return redirect(url_for("message"))  # redirect back to message page

@app.route("/meter_update", methods=["POST"])
def meter_update():
    payload = request.get_json(force=True, silent=True) or {}
    value = payload.get("value")
    mood = payload.get("mood")
    if value is not None and mood:
        send_telegram(f"💗 Love meter update\nValue: {value}%\nMood: {mood}")
        return jsonify(status="ok")
    return jsonify(status="missing"), 400

# Simple admin to add messages (protected by ?key=ADMIN_KEY)
@app.route("/admin", methods=["GET", "POST"])
def admin():
    key = request.args.get("key", "")
    if key != ADMIN_KEY:
        return "Forbidden: provide correct admin key as ?key=YOUR_KEY", 403

    if request.method == "POST":
        new_msg = request.form.get("new_message", "").strip()
        if new_msg:
            MESSAGES.insert(0, new_msg)  # add to front (so appears sooner)
            save_messages(MESSAGES)
            return redirect(url_for("admin") + f"?key={ADMIN_KEY}")
    # show simple admin page
    return """
    <html><body style="font-family:Arial;padding:20px;">
    <h2>Add a new daily message</h2>
    <form method="post">
      <textarea name="new_message" rows="4" cols="60" placeholder="Write new message..."></textarea><br><br>
      <button type="submit">Add message</button>
    </form>
    <p>Messages stored: {count}</p>
    </body></html>
    """.format(count=len(MESSAGES))

# simple pages reused by your existing site
@app.route("/cards")
def cards():
    return render_template("cards.html")

@app.route("/message")
def message():
    return render_template("message.html")

@app.route("/game")
def game():
    return render_template("game.html")

@app.route("/meter")
def meter():
    return render_template("meter.html")

# -------------------------------------------------------
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
