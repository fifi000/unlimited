import pygame


if __name__ == '__main__':
    pygame.init()
    from game import Game

    width, height = 600, 700
    grid_size = 5
    marks_to_win = 5
    game = Game(width, height, grid_size, marks_to_win)
    game.run()
