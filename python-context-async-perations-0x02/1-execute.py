import os 
import mysql.connector
# from logger import logger
import logging
logger = logging.getLogger(__name__)


class ExecuteQuery:
    """
    Context manager that:
    - Opens a MySQL connection on __enter__
    - Executes a given query with optional parameters
    - Returns the results
    - Closes the connection automatically safely on __exit__
    - Rolls back if an exception occurs 
    """

    def __init__(self, query, params=None, database="ALX_prodev"):
        self.query = query
        self.params = params
        self.database = database
        self.conn = None
        self.results = None
    
    def __enter__(self):
        self.conn = mysql.connector.connect(
            host="db",
            user=os.getenv("MYSQL_USER"),
            password=os.getenv("MYSQL_PASSWORD"),
            database=self.database,
            port=3306
        )

        try:
            cursor = self.conn.cursor(dictionary=True)
            cursor.execute(self.query, self.params)
            logger.info(f"CURSOR HAS ROWS STATUS: {cursor.with_rows}")

            if cursor.with_rows:
                self.results = cursor.fetchall()
            else:
                self.conn.commit()
                self.results = None
        except Exception as e:
            if self.conn:
                self.conn.rollback()
            logger.error(f"Error executing query: {e}")
        finally:
            cursor.close()
        return self.results
    
    def __exit__(self, exc_type, exc_value, traceback):
        if self.conn and self.conn.is_connected():
            self.conn.close()
        
        return False


insert_query = """
    INSERT INTO users (user_id, name, email, age)
    SELECT user_id, name, email, age
    FROM user_data;
"""

with ExecuteQuery(insert_query) as _:
    logger.info("Inserted data from user_data into users table.")


# Query users older than 25
select_query = "SELECT * FROM users WHERE age > %s"
params = (25,)

with ExecuteQuery(select_query, params) as results:
    logger.info(f"Users older than 25: {results}")


