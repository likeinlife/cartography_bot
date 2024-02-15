from dataclasses import dataclass

from domain.enums import Scale
from domain.types import NomenclatureTitleFormatter

from business import constants


@dataclass
class ScaleInfo:
    alphabet: list[str] | None
    parts: int
    formatter: NomenclatureTitleFormatter = lambda x, y: f"{x}-{y}"


table = {
    Scale._500K: ScaleInfo(alphabet=constants.UPPER_ALPHA, parts=2),
    Scale._300K: ScaleInfo(alphabet=constants.ROMAN, parts=3, formatter=lambda x, y: f"{y}-{x}"),
    Scale._200K: ScaleInfo(alphabet=constants.ROMAN_EXTENDED, parts=6),
    Scale._100K: ScaleInfo(alphabet=[str(i) for i in range(1, 145)], parts=12),
    Scale._50K: ScaleInfo(alphabet=constants.UPPER_ALPHA, parts=2),
    Scale._25K: ScaleInfo(alphabet=constants.LOWER_ALPHA, parts=2),
    Scale._10K: ScaleInfo(alphabet=[str(i) for i in range(1, 5)], parts=2),
    Scale._5K: ScaleInfo(alphabet=[str(i) for i in range(1, 257)], parts=16, formatter=lambda x, y: f"{x}-({y})"),
    Scale._2K: ScaleInfo(alphabet=[str(i) for i in range(1, 10)], parts=3, formatter=lambda x, y: f"{x}-({y})"),
}


def get_scale_info(scale: Scale) -> ScaleInfo:
    return table[scale]
