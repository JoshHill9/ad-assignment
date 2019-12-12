from flask import Flask, render_template
from google.appengine.api import users

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
    args["title"] = "About"
    args["active"] = "about"
    return displayPage("about")

@app.route("/login")
def login():
    args["active"] = "login"
    args["title"] = "Login"
    return displayPage("login")

@app.route("/register")
def register():
    args["active"] = "register"
    args["title"] = "Register"
    return displayPage("register")

if __name__ == "__main__":
    app.run(debug=True)