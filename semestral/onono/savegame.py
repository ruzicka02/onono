import numpy as np
from pathlib import Path


class SaveGame:
    """
    Stores the state of the game board, especially important when loading/saving the game.
    """
    def __init__(self, dims: tuple = (5, 5)):
        self.board = np.zeros(dims, bool)
        self.x = np.zeros(dims[0], int)
        self.y = np.zeros(dims[0], int)
        self.calculate_sums()

    def load_game(self, name: str) -> bool:
        """
        Loads a text file in the `saves` directory and stores the data into the board.
        """
        path = Path(__file__).parent.parent
        path = (path / 'saves' / name).resolve()
        try:
            self.board = np.loadtxt(path, dtype=bool, delimiter=',')
            self.calculate_sums()
            return True
        except FileNotFoundError:
            return False

    def save_game(self, name: str):
        """
        Saves the data from the board into a text file in the `saves` directory.
        """
        path = Path(__file__).parent.parent
        path = (path / 'saves' / name).resolve()

        # X expects type `int` for some reason
        # noinspection PyTypeChecker
        np.savetxt(path, X=self.board, fmt='%.0d', delimiter=',')

    def calculate_sums(self):
        """
        Calculates and overwrites the sums at x and y axis on the board.
        """
        self.x = self.board.sum(axis=0)
        self.y = self.board.sum(axis=1)
        return self.x, self.y

    def randomize(self, prob: float = 0.5):
        """
        Randomizes the board while keeping the same dimensions. Optional parameter of probability of any field
        being True (between 0 and 1).
        """
        assert(0 <= prob <= 1, "Probability parameter not in range <0, 1>")
        dims = self.board.shape
        self.board = np.random.rand(*dims) < prob

        self.calculate_sums()
