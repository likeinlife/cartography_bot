from .models import MicrometerInput, MicrometerOutput


def calculate_micrometer(
    first: MicrometerInput,
    second: MicrometerInput,
) -> MicrometerOutput:
    """
    Считает значения по отсчетам по микрометру.

    Args:
        first_value: Значения по микрометру в первом столбце
        second_value: Значения по микрометру во втором столбце

    Returns:
        Среднее по верхней, нижней части; коллимационная ошибка, среднее из двух отсчетов

    """
    middle_first = (first.left_circle + second.left_circle) / 2
    middle_second = (first.right_circle + second.right_circle) / 2

    c_2 = middle_first - middle_second

    kl_plus_kp = (middle_first + middle_second) / 2

    return MicrometerOutput(
        average_first=middle_first,
        average_second=middle_second,
        c_2=c_2,
        average=kl_plus_kp,
    )
