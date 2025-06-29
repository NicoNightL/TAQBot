import sqlite3
from typing import Dict


def init_db():
    '''Инициализирует базу данных SQLite и заполняет начальными данными'''
    conn = sqlite3.connect('app/database.db')
    cursor = conn.cursor()

    # Создаём таблицу FAQ
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS faq (
        id INTEGER PRIMARY KEY,
        theme TEXT NOT NULL,
        question TEXT NOT NULL,
        answer TEXT NOT NULL,
        keywords TEXT NOT NULL
    )
    ''')

    # Создаём таблицу настроек пользователей
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS user_settings (
        user_id INTEGER PRIMARY KEY,
        notifications BOOLEAN DEFAULT 1,
        language TEXT DEFAULT 'ru'
    )
    ''')

    # Проверяем, пуста ли таблица FAQ
    cursor.execute('SELECT COUNT(*) FROM faq')
    if cursor.fetchone()[0] == 0:
        # Вставляем начальные данные
        initial_data = [
            (0, 'Общие вопросы', 'Как войти в аккаунт Yandex?',
             'Для входа в аккаунт Yandex перейдите на страницу https://passport.yandex.ru, введите ваш логин или email и пароль, затем нажмите «Войти».',
             'логин,вход,аккаунт,авторизация'),
            (1, 'Почта', 'Как восстановить доступ к Yandex Почте?',
             'Чтобы восстановить доступ, нажмите «Не помню пароль» на странице входа. Введите ваш логин или email, следуйте инструкциям для подтверждения личности и сбросьте пароль.',
             'восстановление,пароль,доступ,почта'),
            (2, 'Диск', 'Как увеличить место на Yandex Диске?',
             'Дополнительное место можно получить, купив подписку Yandex 360 или активировав временные бонусы. Проверьте раздел «Тарифы» в настройках Диска.',
             'хранилище,место,диск,подписка'),
            (3, 'Метрика', 'Как добавить сайт в Yandex Метрику?',
             '1. Зайдите в Метрику (https://metrika.yandex.ru). 2. Нажмите «Добавить счётчик». 3. Укажите данные сайта (URL, название). 4. Примите условия и сохраните. 5. Установите код счётчика на сайт.',
             'метрика,аналитика,сайт,счётчик'),
            (4, 'Почта', 'Как изменить пароль от Yandex Почты?',
             '1. Войдите в аккаунт. 2. Перейдите в настройки (иконка шестерёнки). 3. Выберите «Безопасность». 4. Нажмите «Изменить пароль» и следуйте инструкциям.',
             'пароль,безопасность,почта,изменить'),
            (5, 'Диск', 'Как поделиться файлом с Yandex Диска?',
             '1. Откройте Yandex Диск. 2. Наведите курсор на файл и нажмите «Поделиться». 3. Выберите «Ссылка» или укажите email. 4. Настройте права доступа (просмотр/редактирование).',
             'поделиться,файл,диск,доступ')
        ]
        cursor.executemany(
            'INSERT INTO faq (id, theme, question, answer, keywords) VALUES (?, ?, ?, ?, ?)',
            initial_data
        )

    conn.commit()
    conn.close()


def load_database():
    '''Загружает данные из базы вопросов'''
    conn = sqlite3.connect('app/database.db')
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM faq ORDER BY id')
    result = [dict(row) for row in cursor.fetchall()]
    conn.close()
    return result


def get_user_settings(user_id: int) -> Dict:
    '''Получает настройки пользователя или возвращает настройки по умолчанию'''
    conn = sqlite3.connect('app/database.db')
    cursor = conn.cursor()

    cursor.execute(
        'SELECT notifications, language FROM user_settings WHERE user_id = ?',
        (user_id,)
    )
    result = cursor.fetchone()

    if result:
        settings = {'notifications': bool(result[0]), 'language': result[1]}
    else:
        settings = {'notifications': True, 'language': 'ru'}
        cursor.execute(
            'INSERT INTO user_settings (user_id, notifications, language) VALUES (?, ?, ?)',
            (user_id, 1, 'ru')
        )
        conn.commit()

    conn.close()
    return settings


def update_notification_setting(user_id: int, enabled: bool):
    '''Обновляет настройку уведомлений для указанного пользователя'''
    conn = sqlite3.connect('app/database.db')
    cursor = conn.cursor()

    cursor.execute(
        'INSERT OR REPLACE INTO user_settings (user_id, notifications) VALUES (?, ?)',
        (user_id, int(enabled))
    )

    conn.commit()
    conn.close()


def update_language_setting(user_id: int, language: str):
    '''Обновляет настройку языка для указанного пользователя'''
    conn = sqlite3.connect('app/database.db')
    cursor = conn.cursor()

    cursor.execute(
        'INSERT OR REPLACE INTO user_settings (user_id, language) VALUES (?, ?)',
        (user_id, language)
    )

    conn.commit()
    conn.close()


def get_current_settings_message(user_id: int) -> str:
    '''Формирует сообщение с текущими настройками пользователя'''
    settings = get_user_settings(user_id)
    notifications = '✔️ включены' if settings['notifications'] else '❌ выключены'
    language = '🇷🇺 Русский' if settings['language'] == 'ru' else '🇬🇧 English'
    return (
        f'Текущие настройки:\n\n'
        f'🔔 Уведомления: {notifications}\n'
        f'🌐 Язык: {language}'
    )


# Инициализация базы данных при импорте модуля
init_db()

# Загрузка базы данных
DATABASE = load_database()

# Список команд бота для отображения в /help
BOT_COMMANDS = [
    ('/start', 'Запустить бота'),
    ('/help', 'Показать список команд')
]
