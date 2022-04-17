class DisjointSet:
    def __init__(self):
        """
        Инициализация системы непересекающихся множеств
        """
        # Словарь вида (элемент: родитель)
        self.parents = {}

        # Словарь вида (элемент: ранг), где ранг - верхняя граница высоты дерева
        self.ranks = {}

    def make_set(self, elem):
        """
        Функция, создающая новое множество из одного элемента
        """
        self.parents[elem] = elem
        self.ranks[elem] = 0

    def find(self, elem):
        """
        Функция, которая возвращает родителя множества, которому принажлежит элемент
        """
        if self.parents[elem] == elem:
            return elem

        # Эвристика сжатия путей (path compression)
        self.parents[elem] = self.find(self.parents[elem])

        return self.parents[elem]

    def union(self, first, second):
        """
        Функция объединения множеств, которым принадлежат входные элементы
        """
        first = self.find(first)
        second = self.find(second)
        if first == second:
            return

        # Эвристика объединения по рангу (union by rank)
        if self.ranks[first] <= self.ranks[second]:
            self.parents[first] = second
            if self.ranks[first] == self.ranks[second]:
                self.ranks[second] += 1
        else:
            self.parents[second] = first

    def update_parents(self):
        """
        Вспомогательная функция для вывода СНМ на экран
        (обновляет родителей для всех элементов)
        """
        for key in self.parents:
            self.find(key)

    def __str__(self):
        """
        Функция вывода системы непересекающихся множеств на экран
        """
        self.update_parents()
        out = '{'
        sorted_nodes = sorted(self.parents.items(), key=lambda f: int(f[1]))
        current_parent = sorted_nodes[0][1]
        for key, value in sorted_nodes:
            if value == current_parent:
                out += f'{key}, '
            else:
                out = out[:-2] + '}  {'
                current_parent = value
                out += f'{key}, '
        out = out[:-2] + '}'
        return out
