import numpy as np

if __package__ == "":
    # when imported from __main__
    import savegame
else:
    # when imported from __init__
    from . import savegame


def change_field(game: savegame.SaveGame, pos: np.ndarray, button: int):
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
    reference = game.get_solution(False)
    solution = game.guesses.copy()

    # replace all `no guess` (0) to `X` (1)
    solution[solution == 0] = 1

    # quick check... equality
    if np.array_equal(reference, solution):
        return True

    # todo... step by step checking

    return False
