import json
from typing import Dict


def load_database():
    '''Загружает данные из базы вопросов.'''
    with open('app/database.json', 'r', encoding='utf-8') as file:
        return json.load(file)


def get_user_settings(user_id: int) -> Dict:
    '''Получает настройки пользователя или возвращает настройки по умолчанию.'''
    return user_settings.get(user_id, {
        'notifications': True,
        'language': 'ru'
    })


def update_notification_setting(user_id: int, enabled: bool):
    '''Обновляет настройку уведомлений для указанного пользователя.'''
    if user_id not in user_settings:
        user_settings[user_id] = {}
    user_settings[user_id]['notifications'] = enabled


def update_language_setting(user_id: int, language: str):
    '''Обновляет настройку языка для указанного пользователя.'''
    if user_id not in user_settings:
        user_settings[user_id] = {}
    user_settings[user_id]['language'] = language


def get_current_settings_message(user_id: int) -> str:
    '''Формирует сообщение с текущими настройками пользователя.'''
    settings = get_user_settings(user_id)
    notifications = '✔️ включены' if settings['notifications'] else '❌ выключены'
    language = '🇷🇺 Русский' if settings['language'] == 'ru' else '🇬🇧 English'
    return (
        f'Текущие настройки:\n\n'
        f'🔔 Уведомления: {notifications}\n'
        f'🌐 Язык: {language}'
    )


# Временное хранилище настроек пользователей
user_settings: Dict[int, Dict] = {}

# Загрузка базы данных
DATABASE = load_database()

# Список команд бота для отображения в /help
BOT_COMMANDS = [
    ('/start', 'Запустить бота'),
    ('/help', 'Показать список команд')
]
