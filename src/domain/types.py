from typing import Callable, TypeAlias

ImageType: TypeAlias = bytes
NomenclatureTitleFormatter: TypeAlias = Callable[[str, str], str]
