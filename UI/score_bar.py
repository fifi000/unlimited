import pygame

from UI.base_object import BaseObject
from Structures.player import Player


class ScoreBar(BaseObject):
    def __init__(self,
                 window,
                 x, y, width, height,
                 font,
                 bg_color, fg_color,
                 players: tuple[Player, Player]):
        super().__init__(window, x, y, width, height)

        self.font = font
        self.fg_color = fg_color
        self.bg_color = bg_color

        self.players = players

    def __draw_players(self):
        text = self.font.render(self.players[0].mark, True, self.fg_color)
        x, y = self.x, self.y
        self.window.blit(text, (x, y))

        text = self.font.render(self.players[-1].mark, True, self.fg_color)
        x, y = self.x + self.width - text.get_width(), self.y
        self.window.blit(text, (x, y))

    def __draw_score(self):
        text = self.font.render(f"{self.players[0].score}:{self.players[-1].score}", True, self.fg_color)
        x, y = self.x + (self.width - text.get_width())/2, self.y
        self.window.blit(text, (x, y))

    def draw(self):
        self.__draw_score()
        self.__draw_players()
        pygame.display.update()
