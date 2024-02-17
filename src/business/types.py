from typing import Callable, TypeAlias

from business.enums import Scale

ImageType: TypeAlias = bytes
NomenclatureTitleFormatter: TypeAlias = Callable[[str, str], str]
ImageColorType: TypeAlias = tuple[int, int, int]
NomenclatureTitleDictType: TypeAlias = dict[Scale, str]