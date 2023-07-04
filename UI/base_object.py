from abc import ABC


class BaseObject(ABC):
    def __init__(self, window, x, y, width, height):
        self.window = window

        self.x, self.y = x, y
        self.pos = self.x, self.y

        self.width, self.height = width, height
        self.size = self.width, self.height

    def check_collision(self, x, y) -> bool:
        return (self.x <= x <= self.x + self.width and
                self.y <= y <= self.y + self.height)
