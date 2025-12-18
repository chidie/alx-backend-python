import functools
import os
import time
import mysql.connector
import logging
logger = logging.getLogger(__name__)


def connect_db(database="ALX_prodev", retries=10, delay=5):
    """Decorator that injects a MySQL connection into the wrapped function"""
    
    def decorator(func):

        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            connection = None

            for attempt in range(retries):
                try:
                    logger.info(f"[Attempt {attempt+1}/{retries}] Connecting to MySQL...")

                    conn_params = {
                        "host": "db",
                        "user": os.getenv("MYSQL_USER"),
                        "password": os.getenv("MYSQL_PASSWORD"),
                        "port": 3306
                    }

                    if database:
                        conn_params["database"] = database

                    connection = mysql.connector.connect(**conn_params)
                    
                    logger.info(f"Connected to MySQL database '{database}'")
                    break
            
                except mysql.connector.Error as err:
                    logger.error(f"Connection failed: {err}")
                    time.sleep(delay)

            if not connection:
                logger.error("Failed to connect after all retries.")
                return None
            
            try:
                return func(connection, *args, **kwargs)

            finally:
                if connection.is_connected():
                    connection.close()
                    logger.info("Database connection closed.")

        return wrapper
    
    return decorator

@connect_db(database="ALX_prodev")
def fetch_users(conn):
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM user_data;")
    result = cursor.fetchall()
    cursor.close()
    return result


if __name__ == "__main__":
    users = fetch_users()
    logger.info(f"Users retrieved by decorators: {users}")