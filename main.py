#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pygame
import random
import os
from src import *

if __name__ == '__main__':
    # Systems initialisation
    global TILE_STATE_PAISHAN, TILE_STATE_HAND, TILE_STATE_BOARD
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

    selected_sprites = []       #被选中的牌
    Board.game_state = "GET_TILE"
    Board.current_player = 0

    done = False
    while not done:
        # if Board.game_state == "GET_TILE":
        #     Board.player_get_tile(refresh=False, action=True)
        #     Board.game_state = "WAIT_FOR_OUT_TILE"


        for event in pygame.event.get():
            if Board.game_state == "GET_TILE":
                Board.player_get_tile(refresh=False, action=True)
                Board.game_state = "WAIT_FOR_OUT_TILE"
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                ##等待玩家出牌
                if Board.game_state == "WAIT_FOR_OUT_TILE":
                    mouse_underlay.rect.x = event.pos[0]
                    mouse_underlay.rect.y = event.pos[1]
                    selected_sprites = pygame.sprite.spritecollide(mouse_underlay, graphics.all_sprites, False)
                    if len(selected_sprites) != 0 and selected_sprites[0].tilestate in TILE_STATE_HAND[0]:
                        # out_success_flag = Board.player_out_tile(player=0, tilepos=selected_sprites[0].tilepos)
                        # # selected_sprites = []
                        # if(out_success_flag == -1):     #选中了手牌但却没有成功出牌
                        #     selected_sprites = []
                        #     continue
                        # else:                           #选中了手牌且成功出牌
                        #     Board.game_state = "WAIT_FOR_PRO_TILE"
                        #     action_finish_flag = True
                        Board.player_out_tile(player=0, tilepos=selected_sprites[0].tilepos)
                        Board.game_state = "WAIT_FOR_PRO_TILE"
                        break       #跳出鼠标事件询问状态
                    else:                               #没有选中手牌
                        selected_sprites = []
                ##等待玩家处理出的牌
                elif Board.game_state == "WAIT_FOR_PRO_TILE":
                    Board.board_get_tile(selected_sprites[0])
                    selected_sprites = []
                    Board.game_state = "GET_TILE"
                    break           #跳出鼠标事件询问状态
            elif event.type == pygame.QUIT:
                action_finish_flag = True
                done = True

            # Game handling
            # jeu_mahjong.next_step()

            # Display handling
            graphics.screen.fill(white)
            graphics.draw_game()

            # Limit to 30 frames per second
            clock.tick(30)

            # Buffering
            pygame.display.flip()

        # for event in pygame.event.get():
        #     if event.type == pygame.QUIT:
        #         done = True
        #     elif event.type == pygame.MOUSEBUTTONDOWN:
        #         if event.button == 1:
        #             mouse_underlay.rect.x = event.pos[0]
        #             mouse_underlay.rect.y = event.pos[1]
        #             selected_sprites = pygame.sprite.spritecollide(mouse_underlay, graphics.all_sprites, False)
        #             # TODO: Do something with the click tiles
        #             Board.player_get_tile(player=0, refresh=False, action=True)

        # # Game handling
        # # jeu_mahjong.next_step()
        #
        # # Display handling
        # graphics.screen.fill(white)
        # graphics.draw_game()
        #
        # # Limit to 30 frames per second
        # clock.tick(30)
        #
        # # Buffering
        # pygame.display.flip()

    pygame.quit()