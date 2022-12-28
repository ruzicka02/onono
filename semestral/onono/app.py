import numpy as np
import pygame as pg

if __package__ == "":
    # when imported from __main__
    import savegame
    import gamelogic
    from gui_definitions import *
else:
    # when imported from __init__
    from . import savegame, gamelogic
    from .gui_definitions import *


def run(game: savegame.SaveGame = None):
    if game is None:
        game = prepare_game()

    pg.init()
    screen = pg.display.set_mode(SCREEN_SIZE)
    pg.display.set_caption("Onono! The Puzzle Game")

    pg.font.init()
    font = pg.font.Font(FONT_NAME, 50)

    event_data = {
        "win": False,
        "mouse_button": None,
        "last_position": np.array([-1, -1]),
        "show_timer": False,
        "game": game
    }

    while True:
        # sets the game to 30 FPS... sleep for 33 ms
        pg.time.wait(33)

        get_events(event_data)

        if gamelogic.validate_game(game):
            draw_game(screen, game)
            end_game(screen)
            return

        screen.fill(COLOR["background"])
        header_text = font.render("Onono!", 1, COLOR["full"], COLOR["background"])
        screen.blit(header_text, (50, 20))

        draw_game(screen, game)
        draw_timer(screen, event_data)

        # refresh screen
        pg.display.flip()


def prepare_game() -> savegame.SaveGame:
    """
    Helper function for showcase of board drawing.
    """
    s = savegame.SaveGame((10, 10))
    s.randomize(0.8)
    return s


def get_events(data: dict):
    mouse_event = None
    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            exit(1)
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
    pos = np.array(click.__dict__["pos"])

    # timer toggle
    if pos[0] > SCREEN_SIZE[0] - 200 and pos[1] < 50 and data["mouse_button"] == 1:
        data["show_timer"] = not data["show_timer"]
        data["mouse_button"] = None  # gets switched back immediately otherwise
        return

    pos = (pos - GAME_INITIAL_COORDS) // BLOCK_SIZE

    # fixme... solves the game
    if pos[0] == pos[1] == -1:
        data["game"].get_solution(True)

    if (pos == data["last_position"]).sum() == 2:
        return
    else:
        data["last_position"] = pos

    button = data["mouse_button"]

    # debug data... logging clicks to terminal
    # print(pos, button)

    dims = data["game"].board.shape
    if pos[0] in range(dims[0]) and pos[1] in range(dims[1]):
        gamelogic.change_field(data["game"], pos, button)


def draw_game(screen: pg.Surface, game: savegame.SaveGame):
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
    text, complete = vector
    font = pg.font.Font(FONT_NAME_MONO, 15)
    color = COLOR["full"] if complete else COLOR["black"]
    delta = np.array([0., -font.get_linesize()]) if vertical else np.array([-font.size("10")[0], 0.])

    for num in text[::-1]:
        if num >= 10 and not vertical:
            coords += 1.3 * delta
        else:
            coords += delta
        num_surface = font.render(str(num), True, color)
        screen.blit(num_surface, list(coords))


def draw_timer(screen: pg.Surface, data: dict):
    show = data["show_timer"]

    if show:
        font = pg.font.Font(FONT_NAME_MONO, 50)
        time_sec = pg.time.get_ticks() // 1000
        text = font.render(f"{time_sec // 60:02d}:{time_sec % 60:02d}", True, COLOR["black"])
        pos = np.array([SCREEN_SIZE[0] - font.size("00:00  ")[0], 10])
    else:
        font = pg.font.Font(FONT_NAME, 30)
        text = font.render("Show timer", True, COLOR["empty"])
        pos = np.array([SCREEN_SIZE[0] - font.size("Show timer___")[0], 30])

    screen.blit(text, pos)


def end_game(screen: pg.Surface):
    """
    Ends the game with a win. Is not started when game window is closed.
    """
    font = pg.font.Font(FONT_NAME, 75)

    text = font.render("Winner!", 1, COLOR["full"], COLOR["background"])
    center_shift = (SCREEN_SIZE[0] - text.get_width()) / 2
    screen.blit(text, (center_shift, 100))
    pg.display.flip()
    pg.time.wait(2500)
    pg.quit()
