import sys
sys.path.append('lib')
sys.path.append('models')

from flask import Flask, render_template, redirect, request, flash, url_for
from google.appengine.api import users
from forms import RegistrationForm, LoginForm
from pybcrypt import bcrypt

import User

app = Flask(__name__)
app.config["SECRET_KEY"] = "TestKey"

args = {}

def displayPage(pageName = "home"):
    args["active"] = pageName
    args["user"] = User.getCurrentUser()

    return render_template("views/" + pageName + ".html", args=args)

@app.route("/")
def home():
    return displayPage("home")

@app.route("/about")
def about():
    args["title"] = "About"

    return displayPage("about")

@app.route("/login", methods=["GET", "POST"])
def login():
    args["title"] = "Login"
    args["user_glogin"] = User.getUserLoginURL()
    args["user_glogout"] = User.getUserLogoutURL()

    args["loginForm"] = LoginForm()

    if args["loginForm"].validate_on_submit():

        username = args["loginForm"].username.data
        loginUser = User.findUser(username)
        if loginUser["new"] == True:
            flash("Sorry, this account does not exist", 'danger')
        else:
            loginUser = loginUser["user"]
            checkPw = bcrypt.hashpw(args["loginForm"].password.data, loginUser.password)
            if checkPw == loginUser.password:
                flash("Successfully logged in as " + username + "!", 'success')
            else:
                flash("Sorry, the login information provided was not correct", 'danger')

    return displayPage("login")


@app.route("/register", methods=["GET", "POST"])
def register():
    args["title"] = "Register"

    args["registerForm"] = RegistrationForm()

    if args["registerForm"].validate_on_submit():
        name = args["registerForm"].username.data
        userExists = User.findUser(name)
        if userExists["new"] == False:
            flash("Sorry, the username [" + name + "] is already taken!", 'danger')
        else:
            newAcc = userExists["user"]
            try:
                newAcc.username = args["registerForm"].username.data
                newAcc.email = args["registerForm"].email.data

                hP = bcrypt.hashpw(args["registerForm"].password.data, bcrypt.gensalt(6))
                newAcc.password = hP

                newAcc.put()

                flash("Your account [" + name + "] has been created!", 'success')
            except ValueError:
                pass
    return displayPage("register")

if __name__ == "__main__":
    app.run(debug=True)
