from typing import Generator, TypeAlias

from src.utils.classes import Numenclat

NumenclatList: TypeAlias = list[Numenclat]
ImageGenerator: TypeAlias = Generator[bytes, None, None]
