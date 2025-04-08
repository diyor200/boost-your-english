import asyncio
import logging
import sys
from datetime import datetime

import betterlogging as bl

from aiogram import Dispatcher, Bot, types
from aiogram.client.session.aiohttp import AiohttpSession
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.fsm.storage.redis import RedisStorage, DefaultKeyBuilder
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode

from fastapi import FastAPI
from pydantic import BaseModel

import infrastructure.database.postgresql
from tgbot.config import Config
from tgbot.handlers import routers_list
from tgbot.loader import db, config
from tgbot.middlewares.config import ConfigMiddleware
from tgbot.services import broadcaster


async def on_startup(bot: Bot, db: infrastructure.database.postgresql.Database, admin_ids: list[int]):
    try:
        await db.create()
    except:
        await broadcaster.broadcast(bot, admin_ids, "can't create tables. Program is stopping.....")
        logging.error("can't create tables. Program is stopping.....")
        sys.exit(1)

    await broadcaster.broadcast(bot, admin_ids, "Bot ishga tushdi")


def register_global_middlewares(dp: Dispatcher, cfg: Config, session_pool=None):
    middleware_types = [
        # CheckSubscription(config.tg_bot.channels[0]),
        ConfigMiddleware(cfg),
        # DatabaseMiddleware(session_pool),

    ]
    """
    Register global middlewares for the given dispatcher.
    Global middlewares here are the ones that are applied to all the handlers (you specify the type of update)

    :param dp: The dispatcher instance.
    :type dp: Dispatcher
    :param config: The configuration object from the loaded configuration.
    :param session_pool: Optional session pool object for the database using SQLAlchemy.
    :return: None
    """

    for middleware_type in middleware_types:
        dp.message.outer_middleware(middleware_type)
        dp.callback_query.outer_middleware(middleware_type)


def setup_logging():
    """
    Set up logging configuration for the application.

    This method initializes the logging configuration for the application.
    It sets the log level to INFO and configures a basic colorized log for
    output. The log format includes the filename, line number, log level,
    timestamp, logger name, and log message.

    Returns:
        None

    Example usage:
        setup_logging()
    """
    log_level = logging.INFO
    bl.basic_colorized_config(level=log_level)

    logging.basicConfig(
        level=logging.INFO,
        format="%(filename)s:%(lineno)d #%(levelname)-8s [%(asctime)s] - %(name)s - %(message)s",
    )
    logger = logging.getLogger(__name__)
    logger.info("Starting bot")


def get_storage(config):
    """
    Return storage based on the provided configuration.

    Args:
        config (Config): The configuration object.

    Returns:
        Storage: The storage object based on the configuration.

    """
    if config.tg_bot.use_redis:
        return RedisStorage.from_url(
            config.redis.dsn(),
            key_builder=DefaultKeyBuilder(with_bot_id=True, with_destiny=True),
        )
    else:
        return MemoryStorage()

session = AiohttpSession(proxy="http://172.25.113.50:8085")

setup_logging()
storage = get_storage(config)
dp = Dispatcher(storage=storage)
dp.include_routers(*routers_list)
register_global_middlewares(dp, config)


async def main():
     bot = Bot(token=config.tg_bot.token, default=DefaultBotProperties(parse_mode=ParseMode.HTML), session=session)
     if await bot.get_webhook_info():
         await bot.delete_webhook()

     await on_startup(bot, db, config.tg_bot.admin_ids)
     await dp.start_polling(bot)

if __name__ == "__main__":
     try:
         asyncio.run(main())
     except (KeyboardInterrupt, SystemExit):
         logging.error("bot o'chdi!")
