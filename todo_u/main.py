from flask import Flask
from flask import abort
from flask import render_template
from flask import request

import db

app = Flask(__name__)

DB_NAME = db.DB_NAME
TABLE_NAME = db.TABLE_NAME


@app.route("/")
def home():
    message = "ToDo List"
    return message


@app.route("/api/tasks/<task_id>", methods=["GET", "PUT", "DELETE"])
@app.route("/api/tasks", methods=["GET", "POST"])
def tasks(task_id=None):
    db.create_table()

    if request.method == "GET":
        if task_id:
            task = db.find_one(task_id)
            return task

        else:
            tasks = db.find_all()
            res = {"tasks": tasks}
            return res

    elif request.method == "POST":
        task = request.get_json()
        task = db.insert_task(task)
        return task, 201

    elif request.method == "PUT":
        db.update(task_id)
        new_task = db.find_one(task_id)
        return new_task

    elif request.method == "DELETE":
        db.delete(task_id)
        return "ok", 204


@app.route("/abort500")
def abort500():
    abort(500)


@app.errorhandler(404)
def handle_404(exception):
    return {"message": "Error: Resource not found."}, 404


@app.errorhandler(500)
def handle_500(exception):
    return {"message": "Please contact the administrator."}, 500


if __name__ == "__main__":
    app.run("127.0.0.1", port=8081, debug=True)

# review
