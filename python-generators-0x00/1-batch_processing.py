from seed import connect_db
from logger import logger

connection = connect_db(database="ALX_prodev")

def stream_users_in_batches():
    """Generator that yields users from the database in batches."""
    batch_size = 10
    offset = 0
    cursor = connection.cursor(dictionary=True)

    while True:
        cursor.execute("SELECT * FROM user_data LIMIT %s OFFSET %s;", (batch_size, offset))
        rows = cursor.fetchall()
        if not rows:
            logger.info("No more users to fetch.")
            break
        yield rows
        offset += batch_size

    cursor.close()

def batch_processing():
    """Process users in batches."""
    batch_number = 0
    if not connection:
        logger.error("Failed to connect to the database for batch processing.")
        return
    
    for batch in stream_users_in_batches():
        logger.info(f"Processing batch {batch_number} with {len(batch)} users.")
        for user in batch:
            if user['age'] > 25:
                yield user
        batch_number += 1

def main():
    for user in batch_processing():
        logger.info(f"User over the age of 25: {user}")

if __name__ == "__main__":
    main()