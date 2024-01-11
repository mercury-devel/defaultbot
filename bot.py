import asyncio
from aiogram import Bot, Dispatcher, F
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.types import Message, CallbackQuery
from aiogram.filters.command import Command
from aiogram.fsm.context import FSMContext
from modules.sqlite_requests import Sqlite
from modules.keyboards import *
from modules.states import *
from modules.callback_data import *
from config import *

# Вызов класса, отвечающий за базу данных
db = Sqlite()


# Стартовое меню
async def welcome(message: Message):
    # Идентификатор пользователя telegram
    user_id = message.from_user.id

    # Проверка наличия пользователя в базе данных
    user_exists = await db.select(f"select * from users where tg_id = {user_id}")
    if not user_exists:
        # Запись пользователя в базу данных при условии, что он там ещё не записан
        await db.insert_delete(f"insert into users (tg_id) values ({user_id})")
    await message.answer("__Меню Bot__", reply_markup=start_kb, parse_mode="Markdown")


# Отправка первого параметра
async def send_first_test_data(message: Message, state: FSMContext):
    await message.answer("Введите первое тестовое сообщение:")
    await state.set_state(TestDataState.first_test_data)


# Отправка другого параметра
async def send_second_test_data(message: Message, state: FSMContext):
    await state.update_data(first_data=message.text)
    await message.answer("Введите второе тестовое сообщение:")
    await state.set_state(TestDataState.second_test_data)


# Вывод результата
async def receive_test_data(message: Message, state: FSMContext):
    data = await state.get_data()
    await state.clear()
    first_data = data['first_data']
    second_data = message.text
    await message.answer(f'Ответ 1: `{first_data}`\nОтвет 2: `{second_data}`', parse_mode='markdown')


# Функции отправляющие сообщения с inline-кнопками
async def inline_menu(message: Message):
    await message.answer("Inline-меню", reply_markup=start_inline_kb())


async def categories(call: CallbackQuery):
    await call.message.answer("Список тестовых категорий", reply_markup=categories_kb())


# Функция анализирующая callback параметры в данных из кнопок
async def category(call: CallbackQuery, callback_data: dict):
    category = callback_data.category
    await call.message.edit_text(f"Категория: `{category}`", parse_mode="Markdown", reply_markup=back_kb())


# Функция возвращения в меню
async def back(call: CallbackQuery):
    await call.message.edit_text("Список тестовых категорий", reply_markup=categories_kb())


async def all(message: Message):
    user_id = message.from_user.id
    first_name = message.from_user.first_name
    chat_id = message.chat.id
    text = message.text
    log_message = f"Отправлено сообщение от пользователя:\n" \
          f"Имя: {first_name}\tID: {user_id}\tID Чата: {chat_id}\nСообщение: {text}\n"
    print(log_message+"*"*50)

async def main():
    bot = Bot(token=bot_token)
    dp = Dispatcher(storage=MemoryStorage())

    # Обработчик команд
    dp.message.register(welcome, Command(commands="start"))

    # Обработчики текста с кнопок
    dp.message.register(send_first_test_data, F.text == "Ввести данные")
    dp.message.register(inline_menu, F.text == "Инлайн-меню")

    # Обработчики стейт машин
    dp.message.register(send_second_test_data, TestDataState.first_test_data)
    dp.message.register(receive_test_data, TestDataState.second_test_data)

    # Обработчики Callback-данных
    dp.callback_query.register(categories, F.data == "categories")
    dp.callback_query.register(back, F.data == "back")

    # Обработка и фильтрация Callback-данных
    dp.callback_query.register(category, CategoriesCallbackData.filter())

    # Обработчик всех текстовых сообщений боту
    dp.message.register(all)

    print("Бот запущен")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
