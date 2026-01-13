from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters import Command
from keyboards.reply import main_menu, back_button

router = Router()


@router.message(F.text == "ℹ️ Ma'lumot")
@router.message(Command("help"))
async def show_info(message: Message):
    text = (
        "ℹ️ <b>Bot haqida ma'lumot</b>\n\n"
        "📚 Bu bot orqali siz:\n"
        "• Kitoblar katalogini ko'rishingiz\n"
        "• Kitob sotib olishingiz\n"
        "• Do'stlaringizni taklif qilishingiz mumkin\n\n"
        "<b>Komandalar:</b>\n"
        "/start - Botni ishga tushirish\n"
        "/help - Yordam\n"
        "/profile - Profilim\n"
        "/catalog - Katalog\n\n"
        "📞 Aloqa: @support_username"
    )
    await message.answer(text, reply_markup=back_button())

