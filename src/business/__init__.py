"""Package for cartography business logic: image generation and nomenclature calculations.

Facades use cases:
    >>> images = NomenclatureFacade.generate_from_nomenclature("III-M-41")

    >>> images = NomenclatureFacade.generate_from_coordinates(
        coordinate_pair=CoordinatePair(
            latitude=from_tuple(50, 54, 55),
            longitude=from_tuple(67, 19, 48),
        ),
        needed_scale=10,
    )
"""