import sys
sys.path.append('lib')
sys.path.append('models')
sys.path.append('controllers')

from flask import Flask, render_template, redirect, request, flash, url_for, session
from forms import RegistrationForm, LoginForm, ShowSearchForm

import UserController, OAuthController

import requests
import json

app = Flask(__name__)
app.config["SECRET_KEY"] = "TestKey"

args = {}

def display_page(pageName = "home", loginRequired = True):
    args["active"] = pageName

    if loginRequired:
        if session.get("user"):
            return render_template("views/" + pageName + ".html", args=args)
        flash("You must be logged in to view this page!", 'warning')
        return redirect(url_for('login'))

    if UserController.check_session_refresh():
        flash("Your current user sessions has expired, please log in again to confirm your identity.", 'warning')
        return redirect(url_for('login'))

    return render_template("views/" + pageName + ".html", args=args)

@app.route("/", methods=["GET", "POST"])
def home():
    args["title"] = "Film & TV Show Search | Home"
    args["searchForm"] = ShowSearchForm()
    if args["searchForm"].validate_on_submit():
        term = args["searchForm"].search_term.data
        country = args["searchForm"].search_location.data
        api_url = "https://utelly-tv-shows-and-movies-availability-v1.p.rapidapi.com/lookup"
        query = {"term": term, "country": country}
        headers = {
            'x-rapidapi-host': "utelly-tv-shows-and-movies-availability-v1.p.rapidapi.com",
            'x-rapidapi-key': "18bd841df1mshdd5f213b28bbd71p1611ddjsn225dc187fd4d"
        }
        response = requests.request("GET", api_url, headers=headers, params=query)
        args["api_response"] = json.loads(response.text)
        formatted_results = []
        if "results" in args["api_response"]:
            for result in args["api_response"]["results"]:
                if "name" in result:
                    if "locations" in result:
                        formatted_locations = []
                        alternate_locations = ""
                        for location in result["locations"]:
                            if location["url"]:
                                formatted_locations = formatted_locations + [{"url": location["url"], "icon": location["icon"], "display_name": location["display_name"]}]
                            else:
                                alternate_locations += location["display_name"] + ", "
                        alt_length = len(alternate_locations)
                        if alt_length > 0:
                            alternate_locations = alternate_locations[0:alt_length-2] + "."
                        formatted_results = formatted_results + [{"id": result["id"], "name": result["name"], "picture": result["picture"], "locations": formatted_locations, "alternate_locations": alternate_locations}]
        args["ff_response"] = formatted_results
        return display_page("search_results")
    return display_page("home", False)

@app.route("/about")
def about():
    args["title"] = "About"
    return display_page("about", False)

@app.route("/login", methods=["GET", "POST"])
def login():
    args["title"] = "Login"
    args["loginForm"] = LoginForm()
    if args["loginForm"].validate_on_submit():
        username = args["loginForm"].username.data
        pwd = args["loginForm"].password.data
        if UserController.check_user_pwd(username, pwd):
            pwd = None
            UserController.start_user_session(username)
            flash("Successfully logged in as " + username + "!", 'success')
            return redirect(url_for('account'))
        flash("Sorry, the login information provided was not correct", 'danger')
    return display_page("login", False)

@app.route("/google_login", methods=["POST"])
def google_login():
    req_data = request.get_json()
    if "id_token" in req_data:
        isVerified = OAuthController.verify_token(req_data["id_token"])
        if isVerified:
            OAuthController.check_existing_user(isVerified["user_id"], isVerified["user_email"], isVerified["user_token"])
            req_data["success"] = True
            return req_data
    req_data["success"] = False
    return display_page("home", False)

@app.route("/register", methods=["GET", "POST"])
def register():
    args["title"] = "Register"
    args["registerForm"] = RegistrationForm()
    if args["registerForm"].validate_on_submit():
        name = args["registerForm"].username.data
        if UserController.create_new_user("auto_gen", name, args["registerForm"].email.data, args["registerForm"].password.data, "Website"):
            flash("Your account [" + name + "] has been created!", "success")
        else:
            flash("Account Creation Error. Please attempt to register again", "danger")
    return display_page("register", False)

@app.route("/account")
def account():
    args["title"] = "My Account"
    return display_page('account')

@app.route('/logout')
def logout():
    UserController.end_user_session()
    flash("You have been logged out!", 'info')
    return redirect(url_for('home'))

if __name__ == "__main__":
    app.run()
