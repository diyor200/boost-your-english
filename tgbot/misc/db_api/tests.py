import asyncio

from infrastructure.database.postgresql import Database


async def test():
    db = Database()
    await db.create()
    print()


asyncio.run(test())

# import re

# phone_regex = '^\+998\d{9}$'
# phone_number = '+998908394393'
# match = bool(re.match(phone_regex, phone_number))

# try:
#     int(phone_regex)
#     print(int(phone_number))
#     print("intakan bu")
# except:
#     print("int emas")
# print(match)
