

class Player:
    def __init__(self, mark: str, score: int):
        """
        :param mark: representation of the player on the board. eg. 'X' or 'O'
        :param score: initial score value
        """
        self.mark = mark
        self.score = score
