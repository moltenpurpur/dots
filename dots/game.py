import pygame
import sys
from dots.drawer import Drawer
from dots.end_menu import EndMenu
from dots.map import Map
from dots.opponent import Opponent
from dots.player import Player
from dots.color import Color


class Game:

    def __init__(self, win_size):
        self.game_map = Map(win_size)
        self.drawer = Drawer(win_size)
        self.end_menu = EndMenu(self.drawer.win, win_size)
        self.player = Player(Color.RED, win_size)
        self.opponent = Opponent(Color.BLUE, win_size)

    def start(self):
        while True:
            pygame.time.delay(100)

            if self.game_map.is_end:
                self.end_menu.start_end_menu(self.game_map.score[Color.RED])
                break
            self.check_events()
            self.drawer.draw_scene(self.game_map, self.player)


    def check_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.player.move_left()
        if keys[pygame.K_RIGHT]:
            self.player.move_right()
        if keys[pygame.K_UP]:
            self.player.move_up()
        if keys[pygame.K_DOWN]:
            self.player.move_down()
        if keys[pygame.K_q]:
            self.game_map.undo()
        if keys[pygame.K_w]:
            self.game_map.redo()
        if keys[pygame.K_e]:
            self.game_map.save()
        if keys[pygame.K_r]:
            self.game_map.load()
        if keys[pygame.K_SPACE]:
            self.player.try_set_dot_player(self.game_map)
        self.opponent.try_set_dot_opponent(self.game_map)
