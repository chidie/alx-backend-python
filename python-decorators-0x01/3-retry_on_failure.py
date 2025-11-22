import os
import time
import functools
import mysql.connector
from logger import logger


def with_db_connection(database="ALX_prodev", retries=10, delay=5):
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

def transactional(func):
    """Decorator to wrap DB operations inside a transaction"""

    @functools.wraps(func)
    def wrapper(conn, *args, **kwargs):
        try:
            result = func(conn, *args, **kwargs)
            conn.commit()
            logger.info("Transaction committed successfully.")
            return result
        except Exception as e:
            logger.error(f"Error occurred in {func.__name__}(). Rolling back...")
            conn.rollback()
            raise e
    return wrapper

def retry_on_failure(retries=3, delay=2):
    """Retry a function multiple times if it fails"""
    def decorator(func):

        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            last_exception = None

            for attempt in range(1, retries + 1):
                try:
                    logger.info(f"[Retry {attempt}/{retries}] Running {func.__name__}()...")
                    return func(*args, **kwargs)
                except Exception as e:
                    logger.error(
                        f"{func.__name__} failed on attempt {attempt}."
                        f"Error: {e}. Retrying in {delay}s..."
                    )
                    last_exception = e
                    time.sleep(delay)

            logger.error(f"{func.__name__} failed after {retries} attempts.")
            raise last_exception
        return wrapper
    return decorator

@with_db_connection (database="ALX_prodev")
@retry_on_failure(retries=3, delay=1)
def fetch_users_with_retry(conn):
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM user_data LIMIT 5;")
    result = cursor.fetchall()
    cursor.close()
    return result


if __name__ == "__main__":
    user_data_table = fetch_users_with_retry()
    logger.info(f"Fetched user data: {user_data_table}")