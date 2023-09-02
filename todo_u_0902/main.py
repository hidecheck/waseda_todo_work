from flask import Flask, abort, render_template, request

import db

app = Flask(__name__)

DB_NAME = db.DB_NAME
TABLE_NAME = db.TABLE_NAME
CREATE_TASK_TABLE = f"CREATE TABLE IF NOT EXISTS task (id INTEGER PRIMARY KEY AUTOINCREMENT, content TEXT, done INTEGER DEFAULT false, created_at TEXT)"


@app.route("/time")
def created_at():
    now = datetime.now()
    str_now = now.strftime("%Y/%m/%d %H:%M:%S")
    return render_template("time.html", now=str_now)


@app.route('/')
def home():
    message = 'ToDo List'
    return render_template('index.html', message=message)


@app.route('/abort500')
def abort500():
    abort(500)


@app.errorhandler(404)
def handle_404(exception):
    return {'message': 'Error: Resource not found.'}, 404


@app.errorhandler(500)
def handle_500(exception):
    return {'message': 'Please contact the administrator.'}, 500


@app.route('/api/tasks/<task_id>', methods=['GET', 'PUT', 'DELETE'])
@app.route('/api/tasks', methods=['GET', 'POST'])
def tasks(task_id=None):
    db.create_table()
    if request.method == 'GET':
        if task_id:
            # TODO これ
            task = db.find_one(task_id)
            return task

        else:
            # TODO これ
            tasks = db.find_all()
            res = {
                'tasks': tasks
            }
            return res

    elif request.method == 'POST':
        task = request.get_json()
        # TODO これ
        task = db.insert_task(task)
        return task, 201

    elif request.method == 'PUT':
        task = db.find_one(task_id)
        new_task = db.update(task_id)
        return new_task

    elif request.method == 'DELETE':
        # TODO これ
        db.delete(task_id)
        return "ok", 204


if __name__ == '__main__':
    app.run('127.0.0.1', port=8081, debug=True)
