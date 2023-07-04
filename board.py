import pygame

from UI.base_object import BaseObject
from Structures.unlimited_grid import UnlimitedGrid
from square import Square
from consts import WinningOptions, Direction


class Board(BaseObject):
    class Tracker:
        def __init__(self):
            self.row = 0
            self.col = 0

        def __repr__(self):
            return f"{self.row} {self.col}"

    def __init__(self,
                 window,
                 x, y, side_size,
                 bg_color, fg_color, strike_through_color,
                 showed_grid_size=3):

        # <editor-fold desc="Helper Init Functions">
        def get_line_thickness() -> int:
            if self.showed_grid_size <= 4:
                return 8
            if self.showed_grid_size <= 10:
                return 4
            return 2

        def get_square_size() -> float:
            return (self.width - self.line_thickness * (self.showed_grid_size - 1)) / self.showed_grid_size

        def get_unit() -> float:
            return self.square_size + self.line_thickness

        # </editor-fold>

        super().__init__(window, x, y, side_size, side_size)

        self.showed_grid_size = showed_grid_size

        self.line_thickness = get_line_thickness()
        self.square_size = get_square_size()
        self.unit_size = get_unit()

        self.fg_color = fg_color
        self.bg_color = bg_color
        self.strike_through_color = strike_through_color

        Square.set_globals(
            self.fg_color,
            None,
            pygame.font.SysFont("Comic Sans MS", int(self.square_size * 0.9)),
            self.square_size,
            self.window,
        )

        self.tracker = Board.Tracker()
        self.grid = UnlimitedGrid(Square.new_square, self.__get_base_grid())
        self.showed_grid = []
        self.__update_showed_grid()

    @property
    def squares(self):
        return [sq for row in self.showed_grid for sq in row]

    # <editor-fold desc="Private Methods">
    def __get_base_grid(self):
        return [
            [Square(row=i, col=j, **self.__get_square_pos(i, j)) for j in range(self.showed_grid_size)]
            for i in range(self.showed_grid_size)
        ]

    def __get_square_pos(self, row, col) -> dict[str, float]:
        x = self.x + col * self.unit_size
        y = self.y + row * self.unit_size
        return {"x": x, "y": y}

    def __update_showed_grid(self):
        # get new squares
        self.showed_grid = [
            [self.grid[i+self.tracker.row, j+self.tracker.col] for j in range(self.showed_grid_size)]
            for i in range(self.showed_grid_size)
        ]

        # update squares' (x, y)
        for i, row in enumerate(self.showed_grid):
            for j, sq in enumerate(row):
                sq.set_pos(**self.__get_square_pos(i, j))

    # </editor-fold>

    def draw_squares(self):
        for sq in self.squares:
            if sq.is_clicked:
                sq.draw_mark()

    def move(self, direction):
        if direction == Direction.up:
            self.tracker.row -= 1
        elif direction == Direction.down:
            self.tracker.row += 1
        elif direction == Direction.left:
            self.tracker.col -= 1
        elif direction == Direction.right:
            self.tracker.col += 1
        else:
            raise ValueError("Invalid direction", direction)

        self.__update_showed_grid()
        self.draw_grid()
        self.draw_squares()

    def draw_grid(self):
        self.window.fill(self.bg_color, (self.x, self.y, self.width, self.height))

        # vertical lines
        x = self.x + self.square_size + self.line_thickness / 2
        y = self.y
        for i in range(self.showed_grid_size - 1):
            pygame.draw.line(
                self.window,
                self.fg_color,
                (x, y),
                (x, y + self.height),
                self.line_thickness
            )
            x += self.square_size + self.line_thickness

        # horizontal lines
        x = self.x
        y = self.y + self.square_size + self.line_thickness / 2
        for i in range(self.showed_grid_size - 1):
            pygame.draw.line(
                self.window,
                self.fg_color,
                (x, y),
                (x + self.width, y),
                self.line_thickness
            )
            y += self.square_size + self.line_thickness

        pygame.display.update()

    def clear_grid(self):
        self.draw_grid()

    def draw_strike_through(self, sequence: list[Square], winning_option):
        # horizontal
        if winning_option == WinningOptions.horizontal:
            sequence.sort(key=lambda x: x.col)
            first, last = sequence[0], sequence[-1]
            start_x, start_y = first.x, first.y + first.side_size / 2
            end_x, end_y = last.x + last.side_size, start_y
            pygame.draw.line(
                self.window,
                self.strike_through_color,
                (start_x, start_y),
                (end_x, end_y),
                self.line_thickness)

        # vertical
        elif winning_option == WinningOptions.vertical:
            sequence.sort(key=lambda x: x.row)
            first, last = sequence[0], sequence[-1]
            start_x, start_y = first.x + first.side_size / 2, first.y
            end_x, end_y = start_x, last.y + last.side_size
            pygame.draw.line(
                self.window,
                self.strike_through_color,
                (start_x, start_y),
                (end_x, end_y),
                self.line_thickness)

        # diagonal \
        elif winning_option == WinningOptions.neg_diagonal:
            sequence.sort(key=lambda x: x.col)
            first, last = sequence[0], sequence[-1]
            start_x, start_y = first.x, first.y
            end_x, end_y = last.x + last.side_size, last.y + last.side_size
            pygame.draw.line(
                self.window,
                self.strike_through_color,
                (start_x, start_y),
                (end_x, end_y),
                int(self.line_thickness * 1.5)
            )

        # diagonal /
        elif winning_option == WinningOptions.pos_diagonal:
            sequence.sort(key=lambda x: x.col)
            first, last = sequence[0], sequence[-1]
            start_x, start_y = first.x, first.y + first.side_size
            end_x, end_y = last.x + last.side_size, last.y
            pygame.draw.line(
                self.window,
                self.strike_through_color,
                (start_x, start_y),
                (end_x, end_y),
                int(self.line_thickness * 1.5)
            )

        pygame.display.update()

    def reset(self):
        self.tracker = Board.Tracker()
        self.grid = UnlimitedGrid(Square.new_square, self.__get_base_grid())
        self.__update_showed_grid()
