import pygame


class Square:
    marks = O, X = "O", "X"

    fg_color = None
    window = None
    font = None
    side_size = None

    def __init__(self, row=0, col=0, x=0, y=0):
        self.row = row
        self.col = col

        self.x = x
        self.y = y

        self.is_clicked = False
        self.mark = None

    def click(self, mark):
        self.is_clicked ^= True
        if self.is_clicked:
            self.mark = mark
            self.draw_mark()

    def draw_mark(self):
        text = Square.font.render(self.mark, True, Square.fg_color)
        width, height = text.get_size()
        x = self.x + (self.side_size - width) / 2
        y = self.y + (self.side_size - height) / 2
        Square.window.blit(text, (x, y))
        pygame.display.update()

    def check_collision(self, x, y) -> bool:
        return (self.x <= x <= self.x + Square.side_size and
                self.y <= y <= self.y + Square.side_size)

    def set_pos(self, x, y):
        self.x = x
        self.y = y

    @classmethod
    def reverse_marks(cls):
        cls.marks = cls.marks[::-1]

    @classmethod
    def new_square(cls, row, col):
        return Square(row=row, col=col)

    @classmethod
    def set_globals(cls, fg_color, bg_color, font, side_size, window):
        cls.fg_color = fg_color
        cls.bg_color = bg_color
        cls.font = font
        cls.side_size = side_size
        cls.window = window

    def __repr__(self):
        return f"({self.row}, {self.col}, {self.mark})"
