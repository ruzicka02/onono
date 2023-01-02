"""
Definitions for various GUI elements to be used in other game modules.
"""

from pathlib import Path

import numpy as np

COLOR = {
    "background": "#FFFFFF",
    "empty": "#AAAAAA",
    "full": "#F0AB00",
    "x-placeholder": "#000000",
    "black": "#000000"
}

# Both fonts are available with an open source licence.
# Comic Neue Regular http://comicneue.com/
# Noto Mono Regular https://fonts.adobe.com/fonts/noto-mono#fonts-section
FONT_PATH = (Path(__file__).parent.parent / "data" / "fonts" / "ComicNeue-Regular.ttf").resolve()
FONT_MONO_PATH = (Path(__file__).parent.parent / "data" / "fonts" / "NotoMono-Regular.ttf").resolve()

MENU_CAPTION = "Onono! The Puzzle Game - Menu"
GAME_CAPTION = "Onono! The Puzzle Game"

SCREEN_SIZE = [600, 700]

MENU_INITIAL_COORDS = [50., 300.]
MENU_ITEM = [300., 50.]
MENU_MARGIN = [0., 10.]

BLOCK_SIZE = np.array([45., 45.])
BLOCK_MARGIN = np.array([1., 1.])
GAME_INITIAL_COORDS = [110., 210.]
