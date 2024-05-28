import mysql.connector
from dotenv import load_dotenv
import os
from urllib.parse import urlparse


load_dotenv()
url = urlparse(os.getenv('DATABASE_URL'))
db_config = {
    'user': url.username,
    'password': url.password,
    'host': url.hostname,
    'database': url.path[1:],
    'port': url.port
}


# Создаем декоратор, что бы избежать дублирования кода
def open_db(func):
    def wrapper(*args, **kwargs):
        conn = mysql.connector.connect(user=db_config['user'],
                                       password=db_config['password'],
                                       host=db_config['host'],
                                       database='tasks_db')
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
    curs.execute('SELECT * FROM tasks WHERE id = %s', (id,))
    task = curs.fetchone()
    if task:
        curs.execute('DELETE FROM tasks WHERE id = %s', (id,))
        return True
    return False

# Для использования в тестах
@open_db
def clear_db(curs):
    curs.execute('TRUNCATE TABLE tasks')
