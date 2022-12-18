import numpy as np
import pygame as pg
from datetime import datetime

if __package__ == "":
    import savegame, gamelogic
else:
    from . import savegame, gamelogic

COLOR = {
    "background": "#FFFFFF",
    "empty": "#AAAAAA",
    "full": "#F0AB00",
    "x-placeholder": "#000000",
    "black": "#000000"
}

FONT_NAME = pg.font.get_default_font()
try:
    FONT_NAME_MONO = pg.font.match_font("notomono")
except:
    FONT_NAME_MONO = FONT_NAME


BLOCK_SIZE = np.array([45., 45.])
BLOCK_MARGIN = np.array([1., 1.])
INITIAL_COORDS = [110., 210.]
SCREEN_SIZE = [600, 700]


def run():
    game = prepare_game()

    pg.init()
    screen = pg.display.set_mode(SCREEN_SIZE)
    pg.display.set_caption("Onono! The Puzzle Game")

    pg.font.init()
    font = pg.font.Font(FONT_NAME, 50)
    font_mono = pg.font.Font(FONT_NAME_MONO, 50)

    event_data = {
        "running": True,
        "game": game,
        "screen": screen
    }

    # todo... can be replaced with pg.time
    start_time = datetime.now()

    while event_data["running"]:
        get_events(event_data)

        screen.fill(COLOR["background"])

        header_text = font.render("Onono!", 1, False)
        screen.blit(header_text, (50, 20))

        draw_game(screen, game)

        time_sec = (datetime.now() - start_time).seconds
        time_text = font_mono.render(f"{time_sec // 60:02d}:{time_sec % 60:02d}", 1, False)
        time_pos = np.array([SCREEN_SIZE[0] - font_mono.size("00:00  ")[0], 10])
        screen.blit(time_text, time_pos)

        # refresh screen
        pg.display.flip()

        # do not refresh if no click happens
        # todo... can possibly be further optimized
        pg.event.wait(timeout=1)

    pg.quit()


def prepare_game() -> savegame.SaveGame:
    """
    Helper function for showcase of board drawing.
    """
    s = savegame.SaveGame((10, 10))
    s.randomize(0.8)
    return s


def get_events(data: dict):
    for event in pg.event.get():
        if event.type == pg.QUIT:
            data["running"] = False

    # todo... resolve mouse events
    # pg.mouse.get_pressed(num_buttons=3) -> (button1, button2, button3)


def draw_game(screen: pg.Surface, game: savegame.SaveGame):
    dims = game.board.shape
    assert len(dims) == 2, "Board has to be a 2D array."
    assert dims[0] <= 10 and dims[1] <= 10, "Board has to be 10 x 10 or smaller."

    coords = list(INITIAL_COORDS)  # creates a copy

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

        coords[0] = INITIAL_COORDS[0]  # CR
        coords[1] += BLOCK_SIZE[1]  # LF

    coords = list(INITIAL_COORDS)
    coords = [coords[0] + 0.4 * BLOCK_SIZE[0], coords[1]]
    for lengths in game.x:
        draw_vector(np.array(coords), lengths, screen, True)
        coords[0] += BLOCK_SIZE[0]
        coords[1] = list(INITIAL_COORDS)[1]


def draw_vector(coords: np.ndarray, lengths: list, screen: pg.Surface, vertical: bool):
    font = pg.font.Font(FONT_NAME_MONO, 15)
    delta = np.array([0., -font.get_linesize()]) if vertical else np.array([-font.size("10")[0], 0.])

    for num in lengths[::-1]:
        if num >= 10 and not vertical:
            coords += 1.3 * delta
        else:
            coords += delta
        num_surface = font.render(str(num), 1, False)
        screen.blit(num_surface, list(coords))
