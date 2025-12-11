from flask import Flask, render_template, request, redirect, url_for
from datetime import date
import smtplib
from email.mime.text import MIMEText
import os

app = Flask(__name__)

# ==============================
# EMAIL CONFIGURATION
# ==============================
YOUR_EMAIL = "yourgmail@gmail.com"        # <--- change this to your Gmail
APP_PASSWORD = "your_app_password_here"   # <--- NEW Gmail App Password (no spaces)
# ==============================

# Daily messages
messages = [
    "You make the ordinary feel magical.",
    "Every day with you becomes my favourite day.",
    "Your smile feels like home.",
    "You make my heart feel understood.",
    "I admire the strength and kindness in you.",
    "My world is softer because you're in it.",
    "You are a blessing I don’t take for granted."
]

STORAGE = "sent_messages.txt"
METER_LOG = "meter_log.txt"


@app.route("/")
def home():
    day = date.today().toordinal()
    daily_message = messages[day % len(messages)]
    return render_template("index.html", message=daily_message)


# ======================================================
# Handle messages she writes to you
# ======================================================
@app.route("/submit_message", methods=["POST"])
def submit_message():
    name = request.form.get("name", "Anonymous").strip()
    text = request.form.get("text", "").strip()

    if text:
        # Save message in file
        entry = f"{date.today().isoformat()} | {name} | {text}\n"
        with open(STORAGE, "a", encoding="utf-8") as f:
            f.write(entry)

        # Email you
        try:
            body = f"New message from your website:\n\nFrom: {name}\nMessage:\n{text}"
            msg = MIMEText(body)
            msg["Subject"] = "New Love Message ❤️"
            msg["From"] = YOUR_EMAIL
            msg["To"] = YOUR_EMAIL

            server = smtplib.SMTP_SSL("smtp.gmail.com", 465)
            server.login(YOUR_EMAIL, APP_PASSWORD)
            server.sendmail(YOUR_EMAIL, YOUR_EMAIL, msg.as_string())
            server.quit()

        except Exception as e:
            print("EMAIL ERROR:", e)

    return redirect(url_for("home"))


# ======================================================
# Handle Love Meter updates (save + email)
# ======================================================
@app.route("/meter_update", methods=["POST"])
def meter_update():
    value = request.form.get("value")
    mood = request.form.get("mood")

    # Save to log file
    with open(METER_LOG, "a", encoding="utf-8") as f:
        f.write(f"{date.today().isoformat()} | {value}% | {mood}\n")

    # Email you
    try:
        body = f"Love Meter Update ❤️\n\nShe slid it to: {value}%\nMood: {mood}"
        msg = MIMEText(body)
        msg["Subject"] = "Love Meter Mood Update ❤️"
        msg["From"] = YOUR_EMAIL
        msg["To"] = YOUR_EMAIL

        server = smtplib.SMTP_SSL("smtp.gmail.com", 465)
        server.login(YOUR_EMAIL, APP_PASSWORD)
        server.sendmail(YOUR_EMAIL, YOUR_EMAIL, msg.as_string())
        server.quit()

    except Exception as e:
        print("EMAIL ERROR:", e)

    return "OK"


if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)
