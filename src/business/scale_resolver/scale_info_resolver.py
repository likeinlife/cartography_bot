from dataclasses import dataclass

from domain.chain import ICoordinateChainLink
from domain.enums import Scale
from domain.types import NomenclatureTitleFormatter

from business import constants
from business.chain import coordinate_chain


@dataclass
class ScaleInfo:
    alphabet: list[str]
    parts: int
    name: str
    class_: type[ICoordinateChainLink]
    formatter: NomenclatureTitleFormatter = lambda x, y: f"{x}-{y}"


table = {
    Scale._1M: ScaleInfo(
        alphabet=[" "],
        parts=1,
        name="1/1_000_000",
        class_=coordinate_chain.ChainLink1M,
    ),
    Scale._500K: ScaleInfo(
        alphabet=constants.UPPER_ALPHA,
        parts=2,
        name="1/500_000",
        class_=coordinate_chain.ChainLink500K,
    ),
    Scale._300K: ScaleInfo(
        alphabet=constants.ROMAN,
        parts=3,
        formatter=lambda x, y: f"{y}-{x}",
        name="1/300_000",
        class_=coordinate_chain.ChainLink300K,
    ),
    Scale._200K: ScaleInfo(
        alphabet=constants.ROMAN_EXTENDED,
        parts=6,
        name="1/200_000",
        class_=coordinate_chain.ChainLink200K,
    ),
    Scale._100K: ScaleInfo(
        alphabet=[str(i) for i in range(1, 145)],
        parts=12,
        name="1/100_000",
        class_=coordinate_chain.ChainLink100K,
    ),
    Scale._50K: ScaleInfo(
        alphabet=constants.UPPER_ALPHA,
        parts=2,
        name="1/50_000",
        class_=coordinate_chain.ChainLink50K,
    ),
    Scale._25K: ScaleInfo(
        alphabet=constants.LOWER_ALPHA,
        parts=2,
        name="1/25_000",
        class_=coordinate_chain.ChainLink25K,
    ),
    Scale._10K: ScaleInfo(
        alphabet=[str(i) for i in range(1, 5)],
        parts=2,
        name="1/10_000",
        class_=coordinate_chain.ChainLink10K,
    ),
    Scale._5K: ScaleInfo(
        alphabet=[str(i) for i in range(1, 257)],
        parts=16,
        formatter=lambda x, y: f"{x}-({y})",
        name="1/5_000",
        class_=coordinate_chain.ChainLink5K,
    ),
    Scale._2K: ScaleInfo(
        alphabet=constants.LOWER_ALPHA_EXTENDED,
        parts=3,
        formatter=lambda x, y: f"{x}-({y})",
        name="1/2_000",
        class_=coordinate_chain.ChainLink2K,
    ),
}


def get_scale_info(scale: Scale) -> ScaleInfo:
    return table[scale]
