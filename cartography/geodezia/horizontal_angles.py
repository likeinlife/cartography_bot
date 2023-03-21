def micrometr_actions(first_value: tuple[float, ...], second_value: tuple[float,
                                                                          ...]) -> tuple[float, float, float, float]:
    """Считает значения по отсчетам по микрометру

    Args:
        first_value (tuple[float, float]): Значения по микрометру в первом столбце
        second_value (tuple[float, float]): Значения по микрометру во втором столбце

    Returns:
        tuple[float, float, float, float]: Среднее по верхней, нижней части; коллимационная ошибка, среднее из двух отсчетов
    """
    middle_first = (first_value[0] + second_value[0]) / 2
    middle_second = (first_value[1] + second_value[1]) / 2

    c_2 = middle_first - middle_second

    kl_plus_kp = (middle_first + middle_second) / 2

    return middle_first, middle_second, c_2, kl_plus_kp
