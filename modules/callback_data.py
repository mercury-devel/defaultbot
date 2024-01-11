from aiogram.filters.callback_data import CallbackData


class CategoriesCallbackData(CallbackData, prefix="categories"):
    category: str
