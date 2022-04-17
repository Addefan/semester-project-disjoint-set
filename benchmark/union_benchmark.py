import argparse
from sys import path
from os.path import split, abspath
from os import curdir
from copy import deepcopy
from time import perf_counter_ns
path.append(abspath(curdir))
from src.disjoint_set import DisjointSet  # noqa: E402


DEFAULT_DESCRIPTION = 'Union operation benchmark script'
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
                        help='input CSV file, e.g. dataset/data/union/01/100.csv')

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

    with open(args.input, 'r', encoding='utf-8') as inp_file, \
         open(args.output, 'w', encoding='utf-8') as out_file:

        # Вытаскивание количества поданых элементов из названия файла
        amount = int(split(args.input)[1].split('.')[0])

        # Создание системы непересекающихся множеств из двух множеств по (amount / 2) элементов
        disjoint_set = DisjointSet()
        first_elem = int(inp_file.readline())
        second_elem = int(inp_file.readline())
        disjoint_set.make_set(first_elem)
        disjoint_set.make_set(second_elem)
        for _ in range(amount // 2 - 1):
            elem1 = int(inp_file.readline())
            elem2 = int(inp_file.readline())
            disjoint_set.make_set(elem1)
            disjoint_set.make_set(elem2)
            disjoint_set.union(first_elem, elem1)
            disjoint_set.union(second_elem, elem2)

        # Количество прогонов на наборе данных
        for trial in range(args.trials):

            # Создание копии созданной выше СНМ
            disjoint_set_copy = deepcopy(disjoint_set)

            # Замер времени объединения двух множеств и запись в файл
            start_time = perf_counter_ns()
            disjoint_set_copy.union(first_elem, second_elem)
            finish_time = perf_counter_ns()
            time = finish_time - start_time
            out_file.write(str(time) + '\n')
