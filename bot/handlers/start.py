from aiogram import Router, F
from aiogram.filters import CommandStart, Command
from aiogram.types import Message
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from database.models import User
from keyboards.reply import main_menu

router = Router()


@router.message(CommandStart())
async def cmd_start(message: Message, session: AsyncSession):
    args = message.text.split()
    referrer_id = None
    if len(args) > 1:
        try:
            referrer_id = int(args[1])
        except ValueError:
            pass

    result = await session.execute(
        select(User).where(User.telegram_id == message.from_user.id)
    )
    user = result.scalar_one_or_none()

    if not user:
        user = User(
            telegram_id=message.from_user.id,
            username=message.from_user.username,
            full_name=message.from_user.full_name,
            referrer_id=referrer_id,
        )
        session.add(user)

        if referrer_id:
            result = await session.execute(
                select(User).where(User.telegram_id == referrer_id)
            )
            referrer = result.scalar_one_or_none()
            if referrer:
                referrer.referral_count += 1

        await session.commit()

        await message.answer(
            f"👋 Xush kelibsiz, {message.from_user.full_name}!\n\n"
            "📚 Kitob Do'koniga xush kelibsiz!",
            reply_markup=main_menu(),
        )
    else:
        await message.answer(
            f"👋 Qaytganingizdan xursandmiz, {message.from_user.full_name}!",
            reply_markup=main_menu(),
        )


@router.message(F.text == "🔙 Orqaga")
async def back_to_main(message: Message):
    await message.answer("🏠 Bosh menyu", reply_markup=main_menu())
