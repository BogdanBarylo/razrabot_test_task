import mysql.connector
from dotenv import load_dotenv
import os

load_dotenv()
user = os.getenv('DATABASE_USER')
password = os.getenv('DATABASE_PASSWORD')
host = os.getenv('DATABASE_HOST')


def setup_database():
    # Создание базы данных, если она не существует
    cnx = mysql.connector.connect(user=user, password=password, host=host)
    cursor = cnx.cursor()
    cursor.execute("CREATE DATABASE IF NOT EXISTS tasks_db")
    cursor.close()
    cnx.close()

    # Подключение к созданной базе данных и создание таблицы, если она не существует
    cnx = mysql.connector.connect(user=user, password=password, host=host, database='tasks_db')
    cursor = cnx.cursor()
    create_table_query = """
    CREATE TABLE IF NOT EXISTS tasks (
        id INT AUTO_INCREMENT PRIMARY KEY,
        title VARCHAR(255) NOT NULL,
        description VARCHAR(255),
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
    )
    """
    cursor.execute(create_table_query)
    cursor.close()
    cnx.close()
