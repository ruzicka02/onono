import numpy as np
import pygame as pg


def run():
    pg.init()
    screen = pg.display.set_mode([500, 500])

    # Run until the user asks to quit
    running = True

    while running:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False

        screen.fill((255, 255, 255))
        pg.draw.rect(screen, (0, 0, 255), (200, 200, 100, 100))

        # refresh screen
        pg.display.flip()

    pg.quit()