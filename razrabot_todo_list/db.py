import mysql.connector
from dotenv import load_dotenv
import os


load_dotenv()
user = os.getenv('DATABASE_USER')
password = os.getenv('DATABASE_PASSWORD')
host = os.getenv('DATABASE_HOST')


# Создаем декоратор, что бы избежать дублирования кода
def open_db(func):
    def wrapper(*args, **kwargs):
        conn = mysql.connector.connect(user=user, password=password,
                                       host=host, database='tasks_db')
        with conn:
            curs = conn.cursor(dictionary=True)
            result = func(curs, *args, **kwargs)
            conn.commit()
            return result
    return wrapper


@open_db
def get_tasks(curs):
    query = 'SELECT * FROM tasks'
    curs.execute(query)
    tasks = curs.fetchall()
    return tasks


@open_db
def insert_task(curs, title, description):
    query = 'INSERT INTO tasks (title, description) VALUES(%s, %s)'
    values = (title, description)
    curs.execute(query, values)
    task_id = curs.lastrowid
    curs.execute('SELECT * FROM tasks WHERE id = %s', (task_id,))
    task = curs.fetchone()
    return task


@open_db
def get_task_by_id(curs, id):
    curs.execute('SELECT * FROM tasks WHERE id = %s', (id,))
    task = curs.fetchone()
    return task


@open_db
def update_task_by_id(curs, id, title, description):
    query = 'UPDATE tasks SET title = %s, description = %s WHERE id = %s'
    curs.execute(query, (title, description, id))
    curs.execute('SELECT * FROM tasks WHERE id = %s', (id,))
    task = curs.fetchone()
    return task


@open_db
def del_task(curs, id):
    curs.execute('DELETE FROM tasks WHERE id = %s', (id,))
    return curs.rowcount > 0
