import numpy as np
import pygame as pg

if __package__ == "":
    # when imported from __main__
    import savegame
    import app
    from gui_definitions import *
else:
    # when imported from __init__
    from . import savegame, app
    from .gui_definitions import *


def run():
    pg.init()
    screen = pg.display.set_mode(SCREEN_SIZE)
    pg.display.set_caption("Onono! The Puzzle Game - Menu")

    pg.font.init()
    font_h1 = pg.font.Font(FONT_NAME, 100)
    font_h2 = pg.font.Font(FONT_NAME, 50)
    font = pg.font.Font(FONT_NAME, 25)

    event_data = {
        "running": True,
        "buttons": ["Play", "Lorem", "Ipsum Dolor Sit Amet"],
        "button_clicked": None,  # stores number of selected button (0, 1, ..., n - 1)
        "button_hover": None,
        "screen": screen
    }

    while event_data["running"]:
        # sets the game to 30 FPS... sleep for 33 ms
        pg.time.wait(33)

        get_events(event_data)

        interpret_click(event_data)

        screen.fill(COLOR["background"])

        text = font_h1.render("Onono!", True, COLOR["full"], COLOR["background"])
        center_shift = (SCREEN_SIZE[0] - text.get_width()) / 2
        screen.blit(text, (center_shift, 100))
        text = font_h2.render("The Puzzle Game", True, COLOR["full"], COLOR["background"])
        center_shift = (SCREEN_SIZE[0] - text.get_width()) / 2
        screen.blit(text, (center_shift, 200))

        coords = MENU_INITIAL_COORDS + np.array(MENU_MARGIN)

        i = 0
        for item in event_data["buttons"]:
            color = COLOR["full"] if i == event_data["button_hover"] else COLOR["black"]
            text = font.render(item, True, color, COLOR["background"])
            screen.blit(text, coords)
            coords[1] += MENU_ITEM[1]
            i += 1

        # refresh screen
        pg.display.flip()

    pg.quit()


def get_events(data: dict):
    for event in pg.event.get():
        if event.type == pg.QUIT:
            data["running"] = False
        if event.type == pg.MOUSEBUTTONDOWN and event.__dict__["button"] == 1:
            register_mouse(data, event, True)
        if event.type == pg.MOUSEMOTION:
            register_mouse(data, event, False)


def register_mouse(data: dict, event: pg.event, click: bool):
    pos = np.array(event.__dict__["pos"])
    pos = (pos - MENU_INITIAL_COORDS)
    pos_item = pos // MENU_ITEM
    pos %= MENU_ITEM

    if pos_item[1] not in range(len(data["buttons"])) or pos_item[0] != 0:
        data["button_hover"] = None
        return

    if pos[1] < MENU_MARGIN[1] or pos[1] > MENU_ITEM[1] - MENU_MARGIN[1]:
        return

    if click:
        data["button_clicked"] = int(pos_item[1])

    data["button_hover"] = int(pos_item[1])




def interpret_click(data: dict):
    selected = data["button_clicked"]

    # play
    if selected is None:
        return
    elif selected == 0:
        pg.quit()
        app.run()
        exit(0)
