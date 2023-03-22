"""
Implements various functions for logic of the game.
"""

import numpy as np

if __package__ == "":
    # when imported from __main__
    import savegame
else:
    # when imported from __init__
    from . import savegame


def change_field(game: savegame.SaveGame, pos: np.ndarray, button: int):
    """
    Change value of one field in game board (guesses). Used when the field is clicked by player.
    """
    if button not in [1, 3]:
        return

    col, row = int(pos[0]), int(pos[1])

    left_click = button == 1
    current_state = game.guesses[row, col]

    if left_click:
        game.guesses[row, col] = 2 if current_state != 2 else 0
    else:
        game.guesses[row, col] = 1 if current_state != 1 else 0


def validate_game(game: savegame.SaveGame) -> bool:
    """
    Check if the game is finished. In case of an exact match, rows/columns are not checked at all.
    Otherwise, function iterates over rows/columns and sets the data about their "completeness".
    This feature is used when coloring the hints for completed rows.
    """
    reference = game.get_solution(False)
    solution = game.guesses.copy()

    # replace all `no guess` (0) to `X` (1)
    solution[solution == 0] = 1

    # quick check... equality
    if np.array_equal(reference, solution):
        return True

    # check by iterating the matrix
    dims = solution.shape
    is_correct = True

    for row, i in zip(solution, range(dims[0])):
        row_complete = validate_row(row, game.y[i])
        is_correct = row_complete and is_correct  # one False will set is_correct = False

        game.y[i] = game.y[i][0], row_complete  # overwrite in case this was not fulfilled before

    for col, i in zip(solution.T, range(dims[1])):
        col_complete = validate_row(col, game.x[i])
        is_correct = col_complete and is_correct

        game.x[i] = game.x[i][0], col_complete

    return is_correct


def validate_row(row: np.ndarray, hints: tuple) -> bool:
    """
    Check one row/column.
    """
    vector, _ = hints

    vector_guess = savegame.vector_to_hints(row - 1)
    return np.array_equal(vector, vector_guess)
