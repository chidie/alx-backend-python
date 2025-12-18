from seed import main_seed, connect_db
import logging
logger = logging.getLogger(__name__)

def should_seed(connection):
    cursor = connection.cursor()
    cursor.execute("""
        SELECT COUNT(*)
        FROM information_schema.tables
        WHERE table_schema = 'ALX_prodev'
        AND table_name = 'user_data';
    """)
    table_exists = cursor.fetchone()[0] == 1

    if not table_exists:
        cursor.close()
        return True  # Should seed because the table does not exist
    return False  # Table exists, assume it's seeded

def stream_users():
    connection = connect_db(database="ALX_prodev")
    logger.info("Streaming users from the database...")
    cursor = connection.cursor(dictionary=True)
    cursor.execute("SELECT * FROM user_data;")
    for row in cursor:
        logger.info(f"Yielding user: {row}")
        yield row

def main():
    connection = connect_db()
    logger.info("Starting to stream users from the database...")

    if connection is None:
        logger.error("Failed to connect to the database.")
        return
    
    seed_needed = should_seed(connection)
    logger.info(f"Connected to the database successfully. Seeding required: {seed_needed}")
    
    if seed_needed:
        logger.info("Seeding the database as it is not yet seeded.")
        main_seed()
        logger.info("Database seeding complete.")
        connection.close()
    else:
        logger.info("Database already seeded. Skipping seeding step to stream users from user_data...")
        for user in stream_users():
            logger.info(f"User: {user}")
        logger.info("Finished streaming users from the database.")
    connection.close()
    


if __name__ == "__main__":
    main()