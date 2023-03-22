import filecmp
import os
import pytest

import onono.savegame


@pytest.mark.parametrize('name, valid',
                         [("valid", True),
                          ("invalid1", False),
                          ("invalid2", False),
                          ("invalid3", False),
                          ("miluju_progtest", False)])
def test_load_game(name, valid):
    name = "tests/" + name
    save = onono.savegame.SaveGame()
    assert save.load_game(name) == valid

    if valid:
        assert save.board.shape == save.guesses.shape
        assert save.board.ndim == 2
        x, y = save.board.shape
        assert x == len(save.x) and y == len(save.y)


def test_save_game():
    name = "tests/valid"
    new_name = "tests/temp"

    save = onono.savegame.SaveGame()
    assert save.load_game(name)
    save.save_game(new_name)

    name = "saves/" + name + ".csv"
    new_name = "saves/" + new_name + ".csv"

    assert filecmp.cmp(name, new_name)
    os.remove(new_name)


@pytest.mark.parametrize('prob, ratio_min, ratio_max',
                         [(0.5, 0.1, 0.9),  # i mean, what are the odds...
                          (1, 1, 1),
                          (0, 0, 0)])
def test_randomize(prob, ratio_min, ratio_max):
    dims = (100, 100)
    save = onono.savegame.SaveGame((100, 100))  # bigger board for lower outlier probability
    save.randomize(prob)

    ratio = save.board.sum() / (dims[0] * dims[1])
    assert ratio_min <= ratio <= ratio_max


def test_get_savegames():
    assert len(onono.savegame.get_savegames("tests")) >= 4  # 4 currently used, more can be added later


@pytest.mark.parametrize('name, dims, valid',
                         [("lenna", (10, 10), True),
                          ("lenny", (10, 10), True),
                          ("lenna", (600, 600), False),
                          ("lenny", (600, 600), True),
                          ("tests/invalid1", (10, 10), False),
                          ("tests/miluju_progtest", (10, 10), False)])
def test_image_to_savegame(name, dims, valid):
    save = onono.savegame.SaveGame()

    assert save.load_from_image(name, dims=dims) == valid

    if valid:
        assert save.board.shape == save.guesses.shape
        assert save.board.ndim == 2
        x, y = save.board.shape
        assert x == len(save.x) and y == len(save.y)
