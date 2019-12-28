import sys
sys.path.append("controllers")
sys.path.append("templates")

from flask import Flask, request, render_template
from google.appengine.api import taskqueue
import SearchController

app = Flask(__name__)

@app.route("/create_task", methods=["POST"])
def create_task():
        if "term" in request.form and "country" in request.form:
            if "result" in request.form:
                taskqueue.add(params={"term": request.form["term"], "country": request.form["country"], "result": request.form["result"]})
            elif "expired" in request.form:
                taskqueue.add(params={"term": request.form["term"], "country": request.form["country"], "expired": True})

@app.route("/_ah/queue/default", methods=["POST"])
def task_handler():
    if "term" in request.form and "country" in request.form:
        if "result" in request.form:
            search_result = SearchController.create_search_result(request.form["term"], request.form["country"], request.form["result"])
            if search_result:
                return render_template("views/task_result.html", result="create_success")
        elif "expired" in request.form:
            search_result = SearchController.delete_search_result(request.form["term"], request.form["country"])
            return render_template("views/task_result.html", result="delete_success")
    return render_template("views/task_result.html", result="fail")

if __name__ == "__main__":
    app.run()
