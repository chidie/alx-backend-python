import sqlite3
import asyncio
import aiosqlite
# from logger import logger


create_table_sql = """
CREATE TABLE IF NOT EXISTS users (
    user_id VARCHAR(36) PRIMARY KEY,
    name VARCHAR(100),
    email VARCHAR(100),
    age INT
);
"""

insert_records_sql = """
INSERT INTO users (user_id, name, email, age)
VALUES (?, ?, ?, ?)
"""
records = [
    ("00369a24-c017-4ed4-ac4d-31fc80f9a6ae", "Dustin Mayer",      "chidienew@ceot.com",             56),
    ("004e5d01-fd17-44ab-a1aa-d8c528c3ba01", "Robin Wilkinson",   "Brent_Wilkinson2@hotmail.com",   62),
    ("005e01c3-40c6-433f-a85d-595f51633cca", "Elbert Gutmann",    "Julius15@hotmail.com",           33),
    ("00baf98d-3823-4a85-b613-683191bb20b1", "Dr. Amos Swift Sr.", "Teri67@hotmail.com",             7),
    ("019fb8fa-deb6-4e48-8f07-63b93b3c8454", "Kim Pfeffer",       "Camille.Stanton48@yahoo.com",    23),
]


# cursor.executemany(insert_records_sql, records)
async def async_fetch_users(db_path="user_data.db"):
    """
    Fetch all users from the database asynchronously.
    """
    async with aiosqlite.connect(db_path) as db:
        cursor = await db.execute("SELECT * FROM users")
        rows = await cursor.fetchall()
        await cursor.close()
        return rows

async def async_fetch_older_users(db_path="user_data.db", age_limit=40):
    """
    Fetch users older than 40 asynchronously.
    """
    async with aiosqlite.connect(db_path) as db:
        cursor = await db.execute("SELECT * FROM users WHERE age > ?", (age_limit,))
        rows = await cursor.fetchall()
        await cursor.close()
        return rows

async def fetch_concurrently():
    """ Run both fet operations concurrently using asyncio.gather() """
    all_users_task = async_fetch_users()
    older_users_task = async_fetch_older_users()

    all_users, older_users = await asyncio.gather(
        all_users_task,
        older_users_task
    )

    print("\n=== ALL USERS ===")
    for user in all_users:
        print(user)
    
    print("\n=== USERS OLDER THAN 40 ===")
    for user in older_users:
        print(user)


if __name__ == "__main__":
    connection = sqlite3.connect('user_data.db')
    cursor = connection.cursor()

    cursor.execute(create_table_sql)
    connection.commit()
    print(f"Query executed successfully.")

    cursor.executemany(insert_records_sql, records)
    connection.commit()
    print("Records inserted successfully.")

    cursor.close()
    connection.close()

    asyncio.run(fetch_concurrently())