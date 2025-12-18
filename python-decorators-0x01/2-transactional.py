import os
import time
import functools
import mysql.connector
import logging
logger = logging.getLogger(__name__)


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

@with_db_connection (database="ALX_prodev")
@transactional
def update_user_email(conn, user_id, new_email):
    """ Updates a user's email using safe parameterized SQL.
        Uses automatic connection management + transactions.
    """
    cursor = conn.cursor(dictionary=True)
    cursor.execute("UPDATE user_data SET email = %s where user_id = %s;", (new_email, user_id))
    cursor.execute("select * from user_data LIMIT 5")
    result = cursor.fetchall()
    cursor.close()
    return result


if __name__ == "__main__":
    updated_table = update_user_email(user_id='00369a24-c017-4ed4-ac4d-31fc80f9a6ae', new_email='ruthenewemail@ceot.com') # update_user_email = with_db_connection(transactional(update_user_email))
    logger.info(f"Updated user_date table: {updated_table}")