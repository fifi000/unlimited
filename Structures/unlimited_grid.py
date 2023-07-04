from consts import Direction
from collections import deque
from copy import copy


class UnlimitedGrid_queue:
    def __init__(self, get_obj, start_data=None):
        """
        a data structure represented in a 2D array of unlimited size (extends itself only when needed);
        initially starts with (0, 0) index
        uses negative indexes;
        eg. row=-1 --> one row before row=0
        :param get_obj: a callable with 'row' and 'col' parameters; called to fill the grid with it
        """
        self.get_obj = get_obj
        self.grid: deque = deque([deque([get_obj(row=0, col=0)])])

        if start_data:
            self.set_start_data(start_data)

        self.__lowest_row_index = 0
        self.__highest_row_index = 0
        self.__lowest_col_index = 0
        self.__highest_col_index = 0

    def __get_actual_row(self, i):
        # check boundary
        # if doesn't exist --> extend self.grid
        while i < self.__lowest_row_index:
            self.__extend(Direction.up)
        while i > self.__highest_row_index:
            self.__extend(Direction.down)

        return i - self.__lowest_row_index

    def __get_actual_col(self, i):
        # check boundary
        # if doesn't exist --> extend self.grid
        while i < self.__lowest_col_index:
            self.__extend(Direction.left)
        while i > self.__highest_col_index:
            self.__extend(Direction.right)

        return i - self.__lowest_col_index

    def __extend(self, direction):
        # insert row at the beginning
        if direction == Direction.up:
            self.__lowest_row_index -= 1
            col = self.grid[0][0].col
            self.grid.appendleft(
                deque([self.get_obj(row=self.__lowest_row_index, col=i + col) for i in range(len(self.grid[0]))])
            )

        # append get_obj row
        elif direction == Direction.down:
            col = self.grid[self.__highest_row_index][0].col
            self.__highest_row_index += 1
            self.grid.append(
                deque([self.get_obj(row=self.__highest_row_index, col=col + i) for i in range(len(self.grid[0]))])
            )

        # insert get_obj col at the beginning
        elif direction == Direction.left:
            self.__lowest_col_index -= 1
            row = self.grid[0][0].row
            for i in range(len(self.grid)):
                self.grid[i].appendleft(self.get_obj(row=row + i, col=self.__lowest_col_index))

        # append get_obj col
        elif direction == Direction.right:
            self.__highest_col_index += 1
            row = self.grid[0][0].row
            for i in range(len(self.grid)):
                self.grid[i].append(self.get_obj(row=row + i, col=self.__highest_col_index))
        else:
            raise ValueError("Invalid direction", direction)

    def set_start_data(self, start_data):
        self.grid = deque()
        for i in range(len(start_data)):
            self.grid.append(deque(start_data[i]))

        self.__highest_row_index = len(self.grid) - 1
        self.__highest_col_index = len(self.grid[0]) - 1

    def get_row_range(self, row, start, end) -> list:
        """
        eg. li = [[1, 2, 3], [4, 5, 6]]
            returns -> li[row][start:end]
        :param row: index of the row number
        :param start: included index of the starting column number
        :param end: excluded index of the ending column number
        :return: list of objects
        """
        row = self.__get_actual_row(row)
        i = self.__get_actual_col(start)
        j = self.__get_actual_col(end)

        return [self.grid[row][i] for i in range(i, j)]

    def __repr__(self):
        return str([[sq for sq in row] for row in self.grid])

    def __getitem__(self, key: tuple[int, int]):
        """
        :param key: eg. grid[5, 6]
        """
        i, j = key
        i = self.__get_actual_row(i)
        j = self.__get_actual_col(j)
        return self.grid[i][j]

    def __setitem__(self, key: tuple[int, int], value):
        """
        :param key: eg. grid[5, 6]
        """
        i, j = key
        i = self.__get_actual_row(i)
        j = self.__get_actual_col(j)

        self.grid[i][j] = value

    def __iter__(self):
        for row in self.grid:
            yield row

    def __len__(self):
        return len(self.grid)


class UnlimitedGrid:
    def __init__(self, get_obj, start_data=None):
        """
        a data structure represented in a 2D array of unlimited size (extends itself only when needed);
        initially starts with (0, 0) index
        uses negative indexes;
        eg. row=-1 --> one row before row=0
        :param get_obj: a callable with 'row' and 'col' parameters; called to fill the grid with it
        """
        self.get_obj = get_obj
        self.grid = [[get_obj(row=0, col=0)]]
        if start_data:
            self.set_start_data(start_data)

    @property
    def __lowest_row(self):
        return self.grid[0][0].row

    @property
    def __highest_row(self):
        return self.grid[-1][-1].row

    @property
    def __lowest_col(self):
        return self.grid[0][0].col

    @property
    def __highest_col(self):
        return self.grid[-1][-1].col

    def __get_actual_row(self, i):
        # check boundary
        # if doesn't exist --> extend self.grid
        while i < self.__lowest_row:
            self.__extend(Direction.up)
        while i > self.__highest_row:
            self.__extend(Direction.down)

        return i - self.__lowest_row

    def __get_actual_col(self, i):
        # check boundary
        # if doesn't exist --> extend self.grid
        while i < self.__lowest_col:
            self.__extend(Direction.left)
        while i > self.__highest_col:
            self.__extend(Direction.right)

        return i - self.__lowest_col

    def __extend(self, direction):
        # insert row at the beginning
        if direction == Direction.up:
            new_row = [self.get_obj(row=el.row-1, col=el.col) for el in self.grid[0]]
            self.grid.insert(0, new_row)

        # append row to the end
        elif direction == Direction.down:
            new_row = [self.get_obj(row=el.row + 1, col=el.col) for el in self.grid[-1]]
            self.grid.append(new_row)

        # insert col at the beginning
        elif direction == Direction.left:
            for row in self.grid:
                el = row[0]
                row.insert(0, self.get_obj(row=el.row, col=el.col-1))

        # append get_obj col
        elif direction == Direction.right:
            for row in self.grid:
                el = row[-1]
                row.append(self.get_obj(row=el.row, col=el.col+1))

        else:
            raise ValueError("Invalid direction", direction)

    def set_start_data(self, start_data):
        self.grid = [copy(row) for row in start_data]

    def get_row_range(self, row, start, end) -> list:
        """
        eg. li = [[1, 2, 3], [4, 5, 6]]
            returns -> li[row][start:end]
        :param row: index of the row number
        :param start: included index of the starting column number
        :param end: excluded index of the ending column number
        :return: list of objects
        """
        row = self.__get_actual_row(row)
        i = self.__get_actual_col(start)
        j = self.__get_actual_col(end)

        return self.grid[row][i:j]

    def __repr__(self):
        return str(self.grid)

    def __getitem__(self, key: tuple[int, int]):
        """
        :param key: eg. grid[5, 6]
        """
        i, j = key
        i = self.__get_actual_row(i)
        j = self.__get_actual_col(j)
        return self.grid[i][j]

    def __setitem__(self, key: tuple[int, int], value):
        """
        :param key: eg. grid[5, 6]
        """
        i, j = key
        i = self.__get_actual_row(i)
        j = self.__get_actual_col(j)

        self.grid[i][j] = value

    def __iter__(self):
        for row in self.grid:
            yield row

    def __len__(self):
        return len(self.grid)
