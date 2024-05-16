from aiogram import Dispatcher

from . import geography_coordinates, micrometer, middle_values, nomenclature_title


def register_business_handlers(dp: Dispatcher) -> None:
    dp.include_routers(
        geography_coordinates.router,
        micrometer.router,
        middle_values.router,
        nomenclature_title.router,
    )
