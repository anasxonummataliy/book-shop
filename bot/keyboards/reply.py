from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


def main_menu():
    keyboard = [
        [KeyboardButton(text="📚 Katalog"), KeyboardButton(text="👤 Profil")],
        [KeyboardButton(text="📊 Statistika"), KeyboardButton(text="ℹ️ Ma'lumot")],
    ]
    return ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True)


def catalog_menu():
    keyboard = [
        [KeyboardButton(text="📖 Badiiy adabiyot"), KeyboardButton(text="🔬 Ilmiy")],
        [KeyboardButton(text="💼 Biznes"), KeyboardButton(text="🎓 O'quv")],
        [KeyboardButton(text="🔙 Orqaga")],
    ]
    return ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True)


def back_button():
    return ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text="🔙 Orqaga")]], resize_keyboard=True
    )
