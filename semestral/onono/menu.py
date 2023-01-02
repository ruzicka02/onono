"""
Game manu. By default, the first function to start the game is `run()` from this module.
"""

from datetime import datetime
import sys

import numpy as np
import pygame as pg

if __package__ == "":
    # when imported from __main__
    import savegame
    import app
    import image
    from gui_definitions import \
        COLOR, FONT_NAME, MENU_CAPTION, SCREEN_SIZE, \
        MENU_INITIAL_COORDS, MENU_ITEM, MENU_MARGIN
else:
    # when imported from __init__
    from . import savegame, app, image
    from .gui_definitions import \
        COLOR, FONT_NAME, MENU_CAPTION, SCREEN_SIZE, \
        MENU_INITIAL_COORDS, MENU_ITEM, MENU_MARGIN

GAME_INFO = ["Created by Simon Ruzicka @ FIT CTU, 2022",
             "",
             "Game Guide:",
             "Color the squares by using your mouse buttons",
             "Use the hints on the left and top to solve puzzles"]


def prepare_screen() -> pg.Surface:
    """
    Initiates the game screen and sets caption.
    """
    pg.init()
    screen = pg.display.set_mode(SCREEN_SIZE)
    pg.display.set_caption(MENU_CAPTION)

    return screen


def run():
    """
    Main loop function for the game menu.
    """
    pg.font.init()
    font_h1 = pg.font.Font(FONT_NAME, 100)
    font_h2 = pg.font.Font(FONT_NAME, 50)

    event_data = {
        "buttons": ["Play Now", "Load Game", "Load from Image", "Info", "Quit Game"],
        "button_clicked": None,  # stores number of selected button (0, 1, ..., n - 1)
        "button_hover": None,
        "menu": "default",
        "info": False,
        "screen": prepare_screen()
    }

    while True:
        # sets the game to 30 FPS... sleep for 33 ms
        pg.time.wait(33)

        get_events(event_data)

        handle_click(event_data)

        screen = event_data["screen"]
        screen.fill(COLOR["background"])

        text = font_h1.render("Onono!", True, COLOR["full"], COLOR["background"])
        center_shift = (SCREEN_SIZE[0] - text.get_width()) / 2
        screen.blit(text, (center_shift, 100))

        subtitle = get_subtitle(event_data)
        text = font_h2.render(subtitle, True, COLOR["full"], COLOR["background"])
        center_shift = (SCREEN_SIZE[0] - text.get_width()) / 2
        screen.blit(text, (center_shift, 200))

        if event_data["info"]:
            draw_info(event_data)
            continue

        menu_items = get_menu_items(event_data)
        draw_menu_items(menu_items, event_data)

        # refresh screen
        pg.display.flip()


def draw_info(data: dict):
    """
    Draws the info screen.
    """
    font = pg.font.Font(FONT_NAME, 20)

    coords = np.array(MENU_INITIAL_COORDS)
    for line in GAME_INFO:
        text = font.render(line, True, COLOR["black"], COLOR["background"])
        data["screen"].blit(text, coords)
        coords[1] += MENU_ITEM[1]
    pg.display.flip()
    pg.time.wait(5000)  # 5 seconds
    data["info"] = False


def draw_menu_items(items: list, data: dict):
    """
    Draws the menu items given in a list.
    """
    font = pg.font.Font(FONT_NAME, 25)

    coords = MENU_INITIAL_COORDS + np.array(MENU_MARGIN)
    i = 0
    for item in items:
        color = COLOR["full"] if i == data["button_hover"] else COLOR["black"]
        text = font.render(item, True, color, COLOR["background"])
        data["screen"].blit(text, coords)
        coords[1] += MENU_ITEM[1]
        i += 1


def get_menu_items(data: dict) -> list:
    """
    Loads the needed menu items based on `menu` parameter in the given dictionary.
    """
    if data["menu"] == "default":
        return data["buttons"]

    if data["menu"] == "load_save":
        return savegame.get_savegames()

    if data["menu"] == "load_img":
        return image.get_images()

    if data["menu"] == "save_prompt":
        return ["Save Game", "Don't Save"]

    return []


def get_subtitle(data: dict) -> str:
    """
    Loads the needed game subtitle based on `menu` parameter in the given dictionary.
    """
    if data["menu"] == "save_prompt":
        return "Save Game!"

    if data["menu"] in ["load_save", "load_img"]:
        return "Load Game!"

    return "The Puzzle Game"


def get_events(data: dict):
    """
    Loads all pygame inputs.
    """
    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            sys.exit(1)
        if event.type == pg.MOUSEBUTTONDOWN and event.__dict__["button"] == 1:
            register_mouse(data, event, True)
        if event.type == pg.MOUSEMOTION:
            register_mouse(data, event, False)


def register_mouse(data: dict, event: pg.event, click: bool):
    """
    Register mouse movements, activate hover effect and detect potential click.
    """
    pos = np.array(event.__dict__["pos"])
    pos = (pos - MENU_INITIAL_COORDS)
    pos_item = pos // MENU_ITEM
    pos %= MENU_ITEM

    max_buttons = len(get_menu_items(data))

    # outside of menu items
    if pos_item[1] not in range(max_buttons) or pos_item[0] != 0:
        data["button_hover"] = None
        return

    # menu item margins... still appear as hover
    if pos[1] < MENU_MARGIN[1] or pos[1] > MENU_ITEM[1] - MENU_MARGIN[1]:
        return

    if click:
        data["button_clicked"] = int(pos_item[1])

    data["button_hover"] = int(pos_item[1])


def handle_click(data: dict):
    """
    Handles the click event from `get_events()` and responds. Detects the various
    clickable elements in the game window.
    """
    selected = data["button_clicked"]

    if selected is None:
        return

    # only non-default menu is when loading a game
    if data["menu"] in ["load_save", "load_img"]:
        load_game(data, selected)
        pg.display.set_caption(MENU_CAPTION)
        selected = None

    if data["menu"] == "save_prompt":
        if selected == 0:
            stamp = datetime.now()
            data["game"].save_game(str(stamp))
        data["menu"] = "default"
        selected = None

    # play (random save)
    if selected == 0:
        data["game"] = app.run(data["screen"])  # run the game
        pg.display.set_caption(MENU_CAPTION)
        data["menu"] = "save_prompt"

    # load game
    elif selected == 1:
        data["menu"] = "load_save"
    # load game from image
    elif selected == 2:
        data["menu"] = "load_img"
    # info
    elif selected == 3:
        data["info"] = True
    # quit game
    elif selected == 4:
        pg.quit()
        sys.exit(0)

    data["button_clicked"] = None


def load_game(data: dict, selected: int):
    """
    Loads the game at given position in the list. Based on parameter *menu* in data dict, looks for an image
    or a text file in the saves/ directory.
    """
    load_image = data["menu"] == "load_img"
    game = savegame.SaveGame()
    if load_image:
        success = game.load_from_image(get_menu_items(data)[selected])
        if success:
            app.run(data["screen"], game)
        else:
            app.run(data["screen"])
    else:
        success = game.load_game(get_menu_items(data)[selected])
        if success:
            app.run(data["screen"], game)
        else:
            app.run(data["screen"])

    data["menu"] = "default"
