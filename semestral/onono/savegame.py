import numpy as np
from pathlib import Path

if __package__ == "":
    # when imported from __main__
    import image
else:
    # when imported from __init__
    from . import image


class SaveGame:
    """
    Stores the state of the game board, especially important when loading/saving the game.
    """
    def __init__(self, dims: tuple = (10, 10)):
        self.board = np.zeros(dims, bool)
        self.guesses = np.zeros(dims, int)  # 0 => empty; 1 => X; 2 => full
        self.x = []  # list of row vectors and whether the guesses are complete
        self.y = []  # eg. [([1, 2, 3], False), ([10], True), ([0], True)]

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

    def load_from_image(self, image_name: str, dims: tuple = (10, 10), percent_filled: float = 0.7) -> bool:
        board = image.load_image(image_name, dims, percent_filled)
        if board is not None:
            self.board = board
            self.overwrite_lengths()

        return board is not None

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
            hints = vector_to_hints(row)
            result.append((hints, hints == [0]))

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


def vector_to_hints(vector: np.ndarray) -> list:
    """
    Takes an array of numbers and converts it into a list of hints.
    """
    counter = 0
    row_vector = []

    for pos in vector:
        if pos:
            counter += 1
        elif counter > 0:
            row_vector.append(counter)
            counter = 0

    if len(row_vector) == 0 and counter == 0:
        row_vector.append(0)  # no numbers in row/column
    elif counter != 0:
        row_vector.append(counter)  # will be last number

    return row_vector


def get_savegames():
    """
    Opens the `saves` directory and returns the list of all save games.
    """
    path = Path(__file__).parent.parent
    path = (path / 'saves').resolve().glob("*.csv")
    return [x.stem for x in path if x.is_file()]
