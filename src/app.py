from flask import Flask, render_template

app = Flask(__name__)


@app.route("/dashboard")
def home():
    return render_template("./pages/dashboard.html")

@app.route("/")
def ladingPage():
    return render_template("./pages/home.html")