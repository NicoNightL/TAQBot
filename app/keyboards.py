from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton


def main_keyboard():
    buttons = [
        [KeyboardButton(text='📋 Часто задаваемые вопросы (FAQ)')],
        [KeyboardButton(text='🔎 Поиск'), KeyboardButton(text='⚙️ Настройки')],
    ]
    return ReplyKeyboardMarkup(keyboard=buttons, resize_keyboard=True)


def search_keyboard():
    buttons = [
        [KeyboardButton(text='❌ Отменить поиск')],
    ]
    return ReplyKeyboardMarkup(keyboard=buttons, resize_keyboard=True)


def settings_keyboard():
    buttons = [
        [KeyboardButton(text='🔔 Уведомления')],
        [KeyboardButton(text='🌐 Язык')],
        [KeyboardButton(text='⬅️ Главное меню')]
    ]
    return ReplyKeyboardMarkup(keyboard=buttons, resize_keyboard=True)


def notifications_keyboard(current_state: bool):
    if current_state:
        buttons = [
            [KeyboardButton(text='❌ Выключить уведомления')],
            [KeyboardButton(text='⬅️ Назад к настройкам')]
        ]
    else:
        buttons = [
            [KeyboardButton(text='✔️ Включить уведомления')],
            [KeyboardButton(text='⬅️ Назад к настройкам')]
        ]
    return ReplyKeyboardMarkup(keyboard=buttons, resize_keyboard=True)


def language_keyboard():
    buttons = [
        [KeyboardButton(text='🇷🇺 Русский')],
        [KeyboardButton(text='🇬🇧 English')],
        [KeyboardButton(text='⬅️ Назад к настройкам')]
    ]
    return ReplyKeyboardMarkup(keyboard=buttons, resize_keyboard=True)


def faq_keyboard():
    buttons = [
        [InlineKeyboardButton(text="Общие вопросы",
                              callback_data="faq_general")],
        [InlineKeyboardButton(text="Технические проблемы",
                              callback_data="faq_tech")],
        [InlineKeyboardButton(text="Оплата и счета",
                              callback_data="faq_payment")],
        [InlineKeyboardButton(text="⬅️ Назад",
                              callback_data="back_to_main")],
    ]
    return InlineKeyboardMarkup(inline_keyboard=buttons)
