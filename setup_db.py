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


def setup_database():
    # Создание базы данных, если она не существует
    cnx = mysql.connector.connect(user=db_config['user'],
                                       password=db_config['password'],
                                       host=db_config['host'],
                                       database='tasks_db')
    cursor = cnx.cursor()
    cursor.execute("CREATE DATABASE IF NOT EXISTS tasks_db")
    cursor.close()
    cnx.close()
    # Подключение к созданной базе данных и создание таблицы, если она не существует
    cnx = mysql.connector.connect(user=db_config['user'],
                                       password=db_config['password'],
                                       host=db_config['host'],
                                       database='tasks_db')
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
