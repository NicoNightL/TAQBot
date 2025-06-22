from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

from app.database import DATABASE

def main_keyboard():
    '''
    Создаёт основную клавиатуру бота с тремя кнопками:
    - FAQ (Часто задаваемые вопросы)
    - Поиск
    - Настройки
    '''
    buttons = [
        [KeyboardButton(text='📋 Часто задаваемые вопросы (FAQ)')],
        [KeyboardButton(text='🔎 Поиск'), KeyboardButton(text='⚙️ Настройки')],
    ]
    return ReplyKeyboardMarkup(keyboard=buttons, resize_keyboard=True)


def search_keyboard():
    '''
    Создаёт клавиатуру для режима поиска с одной кнопкой:
    - Отменить поиск
    '''
    buttons = [
        [KeyboardButton(text='❌ Отменить поиск')],
    ]
    return ReplyKeyboardMarkup(keyboard=buttons, resize_keyboard=True)


def settings_keyboard():
    '''
    Создаёт клавиатуру настроек с тремя кнопками:
    - Уведомления
    - Язык
    - Главное меню
    '''
    buttons = [
        [KeyboardButton(text='🔔 Уведомления'), KeyboardButton(text='🌐 Язык')],
        [KeyboardButton(text='⬅️ Главное меню')]
    ]
    return ReplyKeyboardMarkup(keyboard=buttons, resize_keyboard=True)


def notifications_keyboard(current_state: bool):
    '''Создаёт динамическую клавиатуру для управления уведомлениями.
    Вид кнопки зависит от текущего состояния уведомлений.'''
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
    '''
    Создаёт клавиатуру выбора языка с тремя кнопками:
    - Русский
    - English
    - Назад к настройкам
    '''
    buttons = [
        [KeyboardButton(text='🇷🇺 Русский')],
        [KeyboardButton(text='🇬🇧 English')],
        [KeyboardButton(text='⬅️ Назад к настройкам')]
    ]
    return ReplyKeyboardMarkup(keyboard=buttons, resize_keyboard=True)


def faq_themes_keyboard():
    '''Создаёт inline-клавиатуру с темами FAQ из базы данных.
    Для каждой темы показывает количество доступных вопросов.'''
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
    '''Создаёт inline-клавиатуру с вопросами по выбранной теме
    и кнопкой возврата к списку тем.'''
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
    '''
    Создаёт inline-клавиатуру для возврата из просмотра ответа:
    - Назад к вопросам
    - К списку тем
    '''
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
