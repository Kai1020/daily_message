from flask import Flask, render_template
from datetime import date

app = Flask(__name__)

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
    day = date.today().toordinal()
    message = messages[day % len(messages)]
    return render_template("index.html", message=message)

if __name__ == "__main__":
    app.run(debug=True)
