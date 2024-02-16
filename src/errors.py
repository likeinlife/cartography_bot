class BaseError(Exception):
    """Base cartography error."""


class PartNomenclatureError(BaseError):
    ...


class NoLatitudeCharError(BaseError):
    ...


class NoLongitudeIndexError(BaseError):
    ...


class InvalidNomenclatureTitleError(BaseError):
    ...
