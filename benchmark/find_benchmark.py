import argparse
import random
from sys import path
from os.path import split, abspath
from os import curdir
from time import perf_counter_ns
from random import choice
path.append(abspath(curdir))
from src.disjoint_set import DisjointSet  # noqa: E402


DEFAULT_DESCRIPTION = 'Find operation benchmark script'
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
                        help='input CSV file, e.g. dataset/data/find/01/100.csv')

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

        # Создание СНМ из 100 одноэлементных множеств и списка из всех элементов СНМ
        disjoint_set = DisjointSet()
        disjoint_set_element = []
        for _ in range(amount):
            elem = int(inp_file.readline())
            disjoint_set.make_set(elem)
            disjoint_set_element.append(elem)

        # Рандомное распределение одноэлементных множеств на некоторое количество множеств из нескольких элементов
        for _ in range(int(amount * 0.75)):
            disjoint_set.union(choice(disjoint_set_element), choice(disjoint_set_element))

        # Количество прогонов на наборе данных
        for trial in range(args.trials):

            # Замер времени поиска случайного элемента СНМ и запись в файл
            find_elem = choice(disjoint_set_element)
            start_time = perf_counter_ns()
            disjoint_set.find(find_elem)
            finish_time = perf_counter_ns()
            time = finish_time - start_time
            out_file.write(str(time) + '\n')
