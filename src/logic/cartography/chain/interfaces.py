import abc

from domain.models import CoordinatePair, Nomenclature

from logic.cartography.enums import Scale
from logic.cartography.types import NomenclatureTitleDictType, NomenclatureTitleFormatter


class ICoordinateChainLink(abc.ABC):
    """Nomenclature chain for current scale."""

    previous_link: type["ICoordinateChainLink"]
    outbound_class: type["ICoordinateChainLink"]
    scale: Scale
    name: str
    parts: int
    alphabet: list[str]
    title_formatter: NomenclatureTitleFormatter

    @classmethod
    @abc.abstractmethod
    def resolve(
        cls,
        coordinate_pair: CoordinatePair,
    ) -> dict[Scale, Nomenclature]:
        ...


class INomenclatureTitleChainLink(abc.ABC):
    """Nomenclature chain for current scale."""

    previous_link: type["INomenclatureTitleChainLink"]
    outbound_class: type["INomenclatureTitleChainLink"]
    scale: Scale
    name: str
    parts: int
    alphabet: list[str]
    title_formatter: NomenclatureTitleFormatter

    @classmethod
    @abc.abstractmethod
    def resolve(
        cls,
        nomenclature_dict: NomenclatureTitleDictType,
    ) -> dict[Scale, Nomenclature]:
        ...
