import string
from typing import Any

import errors
from domain.models import CoordinatePair, Nomenclature
from domain.types import NomenclatureTitleFormatter
from misc import from_tuple

from business.math_actions import coordinate_actions


def get_1m_nomenclature(nomenclature_title: str) -> Nomenclature:
    """Get 1 millions scale nomenclature."""
    first_part = nomenclature_title.split("-")
    alphabet = string.ascii_uppercase

    for index, char in enumerate(alphabet):
        if char == first_part[0]:
            lower_latitude = from_tuple(index * 4)
            upper_latitude = from_tuple(4 * (index + 1))
            break

    longitude_index = int(first_part[1])
    for this_index in range(30, 61):
        if this_index == longitude_index:
            this_index -= 31
            lower_longitude = from_tuple(this_index * 6)
            upper_longitude = from_tuple(6 * (this_index + 1))
            break

    lower_bound = CoordinatePair(latitude=lower_latitude, longitude=lower_longitude)
    upper_bound = CoordinatePair(latitude=upper_latitude, longitude=upper_longitude)

    outer_lower_bound = CoordinatePair(
        latitude=from_tuple(0),
        longitude=from_tuple(0),
    )
    outer_upper_bound = CoordinatePair(
        latitude=from_tuple(0),
        longitude=from_tuple(0),
    )
    return Nomenclature(
        lower_bound=lower_bound,
        upper_bound=upper_bound,
        title=nomenclature_title,
        outer_lower_bound=outer_lower_bound,
        outer_upper_bound=outer_upper_bound,
    )


def get_nomenclature_by_parts(
    needed_nomenclature_title: str,
    previous_nomenclature: Nomenclature,
    parts_number: int,
    alphabet: list[str],
    nomenclature_title_formatter: NomenclatureTitleFormatter = lambda x, y: f"{x}-{y}",
) -> Nomenclature:
    """
    Get nomenclature depending on bounds, parts_number and needed_part.

    Args:
        needed_nomenclature_title: needed part. Example: `Б`, `2`, 'б'
    """

    def _is_needed_part(part: Any) -> bool:
        return part == needed_nomenclature_title

    upper_latitude = previous_nomenclature.upper_bound.latitude
    lower_longitude = previous_nomenclature.lower_bound.longitude

    initial_longitude = lower_longitude

    latitude_delta = coordinate_actions.divide(
        coordinate_actions.minus(
            previous_nomenclature.upper_bound.latitude,
            previous_nomenclature.lower_bound.latitude,
        ),
        parts_number,
    )
    longitude_delta = coordinate_actions.divide(
        coordinate_actions.minus(
            previous_nomenclature.upper_bound.longitude,
            previous_nomenclature.lower_bound.longitude,
        ),
        parts_number,
    )

    for iteration, part in enumerate(alphabet, start=1):
        if _is_needed_part(part):
            lower_latitude = coordinate_actions.minus(upper_latitude, latitude_delta)
            upper_longitude = coordinate_actions.plus(lower_longitude, longitude_delta)
            nomenclature_title = nomenclature_title_formatter(previous_nomenclature.title, needed_nomenclature_title)
            upper_bound = CoordinatePair(latitude=upper_latitude, longitude=upper_longitude)
            lower_bound = CoordinatePair(latitude=lower_latitude, longitude=lower_longitude)
            return Nomenclature(
                title=nomenclature_title,
                outer_lower_bound=previous_nomenclature.lower_bound,
                outer_upper_bound=previous_nomenclature.upper_bound,
                lower_bound=lower_bound,
                upper_bound=upper_bound,
                cell_to_fill=needed_nomenclature_title,
            )

        if iteration % (parts_number) == 0:
            upper_latitude = coordinate_actions.minus(upper_latitude, latitude_delta)
            lower_longitude = initial_longitude
        else:
            lower_longitude = coordinate_actions.plus(lower_longitude, longitude_delta)

    raise errors.PartNomenclatureError