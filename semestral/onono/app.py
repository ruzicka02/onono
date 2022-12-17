import numpy as np
import pygame as pg

import savegame

COLOR = {
    "background": "#FFFFFF",
    "empty": "#AAAAAA",
    "full": "#F0AB00",
    "text": "#000000"
}

FONT_NAME = pg.font.get_default_font()


def run():
    game = prepare_game()

    pg.init()
    screen = pg.display.set_mode([500, 550])
    pg.display.set_caption("Onono!")

    pg.font.init()
    font = pg.font.SysFont(FONT_NAME, 50)

    # Run until the user asks to quit
    running = True

    while running:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False

        screen.fill(COLOR["background"])

        header_text = font.render("Onono! The Puzzle Game", 1, False)
        screen.blit(header_text, (50, 20))

        draw_game(screen, game)

        # refresh screen
        pg.display.flip()

    pg.quit()


def prepare_game() -> savegame.SaveGame:
    """
    Helper function for showcase of board drawing.
    """
    s = savegame.SaveGame((10, 10))
    s.randomize(0.3)
    return s


def draw_game(screen, game: savegame.SaveGame):
    dims = game.board.shape
    assert len(dims) == 2, "Board has to be a 2D array."
    assert dims[0] <= 10 and dims[1] <= 10, "Board has to be 10 x 10 or smaller."

    font = pg.font.SysFont(FONT_NAME, 30)

    coords = [50, 100]
    coords_init = coords.copy()

    block_size = (40, 40)

    for row, number in zip(game.board, game.y):
        number_surface = font.render(str(number), 1, False)
        number_coords = (coords[0] - (0.75 * block_size[0]), coords[1] + (0.25 * block_size[1]))
        screen.blit(number_surface, number_coords)

        for pos in row:
            color = COLOR["full"] if pos else COLOR["empty"]
            pg.draw.rect(screen, color, (*coords, *block_size))
            coords[0] += block_size[0]

        coords[0] = coords_init[0]  # CR
        coords[1] += block_size[1]  # LF

    coords = coords_init.copy()
    coords = [coords[0] + 0.33 * block_size[0], coords[1] - 0.75 * block_size[1]]
    for number in game.x:
        number_surface = font.render(str(number), 1, False)
        screen.blit(number_surface, coords)
        coords[0] += block_size[0]
