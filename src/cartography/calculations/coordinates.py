import string

from domain.models import Coordinate, CoordinatePair, Nomenclature

from cartography.constants import FINISH_GEO_ZONE, INIT_GEO_ZONE
from cartography.errors import NoLatitudeCharError, NoLongitudeIndexError, PartNomenclatureError
from cartography.types import NomenclatureTitleFormatter


def get_1m_nomenclature(coordinate_pair: CoordinatePair) -> Nomenclature:
    """Get 1 millions scale nomenclature."""
    alphabet = string.ascii_uppercase

    longitude_index = None
    latitude_char = None
    latitude_step = 4
    for index_, char in enumerate(alphabet):
        lower_latitude = Coordinate.from_tuple(index_ * latitude_step)
        upper_latitude = Coordinate.from_tuple(latitude_step * (index_ + 1))
        if coordinate_pair.latitude.actions.between(lower_latitude, upper_latitude):
            latitude_char = char
            break

    if not latitude_char:
        raise NoLatitudeCharError(coordinate_pair.latitude.to_str())

    longitude_step = 6
    INIT_1 = INIT_GEO_ZONE + 1
    for this_index in range(INIT_1, FINISH_GEO_ZONE):
        lower_longitude = Coordinate.from_tuple((this_index - INIT_1) * longitude_step)
        upper_longitude = Coordinate.from_tuple(longitude_step * (this_index + 1 - INIT_1))

        if coordinate_pair.longitude.actions.between(lower_longitude, upper_longitude):
            longitude_index = this_index
            break

    if not longitude_index:
        raise NoLongitudeIndexError(coordinate_pair.longitude.to_str())

    title = f"{latitude_char}-{longitude_index}"
    lower_bound = CoordinatePair(latitude=lower_latitude, longitude=lower_longitude)
    upper_bound = CoordinatePair(latitude=upper_latitude, longitude=upper_longitude)

    outer_lower_bound = CoordinatePair(
        latitude=Coordinate.from_tuple(0),
        longitude=Coordinate.from_tuple(0),
    )
    outer_upper_bound = CoordinatePair(
        latitude=Coordinate.from_tuple(0),
        longitude=Coordinate.from_tuple(0),
    )

    return Nomenclature(
        title=title,
        lower_bound=lower_bound,
        upper_bound=upper_bound,
        outer_lower_bound=outer_lower_bound,
        outer_upper_bound=outer_upper_bound,
    )


def get_nomenclature_by_parts(
    coordinate_pair: CoordinatePair,
    parts_number: int,
    previous_nomenclature: Nomenclature,
    alphabet: list[str] | None = None,
    title_formatter: NomenclatureTitleFormatter = lambda x, y: f"{x}-{y}",
) -> Nomenclature:
    """Get nomenclature depending on bounds, parts_number and coordinates."""
    delta = previous_nomenclature.lower_bound.actions.get_delta(previous_nomenclature.upper_bound, parts_number)

    upper_latitude = previous_nomenclature.upper_bound.latitude
    lower_longitude = previous_nomenclature.lower_bound.longitude
    initial_longitude = lower_longitude

    for this_part in range(1, parts_number**2 + 1):
        lower_latitude = upper_latitude - delta.latitude
        upper_longitude = lower_longitude + delta.longitude
        latitude_ok = coordinate_pair.latitude.actions.between(lower_latitude, upper_latitude)
        longitude_ok = coordinate_pair.longitude.actions.between(lower_longitude, upper_longitude)

        if latitude_ok and longitude_ok:
            current_part_name = alphabet[this_part - 1] if alphabet else str(this_part)
            nomenclature_title = title_formatter(previous_nomenclature.title, current_part_name)
            lower_bound = CoordinatePair(latitude=lower_latitude, longitude=lower_longitude)
            upper_bound = CoordinatePair(latitude=upper_latitude, longitude=upper_longitude)
            return Nomenclature(
                title=nomenclature_title,
                outer_lower_bound=previous_nomenclature.lower_bound,
                outer_upper_bound=previous_nomenclature.upper_bound,
                lower_bound=lower_bound,
                upper_bound=upper_bound,
                cell_to_fill=current_part_name,
            )

        if this_part % parts_number == 0:
            upper_latitude = upper_latitude - delta.latitude
            lower_longitude = initial_longitude
        else:
            lower_longitude = lower_longitude + delta.longitude

    raise PartNomenclatureError(coordinate_pair.to_str())
