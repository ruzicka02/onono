import os
import numpy as np
import pytest
import pyautogui
import subprocess
from time import sleep

from onono.gui_definitions import MENU_ITEM, MENU_INITIAL_COORDS, COLOR
# import onono.app

pyautogui.PAUSE = 1

os.environ['SDL_VIDEO_WINDOW_POS'] = "100,100"


def test_exit_button():
    with subprocess.Popen(["python", "onono"]) as proc:
        sleep(1)
        assert proc.poll() is None  # game is still running

        # exit button
        pyautogui.click(x=110 + MENU_INITIAL_COORDS[0], y=110 + MENU_INITIAL_COORDS[1] + (5 * MENU_ITEM[1]))
        assert proc.poll() == 0  # game is not running anymore


def test_force_exit():
    with subprocess.Popen(["python", "onono"]) as proc:
        sleep(1)
        assert proc.poll() is None  # game is still running

        proc.terminate()
        sleep(1)
        assert proc.poll() == 1  # game is not running anymore


def test_info():
    with subprocess.Popen(["python", "onono"]) as proc:
        sleep(1)

        # info button
        pyautogui.click(x=110 + MENU_INITIAL_COORDS[0], y=110 + MENU_INITIAL_COORDS[1] + (4 * MENU_ITEM[1]))
        assert proc.poll() is None  # game is still running

        # exit button - not working while info is displayed
        pyautogui.click(x=110 + MENU_INITIAL_COORDS[0], y=110 + MENU_INITIAL_COORDS[1] + (5 * MENU_ITEM[1]))
        sleep(1)
        assert proc.poll() is None  # game is still running

        sleep(5)
        # exit button working now
        pyautogui.click(x=110 + MENU_INITIAL_COORDS[0], y=110 + MENU_INITIAL_COORDS[1] + (5 * MENU_ITEM[1]))
        assert proc.poll() == 0  # game is not running anymore


def test_hover():
    color_full = tuple(int(COLOR["full"].strip('#')[i:i+2], 16) for i in (0, 2, 4))
    color_empty = tuple(int(COLOR["empty"].strip('#')[i:i + 2], 16) for i in (0, 2, 4))

    with subprocess.Popen(["python", "onono"]) as proc:
        sleep(1)

        # does not work on Linux
        # assert pyautogui.pixelMatchesColor(150, 450, color_empty)
        pyautogui.moveTo(150, 450)
        # assert pyautogui.pixelMatchesColor(150, 450, color_full)

        # hover should be visible by human eye
        pyautogui.moveTo(150, 200)
        pyautogui.moveTo(150, 700, 3)

        proc.terminate()
