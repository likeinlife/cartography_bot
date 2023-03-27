from typing import Generator, TypeAlias

from cartography.utils.classes import Numenclat

NumenclatList: TypeAlias = list[Numenclat]
ImageGenerator: TypeAlias = Generator[bytes, None, None]