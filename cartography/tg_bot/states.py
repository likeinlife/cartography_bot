from aiogram.fsm.state import StatesGroup, State


class ByNumenclature(StatesGroup):
    enter_numenclature = State()


class ByCoordinates(StatesGroup):
    enter_first_coordinates = State()
    enter_second_coordinates = State()
    enter_operations_number = State()


class GetMiddle(StatesGroup):
    enter_first_coordinates = State()
    enter_second_coordinates = State()
    enter_parts_number = State()
