COMMANDS_HELP = """Команды:
Общие:
/start
/help - Помощь
/show - Открыть клавиатуру
/hide - Скрыть клавиатуру
/stop - Завершить текущую операцию

Картография:
/by_coordinates_images - найти нуменклатуру по заданным координатам и машстабу. 
/by_numenclature_images - найти координаты границ сетки по заданной нуменклатуре.
/get_middle - разбить интервал на части и вывести

Геодезия:
/micro - посчитать отсчеты по микрометру

ТМОГИ:
/student - скинуть таблицу Стьюдента
/laplas - скинуть таблицу Лапласа

"""
NUMENCLATURE_HELP = """Пример нуменклатуры:
U-32 = 1:1_000_000 (A-Z, 30-60)
U-32-А = 1:500_000 (А, Б, В, Г)
I-N-37 = 1:300_000 (I, II, III, IV, ..., IX)
N-37-XXI = 1:200_000 (I, II, III, ..., XXVI)
N-37-39 = 1:100_000 (1..144)

N-37-39-Г = 1:50_000 (А, Б, В, Г)
N-37-39-Г-г = 1:25_000 (а, б, в, г)
N-37-39-Г-г-4 = 1:10_000 (1..4)

N-37-144-(120) = 1:5000 (1..256)
N-37-144-(120-и) = 1:2000 (а, б, в, ..., и)"""

SCALES_HELP = """Количество операций для масштабов:
1 - 1:1_000_000
2 - 1:500_000
3 - 1:300_000
4 - 1:200_000
5 - 1:100_000
6 - 1:50_000
7 - 1:25_000
8 - 1:10_000
9 - 1:5_000
10 - 1:2_000
"""