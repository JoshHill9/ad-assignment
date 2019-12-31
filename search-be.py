import sys
sys.path.append("controllers")
sys.path.append("templates")

from flask import Flask, request, render_template
from google.appengine.api import taskqueue
import SearchResultController, SearchValidatorController

app = Flask(__name__)

@app.route("/create_task", methods=["POST"])
def create_task():
    if "term" in request.form and "country" in request.form:
        term = request.form["term"]
        country = request.form["country"]
        if "csrf" in request.form:
            # Validates request source is from web-fe.py Search Form
            if SearchValidatorController.validate_token(term, country, request.form["csrf"]):
                if "result" in request.form:
                    # Queues Task to store Search Result data in Datastore
                    taskqueue.add(params={"term": request.form["term"], "country": request.form["country"], "result": request.form["result"]})
                elif "expired" in request.form:
                    # Queues Task to delete expired Search Result data and re-store updated data
                    taskqueue.add(params={"term": request.form["term"], "country": request.form["country"], "expired": True, "new_result": request.form["new_result"]})
                # Removes validator Entity from Datastore for security reasons
                SearchValidatorController.delete_validator(term, country)
                return render_template("views/task_result.html", result="form_validated")
            return render_template("views/task_result.html", result="form_invalid")
    return render_template("views/task_result.html", result="request_invalid")

@app.route("/_ah/queue/default", methods=["POST"])
def task_handler():
    if "term" in request.form and "country" in request.form:
        if "result" in request.form:
            search_result = SearchResultController.create_search_result(request.form["term"], request.form["country"], request.form["result"])
            if search_result:
                return render_template("views/task_result.html", result="create_success")
        elif "expired" in request.form:
            search_result = SearchResultController.delete_search_result(request.form["term"], request.form["country"])
            new_result = SearchResultController.create_search_result(request.form["term"], request.form["country"], request.form["new_result"])
            return render_template("views/task_result.html", result="delete_success")
    return render_template("views/task_result.html", result="fail")

if __name__ == "__main__":
    app.run()
