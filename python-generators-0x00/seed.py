import mysql.connector
from dotenv import load_dotenv
import os
import csv
import uuid
import time
import logging
logger = logging.getLogger(__name__)


load_dotenv()

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

def create_database(connection):
    cursor = connection.cursor()
    cursor.execute("CREATE DATABASE IF NOT EXISTS ALX_prodev;")
    connection.commit()
    cursor.close()

def connect_to_prodev():
    return mysql.connector.connect(
        host="db",
        user=os.getenv("MYSQL_USER"),
        password=os.getenv("MYSQL_PASSWORD"),
        database="ALX_prodev"
    )

def create_table(connection):
    cursor = connection.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS user_data (
            user_id CHAR(36) PRIMARY KEY,
            name VARCHAR(100) NOT NULL,
            email VARCHAR(100) NOT NULL UNIQUE,
            age INT NOT NULL,
            INDEX(user_id)
        );
    """)
    connection.commit()
    cursor.close()

def insert_data(connection, data):
    cursor = connection.cursor()
    for row_record in data:
        user_id = str(uuid.uuid4())
        name, email, age = row_record
        cursor.execute("""
            INSERT INTO user_data (user_id, name, email, age)
            VALUES (%s, %s, %s, %s)
        """, (user_id, name, email, age))
    connection.commit()
    cursor.close()

def main_seed():
    db_connection = connect_db()
    create_database(db_connection)
    logger.info("Database and table setup complete.")

    prodev_connection = connect_to_prodev() # Connect to the ALX_prodev database
    logger.info("Connected to ALX_prodev database.")
    create_table(prodev_connection)
    logger.info("Table creation complete.")

    file = 'user_data.csv'
    with open(file=file, newline='') as csvfile:
        data_reader = csv.reader(csvfile)
        next(data_reader)  # Skip header row
        data = [row for row in data_reader]
    
    insert_data(prodev_connection, data)
    logger.info("Data insertion complete.")
    prodev_connection.close()
    db_connection.close()
    

if __name__ == "__main__":
    main_seed()
