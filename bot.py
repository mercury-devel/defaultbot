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


db = Sqlite()

async def welcome(message: Message):
    users = [u[0] for u in await db.select("select tg_id from users")]
    if message.from_user.id not in users:
        await db.insert_delete(f"insert into users (tg_id) values ({message.from_user.id})")
    await message.answer("__Меню Bot__", reply_markup=start_kb, parse_mode="Markdown")


async def send_first_test_data(message: Message, state: FSMContext):
    await message.answer("Введите первое тестовое сообщение:")
    await state.set_state(TestDataState.first_test_data)


async def send_second_test_data(message: Message, state: FSMContext):
    await state.update_data(first_data=message.text)
    await message.answer("Введите второе тестовое сообщение:")
    await state.set_state(TestDataState.second_test_data)


async def receive_test_data(message: Message, state: FSMContext):
    data = await state.get_data()
    await state.clear()
    first_data = data['first_data']
    second_data = message.text
    await message.answer(f'Ответ 1: `{first_data}`\nОтвет 2: `{second_data}`', parse_mode='markdown')


async def inline_menu(message: Message):
    await message.answer("Inline-меню", reply_markup=start_inline_kb())


async def categories(call: CallbackQuery):
    await call.message.answer("Список тестовых категорий", reply_markup=categories_kb())


async def category(call: CallbackQuery, callbackData: dict):
    category = callbackData.category
    await call.message.edit(f"Категория: `{category}`", parse_mode="Markdown", reply_markup=back_kb())


async def main():
    bot = Bot(token=bot_token)
    dp = Dispatcher(storage=MemoryStorage())
    dp.message.register(welcome, Command(commands="start"))
    dp.message.register(send_first_test_data, F.text == "Ввести данные")
    dp.message.register(inline_menu, F.text == "Инлайн-меню")
    dp.message.register(send_second_test_data, TestDataState.first_test_data)
    dp.message.register(receive_test_data, TestDataState.second_test_data)
    dp.callback_query.register(categories, F.data == "categories")
    dp.callback_query.register(category, CategoriesCallbackData.filter())

    print("Бот запущен")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
