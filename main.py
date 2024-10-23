"""
This program shows some platforming that allows sloped surfaces.  It is still
very much a work in progress and needs to be cleaned up a lot.

-Written by Sean J. McKiernan 'Mekire'
"""

import os
import sys
import pygame as pg
import level
import player


CAPTION = "Platformer Genesis Project"


class Control(object):
    """Primary control flow."""
    def __init__(self):
        """Initialize the display and create a player and level."""
        self.screen = pg.display.get_surface()
        self.screen_rect = self.screen.get_rect()
        self.clock = pg.time.Clock()
        self.fps = 60.0
        self.keys = pg.key.get_pressed()
        self.done = False
        self.level = level.LevelMap(SHEET,"bigtest.txt",self.screen_rect.copy())
        self.player = player.Player((50,self.level.rect.bottom-100),(21,15))

    def event_loop(self):
        """Let us quit and jump."""
        for event in pg.event.get():
            self.keys = pg.key.get_pressed()
            if event.type == pg.QUIT or self.keys[pg.K_ESCAPE]:
                self.done = True
            elif event.type == pg.KEYDOWN:
                if event.key == pg.K_SPACE:
                    self.player.jump()
            elif event.type == pg.KEYUP:
                if event.key == pg.K_SPACE:
                    self.player.jump_cut()

    def update(self):
        """Call the update for the level and the actors."""
        self.screen.fill((140,140,255))
        self.player.update(self.level,self.keys)
        self.level.update(self.screen,self.player)
        caption = "{} - FPS: {:.2f}".format(CAPTION,self.clock.get_fps())
        pg.display.set_caption(caption)

    def main_loop(self):
        """Run around."""
        while not self.done:
            self.event_loop()
            self.update()
            pg.display.update()
            self.clock.tick(self.fps)


if __name__ == "__main__":
    os.environ['SDL_VIDEO_CENTERED'] = '1'
    pg.init()
    pg.display.set_mode((544,256))
    SHEET = pg.image.load("tiles_edit.png").convert()
    SHEET.set_colorkey((255,0,255))
    run_it = Control()
    run_it.main_loop()
    pg.quit()
    sys.exit()
