from dataclasses import dataclass

from domain.enums import Scale
from domain.types import NomenclatureTitleFormatter

from business import constants


@dataclass
class ScaleInfo:
    alphabet: list[str]
    parts: int
    name: str
    formatter: NomenclatureTitleFormatter = lambda x, y: f"{x}-{y}"


table = {
    Scale._1M: ScaleInfo(
        alphabet=[" "],
        parts=1,
        name="1/1_000_000",
    ),
    Scale._500K: ScaleInfo(
        alphabet=constants.UPPER_ALPHA,
        parts=2,
        name="1/500_000",
    ),
    Scale._300K: ScaleInfo(
        alphabet=constants.ROMAN,
        parts=3,
        formatter=lambda x, y: f"{y}-{x}",
        name="1/300_000",
    ),
    Scale._200K: ScaleInfo(
        alphabet=constants.ROMAN_EXTENDED,
        parts=6,
        name="1/200_000",
    ),
    Scale._100K: ScaleInfo(
        alphabet=[str(i) for i in range(1, 145)],
        parts=12,
        name="1/100_000",
    ),
    Scale._50K: ScaleInfo(
        alphabet=constants.UPPER_ALPHA,
        parts=2,
        name="1/50_000",
    ),
    Scale._25K: ScaleInfo(
        alphabet=constants.LOWER_ALPHA,
        parts=2,
        name="1/25_000",
    ),
    Scale._10K: ScaleInfo(
        alphabet=[str(i) for i in range(1, 5)],
        parts=2,
        name="1/10_000",
    ),
    Scale._5K: ScaleInfo(
        alphabet=[str(i) for i in range(1, 257)],
        parts=16,
        formatter=lambda x, y: f"{x}-({y})",
        name="1/5_000",
    ),
    Scale._2K: ScaleInfo(
        alphabet=[str(i) for i in range(1, 10)],
        parts=3,
        formatter=lambda x, y: f"{x}-({y})",
        name="1/2_000",
    ),
}


def get_scale_info(scale: Scale) -> ScaleInfo:
    return table[scale]
