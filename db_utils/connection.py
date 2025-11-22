import os
import time
import mysql.connector
from logger import logger

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