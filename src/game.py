#-*- coding: utf-8 -*-
import pygame
import random
import os
from src.graphics import DISPLAY_WIDTH, DISPLAY_HEIGHT, TILE_WIDTH, TILE_HEIGHT
from src.graphics import black, white # Redo with class, plz

MEDIA_PATH = os.path.join(os.path.abspath(os.path.dirname(os.path.dirname(__file__))), 'tiles')

class mahjong_text(pygame.font.Font):
    def __init__(self, text, x, y):
        pygame.font.Font.__init__(self, None, 30) # Font, size en pt
        self.text = text
        self.x = x
        self.y = y
    
    def get_rendering(self):
        return self.render(self.text, True, black) # text, anti-aliasing, color
    
    def get_position(self):
        return [self.x, self.y]


class mahjong_tile(pygame.sprite.Sprite):
    def __init__(self, filename):
        # Call the parent class (Sprite) constructor
        pygame.sprite.Sprite.__init__(self) 
        
        self.name = filename

        self.vertical = True
        self.hidden = pygame.image.load(os.path.join(MEDIA_PATH, "hidden.png")).convert()
        self.hidden_horizontal = pygame.image.load(os.path.join(MEDIA_PATH, "hidden_horizontal.png")).convert()
        self.hidden.set_colorkey(white)
        self.hidden_horizontal.set_colorkey(white)
        self.tile = pygame.image.load(os.path.join(MEDIA_PATH, "MJ" + filename + ".png")).convert()
        self.tile.set_colorkey(white)

        # Visible par d�fault
        self.image = self.tile
        self.visible = True

        # Fetch the rectangle object that has the dimensions of the image
        # image.
        # Update the position of this object by setting the values 
        # of rect.x and rect.y
        self.rect = self.image.get_rect()
        global TILE_WIDTH, TILE_HEIGHT
        if TILE_WIDTH == -1:
            TILE_WIDTH = self.rect.width
        if TILE_HEIGHT == -1:
            TILE_HEIGHT = self.rect.height
            
    def set_angle(self, angle):
        """增加了牌组是否垂直的判断，以让视角正确"""
        rotate = pygame.transform.rotate
        if(self.vertical == True):
            self.image = rotate(self.tile if self.visible == True else self.hidden, angle)
        else:
            self.image = rotate(self.tile if self.visible == True else self.hidden_horizontal, angle)
    
    def set_visibility(self, visible=True):
        if visible:
            self.image = self.tile
            self.visible = True
        else:
            if self.vertical:
                self.image = self.hidden
            else:
                self.image = self.hidden_horizontal
            self.visible = False
    
    def get_name(self):
        return self.name

class mahjong_board(object):
    """
    Tiles (44x53):
    d = Dragons
    f = Vents
    s = Bamboos
    t = Cercles
    w = Character
    """
    def __init__(self, graphic_system):
        self.graphic_system = graphic_system
        self.paishan = []
        self.player = [[],[],[],[]]

        self.paishan_pos = []

        self.vacancy_head = -1
        self.vacancy_tail = 0

        self.generate_paishan()
        self.set_sprites_from_paishan()
        self.refresh_paishan_gfx()
        self.refresh_player_gfx(0)
        self.refresh_player_gfx(1)
        self.refresh_player_gfx(2)
        self.refresh_player_gfx(3)
        
        self.game_state = None
        self.player_actuel = 0
        
    
    def generate_paishan(self):
        self.paishan = [mahjong_tile(a+str(b)) for a in 'stw' for b in range(1,10)] + [mahjong_tile('d'+str(a)) for a in range(1,4)] + [mahjong_tile('f'+str(a)) for a in range(1,5)]
        self.paishan += [mahjong_tile(a+str(b)) for a in 'stw' for b in range(1,10)] + [mahjong_tile('d'+str(a)) for a in range(1,4)] + [mahjong_tile('f'+str(a)) for a in range(1,5)]
        self.paishan += [mahjong_tile(a+str(b)) for a in 'stw' for b in range(1,10)] + [mahjong_tile('d'+str(a)) for a in range(1,4)] + [mahjong_tile('f'+str(a)) for a in range(1,5)]
        self.paishan += [mahjong_tile(a+str(b)) for a in 'stw' for b in range(1,10)] + [mahjong_tile('d'+str(a)) for a in range(1,4)] + [mahjong_tile('f'+str(a)) for a in range(1,5)]
        [a.set_visibility(False) for a in self.paishan] # Hack de compr�hension de liste
        random.shuffle(self.paishan)
        
    def set_sprites_from_paishan(self):
        self.graphic_system.clear_all_sprites()
        for a in self.paishan:
            self.graphic_system.add_sprite(a)
    
    # def get_next_paishan_gfx_position(self):
    #     global DISPLAY_WIDTH, DISPLAY_HEIGHT, TILE_WIDTH, TILE_HEIGHT
    #     wdt_bnd_rto = 0.85 # Tile Width Bounding Ratio
    #     """syk"""
    #     pos_bias_rto = 0.15
    #     """syk"""
    #     #syk: 牌山中上下排的牌没有对齐（下排的牌应稍微偏右），四个方向的牌山存在一定遮挡
    #     while True:
    #         # for x in range(int(DISPLAY_WIDTH/2 + (TILE_WIDTH*wdt_bnd_rto*16)/2), int(DISPLAY_WIDTH/2 - (TILE_WIDTH*wdt_bnd_rto*16)/2), int(-TILE_WIDTH*wdt_bnd_rto)):
    #         #     for y in range(int(DISPLAY_HEIGHT/2 + (TILE_WIDTH*wdt_bnd_rto*15)/2), int(DISPLAY_HEIGHT/2 + (TILE_WIDTH*wdt_bnd_rto*15)/2 + 8), 6):
    #         #         """syk"""
    #         #         if y == int(DISPLAY_HEIGHT/2 + (TILE_WIDTH*wdt_bnd_rto*15)/2):
    #         #             yield x+pos_bias_rto*TILE_WIDTH, y, 0
    #         #         else:
    #         #             yield x, y, 0
    #         #         """syk"""
    #         #         # yield x, y, 0           #syk experiment
    #         for x in range(int(DISPLAY_WIDTH / 2 - (TILE_WIDTH * wdt_bnd_rto * 16) / 2),
    #                        int(DISPLAY_WIDTH / 2 + (TILE_WIDTH * wdt_bnd_rto * 16) / 2),
    #                        int(TILE_WIDTH * wdt_bnd_rto)):
    #             for y in range(int(DISPLAY_HEIGHT / 2 + (TILE_WIDTH * wdt_bnd_rto * 16) / 2),
    #                            int(DISPLAY_HEIGHT / 2 + (TILE_WIDTH * wdt_bnd_rto * 16) / 2 + 8), 6):
    #                 """syk"""
    #                 if y == int(DISPLAY_HEIGHT/2 + (TILE_WIDTH*wdt_bnd_rto*16)/2):
    #                     yield x+pos_bias_rto*TILE_WIDTH, y, 0
    #                 else:
    #                     yield x, y, 0
    #                 """syk"""
    #                 # yield x, y, 0           #syk experiment
    #         for x in range(int(DISPLAY_WIDTH / 2 - (TILE_WIDTH * wdt_bnd_rto * 17) / 2) - int(TILE_HEIGHT / 2),
    #                        int(DISPLAY_WIDTH / 2 - (TILE_WIDTH * wdt_bnd_rto * 17) / 2) - int(TILE_HEIGHT / 2) - 8,
    #                        -6):
    #             for y in range(int(DISPLAY_HEIGHT / 2 + (TILE_WIDTH * wdt_bnd_rto * 16) / 2),
    #                            int(DISPLAY_HEIGHT / 2 - (TILE_WIDTH * wdt_bnd_rto * 16) / 2),
    #                            int(-TILE_WIDTH * wdt_bnd_rto)):
    #                 # for x in range(int(DISPLAY_WIDTH/2 - (TILE_WIDTH*wdt_bnd_rto*17)/2) - (TILE_HEIGHT/2), int(DISPLAY_WIDTH/2 - (TILE_WIDTH*wdt_bnd_rto*17)/2) - (TILE_HEIGHT/2) - 8, -6):     #syk (TILE_HEIGHT/2)化整
    #
    #                 """syk"""
    #                 if x == int(DISPLAY_WIDTH / 2 - (TILE_WIDTH * wdt_bnd_rto * 17) / 2) - int(TILE_HEIGHT / 2):
    #                     yield x, y + pos_bias_rto * TILE_WIDTH, 270
    #                 else:
    #                     yield x, y, 270
    #                 """syk"""
    #                 # yield x - pos_bias_rto*TILE_WIDTH, y, 270
    #         for x in range(int(DISPLAY_WIDTH/2 - (TILE_WIDTH*wdt_bnd_rto*16)/2), int(DISPLAY_WIDTH/2 + (TILE_WIDTH*wdt_bnd_rto*16)/2), int(TILE_WIDTH*wdt_bnd_rto)):
    #             for y in range(int(DISPLAY_HEIGHT/2 - (TILE_WIDTH*wdt_bnd_rto*16)/2), int(DISPLAY_HEIGHT/2 - (TILE_WIDTH*wdt_bnd_rto*16)/2 + 8), 6):
    #                 yield x, y, 0
    #         for y in range(int(DISPLAY_HEIGHT/2 - (TILE_WIDTH*wdt_bnd_rto*16)/2), int(DISPLAY_HEIGHT/2 + (TILE_WIDTH*wdt_bnd_rto*16)/2 ), int(TILE_WIDTH*wdt_bnd_rto)):
    #             # for x in range(int(DISPLAY_WIDTH/2 + (TILE_WIDTH*wdt_bnd_rto*17)/2) + (TILE_HEIGHT/2), int(DISPLAY_WIDTH/2 + (TILE_WIDTH*wdt_bnd_rto*17)/2) + (TILE_HEIGHT/2) + 8, 6):      #syk (TILE_HEIGHT/2)化整
    #             for x in range(int(DISPLAY_WIDTH / 2 + (TILE_WIDTH * wdt_bnd_rto * 17) / 2) + int(TILE_HEIGHT / 2),
    #                            int(DISPLAY_WIDTH / 2 + (TILE_WIDTH * wdt_bnd_rto * 17) / 2) + int(TILE_HEIGHT / 2) + 8, 6):
    #                 yield x, y, 270

    def get_next_paishan_gfx_position(self):
        """return x, y, angle, vertical flag"""
        global DISPLAY_WIDTH, DISPLAY_HEIGHT, TILE_WIDTH, TILE_HEIGHT
        wdt_bnd_rto = 0.85 # Tile Width Bounding Ratio
        """syk"""
        pos_bias_rto = 0.15
        """syk"""
        #syk: 牌山中上下排的牌没有对齐（下排的牌应稍微偏右），四个方向的牌山存在一定遮挡
        #syk: 若要有合适的视角，牌山的排布必须是从左至右，从上至下。因而对于牌山的抽取，pop的牌需要有一定的规律
        #syk: 水平放置的牌需从下而上插入add，垂直放置的牌需从左至右发放置。对于1,2位置有牌image放置与实际游戏放置顺序有所差异，需要进行位置换算
        while True:
            for x in range(int(DISPLAY_WIDTH / 2 - (TILE_WIDTH * wdt_bnd_rto * 16) / 2),    #player 0
                           int(DISPLAY_WIDTH / 2 + (TILE_WIDTH * wdt_bnd_rto * 16) / 2),
                           int(TILE_WIDTH * wdt_bnd_rto)):
                for y in range(int(DISPLAY_HEIGHT / 2 + (TILE_WIDTH * wdt_bnd_rto * 16) / 2),
                               int(DISPLAY_HEIGHT / 2 + (TILE_WIDTH * wdt_bnd_rto * 16) / 2 + 8), 6):
                    """syk"""
                    if y == int(DISPLAY_HEIGHT/2 + (TILE_WIDTH*wdt_bnd_rto*16)/2):
                        yield x+pos_bias_rto*TILE_WIDTH, y, 0, True
                    else:
                        yield x, y, 0, True
                    """syk"""
            for y in range(int(DISPLAY_HEIGHT/2 + (TILE_WIDTH*wdt_bnd_rto*16)/2),           #player 1
                           int(DISPLAY_HEIGHT/2 - (TILE_WIDTH*wdt_bnd_rto*16)/2 ),
                           int(-TILE_WIDTH*wdt_bnd_rto)):
                for x in range(int(DISPLAY_WIDTH / 2 + (TILE_WIDTH * wdt_bnd_rto * 17) / 2) + int(TILE_HEIGHT / 2),
                               int(DISPLAY_WIDTH / 2 + (TILE_WIDTH * wdt_bnd_rto * 17) / 2) + int(TILE_HEIGHT / 2) - 8, -6):
                    if x == int(DISPLAY_WIDTH / 2 + (TILE_WIDTH * wdt_bnd_rto * 17) / 2) + int(TILE_HEIGHT / 2):
                        yield x, y - TILE_WIDTH*pos_bias_rto, 270, False
                    else:
                        yield x, y, 270, False
            for x in range(int(DISPLAY_WIDTH / 2 - (TILE_WIDTH * wdt_bnd_rto * 16) / 2),    #player 2
                           int(DISPLAY_WIDTH / 2 + (TILE_WIDTH * wdt_bnd_rto * 16) / 2),
                           int(TILE_WIDTH * wdt_bnd_rto)):
                for y in range(int(DISPLAY_HEIGHT / 2 - (TILE_WIDTH * wdt_bnd_rto * 16) / 2),
                                   int(DISPLAY_HEIGHT / 2 - (TILE_WIDTH * wdt_bnd_rto * 16) / 2 + 8), 6):
                    if y == int(DISPLAY_HEIGHT / 2 - (TILE_WIDTH * wdt_bnd_rto * 16) / 2):
                        yield x + pos_bias_rto*TILE_WIDTH, y, 0, True
                    else:
                        yield x, y, 0, True
            for y in range(int(DISPLAY_HEIGHT / 2 + (TILE_WIDTH * wdt_bnd_rto * 16) / 2),   #player 3
                           int(DISPLAY_HEIGHT / 2 - (TILE_WIDTH * wdt_bnd_rto * 16) / 2),
                           int(-TILE_WIDTH * wdt_bnd_rto)):
                for x in range(int(DISPLAY_WIDTH / 2 - (TILE_WIDTH * wdt_bnd_rto * 17) / 2) - int(TILE_HEIGHT/2) - 6,
                               int(DISPLAY_WIDTH / 2 - (TILE_WIDTH * wdt_bnd_rto * 17) / 2) - int(TILE_HEIGHT/2) - 6 - 8,
                               -6):

                    # for x in range(int(DISPLAY_WIDTH/2 - (TILE_WIDTH*wdt_bnd_rto*17)/2) - (TILE_HEIGHT/2), int(DISPLAY_WIDTH/2 - (TILE_WIDTH*wdt_bnd_rto*17)/2) - (TILE_HEIGHT/2) - 8, -6):     #syk (TILE_HEIGHT/2)化整

                    """syk"""
                    if x == int(DISPLAY_WIDTH / 2 - (TILE_WIDTH * wdt_bnd_rto * 17) / 2) - int(TILE_HEIGHT / 2) - 6:
                        yield x, y - pos_bias_rto * TILE_WIDTH, 270, False
                    else:
                        yield x, y, 270, False
                    """syk"""


                    # yield x, y, 0           #syk experiment




    def refresh_paishan_gfx(self):        #head, tail is calc by defined by counter clockwise, means the vacancy pos
        """ssS
        Actualise les sprites affichant le paishan
        """
        fgx_pos_iterateur = self.get_next_paishan_gfx_position()
        exceed_flag = False
        head = self.vacancy_head
        tail = self.vacancy_tail
        if head > tail:
            exceed_flag = True
        num = 0
        for tile in self.paishan:
            if exceed_flag == False:
                while num > head and num < tail:
                    next(fgx_pos_iterateur)
                    num += 1
            else:
                while (num >= 0 and num < head) or (num < len(self.paishan)):
                    next(fgx_pos_iterateur)
                    num += 1
            # if num // (17*2) == 2 or num // (17*2) == 3:
            #
            x, y, angle, vertical_flag = next(fgx_pos_iterateur)
            tile.vertical = vertical_flag
            tile.rect.x = x
            tile.rect.y = y
            tile.set_angle(angle)
            num += 1

        # for tile in self.paishan:
        #     # x, y, angle = fgx_pos_iterateur.next()        #syk python2->python3
        #     x, y, angle, vertical_flag = next(fgx_pos_iterateur)
        #     tile.vertical = vertical_flag
        #     tile.rect.x = x
        #     tile.rect.y = y
        #     tile.set_angle(angle)




    def refresh_player_gfx(self, player=0):
        """
        Actualise les sprites affichant les mains des joueurs
        """
        wdt_bnd_rto = 0.85 # Tile Width Bounding Ratio
        hand_bnd_rto = 1.0
        global DISPLAY_WIDTH, DISPLAY_HEIGHT, TILE_WIDTH, TILE_HEIGHT
        for num, tile in enumerate(self.player[player]):
            if player == 0:
                tile.rect.x = int(DISPLAY_WIDTH/2 - (TILE_WIDTH*wdt_bnd_rto*16)/2) + (TILE_WIDTH*hand_bnd_rto*num)
                tile.rect.y = int(DISPLAY_HEIGHT/2 + (TILE_WIDTH*wdt_bnd_rto*18)/2) + TILE_WIDTH/2
                tile.set_angle(0)
            elif player == 1:
                tile.rect.x = int(DISPLAY_WIDTH/2 - (TILE_WIDTH*wdt_bnd_rto*18)/2) - (TILE_HEIGHT/2) - TILE_HEIGHT
                tile.rect.y = int(DISPLAY_HEIGHT/2 - (TILE_WIDTH*wdt_bnd_rto*16)/2) + (TILE_WIDTH*hand_bnd_rto*num)
                tile.set_angle(90)
            elif player == 2:
                tile.rect.x = int(DISPLAY_WIDTH/2 + (TILE_WIDTH*wdt_bnd_rto*16)/2) - (TILE_WIDTH*hand_bnd_rto*num)
                tile.rect.y = int(DISPLAY_HEIGHT/2 - (TILE_WIDTH*wdt_bnd_rto*18)/2) - TILE_WIDTH/2
                tile.set_angle(180)
            else:
                tile.rect.x = int(DISPLAY_WIDTH/2 + (TILE_WIDTH*wdt_bnd_rto*20)/2) + (TILE_HEIGHT/2)
                tile.rect.y = int(DISPLAY_HEIGHT/2 + (TILE_WIDTH*wdt_bnd_rto*16)/2) - (TILE_WIDTH*hand_bnd_rto*num)
                tile.set_angle(270)
    
    def reorder_player_hand(self, player=0):
        self.player[player].sort(key=lambda clef: clef.get_name())
    
    def pioche(self, player=0, refresh=True):
        # D�placer la tile dans la main du joueur
        tile_piochee = self.paishan.pop(0)
        self.vacancy_tail += 1
        if player == 0:
            tile_piochee.set_visibility(True)
        self.player[player].append(tile_piochee)
        self.reorder_player_hand(player)
        
        # Si on veut que la pioche reg�n�re les graphiques (lent)
        if refresh:
            # Regenerer le paishan
            self.refresh_paishan_gfx()
            
            # Regenerer la vue du joueur
            self.refresh_player_gfx(player)
            
            
    def next_step(self):
        if self.game_state == "piocher":
            self.pioche(self.player_actuel)
            self.game_state = "waiting_action"
        elif self.game_state == "waiting_action":
            pass
        elif self.game_state == "done":
            self.player_actuel = (self.player_actuel + 1) if self.player_actuel <4 else 0
        else:
            # On d�bute ou on est perdu
            self.player_actuel = 0
            self.game_state = "piocher"