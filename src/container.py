import core.logger_setup as logger_setup
from dependency_injector import providers
from dependency_injector.containers import DeclarativeContainer
from domain.analytics import IAnalyticsRepository, IAnalyticsService
from domain.facades import INomenclatureFacade
from logic.analytics import AnalyticsService
from logic.analytics.repositories import PsycopgAnalyticsRepository
from logic.cartography.facades import NomenclatureFacade
from logic.cartography.image_generator import IImageGenerator, ImageGenerator


class AppContainer(DeclarativeContainer):
    settings: providers.Configuration = providers.Configuration(strict=True)
    image_settings: providers.Configuration = providers.Configuration(strict=True)

    log_configure: providers.Resource = providers.Resource(
        logger_setup.configure_logging,
        debug_mode=settings.dev_mode,
        logging_level=settings.logging_level,
    )

    image_generator: providers.Singleton[IImageGenerator] = providers.Singleton(
        ImageGenerator,
        resolution=image_settings.resolution,
        background_color=image_settings.background_color,
        font_path=image_settings.font_path,
        padding=image_settings.padding,
        text_color=image_settings.text_color,
        inverse_text_color=image_settings.inverse_text_color,
        filling_color=image_settings.filling_color,
        text_size_coefficient=image_settings.text_size_coefficient,
        text_angle=image_settings.text_angle,
        bottom_label_offset=image_settings.bottom_label_offset,
        right_label_offset=image_settings.right_label_offset,
    )

    nomenclature_facade: providers.Singleton[INomenclatureFacade] = providers.Singleton(
        NomenclatureFacade, image_generator=image_generator
    )

    analytics_repository: providers.Singleton[IAnalyticsRepository] = providers.Singleton(
        PsycopgAnalyticsRepository,
        database_url=settings.database_url,
    )
    analytics_service: providers.Singleton[IAnalyticsService] = providers.Singleton(
        AnalyticsService,
        analytics_repository=analytics_repository,
        source=settings.analytics_source,
    )
