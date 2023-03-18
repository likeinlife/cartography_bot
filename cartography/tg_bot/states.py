from aiogram.fsm.state import State, StatesGroup


class ByNumenclature(StatesGroup):
    enter_numenclature = State()


class ByCoordinates(StatesGroup):
    enter_first_coordinates = State()
    enter_second_coordinates = State()
    enter_operations_number = State()


class ByCoordinatesImages(StatesGroup):
    enter_first_coordinates = State()
    enter_second_coordinates = State()
    enter_operations_number = State()


class GetMiddle(StatesGroup):
    enter_first_coordinates = State()
    enter_second_coordinates = State()
    enter_parts_number = State()


class GeodeziaMocrometr(StatesGroup):
    first_stolb = State()
    second_stolb = State()