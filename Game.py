# Импортируем библиотечки
import random
import math


# Класс Логики игры
class Game:
    # Поля Класса
    __score = 0
    __field = []
    __index = 0
    __row_index = 0
    __col_index = 0
    __rowCounts = 0
    __columnCounts = 0
    __colorsCounts = 0
    __scoreColor = 1.2

    # Немного геттеров
    @property
    def score(self):
        return self.__score

    @property
    def field(self):
        return self.__field

    @property
    def rowCounts(self):
        return self.__rowCounts

    @property
    def columnCounts(self):
        return self.__columnCounts

    @property
    def colorsCounts(self):
        return self.__colorsCounts

    # Конструктор класса
    def __init__(self, row_counts, column_counts, colors_counts):
        self.__rowCounts = row_counts
        self.__columnCounts = column_counts
        self.__colorsCounts = colors_counts

        self.__create_matrix()
        self.__create_field()

    # Метод для создания матрицы
    def __create_matrix(self):
        for row in range(self.__rowCounts):
            self.field.append([])
            for col in range(self.__columnCounts):
                self.field[row].append(0)

    # Метод для заполнение матрицы рандомными значениями
    def __create_field(self):
        for row in range(self.__rowCounts):
            for col in range(self.__columnCounts):
                self.field[row][col] = random.randint(1, self.__colorsCounts)

    # Событие клика мышки
    def click(self, col_index, row_index):
        self.__row_index = int(row_index / 25)
        self.__col_index = int(col_index / 25)

        if self.__row_index < self.__rowCounts and self.__col_index < self.__columnCounts:
            self.__neighbor(self.__row_index, self.__col_index, self.field[self.__row_index][self.__col_index])
            self.__fall_rows()
            self.__fall_columns()

        if self.__index == 0:
            return False
        self.__index = 0
        return True

    # Определяет пустая ли колонка
    def __is_column_empty(self, col_index):
        for r in range(self.__rowCounts):
            if self.field[r][col_index] != 0:
                return False
        return True

    # Копирует колонку в колонку
    def __copy_col_to_col(self, col_from, col_to):
        for row in range(self.__rowCounts):
            self.field[row][col_to] = self.field[row][col_from]

    # Делает колонку пустой
    def __set_col_zero(self, col):
        for row in range(self.__rowCounts):
            self.field[row][col] = 0

    # Метод смещение при пустых колонках влево
    def __fall_columns(self):
        index1 = 0
        for col in range(self.__columnCounts):
            if self.__is_column_empty(col) == False:
                self.__copy_col_to_col(col, index1)
                index1 += 1

        while index1 < self.__columnCounts:
            self.__set_col_zero(index1)
            index1 += 1

    # Метод падения по стракам шариков
    def __fall_rows(self):
        for cols in range(self.__columnCounts):
            index1 = self.__rowCounts - 1
            for rows in range(self.__rowCounts-1, -1, -1):
                if self.field[rows][cols] != 0:
                    self.field[index1][cols] = self.field[rows][cols]
                    index1 -= 1

            for index1 in range(index1, -1, -1):
                self.field[index1][cols] = 0

    # Определяет соседние одинаковые круги и уничтожает их
    def __neighbor(self, row_index, col_index, color_click):
        f = [[0, 1], [0, -1], [1, 0], [-1, 0]]
        for i in range(0, 4):
            if row_index + f[i][0] < self.__rowCounts and row_index + f[i][0] >= 0 and col_index + f[i][1] < self.__columnCounts and col_index + f[i][1] >= 0:
                if (self.field[row_index + f[i][0]][col_index + f[i][1]] == color_click and self.field[row_index + f[i][0]][col_index + f[i][1]] != 0):
                    self.field[row_index][col_index] = 0
                    self.__index += 1
                    self.__neighbor(row_index + f[i][0], col_index + f[i][1], color_click)

        if self.__index == 0:
            return
        self.field[row_index][col_index] = 0
        self.__score += int(math.pow(self.__scoreColor, self.__index))