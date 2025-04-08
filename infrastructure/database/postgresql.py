from typing import Union
import logging
import sys

import asyncpg
from asyncpg import Connection
from asyncpg.pool import Pool
from asyncpg import create_pool

from tgbot.data import config


class Database:
    def __init__(self):
        try:
            self.pool = asyncpg.create_pool(
                user="postgres",
                password="2001",
                host="localhost",
                database="postgres",
            )
        except Exception as e:
            logging.error("can't connect to database", e)
            sys.exit(1)

    async def close(self):
        await self.pool.close()

    async def create(self):
        try:
            self.pool = await asyncpg.create_pool(
                user="postgres",
                password="postgres",
                host="localhost",
                database="boost_your_russian",
            )
        except Exception as e:
            logging.error("can't connect to database", e)
            await self.pool.close()
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

    async def create_tables(self):
        sql = """
            create table if not exists users(
                id serial primary key,
                telegram_id varchar(25) unique not null,
                username varchar(255) ,
                name varchar(255),
                invited_by int default 0,
                created_at timestamp not null default date_trunc('minute', NOW() AT TIME ZONE 'Asia/Tashkent')
            );

            create table if not exists categories(
                id serial primary key ,
                name varchar(255) not null ,
                created_at timestamp not null default date_trunc('minute', NOW() AT TIME ZONE 'Asia/Tashkent')
            );
            
            create table if not exists vocabularies(
                id serial primary key ,
                category_id int references categories(id) not null ,
                word varchar(400) not null ,
                translation varchar(400) not null ,
                created_at timestamp not null default date_trunc('minute', NOW() AT TIME ZONE 'Asia/Tashkent')
            );
        """
        await self.execute(sql, execute=True)

    @staticmethod
    def format_args(sql, parameters: dict):
        sql += " AND ".join([
            f"{item} = ${num}" for num, item in enumerate(parameters.keys(),
                                                          start=1)
        ])
        return sql, tuple(parameters.values())

    # vocabulary
    async def add_word_by_category_id(self, category_id: int, word: str, translation: str):
        sql = "insert into vocabularies(category_id, word, translation) values ($1, $2, $3) returning id"
        await self.execute(sql, category_id, word, translation, fetch=True)

    async def get_all_vocabularies_by_category_id(self, category_id: int):
        sql = "select * from vocabularies where category_id = $1"
        return await self.execute(sql, category_id, fetch=True)

    async def get_vocabularies_count_by_category_id(self, category_id: int):
        sql = "select count(id) from vocabularies where category_id = $1"
        return await self.execute(sql, category_id, fetchrow=True)

    async def get_vocabularies_by_category_id_and_limits(self, category_id: int, limit: int, offset: int):
        sql = "select * from vocabularies where category_id = $1 limit $2 offset $3"
        return await self.execute(sql, category_id, limit, offset, fetch=True)

   # categories
    async def add_category(self, name: str) -> int:
        sql = "insert into categories(name) values ($1) returning id"
        return await self.execute(sql, name, fetchrow=True)

    async def get_all_categories(self):
        sql = "SELECT * FROM categories"
        return await self.execute(sql,fetch=True)

    async def get_category_id_by_name(self, category_name: str):
        sql = "select id from categories where name = $1"
        return await self.execute(sql, category_name, fetchrow=True)

    # users
    async def add_user(self, name, username, telegram_id):
        sql = ("INSERT INTO users(name, username, telegram_id, created_at) VALUES($1, $2, $3,"
               " date_trunc('minute', NOW() AT TIME ZONE 'Asia/Tashkent'))")
        return await self.execute(sql, name, username, telegram_id, execute=True)

    async def select_all_users(self):
        sql = "SELECT * FROM users"
        return await self.execute(sql, fetch=True)

    async def select_user(self, **kwargs):
        sql = "SELECT * FROM users WHERE "
        sql, parameters = self.format_args(sql, parameters=kwargs)
        return await self.execute(sql, *parameters, fetchrow=True)

    async def update_user_username(self, username, telegram_id):
        sql = "UPDATE users SET username=$1 WHERE telegram_id=$2"
        return await self.execute(sql, username, telegram_id, execute=True)
