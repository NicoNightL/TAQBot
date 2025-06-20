from aiogram import Router, F
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

from app.database import (
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

BOT_COMMANDS = [
    ("/start", "Запустить бота"),
    ("/help", "Показать список команд"),
    ("/settings", "Настройки")
]

# Обработчик команды /start
@router.message(CommandStart())
async def cmd_start(message: Message):
    await message.answer(
        "Привет! Я TAQBot - бот для ответов на вопросы.\n"
        "Задайте мне любой вопрос, и я постараюсь ответить!",
        reply_markup=kb.main_keyboard()
    )


# Обработчик команды /help
@router.message(Command('help'))
async def cmd_help(message: Message):
    text = 'Список доступных команд:\n\n'
    for cmd, desc in BOT_COMMANDS:
        text += f'{cmd} — {desc}\n'
    await message.answer(text)


# Обработчик кнопки FAQ
@router.message(F.text.in_(['📋 Часто задаваемые вопросы (FAQ)', 'FAQ', 'faq']))
async def show_faq(message: Message):
    await message.answer('Часто задаваемые вопросы (FAQ):', reply_markup=kb.faq_keyboard())


# Обработчик кнопки "Назад"
@router.callback_query(F.data == 'back_to_main')
async def back_to_main(callback: CallbackQuery):
    await callback.message.edit_reply_markup(reply_markup=None)
    await callback.message.answer('Вы вернулись в главное меню', reply_markup=kb.main_keyboard())
    await callback.answer()


# Обработчик FAQ вопросов
@router.callback_query(F.data.startswith('faq_'))
async def process_faq(callback: CallbackQuery):
    answers = {
        'faq_general': 'Здесь ответы на общие вопросы...',
        'faq_tech': 'Технические решения проблем...',
        'faq_payment': 'Информация об оплате...',
    }
    await callback.message.answer(answers[callback.data])
    await callback.answer()


# Обработчик кнопки настроек
@router.message(F.text.in_(['⚙️ Настройки', 'Настройки']))
async def show_settings(message: Message):
    user_id = message.from_user.id
    settings_message = get_current_settings_message(user_id)
    await message.answer(
        f"{settings_message}\n\nВыберите категорию для изменения:",
        reply_markup=kb.settings_keyboard()
    )


# Обработчик уведомлений
@router.message(F.text.in_(['🔔 Уведомления', 'Уведомления']))
async def notification_settings(message: Message, state: FSMContext):
    user_id = message.from_user.id
    current = get_user_settings(user_id)['notifications']
    keyboard = kb.notifications_keyboard(current)
    await message.answer(
        "Настройки уведомлений:",
        reply_markup=keyboard
    )
    await state.set_state(SettingsStates.waiting_for_notification_choice)


# Обработчик выбора уведомлений
@router.message(SettingsStates.waiting_for_notification_choice)
async def process_notification_choice(message: Message, state: FSMContext):
    user_id = message.from_user.id
    if message.text == '✔️ Включить уведомления':
        update_notification_setting(user_id, True)
        await message.answer("Уведомления включены!", reply_markup=kb.settings_keyboard())
    elif message.text == '❌ Выключить уведомления':
        update_notification_setting(user_id, False)
        await message.answer("Уведомления выключены!", reply_markup=kb.settings_keyboard())
    elif message.text == '⬅️ Назад к настройкам':
        await show_settings(message)
    else:
        await message.answer("Пожалуйста, используйте кнопки меню")
        return
    await state.clear()


# Обработчик языка
@router.message(F.text.in_(['🌐 Язык', 'Язык']))
async def language_settings(message: Message, state: FSMContext):
    await message.answer(
        "Выберите язык:",
        reply_markup=kb.language_keyboard()
    )
    await state.set_state(SettingsStates.waiting_for_language_choice)


# Обработчик выбора языка
@router.message(SettingsStates.waiting_for_language_choice)
async def process_language_choice(message: Message, state: FSMContext):
    user_id = message.from_user.id
    if message.text == '🇷🇺 Русский':
        update_language_setting(user_id, 'ru')
        await message.answer("Язык изменён на русский", reply_markup=kb.settings_keyboard())
    elif message.text == '🇬🇧 English':
        update_language_setting(user_id, 'en')
        await message.answer("Language changed to English", reply_markup=kb.settings_keyboard())
    elif message.text == '⬅️ Назад к настройкам':
        await show_settings(message)
    else:
        await message.answer("Пожалуйста, используйте кнопки меню")
        return
    await state.clear()


# Обработчик возврата в главное меню
@router.message(F.text.in_(['⬅️ Главное меню', 'Главное меню']))
async def back_to_main(message: Message):
    await message.answer(
        "Вы вернулись в главное меню",
        reply_markup=kb.main_keyboard()
    )


