from aiogram.types.reply_keyboard_markup import ReplyKeyboardMarkup
from aiogram.types.keyboard_button import KeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
from modules.callback_data import *


start_kb = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text='Ввести данные')],
    [KeyboardButton(text='Инлайн-меню')],
], resize_keyboard=True)


def start_inline_kb():
    keyboard_builder = InlineKeyboardBuilder()
    keyboard_builder.button(text="Выбрать категорию", callback_data="catagories")
    keyboard_builder.button(text="Веб-страница", url="https://www.google.com/")
    keyboard_builder.adjust(1)
    return keyboard_builder.as_markup()


def categories_kb():
    keyboard_builder = InlineKeyboardBuilder()
    keyboard_builder.button(text="Фото", callback_data=CategoriesCallbackData(category="photo"))
    keyboard_builder.button(text="Видео", callback_data=CategoriesCallbackData(category="video"))
    keyboard_builder.button(text="Музыка", callback_data=CategoriesCallbackData(category="music"))

    keyboard_builder.adjust(2, 1)
    return keyboard_builder.as_markup()


def back_kb():
    keyboard_builder = InlineKeyboardBuilder()
    keyboard_builder.button(text="Назад", callback_data=CategoriesCallbackData(category="back"))
    keyboard_builder.adjust(1)
    return keyboard_builder.as_markup()
