import argparse
from sys import path
from os.path import split, abspath
from os import curdir, makedirs
from time import perf_counter_ns
path.append(abspath(curdir))
from src.disjoint_set import DisjointSet  # noqa: E402


DEFAULT_DESCRIPTION = 'Make operation benchmark script'
DEFAULT_TRIALS = 10


def parse_args():
    """
    Парсинг аргументов командной строки (CLI).
    :return интерфейс для работы с аргументами.

    Больше информации на https://docs.python.org/3.7/howto/argparse.html
    """
    parser = argparse.ArgumentParser(description=DEFAULT_DESCRIPTION)

    parser.add_argument('input',
                        type=str,
                        help='input CSV file, e.g. dataset/data/make/01/100.csv')

    parser.add_argument('output',
                        type=str,
                        help='output CSV file, e.g. benchmark/metrics.txt')

    parser.add_argument('--trials',
                        type=int,
                        default=DEFAULT_TRIALS,
                        help=f'number of samples to generate (default: {DEFAULT_TRIALS})')

    return parser.parse_args()


if __name__ == '__main__':
    args = parse_args()

    if args.trials < 0:
        raise ValueError('Number of trials must be greater than 0.')

    # Создание директорий по пути к файлу, если они не существуют
    try:
        makedirs(args.output.split[0])
    except FileExistsError:
        pass


    with open(args.input, 'r', encoding='utf-8') as inp_file, \
         open(args.output, 'w', encoding='utf-8') as out_file:

        # Вытаскивание количества поданых элементов из названия файла
        amount = int(split(args.input)[1].split('.')[0])

        # Количество прогонов на наборе данных
        for trial in range(args.trials):

            # Создание системы непересекающихся множеств из amount одноэлементных множеств,
            # замеряется время каждого создания одноэлементного множества
            disjoint_set = DisjointSet()
            all_time = 0
            for _ in range(amount):
                elem = int(inp_file.readline())
                start_time = perf_counter_ns()
                disjoint_set.make_set(elem)
                finish_time = perf_counter_ns()
                all_time += finish_time - start_time

            # Перемещение указателя в файле на начало
            inp_file.seek(0)

            # Нахождение среднего времени создания одноэлементного множества и его запись в файл
            average_time = all_time / amount
            out_file.write(str(average_time) + '\n')
