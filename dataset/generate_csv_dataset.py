"""
Генерация наборов данных (формат хранения - CSV)
"""
import argparse
from random import randint
from os.path import join, split
from os import makedirs

DEFAULT_DESCRIPTION = 'CSV dataset generator script'
DEFAULT_SAMPLES = 100


def parse_args():
    """
    Парсинг аргументов командной строки (CLI).
    :return интерфейс для работы с аргументами.

    Больше информации на https://docs.python.org/3.7/howto/argparse.html
    """
    parser = argparse.ArgumentParser(description=DEFAULT_DESCRIPTION)

    parser.add_argument('output',
                        type=str,
                        help='output CSV file, e.g. data/output.csv')

    parser.add_argument('--samples',
                        type=int,
                        default=DEFAULT_SAMPLES,
                        help=f'number of samples to generate (default: {DEFAULT_SAMPLES})')

    return parser.parse_args()


def generate_all_datasets():
    """
    Генерация всех наборов данных
    """
    # Три операции: создание, поиск, объединение
    for operation in ('make', 'find', 'union'):

        # Порядковый номер набора данных
        for dataset in range(1, 6):

            # Количество элементов в наборе данных
            for amount in (100, 500, 1000, 5000, 10000, 25000, 50000, 100000, 250000, 500000, 750000, 1000000):

                # Приведение к двухсимвольному числу
                dataset = str(dataset)
                dataset = '0' + dataset if len(dataset) == 1 else dataset

                # Пути к файлу и к директории, в которой файл находится
                dir_path = join('data', operation, dataset)
                file_path = join(dir_path, str(amount) + '.csv')

                # Создание директорий по пути к файлу, если они не существуют
                try:
                    makedirs(dir_path)
                except FileExistsError:
                    pass

                # Заполнение файла числами
                finally:
                    with open(file_path, 'w', encoding='utf-8') as file:
                        for _ in range(amount - 1):
                            file.write(str(randint(0, 10 ** 7 + 1)) + '\n')
                        file.write(str(randint(0, 10 ** 7 + 1)))


if __name__ == '__main__':
    args = parse_args()

    # валидация аргументов
    if args.samples < 0:
        raise ValueError('Number of samples must be greater than 0.')

    # Создание директорий по пути к файлу, если они не существуют
    try:
        makedirs(split(args.output)[0])
    except FileExistsError:
        pass

    # запись данных в файл
    with open(args.output, 'w', encoding='utf-8') as file:
        for i in range(args.samples - 1):
            file.write(str(randint(0, 10 ** 7 + 1)) + '\n')
        file.write(str(randint(0, 10 ** 7 + 1)))

    # Раскомментируйте сточку ниже, чтобы сгенерировать сразу все наборы данных
    # generate_all_datasets()
