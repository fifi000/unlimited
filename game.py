from __future__ import annotations

import pygame

from square import Square
from Structures.player import Player
from UI.score_bar import ScoreBar
from consts import BLACK, WHITE, GREY, WinningOptions, Direction
from board import Board


class Game:
    def __init__(self,
                 width=500, height=700,
                 showed_grid_size=3, marks_needed_to_win=3,
                 bg_color=WHITE, fg_color=BLACK):
        # rect
        self.x, self.y = (0, 0)
        self.size = width, height
        self.width, self.height = self.size

        # grid
        self.showed_grid_size = showed_grid_size

        # colors
        self.bg_color = bg_color
        self.fg_color = fg_color

        # window set up
        pygame.display.set_caption("Tic Tac Toe")
        self.window = pygame.display.set_mode((width, height))
        self.window.fill(bg_color)

        # game attributes
        self.move_counter = 0
        self.marks_needed_to_win = marks_needed_to_win
        self.players = (
            Player(Square.marks[0], score=0),
            Player(Square.marks[1], score=0),
        )

        # layout
        self.margin = 30
        self.game_x, self.game_y = self.margin, self.margin
        self.game_width, self.game_height = (size - 2 * self.margin for size in self.size)

        # upper section with players' scores
        self.score_bar = ScoreBar(
            window=self.window,
            x=self.game_x, y=self.game_y,
            width=self.game_width, height=100,
            font=pygame.font.SysFont("Comic Sans MS", 56),
            fg_color=self.fg_color, bg_color=self.bg_color,
            players=self.players
        )

        self.board = Board(
            window=self.window,
            x=self.margin, y=self.score_bar.y + self.score_bar.height,
            side_size=self.game_width,
            bg_color=self.bg_color, fg_color=self.fg_color, strike_through_color=GREY,
            showed_grid_size=self.showed_grid_size)

    def __is_winning_sequence(self, sequence: list[Square], mark) -> list[Square]:
        counter = 0
        start_index = 0
        for i, sq in enumerate(sequence):
            if sq.mark == mark:
                if counter == 0:
                    start_index = i
                counter += 1
            else:
                if counter >= self.marks_needed_to_win:
                    return sequence[start_index:start_index + counter]
                counter = 0

        if counter >= self.marks_needed_to_win:
            return sequence[start_index:start_index + counter]

        return []

    def __check_if_win(self, square) -> tuple[list[Square], str]:
        mark = square.mark
        col_nr = square.col
        row_nr = square.row

        # - horizontal
        # get right and left range of squares +/- marks needed to win
        left_index = col_nr - (self.marks_needed_to_win - 1)
        right_index = col_nr + (self.marks_needed_to_win - 1)
        sequence = self.board.grid.get_row_range(row_nr, left_index, right_index + 1)
        if sequence := self.__is_winning_sequence(sequence, mark):
            return sequence, WinningOptions.horizontal

        # | vertical
        # get top and bottom range of squares +/- marks needed to win
        # top_index < bottom_index
        top_index = row_nr - (self.marks_needed_to_win - 1)
        bottom_index = row_nr + (self.marks_needed_to_win - 1)
        sequence = [self.board.grid[i, col_nr] for i in range(top_index, bottom_index + 1)]
        if sequence := self.__is_winning_sequence(sequence, mark):
            return sequence, WinningOptions.vertical

        # \ negative diagonal
        a = 1
        b = row_nr - a * col_nr
        row = lambda c: (a * c) + b
        left_index = col_nr - (self.marks_needed_to_win - 1)
        right_index = col_nr + (self.marks_needed_to_win - 1)
        sequence = [
            self.board.grid[row(col), col]
            for col in range(left_index, right_index + 1)
        ]
        if sequence := self.__is_winning_sequence(sequence, mark):
            return sequence, WinningOptions.neg_diagonal

        # / positive diagonal
        a = -1
        b = row_nr - a * col_nr
        row = lambda c: (a * c) + b
        left_index = col_nr - (self.marks_needed_to_win - 1)
        right_index = col_nr + (self.marks_needed_to_win - 1)
        sequence = [
            self.board.grid[row(col), col]
            for col in range(left_index, right_index + 1)
        ]
        if sequence := self.__is_winning_sequence(sequence, mark):
            return sequence, WinningOptions.pos_diagonal

        # not found
        return [], ""

    def __check_if_game_ended(self, square):
        sequence, winning_option = self.__check_if_win(square)

        if not sequence:
            return

        # remove squares which are not currently shown
        sequence = [sq for sq in sequence if sq in self.board.squares]

        self.board.draw_strike_through(sequence, winning_option)
        self.__increment_player_score(square.mark)

        Game.wait_for_user_input()
        self.__set_new_round()

    def __set_new_round(self):
        self.move_counter = 0
        Square.reverse_marks()

        self.window.fill(self.bg_color)
        self.board.reset()
        self.board.draw_grid()
        self.score_bar.draw()

    def __increment_player_score(self, mark):
        for player in self.players:
            if player.mark == mark:
                player.score += 1
                return

    def run(self):
        self.__set_new_round()

        while True:
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = pygame.mouse.get_pos()

                    for square in self.board.squares:
                        if not square.is_clicked and square.check_collision(*mouse_pos):
                            self.move_counter += 1
                            square.click(Square.marks[self.move_counter % 2])
                            self.__check_if_game_ended(square)
                            break

                if event.type == pygame.KEYDOWN:
                    # up
                    if event.key in [pygame.K_UP, pygame.K_w]:
                        self.board.move(Direction.up)
                    # down
                    elif event.key in [pygame.K_DOWN, pygame.K_s]:
                        self.board.move(Direction.down)
                    # left
                    elif event.key in [pygame.K_LEFT, pygame.K_a]:
                        self.board.move(Direction.left)
                    # right
                    elif event.key in [pygame.K_RIGHT, pygame.K_d]:
                        self.board.move(Direction.right)

                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()

    @staticmethod
    def wait_for_user_input():
        while True:
            for event in pygame.event.get():
                if (event.type == pygame.MOUSEBUTTONDOWN
                        or event.type == pygame.KEYDOWN):
                    return
