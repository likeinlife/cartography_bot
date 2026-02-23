from dishka import Provider, Scope, make_async_container, provide
from dishka.integrations.aiogram import AiogramProvider
from core.settings import ImageConfig
from domain.facades import INomenclatureFacade
from logic.cartography.facades import NomenclatureFacade
from logic.cartography.image_generator import IImageGenerator, ImageGenerator


class AppProvider(Provider):
    def __init__(self, image_settings: ImageConfig) -> None:
        super().__init__()
        self._image_settings = image_settings

    @provide(scope=Scope.APP)
    def image_generator(self) -> IImageGenerator:
        return ImageGenerator(
            resolution=self._image_settings.resolution,
            background_color=self._image_settings.background_color,
            font_path=self._image_settings.font_path,
            padding=self._image_settings.padding,
            text_color=self._image_settings.text_color,
            inverse_text_color=self._image_settings.inverse_text_color,
            filling_color=self._image_settings.filling_color,
            text_size_coefficient=self._image_settings.text_size_coefficient,
            text_angle=self._image_settings.text_angle,
            bottom_label_offset=self._image_settings.bottom_label_offset,
            right_label_offset=self._image_settings.right_label_offset,
        )

    @provide(scope=Scope.APP)
    def nomenclature_facade(self, image_generator: IImageGenerator) -> INomenclatureFacade:
        return NomenclatureFacade(image_generator=image_generator)


def create_container(image_settings: ImageConfig):
    return make_async_container(
        AppProvider(image_settings=image_settings),
        AiogramProvider(),
    )
