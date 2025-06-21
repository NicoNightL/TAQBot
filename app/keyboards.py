from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

from app.database import DATABASE

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
        [KeyboardButton(text='🔔 Уведомления'), KeyboardButton(text='🌐 Язык')],
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


def faq_themes_keyboard():
    '''Клавиатура с темами FAQ'''
    builder = InlineKeyboardBuilder()
    themes = list({item['theme'] for item in DATABASE})

    for theme in themes:
        count = sum(1 for item in DATABASE if item['theme'] == theme)
        builder.button(
            text=f'{theme} ({count})',
            callback_data=f'faq_theme_{theme}'
        )
    builder.adjust(1)
    return builder.as_markup()


def faq_questions_keyboard(theme: str):
    '''Клавиатура с вопросами по теме'''
    builder = InlineKeyboardBuilder()
    questions = [item for item in DATABASE if item['theme'] == theme]

    for question in questions:
        builder.button(
            text=question['question'],
            callback_data=f'faq_id_{question['id']}'
        )

    builder.button(
        text='⬅️ Назад к темам',
        callback_data='back_to_faq'
    )
    builder.adjust(1)
    return builder.as_markup()


def back_to_questions_keyboard(theme: str):
    '''Клавиатура для возврата к вопросам темы'''
    builder = InlineKeyboardBuilder()
    builder.button(
        text='⬅️ Назад к вопросам',
        callback_data=f'faq_theme_{theme}'
    )
    builder.button(
        text='📚 К списку тем',
        callback_data='back_to_faq'
    )
    builder.adjust(2)
    return builder.as_markup()
