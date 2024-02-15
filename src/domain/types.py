from typing import Callable, TypeAlias

ImageType: TypeAlias = bytes
NomenclatureTitleFormatter: TypeAlias = Callable[[str, str], str]
ImageColorType: TypeAlias = tuple[int, int, int]
