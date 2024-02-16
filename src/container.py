import core.logger_setup as logger_setup
from dependency_injector.containers import DeclarativeContainer
from dependency_injector.providers import Configuration, Resource


class AppContainer(DeclarativeContainer):
    settings: Configuration = Configuration(strict=True)

    log_configure: Resource = Resource(
        logger_setup.configure_structlog,
        log_level=settings.logging_level,
    )


class ImageContainer(DeclarativeContainer):
    settings: Configuration = Configuration(strict=True)
