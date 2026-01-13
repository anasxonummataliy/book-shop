from typing import Callable, Dict, Any, Awaitable
from aiogram import BaseMiddleware
from aiogram.types import Message
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from database.models import User


class UserCheckMiddleware(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
        event: Message,
        data: Dict[str, Any],
    ) -> Any:
        session: AsyncSession = data.get("session")

        if session and event.from_user:
            result = await session.execute(
                select(User).where(User.telegram_id == event.from_user.id)
            )
            user = result.scalar_one_or_none()
            data["user"] = user

        return await handler(event, data)
