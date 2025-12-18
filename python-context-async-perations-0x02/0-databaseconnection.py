import os
import mysql.connector
# from logger import logger
import logging
logger = logging.getLogger(__name__)


class DatabaseConnection:
    """
    Custom context manager to handle MYSQL DB connections.
    Opens the connection in __enter__ and closes it in __exit__.
    """

    def __init__(self, database="ALX_prodev"):
        self.database = database
        self.conn = None

    def __enter__(self):
        self.conn = mysql.connector.connect(
            host="db",
            user=os.getenv("MYSQL_USER"),
            password=os.getenv("MYSQL_PASSWORD"),
            database="ALX_prodev",
            port=3306
        )
        return self.conn
    
    def __exit__(self, exc_type, exc_value, traceback):
        if self.conn and self.conn.is_connected():
            self.conn.close()
        
create_table_sql = """
    CREATE TABLE IF NOT EXISTS users (
        user_id VARCHAR(36) PRIMARY KEY,
        name VARCHAR(100),
        email VARCHAR(100),
        age INT
    );
"""

insert_records_sql = """
    INSERT INTO users (user_id, name, email, age) VALUES (%s, %s, %s, %s)
"""

records = [
    ("00369a24-c017-4ed4-ac4d-31fc80f9a6ae", "Dustin Mayer",      "chidienew@ceot.com",             56),
    ("004e5d01-fd17-44ab-a1aa-d8c528c3ba01", "Robin Wilkinson",   "Brent_Wilkinson2@hotmail.com",   62),
    ("005e01c3-40c6-433f-a85d-595f51633cca", "Elbert Gutmann",    "Julius15@hotmail.com",           33),
    ("00baf98d-3823-4a85-b613-683191bb20b1", "Dr. Amos Swift Sr.", "Teri67@hotmail.com",             7),
    ("019fb8fa-deb6-4e48-8f07-63b93b3c8454", "Kim Pfeffer",       "Camille.Stanton48@yahoo.com",    None),
]

with DatabaseConnection() as conn:
    cursor = conn.cursor(dictionary=True)
    cursor.execute(create_table_sql)
    cursor.executemany(insert_records_sql, records)

    cursor.execute("SELECT * FROM users LIMIT 3;")
    results = cursor.fetchall()
    cursor.close()

    logger.info(f"Database Query Results For Users: {results}")