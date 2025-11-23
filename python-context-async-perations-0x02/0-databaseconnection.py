import os
import mysql.connector
from logger import logger


class DatabaseConnection:
    """
    Custom context manager to handle MYSQL DB connections.
    Opens the connection in __enter__ and closes it in __exit__.
    """

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
        

with DatabaseConnection() as conn:
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM user_data LIMIT 10;")
    results = cursor.fetchall()
    cursor.close()

    logger.info(f"Database Query Results: {results}")