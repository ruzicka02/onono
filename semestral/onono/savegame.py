import numpy as np
from pathlib import Path


class SaveGame:
    """
    Stores the state of the game board, especially important when loading/saving the game.
    """
    def __init__(self, dims: tuple = (10, 10)):
        self.board = np.zeros(dims, bool)
        self.guesses = np.zeros(dims, int)  # 0 => empty; 1 => X; 2 => full
        self.x = np.array([0])
        self.y = np.array([0])

        self.overwrite_lengths()

    def load_game(self, name: str) -> bool:
        """
        Loads a text file in the `saves` directory and stores the data into the board.
        """
        name += ".csv"
        path = Path(__file__).parent.parent
        path = (path / 'saves' / name).resolve()
        try:
            self.board = np.loadtxt(path, dtype=bool, delimiter=',')
            self.overwrite_lengths()
            return True
        except (FileNotFoundError, ValueError):
            return False

    def save_game(self, name: str):
        """
        Saves the data from the board into a text file in the `saves` directory.
        """
        name += ".csv"
        path = Path(__file__).parent.parent
        path = (path / 'saves' / name).resolve()

        # X expects type `int` for some reason
        # noinspection PyTypeChecker
        np.savetxt(path, X=self.board, fmt='%.0d', delimiter=',')

    def calculate_lengths(self, transposed: bool):
        """
        Calculates and overwrites the lengths at x or y-axis on the board.

        Returns a list of lists due to varying lengths.
        """
        board = self.board.transpose() if transposed else self.board
        result = []

        for row in board:
            counter = 0
            row_vector = []

            for pos in row:
                if pos:
                    counter += 1
                elif counter > 0:
                    row_vector.append(counter)
                    counter = 0

            if len(row_vector) == 0 or counter != 0:
                row_vector.append(counter)  # will be last number or 0
            result.append(row_vector)

        return result

    def overwrite_lengths(self):
        """
        Uses `calculate_lengths` to set both x and y-axis length vectors.
        """
        self.x = self.calculate_lengths(True)
        self.y = self.calculate_lengths(False)

    def randomize(self, prob: float = 0.5):
        """
        Randomizes the board while keeping the same dimensions. Optional parameter of probability of any field
        being True (between 0 and 1).
        """
        assert 0 <= prob <= 1, "Probability parameter not in range <0, 1>"
        dims = self.board.shape
        self.board = np.random.rand(*dims) < prob

        self.overwrite_lengths()

    def get_solution(self, overwrite: bool = False):
        """
        Takes the correct solution and converts it into format of matrix of guesses. If the overwrite parameter
        is set as `True`, the result overwrites the current guesses inside the object.
        """
        guesses = 1 + self.board

        if overwrite:
            self.guesses = guesses

        return guesses
