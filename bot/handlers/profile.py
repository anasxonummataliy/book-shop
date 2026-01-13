from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from database.models import User
from keyboards.reply import main_menu, back_button
from keyboards.inline import referral_button

router = Router()


@router.message(F.text == "👤 Profil")
async def show_profile(message: Message, session: AsyncSession, bot):
    result = await session.execute(
        select(User).where(User.telegram_id == message.from_user.id)
    )
    user = result.scalar_one_or_none()

    if user:
        bot_info = await bot.get_me()
        ref_link = f"https://t.me/{bot_info.username}?start={user.telegram_id}"

        text = (
            f"👤 <b>Sizning profilingiz</b>\n\n"
            f"🆔 ID: <code>{user.telegram_id}</code>\n"
            f"👨‍💼 Ism: {user.full_name}\n"
            f"📅 Ro'yxatdan o'tgan: {user.created_at.strftime('%d.%m.%Y')}\n"
            f"👥 Taklif qilganlar: {user.referral_count} ta\n\n"
            f"🔗 Sizning referral havolangiz:\n"
            f"<code>{ref_link}</code>\n\n"
            f"Do'stlaringizni taklif qiling va bonuslar oling! 🎁"
        )

        await message.answer(text, reply_markup=back_button())


@router.message(F.text == "📊 Statistika")
async def show_stats(message: Message, session: AsyncSession):
    result = await session.execute(select(User))
    total_users = len(result.scalars().all())

    result = await session.execute(
        select(User).where(User.telegram_id == message.from_user.id)
    )
    user = result.scalar_one_or_none()

    text = (
        f"📊 <b>Statistika</b>\n\n"
        f"👥 Jami foydalanuvchilar: {total_users}\n"
        f"🎯 Sizning referallaringiz: {user.referral_count if user else 0}\n"
    )

    await message.answer(text, reply_markup=back_button())
