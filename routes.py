import sys
sys.path.append('lib')
sys.path.append('models')
sys.path.append('controllers')

from flask import Flask, render_template, redirect, request, flash, url_for, session
from google.appengine.api import users
from forms import RegistrationForm, LoginForm, ShowSearchForm

import UserController, OAuthController

import requests

app = Flask(__name__)
app.config["SECRET_KEY"] = "TestKey"

args = {}

def displayPage(pageName = "home", loginRequired = True):
    args["active"] = pageName

    if loginRequired:
        if session.get("user"):
            return render_template("views/" + pageName + ".html", args=args)
        flash("You must be logged in to view this page!", 'warning')
        return redirect(url_for('login'))

    if UserController.checkSessionRefresh():
        flash("Your current user sessions has expired, please log in again to confirm your identity.", 'warning')
        return redirect(url_for('login'))

    return render_template("views/" + pageName + ".html", args=args)

@app.route("/")
def home():
    args["title"] = None
    return displayPage("home", False)

@app.route("/about")
def about():
    args["title"] = "About"
    return displayPage("about")

@app.route("/login", methods=["GET", "POST"])
def login():
    args["title"] = "Login"
    args["loginForm"] = LoginForm()
    if args["loginForm"].validate_on_submit():
        username = args["loginForm"].username.data
        pwd = args["loginForm"].password.data
        if UserController.checkUserPwd(username, pwd):
            pwd = None
            UserController.startUserSession(username)
            flash("Successfully logged in as " + username + "!", 'success')
            return redirect(url_for('account'))
        flash("Sorry, the login information provided was not correct", 'danger')
    return displayPage("login", False)

@app.route("/google_login", methods=["POST"])
def google_login():
    req_data = request.get_json()
    if "id_token" in req_data:
        isVerified = OAuthController.verifyToken(req_data["id_token"])
        if isVerified:
            OAuthController.checkExistingUser(isVerified["user_email"], isVerified["user_token"])
            req_data["success"] = True
            return req_data
    req_data["success"] = False
    return displayPage("home", False)

@app.route("/register", methods=["GET", "POST"])
def register():
    args["title"] = "Register"
    args["registerForm"] = RegistrationForm()
    if args["registerForm"].validate_on_submit():
        name = args["registerForm"].username.data
        if UserController.createNewUser(name, name, args["registerForm"].email.data, args["registerForm"].password.data, "Website"):
            flash("Your account [" + name + "] has been created!", "success")
        else:
            flash("Account Creation Error. Please attempt to register again", "danger")
    return displayPage("register", False)

@app.route("/search", methods=["GET", "POST"])
def show_search():
    args["title"] = "Show Search"
    args["searchForm"] = ShowSearchForm()
    if args["searchForm"].validate_on_submit():
        term = args["searchForm"].search_term.data
        country = args["searchForm"].search_location.data
        api_url = "https://utelly-tv-shows-and-movies-availability-v1.p.rapidapi.com/lookup"
        query = {"term": term, "country": country}
        headers = {"x-rapidapi-host": "utelly-tv-shows-and-movies-availability-v1.p.rapidapi.com", "x-rapidapi-key": "18bd841df1mshdd5f213b28bbd71p1611ddjsn225dc187fd4d"}
        response = requests.request("GET", api_url, headers=headers, params=query)
        args["api_response"] = response
        return displayPage("search_results", False)
    return displayPage("search", False)

@app.route("/account")
def account():
    args["title"] = "My Account"
    return displayPage('account')

@app.route('/logout')
def logout():
    UserController.endUserSession()
    flash("You have been logged out!", 'info')
    return redirect(url_for('home'))

@app.route('/todos')
def todos():
    args["title"] = "My To DOs"
    return displayPage('todos', False)

if __name__ == "__main__":
    app.run()
