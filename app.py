from flask import Flask, render_template, request
from datetime import date
import smtplib

app = Flask(__name__)

# ---------------------------------------------------------------------
# EMAIL SETTINGS (REPLACE THESE)
# ---------------------------------------------------------------------
YOUR_EMAIL = "kai2672004@gmail.com"      # keep quotes
APP_PASSWORD = "nssxpgyxcobu"      # keep quotes


# ---------------------------------------------------------------------
# DAILY MESSAGES
# ---------------------------------------------------------------------
messages = [
    "You make the ordinary feel magical.",
    "Every day with you becomes my favourite day.",
    "Your smile feels like home.",
    "You make my heart feel understood.",
    "I admire the strength and kindness in you.",
    "My world is softer because you're in it.",
    "You are a blessing I don’t take for granted."
]


# ---------------------------------------------------------------------
# HOME PAGE (DAILY MESSAGE)
# ---------------------------------------------------------------------
@app.route("/")
def home():
    day = date.today().toordinal()
    message = messages[day % len(messages)]
    return render_template("index.html", message=message)


# ---------------------------------------------------------------------
# GAME PAGE
# ---------------------------------------------------------------------
@app.route("/game")
def game():
    return render_template("game.html")


# ---------------------------------------------------------------------
# RECEIVE A MESSAGE (SEND TO YOUR EMAIL)
# ---------------------------------------------------------------------
@app.route("/submit_message", methods=["POST"])
def submit_message():
    name = request.form.get("name", "Someone")
    msg = request.form.get("message", "")

    full_message = f"Message from {name}:\n\n{msg}"

    try:
        server = smtplib.SMTP_SSL("smtp.gmail.com", 465)
        server.login(YOUR_EMAIL, APP_PASSWORD)
        server.sendmail(YOUR_EMAIL, YOUR_EMAIL, full_message)
        server.quit()
    except Exception as e:
        print("EMAIL ERROR:", e)

    return "Message sent successfully 💖"


# ---------------------------------------------------------------------
# LOVE METER MOOD UPDATE
# ---------------------------------------------------------------------
@app.route("/meter_update", methods=["POST"])
def meter_update():
    value = request.form.get("value")
    mood = request.form.get("mood")

    mood_message = f"Love Meter Update:\nValue: {value}%\nMood: {mood}\n"

    try:
        server = smtplib.SMTP_SSL("smtp.gmail.com", 465)
        server.login(YOUR_EMAIL, APP_PASSWORD)
        server.sendmail(YOUR_EMAIL, YOUR_EMAIL, mood_message)
        server.quit()
    except Exception as e:
        print("EMAIL ERROR:", e)

    return "OK"


# ---------------------------------------------------------------------
# RUN
# ---------------------------------------------------------------------
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
