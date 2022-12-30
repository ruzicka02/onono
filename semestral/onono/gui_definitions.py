import numpy as np
import pygame as pg

COLOR = {
    "background": "#FFFFFF",
    "empty": "#AAAAAA",
    "full": "#F0AB00",
    "x-placeholder": "#000000",
    "black": "#000000"
}

FONT_NAME = pg.font.get_default_font()
FONT_NAME_MONO = pg.font.match_font("notomono")
if FONT_NAME_MONO == '':  # fallback font
    FONT_NAME_MONO = FONT_NAME

MENU_CAPTION = "Onono! The Puzzle Game - Menu"
GAME_CAPTION = "Onono! The Puzzle Game"

SCREEN_SIZE = [600, 700]

MENU_INITIAL_COORDS = [50., 300.]
MENU_ITEM = [300., 50.]
MENU_MARGIN = [0., 10.]

BLOCK_SIZE = np.array([45., 45.])
BLOCK_MARGIN = np.array([1., 1.])
GAME_INITIAL_COORDS = [110., 210.]
