from typing import Union
import logging
import sys

import asyncpg
from asyncpg import Connection
from asyncpg.pool import Pool

from tgbot.data import config


class Database:
    def __init__(self):
        self.pool: Union[Pool, None]

    async def close(self):
        await self.pool.close()

    async def create(self):
        try:
            self.pool = await asyncpg.create_pool(
                user=config.DB_USER,
                password=config.DB_PASS,
                host=config.DB_HOST,
                database=config.DB_NAME,
            )
        except:
            logging.error("can't connect to database")
            sys.exit(1)

    async def execute(self, command, *args,
                      fetch: bool = False,
                      fetchval: bool = False,
                      fetchrow: bool = False,
                      execute: bool = False
                      ):
        async with self.pool.acquire() as connection:
            connection: Connection
            async with connection.transaction():
                if fetch:
                    result = await connection.fetch(command, *args)
                elif fetchval:
                    result = await connection.fetchval(command, *args)
                elif fetchrow:
                    result = await connection.fetchrow(command, *args)
                elif execute:
                    result = await connection.execute(command, *args)
            return result

    async def create_table_users(self):
        sql = """
        create table if not exists users(
    id serial primary key,
    telegram_id varchar(25) unique not null,
    username varchar(255) ,
    name varchar(255),
    invited_by int default 0,
    created_at timestamp default now()
    );

create table if not exists books(
    id serial primary key,
    name varchar(255) not null ,
    created_at timestamp default now()
    );

create table if not exists tests(
    id serial primary key,
    book_id int references books(id) not null,
    number int not null ,
    created_at timestamp default now()
    );

create table if not exists passages(
    id serial primary key,
    test_id int references tests(id) not null,
    number int not null,
    created_at timestamp default now()
   );

create table if not exists vocabulary(
    id serial primary key ,
    passage_id int references passages(id) not null ,
    word varchar(255) not null ,
    definition varchar(500),
    translation varchar(500) not null,
    created_at timestamp default now()
);

create table if not exists test_source(
    id serial primary key ,
    book_id int references books(id),
    test_id int references tests(id),
    passage_id int references passages(id),
    word_id int references vocabulary(id),
    created_at timestamp default now()
);

create table if not exists test(
    id serial primary key ,
    source_id int references test_source(id),
    user_id int references users(id),
    created_at timestamp default now()
);

create table if not exists test_results(
    id serial primary key ,
    user_id int references users(id),
    test_id int references test(id),
    score int not null ,
    created_at timestamp default now()
)
        """
        await self.execute(sql, execute=True)

    @staticmethod
    def format_args(sql, parameters: dict):
        sql += " AND ".join([
            f"{item} = ${num}" for num, item in enumerate(parameters.keys(),
                                                          start=1)
        ])
        return sql, tuple(parameters.values())

    # book
    async def add_book(self, name):
        sql = ("INSERT INTO books(name, created_at)"
               " VALUES($1 date_trunc('minute', NOW() AT TIME ZONE 'Asia/Tashkent'))")
        return await self.execute(sql, name, execute=True)

    async def get_all_books(self):
        return await self.execute("select name from books", fetch=True)

    #  book's tests
    async def add_book_test(self, name, book):
        sql = ("insert into tests(book_id, number, created_at) values ((select id from books where name=$1), $2,"
               " date_trunc('minute', NOW() AT TIME ZONE 'Asia/Tashkent'))")
        return await self.execute(sql, name, book, execute=True)

    async def get_book_tests(self):
        return await self.execute("select number from tests where book_id=(select id from books where name=$1);", fetch=True)

    #  book's tests
    async def add_book_test(self, name, book):
        sql = ("insert into tests(book_id, number, created_at) values ((select id from books where name=$1), $2,"
               " date_trunc('minute', NOW() AT TIME ZONE 'Asia/Tashkent'))")
        return await self.execute(sql, name, book, execute=True)

    async def get_book_tests(self):
        return await self.execute("select number from tests where book_id=(select id from books where name=$1);",
                                  fetch=True)

    # users
    async def add_user(self, name, username, telegram_id):
        sql = ("INSERT INTO users (name, username, telegram_id, created_at) VALUES($1, $2, $3,"
               " date_trunc('minute', NOW() AT TIME ZONE 'Asia/Tashkent'))")
        return await self.execute(sql, name, username, telegram_id, execute=True)

    async def select_all_users(self):
        sql = "SELECT * FROM users"
        return await self.execute(sql, fetch=True)

    async def select_user(self, **kwargs):
        sql = "SELECT * FROM users WHERE "
        sql, parameters = self.format_args(sql, parameters=kwargs)
        return await self.execute(sql, *parameters, fetchrow=True)

    async def count_users(self):
        sql = "SELECT COUNT(*) FROM Users"
        return await self.execute(sql, fetchval=True)

    async def update_user_username(self, username, telegram_id):
        sql = "UPDATE Users SET username=$1 WHERE telegram_id=$2"
        return await self.execute(sql, username, telegram_id, execute=True)

    async def delete_users(self):
        await self.execute("DELETE FROM Users WHERE TRUE", execute=True)
