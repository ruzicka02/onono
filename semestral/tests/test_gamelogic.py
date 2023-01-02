import numpy as np

import onono.savegame
import onono.gamelogic


def test_change_field():
    save = onono.savegame.SaveGame()
    pos = np.array((0, 0))  # does not really matter - can be anywhere

    assert save.guesses[pos[0], pos[1]] == 0

    onono.gamelogic.change_field(save, pos, 1)
    assert save.guesses[pos[0], pos[1]] == 2

    onono.gamelogic.change_field(save, pos, 1)
    assert save.guesses[pos[0], pos[1]] == 0

    onono.gamelogic.change_field(save, pos, 3)
    assert save.guesses[pos[0], pos[1]] == 1

    onono.gamelogic.change_field(save, pos, 1)
    assert save.guesses[pos[0], pos[1]] == 2


def test_validate_filled():
    dims = (10, 10)
    save = onono.savegame.SaveGame(dims)
    save.randomize()
    save.get_solution(True)  # overwrite the guesses to correct

    # the game is surely correctly filled in
    validate_asserts(save, True)


def test_validate_incorrect():
    dims = (1000, 1000)  # bigger board for less likely random match
    save = onono.savegame.SaveGame(dims)
    save.randomize(0.5)
    save.get_solution(True)  # overwrite the guesses
    save.randomize(0.5)

    # the games cannot possibly be identical, not even have identical rows and columns
    validate_asserts(save, False)


def test_validate_empty():
    dims = (1000, 1000)
    save = onono.savegame.SaveGame(dims)
    save.randomize(0.8)

    # empty guesses... the game is surely has some non-empty fields in every row and column as well
    validate_asserts(save, False)


def test_validate_diagonal():
    """
    Testing puzzle which has MANY solutions.
    """
    name = "tests/diagonal"
    save = onono.savegame.SaveGame()
    assert save.load_game(name)

    save.get_solution(True)

    for i in range(save.board.shape[0]):
        validate_asserts(save, True)
        save.guesses = np.roll(save.guesses, 1, axis=0)

    for i in range(save.board.shape[1]):
        validate_asserts(save, True)
        save.guesses = np.roll(save.guesses, 1, axis=1)


def validate_asserts(save: onono.savegame.SaveGame, valid: bool):
    """
    Used as a part of validation tests. Checks both functions `validate_game` and `validate_row`.
    """
    assert onono.gamelogic.validate_game(save) == valid

    dims = save.board.shape
    for row, i in zip(save.guesses, range(dims[0])):
        assert onono.gamelogic.validate_row(row, save.y[i]) == valid

    for col, i in zip(save.guesses.T, range(dims[1])):
        assert onono.gamelogic.validate_row(col, save.x[i]) == valid
