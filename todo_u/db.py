import sqlite3

DB_NAME = "todo.db"
TABLE_NAME = "tasks"
CREATE_TASK_TABLE = f"CREATE TABLE IF NOT EXISTS {TABLE_NAME}(id INTEGER PRIMARY KEY AUTOINCREMENT, content TEXT, done INTEGER DEFAULT false)"


def create_table():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute(CREATE_TASK_TABLE)
    conn.close()


def insert_task(task):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute(f"INSERT INTO {TABLE_NAME} (content) VALUES (?)", [task["content"]])
    task["id"] = cursor.lastrowid
    task["done"] = False
    conn.commit()
    conn.close()
    return task


def find_one(task_id):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM tasks WHERE id=?", [task_id])
    task = cursor.fetchone()
    conn.close()
    return task


def find_all():
    """
    DBから取得したすべての task をリストで返す
    :return:
    """
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute(f"SELECT * FROM {TABLE_NAME}")

    # タスクのリストを作成する
    tasks = []
    for row in cursor:
        # TODO task にid, content, done をセットする
        task = {"id": row[0], "content": row[1], "done": bool(row[2])}

        tasks.append(task)
    conn.close()
    return tasks


def update(task):
    print("変更前")
    task_id = task[0]
    find_one(task_id)

    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("UPDATE tasks SET done=? WHERE id=?", [1, task_id])
    conn.commit()
    conn.close()

    print("変更後")
    find_one(task_id)


def delete(task_id):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM tasks WHERE id=?", [task_id])
    conn.commit()
    conn.close()

# review
