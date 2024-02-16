from aiogram.fsm.state import State, StatesGroup


class ByNomenclatureImages(StatesGroup):
    enter_nomenclature = State()


class ByCoordinatesImages(StatesGroup):
    enter_first_coordinates = State()
    enter_second_coordinates = State()
    enter_operations_number = State()


class GetMiddle(StatesGroup):
    enter_first_coordinates = State()
    enter_second_coordinates = State()
    enter_parts_number = State()


class MicrometerState(StatesGroup):
    first_column = State()
    second_column = State()
