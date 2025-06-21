import json
from typing import Dict


def load_database():
    with open('app/database.json', 'r', encoding='utf-8') as file:
        return json.load(file)


def get_user_settings(user_id: int) -> Dict:
    return user_settings.get(user_id, {
        'notifications': True,
        'language': 'ru'
    })


def update_notification_setting(user_id: int, enabled: bool):
    if user_id not in user_settings:
        user_settings[user_id] = {}
    user_settings[user_id]['notifications'] = enabled


def update_language_setting(user_id: int, language: str):
    if user_id not in user_settings:
        user_settings[user_id] = {}
    user_settings[user_id]['language'] = language


def get_current_settings_message(user_id: int) -> str:
    settings = get_user_settings(user_id)
    notifications = '✔️ включены' if settings['notifications'] else '❌ выключены'
    language = '🇷🇺 Русский' if settings['language'] == 'ru' else '🇬🇧 English'
    return (
        f'Текущие настройки:\n\n'
        f'🔔 Уведомления: {notifications}\n'
        f'🌐 Язык: {language}'
    )


# Временное хранилище
user_settings: Dict[int, Dict] = {}

DATABASE = load_database()

BOT_COMMANDS = [
    ('/start', 'Запустить бота'),
    ('/help', 'Показать список команд')
]
