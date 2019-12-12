from flask import Flask, render_template, redirect, request, flash
from google.appengine.api import users

import sys
sys.path.append('lib')
sys.path.append('models')

import User
from wtforms_appengine.ndb import model_form

app = Flask(__name__)
app.config["SECRET_KEY"] = "TestKey"

args = {}

def displayPage(pageName = "home"):
    return render_template("views/" + pageName + ".html", args=args)

@app.route("/")
def home():
    args["active"] = "home"
    return displayPage("home")

@app.route("/about")
def about():
    args["title"] = "About"
    args["active"] = "about"
    return displayPage("about")

LoginForm = model_form(User.User)

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        args["active"] = "login"
        args["title"] = "Login"
        user = User.getCurrentUser()
        if user:
            args["user"] = user
            args["logged_in"] = True
            return redirect('/account')
        args["loginForm"] = LoginForm()
        args["logged_in"] = False
        return displayPage('login')
    else:
        us = request.form["username"]
        p = request.form["password"]
        em = request.form["email"]
        newUser = User.User(username=us, email=em, password=p)
        newUser.put()
        return displayPage('account')


@app.route("/register")
def register():
    args["active"] = "register"
    args["title"] = "Register"
    return displayPage('register')

@app.route('/account')
def account():
    return displayPage('account')


if __name__ == "__main__":
    app.run(debug=True)
