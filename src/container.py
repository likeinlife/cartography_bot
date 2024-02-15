from dependency_injector.containers import DeclarativeContainer
from dependency_injector.providers import Configuration


class AppContainer(DeclarativeContainer):
    settings: Configuration = Configuration(strict=True)


class ImageContainer(DeclarativeContainer):
    settings: Configuration = Configuration(strict=True)
