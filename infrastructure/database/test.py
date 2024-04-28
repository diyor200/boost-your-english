import asyncio
import logging

from infrastructure.database.postgresql import Database
dsn = {"dsn": 'postgresql://postgres:2001@localhost:5432/postgres?sslmode=disable'}
db = Database(dsn)


async def test_get_all_books():
    try:
        # await db.create()

        books = await db.get_all_books()
        print(books)
    except Exception as e:
        print(e)
        logging.error(e)


async def main():
    await db.connect()
    await test_get_all_books()


if __name__ == '__main__':
    asyncio.run(main())
