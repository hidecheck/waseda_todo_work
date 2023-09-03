import logging
import sqlite3
from datetime import datetime

DB_NAME = 'todo.db'
TABLE_NAME = "tasks"
CREATE_TASK_TABLE = f"CREATE TABLE IF NOT EXISTS {TABLE_NAME}(id INTEGER PRIMARY KEY AUTOINCREMENT, content TEXT, done INTEGER DEFAULT false, created_at TEXT)"


def create_table():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute(CREATE_TASK_TABLE)
    conn.close()


def insert_task(task):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    now = datetime.now()
    task["created_at"] = now.strftime("%Y/%m/%d %H:%M:%S")
    cursor.execute(f"INSERT INTO {TABLE_NAME} (content, done, created_at) VALUES (?, ?, ?)",
                   (task["content"], task["done"], task["created_at"]))
    task["id"] = cursor.lastrowid
    task["done"] = False
    conn.commit()
    conn.close()
    return task


def find_one(id):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM tasks WHERE id=?", [id])
    row = cursor.fetchone()
    task = {
        "id": row[0],
        "content": row[1],
        "done": bool(row[2]),
        "created_at": row[3]
    }
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
        task = {
            "id": row[0],
            "content": row[1],
            "done": bool(row[2]),
            "created_at": row[3]

        }

        tasks.append(task)
    conn.close()
    return tasks


def update(task_id):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("UPDATE tasks SET done=? WHERE id=?", [1, id])
    conn.commit()
    conn.close()

    new_task = find_one(task_id)
    return new_task


def delete(task_id):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM tasks WHERE id=?", [task_id])
    conn.commit()
    conn.close()


def delete_all():
    conn = None
    try:
        conn = sqlite3.connect('todo.db')
        cursor = conn.cursor()
        cursor.execute("DELETE FROM tasks")
        conn.commit()
        logging.info("削除が成功しました。")
        return True
    except Exception as e:
        logging.info("削除中にエラーが発生しました。")
        return False
    finally:
        if conn:
            conn.close()