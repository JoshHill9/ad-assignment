import sys
sys.path.append('lib')
sys.path.append('models')
sys.path.append('controllers')

from flask import Flask, render_template, redirect, request, flash, url_for, session
from google.appengine.api import users
from forms import RegistrationForm, LoginForm, ShowSearchForm

import UserController, OAuthController

import requests
import json

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

@app.route("/film_search", methods=["GET", "POST"])
def film_search():
    args["title"] = "Film & TV Show Search"
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
        #args["api_response"] = {u'updated': u'2019-12-22T04:04:07+0000', u'status_code': 200, u'variant': u'utelly', u'results': [{u'name': u'Sticks and Stones', u'locations': [{u'name': u'STV HD', u'icon': u'https://utellyassets7.imgix.net/locations_icons/utelly/live_tv_square/50d35301f0ca9f57980045a5.jpg?w=92&auto=compress&app_version=0f692b6a-217b-4753-a78b-4351ba443607_2019-12-22', u'id': u'50d35301f0ca9f57980045a5', u'display_name': u'STV HD', u'url': None}, {u'name': u'ITV HD', u'icon': u'https://utellyassets7.imgix.net/locations_icons/utelly/live_tv_square/57705920ebb7f92b2055435e.jpg?w=92&auto=compress&app_version=0f692b6a-217b-4753-a78b-4351ba443607_2019-12-22', u'id': u'57705920ebb7f92b2055435e', u'display_name': u'ITV HD', u'url': None}, {u'name': u'ITV Granada HD', u'icon': u'https://utellyassets7.imgix.net/locations_icons/utelly/live_tv_square/50d3530df0ca9f5798004f49.jpg?w=92&auto=compress&app_version=0f692b6a-217b-4753-a78b-4351ba443607_2019-12-22', u'id': u'50d3530df0ca9f5798004f49', u'display_name': u'ITV Granada HD', u'url': None}, {u'name': u'ITV Yorkshire', u'icon': u'https://utellyassets7.imgix.net/locations_icons/utelly/live_tv_square/50d353a6f0ca9f579800c27a.jpg?w=92&auto=compress&app_version=0f692b6a-217b-4753-a78b-4351ba443607_2019-12-22', u'id': u'50d353a6f0ca9f579800c27a', u'display_name': u'ITV Yorkshire', u'url': None}, {u'name': u'ITV - Channel TV', u'icon': u'https://utellyassets7.imgix.net/locations_icons/utelly/live_tv_square/50d352f2f0ca9f5798003b87.jpg?w=92&auto=compress&app_version=0f692b6a-217b-4753-a78b-4351ba443607_2019-12-22', u'id': u'50d352f2f0ca9f5798003b87', u'display_name': u'ITV - Channel TV', u'url': None}, {u'name': u'ITV Yorkshire Tyne Tees +1', u'icon': u'https://utellyassets7.imgix.net/locations_icons/utelly/live_tv_square/55c20fc2ebb7f94c833a98a2.jpg?w=92&auto=compress&app_version=0f692b6a-217b-4753-a78b-4351ba443607_2019-12-22', u'id': u'55c20fc2ebb7f94c833a98a2', u'display_name': u'ITV Yorkshire Tyne Tees +1', u'url': None}, {u'name': u'ITV Granada Border +1', u'icon': u'https://utellyassets7.imgix.net/locations_icons/utelly/live_tv_square/50d352b3f0ca9f5798000b74.jpg?w=92&auto=compress&app_version=0f692b6a-217b-4753-a78b-4351ba443607_2019-12-22', u'id': u'50d352b3f0ca9f5798000b74', u'display_name': u'ITV Granada Border +1', u'url': None}, {u'name': u'ITV West Country', u'icon': u'https://utellyassets7.imgix.net/locations_icons/utelly/live_tv_square/55c20fc7ebb7f94c833aa257.jpg?w=92&auto=compress&app_version=0f692b6a-217b-4753-a78b-4351ba443607_2019-12-22', u'id': u'55c20fc7ebb7f94c833aa257', u'display_name': u'ITV West Country', u'url': None}, {u'name': u'STV + 1 (North)', u'icon': u'https://utellyassets7.imgix.net/locations_icons/utelly/live_tv_square/5d421008302b84002fc548b0.jpg?w=92&auto=compress&app_version=0f692b6a-217b-4753-a78b-4351ba443607_2019-12-22', u'id': u'5d421008302b84002fc548b0', u'display_name': u'STV + 1 (North)', u'url': None}, {u'name': u'ITV London', u'icon': u'https://utellyassets7.imgix.net/locations_icons/utelly/live_tv_square/52748d36f0ca9f108216c7a6.jpg?w=92&auto=compress&app_version=0f692b6a-217b-4753-a78b-4351ba443607_2019-12-22', u'id': u'52748d36f0ca9f108216c7a6', u'display_name': u'ITV London', u'url': None}, {u'name': u'ITV Anglia', u'icon': u'https://utellyassets7.imgix.net/locations_icons/utelly/live_tv_square/528b4a6ef0ca9f78cc250834.jpg?w=92&auto=compress&app_version=0f692b6a-217b-4753-a78b-4351ba443607_2019-12-22', u'id': u'528b4a6ef0ca9f78cc250834', u'display_name': u'ITV Anglia', u'url': None}, {u'name': u'UTV+1', u'icon': u'https://utellyassets7.imgix.net/locations_icons/utelly/live_tv_square/5d338fa9302b84002f689e07.jpg?w=92&auto=compress&app_version=0f692b6a-217b-4753-a78b-4351ba443607_2019-12-22', u'id': u'5d338fa9302b84002f689e07', u'display_name': u'UTV +1', u'url': None}, {u'name': u'STV North', u'icon': u'https://utellyassets7.imgix.net/locations_icons/utelly/live_tv_square/55c20fc3ebb7f94c833a99df.jpg?w=92&auto=compress&app_version=0f692b6a-217b-4753-a78b-4351ba443607_2019-12-22', u'id': u'55c20fc3ebb7f94c833a99df', u'display_name': u'STV North', u'url': None}, {u'name': u'ITV Central HD', u'icon': u'https://utellyassets7.imgix.net/locations_icons/utelly/live_tv_square/50d352cef0ca9f5798001f29.jpg?w=92&auto=compress&app_version=0f692b6a-217b-4753-a78b-4351ba443607_2019-12-22', u'id': u'50d352cef0ca9f5798001f29', u'display_name': u'ITV Central HD', u'url': None}, {u'name': u'stv Central', u'icon': u'https://utellyassets7.imgix.net/locations_icons/utelly/live_tv_square/55c20fbcebb7f94c833a8e1a.jpg?w=92&auto=compress&app_version=0f692b6a-217b-4753-a78b-4351ba443607_2019-12-22', u'id': u'55c20fbcebb7f94c833a8e1a', u'display_name': u'stv Central', u'url': None}, {u'name': u'ITV London HD', u'icon': u'https://utellyassets7.imgix.net/locations_icons/utelly/live_tv_square/55c20fbeebb7f94c833a90a7.jpg?w=92&auto=compress&app_version=0f692b6a-217b-4753-a78b-4351ba443607_2019-12-22', u'id': u'55c20fbeebb7f94c833a90a7', u'display_name': u'ITV London HD', u'url': None}, {u'name': u'UTV', u'icon': u'https://utellyassets7.imgix.net/locations_icons/utelly/live_tv_square/5d42104d302b84002fc548e3.jpg?w=92&auto=compress&app_version=0f692b6a-217b-4753-a78b-4351ba443607_2019-12-22', u'id': u'5d42104d302b84002fc548e3', u'display_name': u'UTV', u'url': None}, {u'name': u'ITV Border', u'icon': u'https://utellyassets7.imgix.net/locations_icons/utelly/live_tv_square/50d352b3f0ca9f5798000b5c.jpg?w=92&auto=compress&app_version=0f692b6a-217b-4753-a78b-4351ba443607_2019-12-22', u'id': u'50d352b3f0ca9f5798000b5c', u'display_name': u'ITV Border', u'url': None}, {u'name': u'ITV Meridian', u'icon': u'https://utellyassets7.imgix.net/locations_icons/utelly/live_tv_square/55c20fbdebb7f94c833a8f92.jpg?w=92&auto=compress&app_version=0f692b6a-217b-4753-a78b-4351ba443607_2019-12-22', u'id': u'55c20fbdebb7f94c833a8f92', u'display_name': u'ITV Meridian', u'url': None}, {u'name': u'UTV HD', u'icon': u'https://utellyassets7.imgix.net/locations_icons/utelly/live_tv_square/55c20fc5ebb7f94c833a9db7.jpg?w=92&auto=compress&app_version=0f692b6a-217b-4753-a78b-4351ba443607_2019-12-22', u'id': u'55c20fc5ebb7f94c833a9db7', u'display_name': u'UTV HD', u'url': None}, {u'name': u'ITV Granada', u'icon': u'https://utellyassets7.imgix.net/locations_icons/utelly/live_tv_square/50d3530cf0ca9f5798004ec8.jpg?w=92&auto=compress&app_version=0f692b6a-217b-4753-a78b-4351ba443607_2019-12-22', u'id': u'50d3530cf0ca9f5798004ec8', u'display_name': u'ITV Granada', u'url': None}, {u'name': u'ITV +1', u'icon': u'https://utellyassets7.imgix.net/locations_icons/utelly/live_tv_square/5b1da126371559003e9874fd.jpg?w=92&auto=compress&app_version=0f692b6a-217b-4753-a78b-4351ba443607_2019-12-22', u'id': u'5b1da126371559003e9874fd', u'display_name': u'ITV +1', u'url': None}, {u'name': u'ITV Wales HD', u'icon': u'https://utellyassets7.imgix.net/locations_icons/utelly/live_tv_square/55c20fd1ebb7f94c833ab2ae.jpg?w=92&auto=compress&app_version=0f692b6a-217b-4753-a78b-4351ba443607_2019-12-22', u'id': u'55c20fd1ebb7f94c833ab2ae', u'display_name': u'ITV Wales HD', u'url': None}, {u'name': u'ITV South East +1', u'icon': u'https://utellyassets7.imgix.net/locations_icons/utelly/live_tv_square/55c20fc5ebb7f94c833a9df1.jpg?w=92&auto=compress&app_version=0f692b6a-217b-4753-a78b-4351ba443607_2019-12-22', u'id': u'55c20fc5ebb7f94c833a9df1', u'display_name': u'ITV South East +1', u'url': None}, {u'name': u'ITV London +1', u'icon': u'https://utellyassets7.imgix.net/locations_icons/utelly/live_tv_square/50d35326f0ca9f5798006224.jpg?w=92&auto=compress&app_version=0f692b6a-217b-4753-a78b-4351ba443607_2019-12-22', u'id': u'50d35326f0ca9f5798006224', u'display_name': u'ITV London +1', u'url': None}, {u'name': u'ITV Wales', u'icon': u'https://utellyassets7.imgix.net/locations_icons/utelly/live_tv_square/50d3538df0ca9f579800af27.jpg?w=92&auto=compress&app_version=0f692b6a-217b-4753-a78b-4351ba443607_2019-12-22', u'id': u'50d3538df0ca9f579800af27', u'display_name': u'ITV Wales', u'url': None}, {u'name': u'STV + 1 (Central)', u'icon': u'https://utellyassets7.imgix.net/locations_icons/utelly/live_tv_square/50d35300f0ca9f5798004539.jpg?w=92&auto=compress&app_version=0f692b6a-217b-4753-a78b-4351ba443607_2019-12-22', u'id': u'50d35300f0ca9f5798004539', u'display_name': u'STV + 1 (Central)', u'url': None}, {u'name': u'ITV Meridian HD', u'icon': u'https://utellyassets7.imgix.net/locations_icons/utelly/live_tv_square/55c20fc1ebb7f94c833a9665.jpg?w=92&auto=compress&app_version=0f692b6a-217b-4753-a78b-4351ba443607_2019-12-22', u'id': u'55c20fc1ebb7f94c833a9665', u'display_name': u'ITV Meridian HD', u'url': None}, {u'name': u'ITV Border Scotland', u'icon': u'https://utellyassets7.imgix.net/locations_icons/utelly/live_tv_square/5c5cb9ff302b84002f171284.jpg?w=92&auto=compress&app_version=0f692b6a-217b-4753-a78b-4351ba443607_2019-12-22', u'id': u'5c5cb9ff302b84002f171284', u'display_name': u'ITV Border Scotland', u'url': None}, {u'name': u'ITVPlayer', u'icon': u'https://utellyassets7.imgix.net/locations_icons/utelly/black_new/ITVPlayer.png?w=92&auto=compress&app_version=0f692b6a-217b-4753-a78b-4351ba443607_2019-12-22', u'id': u'524a7548f0ca9f60fe402581', u'display_name': u'ITV Hub', u'url': None}, {u'name': u'ITV Central +1', u'icon': u'https://utellyassets7.imgix.net/locations_icons/utelly/live_tv_square/50d352cdf0ca9f5798001ebf.jpg?w=92&auto=compress&app_version=0f692b6a-217b-4753-a78b-4351ba443607_2019-12-22', u'id': u'50d352cdf0ca9f5798001ebf', u'display_name': u'ITV Central +1', u'url': None}, {u'name': u'ITV West of England', u'icon': u'https://utellyassets7.imgix.net/locations_icons/utelly/live_tv_square/50d35319f0ca9f5798005869.jpg?w=92&auto=compress&app_version=0f692b6a-217b-4753-a78b-4351ba443607_2019-12-22', u'id': u'50d35319f0ca9f5798005869', u'display_name': u'ITV West of England', u'url': None}, {u'name': u'ITV Central', u'icon': u'https://utellyassets7.imgix.net/locations_icons/utelly/live_tv_square/55c20fc1ebb7f94c833a9671.jpg?w=92&auto=compress&app_version=0f692b6a-217b-4753-a78b-4351ba443607_2019-12-22', u'id': u'55c20fc1ebb7f94c833a9671', u'display_name': u'ITV Central', u'url': None}, {u'name': u'ITV West +1', u'icon': u'https://utellyassets7.imgix.net/locations_icons/utelly/live_tv_square/55c20fc7ebb7f94c833aa1f4.jpg?w=92&auto=compress&app_version=0f692b6a-217b-4753-a78b-4351ba443607_2019-12-22', u'id': u'55c20fc7ebb7f94c833aa1f4', u'display_name': u'ITV West +1', u'url': None}, {u'name': u'ITV Tyne Tees', u'icon': u'https://utellyassets7.imgix.net/locations_icons/utelly/live_tv_square/50d35380f0ca9f579800a586.jpg?w=92&auto=compress&app_version=0f692b6a-217b-4753-a78b-4351ba443607_2019-12-22', u'id': u'50d35380f0ca9f579800a586', u'display_name': u'ITV Tyne Tees', u'url': None}], u'weight': 9999, u'id': u'5dec4975302b8400573ee1ee', u'picture': None}, {u'name': u'Power Rangers Super Samurai', u'locations': [{u'name': u'Netflix', u'icon': u'https://utellyassets7.imgix.net/locations_icons/utelly/black_new/Netflix.png?w=92&auto=compress&app_version=0f692b6a-217b-4753-a78b-4351ba443607_2019-12-22', u'id': u'5270b96ff0ca9f2a3c17b4ef', u'display_name': u'Netflix', u'url': u'https://www.netflix.com/title/70221673'}], u'weight': 519, u'id': u'5762e6dbebb7f923a574052d', u'picture': u'https://utellyassets2-9.imgix.net/2/Open/Nickelodeon/Program/18995200/HS_template1X1_6_1572406935183_0.jpg?fit=crop&auto=compress&crop=faces,top'}, {u'name': u'Samurai Jack', u'locations': [{u'name': u'4onDemand', u'icon': u'https://utellyassets7.imgix.net/locations_icons/utelly/black_new/4onDemand.png?w=92&auto=compress&app_version=0f692b6a-217b-4753-a78b-4351ba443607_2019-12-22', u'id': u'524a7548f0ca9f60fe402583', u'display_name': u'All 4', u'url': u'http://www.channel4.com/programmes/samurai-jack/on-demand'}, {u'name': u'Amazon', u'icon': u'https://utellyassets7.imgix.net/locations_icons/utelly/black_new/Amazon.png?w=92&auto=compress&app_version=0f692b6a-217b-4753-a78b-4351ba443607_2019-12-22', u'id': u'531072c6f0ca9f1c439eb6cf', u'display_name': u'Amazon Prime', u'url': u'http://www.amazon.co.uk/gp/product/B071CM92BN?tag=utellycom00-21'}], u'weight': 440, u'id': u'57632b47d9ad0e15d5366db0', u'picture': u'https://utellyassets2-7.imgix.net/2/Open/Cartoon_Network_365/Program/29741729/_16by9/SamuraiJack_S5_HKA.jpg?fit=crop&auto=compress&crop=faces,top'}, {u'name': u'The Last Samurai', u'locations': [{u'name': u'Sky Cinema Action HD', u'icon': u'https://utellyassets7.imgix.net/locations_icons/utelly/live_tv_square/55c20fdfebb7f94c833acc08.jpg?w=92&auto=compress&app_version=0f692b6a-217b-4753-a78b-4351ba443607_2019-12-22', u'id': u'55c20fdfebb7f94c833acc08', u'display_name': u'Sky Cinema Action HD', u'url': None}, {u'name': u'WuakiTV', u'icon': u'https://utellyassets7.imgix.net/locations_icons/utelly/black_new/WuakiTV.png?w=92&auto=compress&app_version=0f692b6a-217b-4753-a78b-4351ba443607_2019-12-22', u'id': u'56c6edcba54d7559fe5028e1', u'display_name': u'Rakuten TV', u'url': u'https://uk.wuaki.tv/movies/the-last-samurai'}, {u'name': u'Sky Cinema Action', u'icon': u'https://utellyassets7.imgix.net/locations_icons/utelly/live_tv_square/55c20fdfebb7f94c833acc01.jpg?w=92&auto=compress&app_version=0f692b6a-217b-4753-a78b-4351ba443607_2019-12-22', u'id': u'55c20fdfebb7f94c833acc01', u'display_name': u'Sky Cinema Action', u'url': None}, {u'name': u'BlinkBox', u'icon': u'https://utellyassets7.imgix.net/locations_icons/utelly/black_new/BlinkBox.png?w=92&auto=compress&app_version=0f692b6a-217b-4753-a78b-4351ba443607_2019-12-22', u'id': u'5270b96ff0ca9f2a3c17b4f1', u'display_name': u'TalkTalk TV Store', u'url': u'https://www.talktalktvstore.co.uk/movies/the-last-samurai-(1290)'}, {u'name': u'Amazon', u'icon': u'https://utellyassets7.imgix.net/locations_icons/utelly/black_new/Amazon.png?w=92&auto=compress&app_version=0f692b6a-217b-4753-a78b-4351ba443607_2019-12-22', u'id': u'531072c6f0ca9f1c439eb6cf', u'display_name': u'Amazon Prime', u'url': u'http://www.amazon.co.uk/gp/product/B00I6VWCS8?tag=utellycom00-21'}, {u'name': u'NowTV', u'icon': u'https://utellyassets7.imgix.net/locations_icons/utelly/black_new/NowTV.png?w=92&auto=compress&app_version=0f692b6a-217b-4753-a78b-4351ba443607_2019-12-22', u'id': u'5270b96ff0ca9f2a3c17b4ee', u'display_name': u'Now TV', u'url': u'http://watch.nowtv.com/watch-movies/show-title/01fd14b71fcc3610VgnVCM1000000b43150a____'}], u'weight': 365, u'id': u'570d6895ebb7f950c14098f5', u'picture': u'https://utellyassets2-8.imgix.net/2/Open/Warner_Brothers_360/Program/4039020/_4by3/The%20Last%20Samurai_1%201key%20art.jpg?fit=crop&auto=compress&crop=faces,top'}, {u'name': u'Shameless', u'locations': [{u'name': u'GooglePlay', u'icon': u'https://utellyassets7.imgix.net/locations_icons/utelly/black_new/GooglePlay.png?w=92&auto=compress&app_version=0f692b6a-217b-4753-a78b-4351ba443607_2019-12-22', u'id': u'5523f21391072d0e23728ab9', u'display_name': u'Google Play', u'url': u'https://play.google.com/store/tv/show?id=qmN08xQ7J5U'}, {u'name': u'Amazon', u'icon': u'https://utellyassets7.imgix.net/locations_icons/utelly/black_new/Amazon.png?w=92&auto=compress&app_version=0f692b6a-217b-4753-a78b-4351ba443607_2019-12-22', u'id': u'531072c6f0ca9f1c439eb6cf', u'display_name': u'Amazon Prime', u'url': u'http://www.amazon.co.uk/gp/product/B00FZA5ZPU?tag=utellycom00-21'}], u'weight': 717, u'id': u'585e2b6cebb7f93f871ee568', u'picture': u'https://utellyassets2-8.imgix.net/2/Open/Showtime_Networks_41/Program/17307716/_2by1/17307716_Shameless_S9_KA1.jpg?fit=crop&auto=compress&crop=faces,top'}], u'term': u'sam'}
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

@app.route('/watchlist')
def watchlist():
    args["title"] = "My Watchlist"
    return displayPage('watchlist', False)

if __name__ == "__main__":
    app.run()
