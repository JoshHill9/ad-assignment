from flask import Flask, render_template
from google.appengine.api import users

app = Flask(__name__)

@app.route('/')
def home():
    return render_template("views/home.html", active="home")

@app.route('/about')
def about():
    return render_template("views/about.html", title="About", active="about")

@app.route('/login')
def login():
    return render_template("views/login.html", active="login")

if __name__ == "__main__":
    app.run(debug=True)