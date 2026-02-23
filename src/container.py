from dishka import Provider, Scope, make_async_container, provide
from dishka.integrations.aiogram import AiogramProvider
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from core.settings import Config, ImageConfig
from domain.analytics.repository import IAnalyticsRepository
from domain.facades import INomenclatureFacade
from logic.analytics.repositories.psycopg_repository import PsycopgAnalyticsRepository
from logic.cartography.facades.nomenclature_facade import NomenclatureFacade
from logic.cartography.image_generator.generator import ImageGenerator
from logic.cartography.image_generator.interface import IImageGenerator


class SettingsProvider(Provider):
    @provide(scope=Scope.APP)
    def app_settings(self) -> Config:
        return Config()

    @provide(scope=Scope.APP)
    def image_settings(self, app_settings: Config) -> ImageConfig:
        return ImageConfig(static_path=app_settings.static_path)


class AppProvider(Provider):
    @provide(scope=Scope.APP)
    def image_generator(self, image_settings: ImageConfig) -> IImageGenerator:
        return ImageGenerator(
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

    @provide(scope=Scope.APP)
    def nomenclature_facade(self, image_generator: IImageGenerator) -> INomenclatureFacade:
        return NomenclatureFacade(image_generator=image_generator)


class DbProvider(Provider):
    @provide(scope=Scope.APP)
    def session_factory(self, app_settings: Config) -> async_sessionmaker[AsyncSession]:
        if not app_settings.database_url:
            raise RuntimeError("DATABASE_URL must be set when ANALYTICS_ENABLED=True")
        engine = create_async_engine(app_settings.database_url, pool_pre_ping=True)
        return async_sessionmaker(engine, expire_on_commit=False)

    @provide(scope=Scope.APP)
    def analytics_repository(
        self,
        session_factory: async_sessionmaker[AsyncSession],
    ) -> IAnalyticsRepository:
        return PsycopgAnalyticsRepository(session_factory=session_factory)


def create_container():
    return make_async_container(
        SettingsProvider(),
        DbProvider(),
        AppProvider(),
        AiogramProvider(),
    )
