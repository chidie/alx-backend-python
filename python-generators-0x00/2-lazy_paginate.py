from seed import connect_db
import logging
logger = logging.getLogger(__name__)

connection = connect_db(database="ALX_prodev")

def paginate_users(page_size, offset):
    """Fetch a page of users from the database."""
    cursor = connection.cursor(dictionary=True)
    cursor.execute("SELECT * FROM user_data LIMIT %s OFFSET %s;", (page_size, offset))
    rows = cursor.fetchall()
    cursor.close()
    return rows

def lazy_paginate(page_size):
    """Generator that yields users from the database lazily in pages."""
    if not connection:
        logger.error("Failed to connect to the database for pagination.")
        return
    
    offset = 0
    while True:
        page = paginate_users(page_size, offset)
        if not page:
            logger.info("No more users to fetch.")
            break
        
        yield page
        offset += page_size
    
    connection.close()

def main():
    page_number = 0
    for page in lazy_paginate(page_size=20):
        logger.info(f"Processing page {page_number} with {len(page)} users.")
        for user in page:
            logger.info(f"User: {user}")
        
        page_number += 1


if __name__ == "__main__":
    main()