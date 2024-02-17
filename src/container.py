import core.logger_setup as logger_setup
from dependency_injector import providers
from dependency_injector.containers import DeclarativeContainer


class AppContainer(DeclarativeContainer):
    settings: providers.Configuration = providers.Configuration(strict=True)

    log_configure: providers.Resource = providers.Resource(
        logger_setup.configure_structlog,
        log_level=settings.logging_level,
    )


class ImageContainer(DeclarativeContainer):
    settings: providers.Configuration = providers.Configuration(strict=True)
