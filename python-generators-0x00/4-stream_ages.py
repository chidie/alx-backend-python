from seed import connect_db
import logging
logger = logging.getLogger(__name__)

connection = connect_db(database="ALX_prodev")

def stream_user_ages():
    """Generator that yields user ages from the database."""
    if not connection:
        logger.error("Failed to connect to the database for streaming ages.")
        return
    
    cursor = connection.cursor(dictionary=True)
    cursor.execute("SELECT age FROM user_data;")
    for row in cursor:
        logger.info(f"Yielding age: {row['age']}")
        yield row['age']
    
    cursor.close()
    connection.close()

def calculate_average_age():
    """Calculate the average age of users in the database."""
    total_age = 0
    number_of_users = 0
    for age in stream_user_ages():
        total_age += age
        number_of_users += 1
    
    average_age = total_age / number_of_users if number_of_users > 0 else 0
    return average_age

def main():
    logger.info("Starting to calculate average age of users...")
    average_age = calculate_average_age()
    logger.info(f"Average age of users: {average_age}")


if __name__ == "__main__":
    main()