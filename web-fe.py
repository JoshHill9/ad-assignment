import sys
sys.path.append('lib')
sys.path.append('models')
sys.path.append('controllers')

from flask import Flask, render_template, redirect, request, flash, url_for, session
from forms import RegistrationForm, LoginForm, SearchForm

import UserController, OAuthController, SearchResultController, SearchValidatorController
import os

app = Flask(__name__)
app.config["SECRET_KEY"] = os.urandom(24)

args = {}

# Renders page view and sets active page in navigation bar.
# Prevents access to pages that require login_form
# Notifies User of end of Session
def display_page(page_name = "home", login_required = True):
    args["active"] = page_name

    if login_required:
        if session.get("user"):
            return render_template("views/" + page_name + ".html", args=args)
        flash("You must be logged in to view this page!", 'warning')
        return redirect(url_for('login'))

    if UserController.check_session_refresh():
        flash("Your current user sessions has expired, please log in again to confirm your identity.", 'warning')
        return redirect(url_for('login'))

    return render_template("views/" + page_name + ".html", args=args)

# Display home page and load film/tv show search form
@app.route("/", methods=["GET", "POST"])
def home():
    args["title"] = "Film & TV Show Search | Home"
    args["search_form"] = SearchForm()
    if args["search_form"].validate_on_submit():
        term = args["search_form"].search_term.data
        country = args["search_form"].search_location.data
        # Check to see if the search has been performed recently and stored in Datastore
        saved_result = SearchResultController.get_search_result(term, country)
        csrf_token = args["search_form"].csrf_token.current_token
        if saved_result:
            # Check if the stored search result is expired (more than 1 day old)
            if SearchResultController.check_result_expiry(term, country):
                # Gets new search result from Utelly API
                args["search_results"] = SearchResultController.perform_search(term, country)
                args["search_date"] = "Just Now"
                SearchValidatorController.create_validator(term, country, csrf_token)
                # Queues a task on task-be module to delete expired Datastore search result
                SearchResultController.queue_search_task({"term": term, "country": country, "expired": True, "csrf": csrf_token})
                # Queues a task on task-be module to save new search result from Utelly API
                SearchResultController.queue_search_task({"term": term, "country": country, "result": str(args["search_results"]), "csrf": csrf_token})
            else:
                # Formats stored result from String to List type for correct displaying
                args["search_results"] = SearchResultController.format_saved_result(saved_result.search_result)
                args["search_date"] = saved_result.search_date
        else:
            args["search_results"] = SearchResultController.perform_search(term, country)
            args["search_date"] = "Just Now"
            SearchValidatorController.create_validator(term, country, csrf_token)
            SearchResultController.queue_search_task({"term": term, "country": country, "result": str(args["search_results"]), "csrf": csrf_token})
        return display_page("search_results")
    return display_page("home", False)

@app.route("/about")
def about():
    args["title"] = "About"
    return display_page("about", False)


@app.route("/login", methods=["GET", "POST"])
def login():
    args["title"] = "Login"
    args["login_form"] = LoginForm()
    if args["login_form"].validate_on_submit():
        username = args["login_form"].username.data
        pwd = args["login_form"].password.data
        if UserController.check_user_pwd(username, pwd):
            pwd = None
            UserController.start_user_session(username)
            flash("Successfully logged in as " + username + "!", 'success')
            return redirect(url_for('account'))
        flash("Sorry, the login information provided was not correct", 'danger')
    return display_page("login", False)

# Handles Request sent from Google Sign In button
# Verifies provided token with OAuth2.0 and allows sign in from google users
@app.route("/google_login", methods=["POST"])
def google_login():
    request_data = request.get_json()
    if "id_token" in request_data:
        is_verified = OAuthController.verify_token(request_data["id_token"])
        if is_verified:
            OAuthController.check_existing_user(is_verified["user_id"], is_verified["user_email"], is_verified["user_token"])
            # Notifies client of successful User Authentication
            request_data['success'] = True
            return request_data
    return display_page("home", False)


@app.route("/register", methods=["GET", "POST"])
def register():
    args["title"] = "Register"
    args["registration_form"] = RegistrationForm()
    if args["registration_form"].validate_on_submit():
        username = args["registration_form"].username.data
        if UserController.create_user("auto_gen", username, args["registration_form"].email.data, args["registration_form"].password.data, "Website"):
            flash("Your account [" + username + "] has been created! Please login to continue.", "success")
            return redirect(url_for("login"))
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
