from domain.models import CoordinatePair, Nomenclature

from logic.cartography import constants
from logic.cartography.calculations.coordinates import get_1m_nomenclature, get_nomenclature_by_parts
from logic.cartography.enums import Scale

from .interfaces import ICoordinateChainLink


class BaseCoordinateChainLink(ICoordinateChainLink):
    title_formatter = lambda x, y: f"{x}-{y}"

    @classmethod
    def resolve(
        cls,
        coordinate_pair: CoordinatePair,
    ) -> dict[Scale, Nomenclature]:
        previous = cls.previous_link.resolve(coordinate_pair)
        this = {
            cls.scale: get_nomenclature_by_parts(
                coordinate_pair=coordinate_pair,
                parts_number=cls.parts,
                previous_nomenclature=previous[cls.outbound_class.scale],
                alphabet=cls.alphabet,
                title_formatter=cls.title_formatter,
            )
        }
        return previous | this


class ChainLink1M(BaseCoordinateChainLink):
    previous_link = None  # type: ignore
    scale = Scale._1M
    alphabet = None  # type: ignore
    parts = 1
    name = "1/1_000_000"
    outbound_class = None  # type: ignore

    @classmethod
    def resolve(
        cls,
        coordinate_pair: CoordinatePair,
    ) -> dict[Scale, Nomenclature]:
        return {cls.scale: get_1m_nomenclature(coordinate_pair)}


class ChainLink500K(BaseCoordinateChainLink):
    previous_link = ChainLink1M
    scale = Scale._500K
    alphabet = constants.UPPER_ALPHA
    parts = 2
    name = "1/500_000"
    outbound_class = ChainLink1M


class ChainLink300K(BaseCoordinateChainLink):
    previous_link = ChainLink500K
    scale = Scale._300K
    alphabet = constants.ROMAN
    parts = 3
    title_formatter = lambda x, y: f"{y}-{x}"
    name = "1/300_000"
    outbound_class = ChainLink1M


class ChainLink200K(BaseCoordinateChainLink):
    previous_link = ChainLink300K
    scale = Scale._200K
    alphabet = constants.ROMAN_EXTENDED
    parts = 6
    name = "1/200_000"
    outbound_class = ChainLink1M


class ChainLink100K(BaseCoordinateChainLink):
    previous_link = ChainLink200K
    scale = Scale._100K
    parts = 12
    alphabet = [str(i) for i in range(1, parts**2 + 1)]
    name = "1/100_000"
    outbound_class = ChainLink1M


class ChainLink50K(BaseCoordinateChainLink):
    previous_link = ChainLink100K
    scale = Scale._50K
    alphabet = constants.UPPER_ALPHA
    parts = 2
    name = "1/50_000"
    outbound_class = ChainLink100K


class ChainLink25K(BaseCoordinateChainLink):
    previous_link = ChainLink50K
    scale = Scale._25K
    alphabet = constants.LOWER_ALPHA
    parts = 2
    name = "1/25_000"
    outbound_class = ChainLink50K


class ChainLink10K(BaseCoordinateChainLink):
    previous_link = ChainLink25K
    scale = Scale._10K
    parts = 2
    alphabet = [str(i) for i in range(1, parts**2 + 1)]
    name = "1/10_000"
    outbound_class = ChainLink25K


class ChainLink5K(BaseCoordinateChainLink):
    previous_link = ChainLink10K
    scale = Scale._5K
    parts = 16
    alphabet = [str(i) for i in range(1, parts**2 + 1)]
    title_formatter = lambda x, y: f"{x}-({y})"
    name = "1/5_000"
    outbound_class = ChainLink100K


class ChainLink2K(BaseCoordinateChainLink):
    previous_link = ChainLink5K
    scale = Scale._2K
    alphabet = constants.LOWER_ALPHA_EXTENDED
    parts = 3
    title_formatter = lambda x, y: f"{x}-({y})"
    name = "1/2_000"
    outbound_class = ChainLink5K
