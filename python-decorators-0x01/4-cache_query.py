import os
import time
import functools
import mysql.connector
import logging
logger = logging.getLogger(__name__)

query_cache = {}

def cache_query(func):
    """
    Caches results of SQL queries.
    Cache key = the query string passed to the function.
    """
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        query = kwargs.get("query")

        if query in query_cache:
            logger.info("[CACHE] Returning cached result for query")
            return query_cache[query]
        
        result = func(*args, **kwargs)
        query_cache[query] = result
        logger.info("[CACHE] Query result stored in cache")
        return result
    return wrapper

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

@with_db_connection(database="ALX_prodev")
@cache_query
def fetch_users_with_cache(conn, query):
    cursor = conn.cursor(dictionary=True)
    cursor.execute(query)
    result = cursor.fetchall()
    cursor.close()
    return result


if __name__ == "__main__":
    users = fetch_users_with_cache(query="SELECT * FROM user_data LIMIT 5;")    # First call -> query runs and caches it
    users_again = fetch_users_with_cache(query="SELECT * FROM user_data LIMIT 6;")
    logger.info(f"Display batch1: {users}")
    logger.info(f"Display batch2: {users_again}")