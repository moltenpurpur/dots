from typing import *
from dots.color import Color

import pygame

from dots.dot import Dot
from dots.map import Map
from dots.player import Player


class Drawer:
    def __init__(self, window_size: Tuple[int, int]):
        self.window_size: Tuple[int, int] = window_size
        self.step: int = 50
        self.win = pygame.display.set_mode(
            ((self.window_size[0] + 1) * self.step,
             (self.window_size[1] + 1) * self.step + 50))
        pygame.init()

    def draw_scene(self, game_map: Map, player: Player):
        self.win.fill((255, 255, 255))
        self.draw_lines()
        self.draw_dots(game_map.dots)
        # self.draw_score(game_map)
        self.draw_cycle(game_map.cycle_way)
        self.draw_cursor(player)

        pygame.display.update()

    def draw_lines(self):
        end_y = (self.window_size[0] + 2) * self.step
        end_x = (self.window_size[1] + 1) * self.step

        for y in range(self.step, end_y, self.step):
            pygame.draw.line(self.win, (0, 0, 0), (0, y), (end_y, y), 1)

        for x in range(self.step, end_x, self.step):
            pygame.draw.line(self.win, (0, 0, 0), (x, 0), (x, end_x), 1)

    def draw_dots(self, game_map: List[List[Color]]):
        for x in range(len(game_map)):
            for y in range(len(game_map[x])):
                if game_map[x][y] in [Color.RED, Color.BLOCKED_RED]:
                    pygame.draw.circle(self.win, (255, 0, 0),
                                       ((x + 1) * self.step,
                                        (y + 1) * self.step), 5, 3)
                if game_map[x][y] in [Color.BLUE, Color.BLOCKED_BLUE]:
                    pygame.draw.circle(self.win, (0, 0, 255),
                                       ((x + 1) * self.step,
                                        (y + 1) * self.step), 5, 3)

    def draw_cursor(self, player: Player):
        pygame.draw.circle(self.win, (0, 255, 0),
                           ((player.current_dot.x + 1) * self.step,
                            (player.current_dot.y + 1) * self.step), 10, 2)

    def draw_cycle(self, dict_cycle_way: Dict[Color, List[List[Dot]]]):
        for color in dict_cycle_way:
            for cycle in dict_cycle_way[color]:
                for i in range(1, len(cycle)):
                    pygame.draw.line(self.win, (255, 0, 0),
                                     ((cycle[i - 1].x + 1) * self.step,
                                      (cycle[i - 1].y + 1) * self.step),
                                     ((cycle[i].x + 1) * self.step,
                                      (cycle[i].y + 1) * self.step), 3)
