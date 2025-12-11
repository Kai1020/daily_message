from flask import Flask, render_template, request, redirect, url_for
from datetime import date
import smtplib
from email.mime.text import MIMEText
import os

app = Flask(__name__)

# ==============================
# CONFIGURE YOUR EMAIL HERE
# ==============================
YOUR_EMAIL = "yourgmail@gmail.com"   # <-- change to YOUR Gmail
APP_PASSWORD = "your_app_password"   # <-- paste your NEW Gmail App Password (no spaces)
# ==============================

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


@app.route("/")
def home():
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

        # Send email notification
        try:
            body = f"New message from your website:\n\nFrom: {name}\nMessage:\n{text}"
            msg = MIMEText(body)
            msg["Subject"] = "New Love Message ❤️"
            msg["From"] = YOUR_EMAIL
            msg["To"] = YOUR_EMAIL

            server = smtplpt.SMTP_SSL("smtp.gmail.com", 465)
            server.login(YOUR_EMAIL, APP_PASSWORD)
            server.sendmail(YOUR_EMAIL, YOUR_EMAIL, msg.as_string())
            server.quit()
        except Exception as e:
            print("EMAIL ERROR:", e)

    return redirect(url_for("home"))


if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)
