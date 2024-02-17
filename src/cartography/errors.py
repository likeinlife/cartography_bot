from typing import Any

from errors import BaseMsgError


class AdditionalInputMixin(BaseMsgError):
    msg: str

    def __init__(self, info: Any) -> None:
        self.msg = self.msg + f": {info}"


class PartNomenclatureError(AdditionalInputMixin):
    msg = "Invalid part"


class InvalidLatitudeOrLongitude(AdditionalInputMixin):
    msg = "Invalid latitude or longitude"


class NoLatitudeCharError(AdditionalInputMixin):
    msg = "Invalid latitude char"


class NoLongitudeIndexError(AdditionalInputMixin):
    msg = "Invalid longitude index"


class InvalidNomenclatureTitleError(AdditionalInputMixin):
    msg = "Invalid nomenclature part"
