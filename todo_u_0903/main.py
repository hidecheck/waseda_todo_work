from flask import Flask, abort, render_template, request

import db

app = Flask(__name__)

DB_NAME = db.DB_NAME
TABLE_NAME = db.TABLE_NAME
CREATE_TASK_TABLE = f"CREATE TABLE IF NOT EXISTS task (id INTEGER PRIMARY KEY AUTOINCREMENT, content TEXT, done INTEGER DEFAULT false, created_at TEXT)"


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
@app.route('/api/tasks', methods=['GET', 'POST', 'DELETE'])
def tasks(task_id=None):
    if task_id and not task_id.isdigit():
        return "Invalid task_id", 400
    db.create_table()
    if request.method == 'GET':
        if task_id:
            return task

        else:
            tasks = db.find_all()
            res = {
                'tasks': tasks
            }
            return res

    elif request.method == 'POST':
        task = request.get_json()
        task = db.insert_task(task)
        return task, 201

    elif request.method == 'PUT':
        new_task = db.update(task_id)
        return new_task

    elif request.method == 'DELETE':
        if task_id:
            db.delete(task_id)
            return "ok", 204
    else:
        db.delete_all()
        return "All tasks deleted", 204


# 一括削除処理を追加する


if __name__ == '__main__':
    app.run('127.0.0.1', port=8081, debug=True)
