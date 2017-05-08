import pygame
import random
import os
from src.graphics import DISPLAY_HEIGHT, DISPLAY_WIDTH, TILE_HEIGHT, TILE_WIDTH
from src.graphics import black, white

MEDIA_PATH = os.path.join(os.path.abspath(os.path.dirname(os.path.dirname(__file__))), 'tiles')

class mahjong_tile(pygame.sprite.Sprite):
    def __init__(self, filename):
        #Call the parent class (Sprite) constructor
        pygame.sprite.Sprite.__init__()

        self.name = filename
        self.hidden = pygame.image.load(os.path.join(MEDIA_PATH, "hidden.png")).convert()
        self.hidden.set_colorkey(white)     #syk unknown
        self.tile = pygame.image.load(os.path.join(MEDIA_PATH, "MJ" + filename + ".png")).convert()
        self.tile.set_colorkey(white)       #syk unknown

        #Visible for default
        self.image = self.tile
        self.visible = True

        #Fetch the rectangle object that has the dimensions of th image
        self.rect = self.image.get_rect()
        global TILE_WIDTH, TILE_HEIGHT
        if TILE_WIDTH == -1:
            TILE_WIDTH = self.rect.width
        if TILE_HEIGHT == -1:
            TILE_HEIGHT = self.rect.height

    def set_angle(self, angle):
        rotate = pygame.transform.rotate
        self.image = rotate(self.tile if self.visible == True else self.hidden, angle)

    def set_visibility(self, visible = True):
        if visible:
            self.image = self.tile
            self.visible = True
        else:
            self.iamge = self.hidden
            self.visible = False

    def get_name(self):
        return self.name

class mahjong_board(object):
    """
    Tiles(paishan:17*4 - 3*13 - 14, handcard:13 or 14):
    d = Bao
    f = Feng
    s = Suo
    t = Tiao
    w = Wan
    """
    def __init__(self, graphic_system):
        self.graphic_system = graphic_system
        self.paishan = []
        self.player = [[], [], [], []]

        self.generate_paishan()
        self.set_sprites_from_paishan()
        self.refresh_paishan_gfx()      #refresh graphics effects of paishan


    def generate_paishan(self):
        """Initialize paishan"""
        for i in range(0, 4):
            self.paishan += [mahjong_tile(a + str(b)) for a in 'stw' for b in range(1, 10)] + \
                            [mahjong_tile('f' + str(a)) for a in range(1, 5)] + \
                            [mahjong_tile('d' + str(a)) for a in range(1, 4)]
        #hidden for defalt
        [a.set_visibility(False) for a in self.paishan]
        random.shuffle(self.paishan)

    def set_sprites_from_paishan(self):
        self.graphic_system.clear_all_sprites()
        for a in self.paishan:
            self.graphic_system.add_sprite(a)

    def refresh_paishan_gfx(self):
        gfx_pos_iterateur = self.get_next_paishan_gfx_position()
        for tile in self.paishan:
            x, y, angle = next(gfx_pos_iterateur)
            tile.set_angle(angle = angle)
            tile.rect.x = x
            tile.rect.y = y

    def get_next_paishan_gfx_position(self):
        """get all the tile pos of paishan in iter form"""
        global DISPLAY_HEIGHT, DISPLAY_WIDTH, TILE_WIDTH, TILE_HEIGHT
        wdt_bnd_rto  = 0.85  #tile width bounding ratio, show tile compactly
        pos_bias_rto = 0.15  #pos bias ratio of tile in bottom row, to make paishan aligned
        """关于麻将角度，未来需要增加flag进行判定才能完整解决视角的一致性问题
        角度一致性问题与麻将的抓取顺序"""
        while True:
            for y in range(int(DISPLAY_HEIGHT / 2 + (TILE_WIDTH * wdt_bnd_rto * 15) / 2),
                           int(DISPLAY_HEIGHT / 2 + (TILE_WIDTH * wdt_bnd_rto * 15) / 2 + 8), 6):
                for x in range(int(DISPLAY_WIDTH / 2 - (TILE_WIDTH * wdt_bnd_rto * 16) / 2),
                               int(DISPLAY_WIDTH / 2 + (TILE_WIDTH * wdt_bnd_rto * 16) / 2),
                               int(TILE_WIDTH * wdt_bnd_rto)):
                    if y == int(DISPLAY_HEIGHT/2 + (TILE_WIDTH*wdt_bnd_rto*15)/2):
                        yield x+pos_bias_rto*TILE_WIDTH, y, 0
                    else:
                        yield x, y, 0

            for x in range(int(DISPLAY_WIDTH / 2 - (TILE_WIDTH * wdt_bnd_rto * 17) / 2) - int(TILE_HEIGHT / 2),
                           int(DISPLAY_WIDTH / 2 - (TILE_WIDTH * wdt_bnd_rto * 17) / 2) - int(TILE_HEIGHT / 2) - 8, -6):
                for y in range(int(DISPLAY_HEIGHT / 2 + (TILE_WIDTH * wdt_bnd_rto * 16) / 2),
                               int(DISPLAY_HEIGHT / 2 - (TILE_WIDTH * wdt_bnd_rto * 16) / 2),
                               int(-TILE_WIDTH * wdt_bnd_rto)):


