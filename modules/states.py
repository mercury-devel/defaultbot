from aiogram.fsm.state import State, StatesGroup


class TestDataState(StatesGroup):
    first_test_data = State()
    second_test_data = State()

