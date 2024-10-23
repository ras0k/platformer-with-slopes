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
import pygame.math


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
        self.level = level.LevelMap(SHEET,"sisyphus1.txt",self.screen_rect.copy())
        self.player = player.Player((50,self.level.rect.bottom-100),(21,15))
        self.boulder = Boulder(400, 300)  # Create a boulder in the middle of the screen
        self.all_sprites.add(self.boulder)

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


class Boulder(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((30, 30))
        self.image.fill((100, 100, 100))  # Gray color for the boulder
        pygame.draw.circle(self.image, (80, 80, 80), (15, 15), 15)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.velocity = pygame.math.Vector2(0, 0)
        self.friction = 0.95

    def update(self):
        self.rect.x += self.velocity.x
        self.rect.y += self.velocity.y
        self.velocity *= self.friction

    def handle_boulder_collision(self):
        if pygame.sprite.collide_rect(self.player, self.boulder):
            push_direction = pygame.math.Vector2(
                self.boulder.rect.centerx - self.player.rect.centerx,
                self.boulder.rect.centery - self.player.rect.centery
            )
            if push_direction.length() > 0:
                push_direction.normalize_ip()
                self.boulder.velocity = push_direction * 5  # Adjust the pushing force as needed


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
