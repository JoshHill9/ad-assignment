import sys
sys.path.append('lib')
sys.path.append('models')

from flask import Flask, render_template, redirect, request, flash, url_for
from google.appengine.api import users
from forms import RegistrationForm, LoginForm
from pybcrypt import bcrypt

import User
from datetime import datetime, timedelta

app = Flask(__name__)
app.config["SECRET_KEY"] = "TestKey"

args = {}

def displayPage(pageName = "home", loginRequired = True):
    args["active"] = pageName
    if args.get("session_end_time"):
        # Logs out User every 45 minutes from the login time
        if datetime.now() > args["session_end_time"]:
            args["user"] = None
            args["session_start_time"] = None
            args["session_end_time"] = None
            args["session_vars"] = None
            flash("Your current user sessions has expired, please log in again to confirm your identity.", 'warning')
            return redirect(url_for('login'))

    if loginRequired:
        if args.get("user"):
            return render_template("views/" + pageName + ".html", args=args)
        flash("You must be logged in to view this page!", 'warning')
        return redirect(url_for('login'))

    return render_template("views/" + pageName + ".html", args=args)

@app.route("/")
def home():
    return displayPage("home", False)

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
        loginUser = User.findUserByName(username)
        checkPw = bcrypt.hashpw(args["loginForm"].password.data, loginUser.password)
        if checkPw == loginUser.password:
            args["user"] = loginUser.username
            args["session_start_time"] = datetime.now()
            args["session_end_time"] = args["session_start_time"] + timedelta(minutes=45)
            flash("Successfully logged in as " + username + "!", 'success')
            return redirect(url_for('account')) if not request.args.get('next') else redirect(url_for(request.args["next"]))
        else:
            flash("Sorry, the login information provided was not correct", 'danger')
    return displayPage("login", False)


@app.route("/register", methods=["GET", "POST"])
def register():
    args["title"] = "Register"
    args["registerForm"] = RegistrationForm()
    if args["registerForm"].validate_on_submit():
        name = args["registerForm"].username.data
        newAcc = User.createNewUser(name)
        try:
            newAcc.username = args["registerForm"].username.data
            newAcc.email = args["registerForm"].email.data
            hP = bcrypt.hashpw(args["registerForm"].password.data, bcrypt.gensalt(6))
            newAcc.password = hP
            newAcc.put()
            flash("Your account [" + name + "] has been created!", 'success')
        except ValueError:
            pass
    return displayPage("register", False)

@app.route("/account")
def account():
    args["title"] = "My Account"
    return displayPage('account')

@app.route('/logout')
def logout():
    args["user"] = None
    args["session_start_time"] = None
    args["session_end_time"] = None
    args["session_vars"] = None
    flash("You have been logged out!", 'info')
    return redirect(url_for('login'))

@app.route('/todos')
def todos():
    args["title"] = "My To DOs"
    return displayPage('todos', False)

if __name__ == "__main__":
    app.run(debug=True)
