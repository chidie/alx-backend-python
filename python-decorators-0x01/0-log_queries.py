import os
import time
import functools
import mysql.connector
from datetime import datetime
import logging
logger = logging.getLogger(__name__)


def connect_db(retries=10, delay=5, database=None):
    for attempt in range(retries):
        try:
            logger.info("Connecting to the MySQL database...")

            conn_params = {
                "host": "db",
                "user": os.getenv("MYSQL_USER"),
                "password": os.getenv("MYSQL_PASSWORD"),
                "port": 3306
            }
            if database:
                conn_params["database"] = database

            connection = mysql.connector.connect(**conn_params)

            logger.info(
                "Successfully connected to MySQL"
                + (f" database '{database}'." if database else " (no default database).")
            )
            return connection

        except mysql.connector.Error as err:
            logger.error(f"Error connecting to the database: {err}")
            time.sleep(delay)

        finally:
            logger.info("Database connection attempt finished.")
    return None

def log_queries(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        query = kwargs.get("query")
        if query is None and len(args) > 0:
            query = args[0]
        result = func(*args, **kwargs)
        print(f"[LOG] Executing SQL Query: {query}")
        return result
    return wrapper

@log_queries
def fetch_all_users(query):
    db_connection = connect_db(database="ALX_prodev")
    cursor = db_connection.cursor()
    cursor.execute(query)
    results = cursor.fetchall()
    db_connection.close
    return results


if __name__ == "__main__":
    start_time = datetime.utcnow()
    users = fetch_all_users(query="SELECT * FROM user_data;")
    end_time = datetime.utcnow()
    logger.info(f"Query executed in: {(end_time - start_time).total_seconds()} seconds")
    logger.info(f"Users: ", users)

