import time
from typing import Any, Callable, Dict, Awaitable
from aiogram.types.user import User
from aiogram.enums import ChatMemberStatus
from aiogram.types.chat import Chat

from aiogram.types.chat_member_owner import ChatMemberOwner
from aiogram import BaseMiddleware
from aiogram.types import TelegramObject
from tgbot.config import Config


class CheckSubscription(BaseMiddleware):
    def __init__(self, channel: int):
        self.channel = channel

    async def __call__(
            self, handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
            event: TelegramObject,
            data: Dict[str, Any]):
        user_id: int = data["event_from_user"].id
        member = await event.bot.get_chat_member(user_id=user_id, chat_id=self.channel)
        if not (member.status == "member" or "creator" or "administrator"):
            return await event.bot.send_message(chat_id=user_id,
                                                text="Botdan foydalanish uchun quyidagi kanallarga a'zo bo'ling:"
                                                     "https://t.me/cyberdefine")

        return await handler(event, data)
