from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def book_actions(book_id: int):
    keyboard = [
        [InlineKeyboardButton(text="🛒 Sotib olish", callback_data=f"buy_{book_id}")],
        [InlineKeyboardButton(text="📖 Batafsil", callback_data=f"detail_{book_id}")],
        [InlineKeyboardButton(text="🔙 Orqaga", callback_data="back_to_catalog")],
    ]
    return InlineKeyboardMarkup(inline_keyboard=keyboard)


def confirm_purchase(book_id: int):
    keyboard = [
        [
            InlineKeyboardButton(
                text="✅ Tasdiqlash", callback_data=f"confirm_{book_id}"
            )
        ],
        [InlineKeyboardButton(text="❌ Bekor qilish", callback_data="cancel_purchase")],
    ]
    return InlineKeyboardMarkup(inline_keyboard=keyboard)


def referral_button(bot_username: str, user_id: int):
    ref_link = f"https://t.me/{bot_username}?start={user_id}"
    keyboard = [[InlineKeyboardButton(text="📤 Ulashish", url=ref_link)]]
    return InlineKeyboardMarkup(inline_keyboard=keyboard)
