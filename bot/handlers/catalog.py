from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from database.models import Book, Order, User
from keyboards.reply import main_menu, catalog_menu, back_button
from keyboards.inline import book_actions, confirm_purchase

router = Router()


@router.message(F.text == "📚 Katalog")
async def show_catalog(message: Message):
    await message.answer(
        "📚 <b>Kitoblar katalogi</b>\n\n" "Qiziqtirgan bo'limni tanlang:",
        reply_markup=catalog_menu(),
    )


@router.message(F.text == "📖 Badiiy adabiyot")
async def show_fiction_books(message: Message, session: AsyncSession):
    # Demo kitoblar (real loyihada DBdan olasiz)
    books = [
        {
            "id": 1,
            "title": "O'tkan kunlar",
            "author": "Abdulla Qodiriy",
            "price": 50000,
        },
        {
            "id": 2,
            "title": "Mehrobdan chayon",
            "author": "Abdulla Qodiriy",
            "price": 45000,
        },
    ]

    text = "📖 <b>Badiiy adabiyot</b>\n\n"
    for book in books:
        text += f"📕 <b>{book['title']}</b>\n"
        text += f"✍️ Muallif: {book['author']}\n"
        text += f"💰 Narx: {book['price']:,} so'm\n\n"

    await message.answer(text, reply_markup=back_button())


@router.message(F.text == "🔬 Ilmiy")
async def show_science_books(message: Message):
    text = (
        "🔬 <b>Ilmiy kitoblar</b>\n\n"
        "📗 <b>Fizika asoslari</b>\n"
        "✍️ Muallif: A. Karimov\n"
        "💰 Narx: 65,000 so'm\n\n"
        "📗 <b>Matematika</b>\n"
        "✍️ Muallif: B. Valiyev\n"
        "💰 Narx: 70,000 so'm"
    )
    await message.answer(text, reply_markup=back_button())


@router.message(F.text == "💼 Biznes")
async def show_business_books(message: Message):
    text = (
        "💼 <b>Biznes kitoblar</b>\n\n"
        "📘 <b>Boy ota, Kambag'al ota</b>\n"
        "✍️ Muallif: Robert Kiyosaki\n"
        "💰 Narx: 55,000 so'm\n\n"
        "📘 <b>O'ylab ko'ring va boy bo'ling</b>\n"
        "✍️ Muallif: Napoleon Hill\n"
        "💰 Narx: 60,000 so'm"
    )
    await message.answer(text, reply_markup=back_button())


@router.message(F.text == "🎓 O'quv")
async def show_educational_books(message: Message):
    text = (
        "🎓 <b>O'quv qo'llanmalar</b>\n\n"
        "📙 <b>Python dasturlash</b>\n"
        "✍️ Muallif: Mark Lutz\n"
        "💰 Narx: 80,000 so'm\n\n"
        "📙 <b>Ingliz tili grammatikasi</b>\n"
        "✍️ Muallif: Raymond Murphy\n"
        "💰 Narx: 45,000 so'm"
    )
    await message.answer(text, reply_markup=back_button())


# Inline button callbacks
@router.callback_query(F.data.startswith("buy_"))
async def buy_book(callback: CallbackQuery):
    book_id = int(callback.data.split("_")[1])

    text = (
        f"🛒 <b>Buyurtma tasdiqlash</b>\n\n"
        f"Kitob: Kitob nomi\n"
        f"Narx: 50,000 so'm\n\n"
        f"Buyurtmani tasdiqlaysizmi?"
    )

    await callback.message.edit_text(text, reply_markup=confirm_purchase(book_id))
    await callback.answer()


@router.callback_query(F.data.startswith("confirm_"))
async def confirm_order(callback: CallbackQuery, session: AsyncSession):
    book_id = int(callback.data.split("_")[1])

    # User topish
    result = await session.execute(
        select(User).where(User.telegram_id == callback.from_user.id)
    )
    user = result.scalar_one_or_none()

    if user:
        # Buyurtma yaratish
        order = Order(user_id=user.id, book_id=book_id)
        session.add(order)
        await session.commit()

        await callback.message.edit_text(
            "✅ <b>Buyurtma qabul qilindi!</b>\n\n"
            "Tez orada siz bilan bog'lanamiz. 📞"
        )
    else:
        await callback.message.edit_text("❌ Xatolik yuz berdi. /start ni bosing.")

    await callback.answer()


@router.callback_query(F.data == "cancel_purchase")
async def cancel_purchase(callback: CallbackQuery):
    await callback.message.edit_text("❌ Buyurtma bekor qilindi.")
    await callback.answer()


@router.callback_query(F.data == "back_to_catalog")
async def back_to_catalog(callback: CallbackQuery):
    await callback.message.delete()
    await callback.message.answer(
        "📚 <b>Kitoblar katalogi</b>\n\n" "Qiziqtirgan bo'limni tanlang:",
        reply_markup=catalog_menu(),
    )
    await callback.answer()
