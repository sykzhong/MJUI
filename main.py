#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pygame
import random
import os
from src import *

if __name__ == '__main__':
    # Systems initialisation
    graphics = graphic_system()
    Board = mahjong_board(graphics)

    # Piocher les 13 tuiles - REDO with real rules
    # for player in range(4):
    #     for tile in range(13):
    #         jeu_mahjong.tile_get(player, refresh=False)
    #     jeu_mahjong.refresh_player_gfx(player)
    # jeu_mahjong.refresh_paishan_gfx()

    # Mouse handling
    mouse_underlay = mouse_cursor_underlay()

    # Framerate handling
    clock = pygame.time.Clock()

    done = False
    while not done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    mouse_underlay.rect.x = event.pos[0]
                    mouse_underlay.rect.y = event.pos[1]
                    selected_sprites = pygame.sprite.spritecollide(mouse_underlay, graphics.all_sprites, False)
                    # TODO: Do something with the click tiles
                    Board.player_get_tile(player=0, refresh=False, action=True)

        # Game handling
        # jeu_mahjong.next_step()

        # Display handling
        graphics.screen.fill(white)
        graphics.draw_game()

        # Limit to 30 frames per second
        clock.tick(30)

        # Buffering
        pygame.display.flip()

    pygame.quit()