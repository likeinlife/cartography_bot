from typing import Callable

from domain.chain import IChainLink
from domain.models import CoordinatePair, Nomenclature

from business import constants
from business.calculate_nomenclature import get_1m_nomenclature, get_nomenclature_by_parts


class ChainLinkShortcut(IChainLink):
    @classmethod
    def _resolve_shortcut(
        cls,
        coordinate_pair: CoordinatePair,
        previous_scale_name: str,
        parts_number: int,
        alphabet: list[str] | None = None,
        title_formatter: Callable[[str, str], str] = lambda x, y: f"{x}-{y}",
    ) -> dict[str, Nomenclature]:
        previous = cls.previous_link.resolve(coordinate_pair)
        this = {
            cls.scale: get_nomenclature_by_parts(
                coordinate_pair=coordinate_pair,
                parts_number=parts_number,
                previous_nomenclature=previous[previous_scale_name],
                alphabet=alphabet,
                title_formatter=title_formatter,
            )
        }
        return previous | this


class ChainLink1M(IChainLink):
    previous_link = None  # type: ignore
    scale = "1m"

    @classmethod
    def resolve(
        cls,
        coordinate_pair: CoordinatePair,
    ) -> dict[str, Nomenclature]:
        return {cls.scale: get_1m_nomenclature(coordinate_pair)}


class ChainLink500K(ChainLinkShortcut, IChainLink):
    previous_link = ChainLink1M
    scale = "500k"

    @classmethod
    def resolve(
        cls,
        coordinate_pair: CoordinatePair,
    ) -> dict[str, Nomenclature]:
        return cls._resolve_shortcut(
            coordinate_pair=coordinate_pair,
            previous_scale_name=ChainLink1M.scale,
            parts_number=2,
            alphabet=constants.UPPER_ALPHA,
        )


class ChainLink300K(ChainLinkShortcut, IChainLink):
    previous_link = ChainLink500K
    scale = "300k"

    @classmethod
    def resolve(
        cls,
        coordinate_pair: CoordinatePair,
    ) -> dict[str, Nomenclature]:
        title_formatter = lambda x, y: f"{y}-{x}"

        return cls._resolve_shortcut(
            coordinate_pair=coordinate_pair,
            previous_scale_name=ChainLink1M.scale,
            parts_number=3,
            title_formatter=title_formatter,
            alphabet=constants.ROMAN,
        )


class ChainLink200K(ChainLinkShortcut, IChainLink):
    previous_link = ChainLink300K
    scale = "200k"

    @classmethod
    def resolve(
        cls,
        coordinate_pair: CoordinatePair,
    ) -> dict[str, Nomenclature]:
        return cls._resolve_shortcut(
            coordinate_pair=coordinate_pair,
            previous_scale_name=ChainLink1M.scale,
            parts_number=6,
            alphabet=constants.ROMAN,
        )


class ChainLink100K(ChainLinkShortcut, IChainLink):
    previous_link = ChainLink200K
    scale = "100k"

    @classmethod
    def resolve(
        cls,
        coordinate_pair: CoordinatePair,
    ) -> dict[str, Nomenclature]:
        return cls._resolve_shortcut(
            coordinate_pair=coordinate_pair,
            previous_scale_name=ChainLink1M.scale,
            parts_number=12,
        )


class ChainLink50K(ChainLinkShortcut, IChainLink):
    previous_link = ChainLink100K
    scale = "50k"

    @classmethod
    def resolve(
        cls,
        coordinate_pair: CoordinatePair,
    ) -> dict[str, Nomenclature]:
        return cls._resolve_shortcut(
            coordinate_pair=coordinate_pair,
            previous_scale_name=cls.previous_link.scale,
            parts_number=2,
            alphabet=constants.UPPER_ALPHA,
        )


class ChainLink25K(ChainLinkShortcut, IChainLink):
    previous_link = ChainLink50K
    scale = "25k"

    @classmethod
    def resolve(
        cls,
        coordinate_pair: CoordinatePair,
    ) -> dict[str, Nomenclature]:
        return cls._resolve_shortcut(
            coordinate_pair=coordinate_pair,
            previous_scale_name=cls.previous_link.scale,
            parts_number=2,
            alphabet=constants.LOWER_ALPHA,
        )


class ChainLink10K(ChainLinkShortcut, IChainLink):
    previous_link = ChainLink25K
    scale = "10k"

    @classmethod
    def resolve(
        cls,
        coordinate_pair: CoordinatePair,
    ) -> dict[str, Nomenclature]:
        return cls._resolve_shortcut(
            coordinate_pair=coordinate_pair,
            previous_scale_name=cls.previous_link.scale,
            parts_number=2,
        )


class ChainLink5K(ChainLinkShortcut, IChainLink):
    previous_link = ChainLink10K
    scale = "5k"

    @classmethod
    def resolve(
        cls,
        coordinate_pair: CoordinatePair,
    ) -> dict[str, Nomenclature]:
        title_formatter = lambda x, y: f"{x}-({y})"
        return cls._resolve_shortcut(
            coordinate_pair=coordinate_pair,
            previous_scale_name=cls.previous_link.scale,
            parts_number=16,
            title_formatter=title_formatter,
        )


class ChainLink2K(ChainLinkShortcut, IChainLink):
    previous_link = ChainLink5K
    scale = "2k"

    @classmethod
    def resolve(
        cls,
        coordinate_pair: CoordinatePair,
    ) -> dict[str, Nomenclature]:
        title_formatter = lambda x, y: f"{x}-({y})"
        return cls._resolve_shortcut(
            coordinate_pair=coordinate_pair,
            previous_scale_name=cls.previous_link.scale,
            parts_number=3,
            alphabet=constants.LOWER_ALPHA_EXTENDED,
            title_formatter=title_formatter,
        )
