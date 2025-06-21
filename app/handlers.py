from aiogram import Router, F
from aiogram.filters import CommandStart, Command, StateFilter
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.enums import ParseMode

from app.database import (
    DATABASE,
    BOT_COMMANDS,
    get_user_settings,
    update_notification_setting,
    update_language_setting,
    get_current_settings_message
)
import app.keyboards as kb

router = Router()


class SearchStates(StatesGroup):
    waiting_for_search_query = State()


class SettingsStates(StatesGroup):
    waiting_for_notification_choice = State()
    waiting_for_language_choice = State()


class FAQStates(StatesGroup):
    waiting_for_theme_selection = State()
    waiting_for_question_selection = State()


# КОМАНДЫ

@router.message(CommandStart())
async def cmd_start(message: Message):
    '''Обработчик команды /start. Отправляет приветственное сообщение 
    и показывает основную клавиатуру с командами.'''
    await message.answer(
        'Привет! Я TAQBot - бот для ответов на вопросы.\n'
        'Задайте мне любой вопрос, и я постараюсь ответить!',
        reply_markup=kb.main_keyboard()
    )


@router.message(Command('help'))
async def cmd_help(message: Message):
    '''Обработчик команды /help. Выводит список всех доступных команд бота.'''
    text = 'Список доступных команд:\n\n'
    for cmd, desc in BOT_COMMANDS:
        text += f'{cmd} — {desc}\n'
    await message.answer(text)


# СИСТЕМА FAQ (ЧАСТО ЗАДАВАЕМЫЕ ВОПРОСЫ)

@router.message(F.text.in_(['📋 Часто задаваемые вопросы (FAQ)', 'FAQ', 'faq']))
async def show_faq(message: Message, state: FSMContext):
    '''Показывает список тем FAQ.'''
    await state.set_state(FAQStates.waiting_for_theme_selection)
    await message.answer(
        '📚 Выберите интересующую вас тему:',
        reply_markup=kb.faq_themes_keyboard()
    )


@router.callback_query(F.data.startswith('faq_theme_'))
async def show_questions(callback: CallbackQuery, state: FSMContext):
    '''Показывает список вопросов по теме FAQ.'''
    theme = callback.data.replace('faq_theme_', '')
    await state.update_data(current_theme=theme)
    await state.set_state(FAQStates.waiting_for_question_selection)

    await callback.message.edit_text(
        f'📖 Тема: {theme}\n\nВыберите вопрос:',
        reply_markup=kb.faq_questions_keyboard(theme)
    )
    await callback.answer()


@router.callback_query(FAQStates.waiting_for_question_selection, F.data.startswith('faq_id_'))
async def show_answer(callback: CallbackQuery, state: FSMContext):
    '''Показывает полный ответ на выбранный вопрос FAQ. Форматирует ответ
    и предоставляет кнопку возврата к вопросам.'''
    question_id = int(callback.data.replace('faq_id_', ''))
    user_data = await state.get_data()
    theme = user_data.get('current_theme', '')

    question = next(
        (q for q in DATABASE if q['id'] == question_id and q['theme'] == theme), None)

    if not question:
        await callback.answer('Вопрос не найден!', show_alert=True)
        return

    await callback.message.edit_text(
        f'📌 <b>Тема:</b> {question['theme']}\n\n'
        f'❓ <b>Вопрос:</b> {question['question']}\n\n'
        f'💡 <b>Ответ:</b> {question['answer']}',
        parse_mode=ParseMode.HTML,
        reply_markup=kb.back_to_questions_keyboard(theme)
    )
    await callback.answer()


@router.callback_query(F.data == 'back_to_faq')
async def back_to_faq(callback: CallbackQuery, state: FSMContext):
    '''Возвращает пользователя к списку тем FAQ.'''
    await state.set_state(FAQStates.waiting_for_theme_selection)
    await callback.message.edit_text(
        '📚 Выберите интересующую вас тему:',
        reply_markup=kb.faq_themes_keyboard()
    )
    await callback.answer()


@router.callback_query(F.data == 'back_to_main')
async def back_to_main(callback: CallbackQuery, state: FSMContext):
    '''Возвращает в главное меню.'''
    await state.clear()
    await callback.message.edit_text(
        'Главное меню',
        reply_markup=kb.main_keyboard()
    )
    await callback.answer()


# СИСТЕМА НАСТРОЕК

@router.message(F.text.in_(['⚙️ Настройки', 'Настройки']))
async def show_settings(message: Message):
    '''Показывает текущие настройки пользователя и клавиатуру
    для их изменения.'''
    user_id = message.from_user.id
    settings_message = get_current_settings_message(user_id)
    await message.answer(
        f'{settings_message}\n\nВыберите категорию для изменения:',
        reply_markup=kb.settings_keyboard()
    )


@router.message(F.text.in_(['🔔 Уведомления', 'Уведомления']))
async def notification_settings(message: Message, state: FSMContext):
    '''Показывает настройки уведомлений.'''
    user_id = message.from_user.id
    current = get_user_settings(user_id)['notifications']
    keyboard = kb.notifications_keyboard(current)
    await message.answer(
        'Настройки уведомлений:',
        reply_markup=keyboard
    )
    await state.set_state(SettingsStates.waiting_for_notification_choice)


@router.message(SettingsStates.waiting_for_notification_choice)
async def process_notification_choice(message: Message, state: FSMContext):
    '''Обрабатывает выбор пользователя по уведомлениям. Обновляет настройки
    в базе данных и возвращает в меню настроек'''
    user_id = message.from_user.id
    if message.text == '✔️ Включить уведомления':
        update_notification_setting(user_id, True)
        await message.answer('Уведомления включены!', reply_markup=kb.settings_keyboard())
    elif message.text == '❌ Выключить уведомления':
        update_notification_setting(user_id, False)
        await message.answer('Уведомления выключены!', reply_markup=kb.settings_keyboard())
    elif message.text == '⬅️ Назад к настройкам':
        await show_settings(message)
    else:
        await message.answer('Пожалуйста, используйте кнопки меню')
        return
    await state.clear()


@router.message(F.text.in_(['🌐 Язык', 'Язык']))
async def language_settings(message: Message, state: FSMContext):
    '''Показывает доступные языки интерфейса.'''
    await message.answer(
        'Выберите язык:',
        reply_markup=kb.language_keyboard()
    )
    await state.set_state(SettingsStates.waiting_for_language_choice)


@router.message(SettingsStates.waiting_for_language_choice)
async def process_language_choice(message: Message, state: FSMContext):
    '''Обрабатывает выбор языка. Обновляет настройки в базе данных
    и возвращает в меню настроек.'''
    user_id = message.from_user.id
    if message.text == '🇷🇺 Русский':
        update_language_setting(user_id, 'ru')
        await message.answer('Язык изменён на русский', reply_markup=kb.settings_keyboard())
    elif message.text == '🇬🇧 English':
        update_language_setting(user_id, 'en')
        await message.answer('Language changed to English', reply_markup=kb.settings_keyboard())
    elif message.text == '⬅️ Назад к настройкам':
        await show_settings(message)
    else:
        await message.answer('Пожалуйста, используйте кнопки меню')
        return
    await state.clear()


@router.message(F.text.in_(['⬅️ Главное меню', 'Главное меню']))
async def back_to_main(message: Message):
    '''Текстовая команда возврата в главное меню.'''
    await message.answer(
        'Вы вернулись в главное меню',
        reply_markup=kb.main_keyboard()
    )


# СИСТЕМА ПОИСКА

@router.message(F.text.in_(['🔎 Поиск', 'Поиск']))
async def start_search(message: Message, state: FSMContext):
    '''Активирует режим поиска. Переводит в состояние ожидания
    поискового запроса'''
    await message.answer(
        '🔍 Введите ваш вопрос или ключевые слова для поиска:',
        reply_markup=kb.search_keyboard()
    )
    await state.set_state(SearchStates.waiting_for_search_query)


@router.message(StateFilter(SearchStates.waiting_for_search_query), F.text == '❌ Отменить поиск')
async def cancel_search(message: Message, state: FSMContext):
    '''Отменяет режим поиска. Очищает состояние и возвращает
    в главное меню.'''
    await message.answer(
        'Поиск отменён',
        reply_markup=kb.main_keyboard()
    )
    await state.clear()
