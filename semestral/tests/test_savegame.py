import numpy as np
import filecmp
import os
import pytest

import onono.savegame
from onono.savegame import SaveGame


def test_pytest():
    print("Check, one two")
    savegame = SaveGame()
    print(savegame.board)


@pytest.mark.parametrize('name, valid',
                         [("valid", True), ("invalid1", False), ("invalid2", False), ("invalid3", False)])
def test_load_game(name, valid):
    name = "tests/" + name
    save = onono.savegame.SaveGame()
    assert save.load_game(name) == valid


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
