"""
GUI module for running the game itself. Function `run()` can be launched from menu
or on its own, with an optional parameter of SaveGame object.
"""
import time
import sys

import numpy as np
import pygame as pg

if __package__ == "":
    # when imported from __main__
    import savegame
    import gamelogic
    from gui_definitions import \
        COLOR, FONT_PATH, FONT_MONO_PATH, GAME_CAPTION, SCREEN_SIZE, \
        GAME_INITIAL_COORDS, BLOCK_SIZE, BLOCK_MARGIN
else:
    # when imported from __init__
    from . import savegame, gamelogic
    from .gui_definitions import \
        COLOR, FONT_PATH, FONT_MONO_PATH, GAME_CAPTION, SCREEN_SIZE, \
        GAME_INITIAL_COORDS, BLOCK_SIZE, BLOCK_MARGIN


def run(screen: pg.Surface = None, game: savegame.SaveGame = None):
    """
    Start the game window. Gets two parameters - pygame screen and SaveGame object. If they
    are not given, they are newly created within this function (new game is randomly generated).
    """
    no_screen = screen is None
    if no_screen:
        pg.init()
        screen = pg.display.set_mode(SCREEN_SIZE)

    if game is None:
        game = prepare_game()

    pg.display.set_caption(GAME_CAPTION)

    pg.font.init()
    font = pg.font.Font(FONT_PATH, 50)

    event_data = {
        "win": False,
        "mouse_button": None,
        "last_position": np.array([-1, -1]),
        "show_timer": False,
        "start": time.time(),
        "game": game,
        "screen": screen,
        "started_without_screen": no_screen  # screen that was created here will be shut down
    }

    while True:
        # sets the game to 30 FPS... sleep for 33 ms
        pg.time.wait(33)

        get_events(event_data)

        if gamelogic.validate_game(game):
            draw_game(screen, game)
            end_game(event_data)
            return game  # used when saving generated game

        screen.fill(COLOR["background"])
        header_text = font.render("Onono!", True, COLOR["full"], COLOR["background"])
        screen.blit(header_text, (50, 20))

        draw_game(screen, game)
        draw_timer(event_data)

        # refresh screen
        pg.display.flip()


def prepare_game() -> savegame.SaveGame:
    """
    Helper function for randomly generating a SaveGame.
    """
    s = savegame.SaveGame((10, 10))
    s.randomize(0.8)
    return s


def get_events(data: dict):
    """
    Loads all pygame inputs.
    """
    mouse_event = None
    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            sys.exit(1)
        if event.type == pg.MOUSEBUTTONDOWN and event.__dict__["button"] in [1, 3]:
            data["mouse_button"] = event.__dict__["button"]
            mouse_event = event
        if event.type == pg.MOUSEMOTION:
            mouse_event = event
        if event.type == pg.MOUSEBUTTONUP and event.__dict__["button"] in [1, 3]:
            data["mouse_button"] = None
            data["last_position"] = np.array([-1, -1])

        if data["mouse_button"] is not None and mouse_event is not None:
            handle_click(mouse_event, data)


def handle_click(click: pg.event.Event, data: dict):
    """
    Handles the click event from `get_events()` and responds. Detects the various
    clickable elements in the game window.
    """
    pos = np.array(click.__dict__["pos"])

    # timer toggle
    if pos[0] > SCREEN_SIZE[0] - 200 and pos[1] < 50 and data["mouse_button"] == 1:
        data["show_timer"] = not data["show_timer"]
        data["mouse_button"] = None  # gets switched back immediately otherwise
        return

    pos = (pos - GAME_INITIAL_COORDS) // BLOCK_SIZE

    # solves the game... remove for production
    if pos[0] == pos[1] == -1:
        data["game"].get_solution(True)

    if (pos == data["last_position"]).sum() == 2:
        return

    data["last_position"] = pos
    button = data["mouse_button"]

    # debug data... logging clicks to terminal
    # print(pos, button)

    dims = data["game"].board.shape
    if pos[0] in range(dims[0]) and pos[1] in range(dims[1]):
        gamelogic.change_field(data["game"], pos, button)


def draw_game(screen: pg.Surface, game: savegame.SaveGame):
    """
    Draws the game board tiles and the connected hints.
    """
    dims = game.board.shape
    assert len(dims) == 2, "Board has to be a 2D array."
    assert dims[0] <= 10 and dims[1] <= 10, "Board has to be 10 x 10 or smaller."

    coords = list(GAME_INITIAL_COORDS)  # creates a copy

    for row, lengths in zip(game.guesses, game.y):
        lengths_coords = (coords[0], coords[1] + (0.4 * BLOCK_SIZE[1]))
        draw_vector(np.array(lengths_coords), lengths, screen, False)

        for pos in row:
            pg.draw.rect(screen, COLOR["black"], (*(coords - BLOCK_MARGIN), *(BLOCK_SIZE + 2 * BLOCK_MARGIN)))

            if pos == 0:
                color = COLOR["empty"]
            elif pos == 1:
                color = COLOR["x-placeholder"]
            else:
                color = COLOR["full"]
            pg.draw.rect(screen, color, (*(coords + BLOCK_MARGIN), *(BLOCK_SIZE - 2 * BLOCK_MARGIN)))
            coords[0] += BLOCK_SIZE[0]

        coords[0] = GAME_INITIAL_COORDS[0]  # CR
        coords[1] += BLOCK_SIZE[1]  # LF

    coords = list(GAME_INITIAL_COORDS)
    coords = [coords[0] + 0.4 * BLOCK_SIZE[0], coords[1]]
    for lengths in game.x:
        draw_vector(np.array(coords), lengths, screen, True)
        coords[0] += BLOCK_SIZE[0]
        coords[1] = list(GAME_INITIAL_COORDS)[1]


def draw_vector(coords: np.ndarray, vector: (list, bool), screen: pg.Surface, vertical: bool):
    """
    Draws one vector of hints to the game screen.
    """
    text, complete = vector
    font = pg.font.Font(FONT_MONO_PATH, 15)
    color = COLOR["full"] if complete else COLOR["black"]
    delta = np.array([0., -font.get_linesize()]) if vertical else np.array([-font.size("10")[0], 0.])

    for num in text[::-1]:
        if num >= 10 and not vertical:
            coords += 1.3 * delta
        else:
            coords += delta
        num_surface = font.render(str(num), True, color)
        screen.blit(num_surface, list(coords))


def draw_timer(data: dict):
    """
    Draws the timer (or text "Show timer") to the game screen.
    """
    show = data["show_timer"]

    if show:
        font = pg.font.Font(FONT_MONO_PATH, 50)
        time_sec = int(time.time() - data["start"])
        text = font.render(f"{time_sec // 60:02d}:{time_sec % 60:02d}", True, COLOR["black"])
        pos = np.array([SCREEN_SIZE[0] - font.size("00:00  ")[0], 10])
    else:
        font = pg.font.Font(FONT_PATH, 30)
        text = font.render("Show timer", True, COLOR["empty"])
        pos = np.array([SCREEN_SIZE[0] - font.size("Show timer___")[0], 30])

    data["screen"].blit(text, pos)


def end_game(data: dict):
    """
    Ends the game with a win. Is not started when game window is closed.
    """
    font = pg.font.Font(FONT_PATH, 75)

    text = font.render("Winner!", True, COLOR["full"], COLOR["background"])
    center_shift = (SCREEN_SIZE[0] - text.get_width()) / 2
    data["screen"].blit(text, (center_shift, 100))
    pg.display.flip()
    pg.time.wait(2500)

    if data["started_without_screen"]:
        pg.quit()
