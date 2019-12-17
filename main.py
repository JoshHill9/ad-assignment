from flask import Flask, render_template
from google.appengine.api import users
from forms import RegistrationForm

import sys
sys.path.append('lib')

import models

app = Flask(__name__)
app.config["SECRET_KEY"] = "TestKey"

args = {}

def displayPage(pageName = "home"):
    if pageName:
        return render_template("views/" + pageName + ".html", args=args)

@app.route("/")
def home():
    args["active"] = "home"
    return displayPage("home")

@app.route("/about")
def about():
    args["active"] = "about"
    args["title"] = "About"
    return displayPage("about")

@app.route("/login")
def login():
    args["active"] = "login"
    args["title"] = "Login"
    args["user"] = models.isUserLoggedIn()
    return displayPage("login")

@app.route("/register")
def register():
    args["active"] = "register"
    args["title"] = "Register"

    args["form"] = RegistrationForm()

    return displayPage("register")

if __name__ == "__main__":
    app.run(debug=True)
