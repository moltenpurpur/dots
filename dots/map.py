import collections
import copy

from dots.dot import Dot
from dots.color import Color
from typing import *


class Map:
    def __init__(self, win_size):
        self.dots: List[List[Color]] = []
        self.size: Tuple[int, int] = win_size
        self.players: List[Color] = [Color.RED, Color.BLUE]
        self.set_turn: int = 0
        self.fill_map()
        self.cycle_way: Dict[Color, List[List[Dot]]] = \
            collections.defaultdict(list)

    def __getitem__(self, item: Dot):
        return self.dots[item.x][item.y]

    def __setitem__(self, key, value):
        if self.dots[key.x][key.y] == Color.EMPTY:
            self.dots[key.x][key.y] = value

    def fill_map(self):
        for x in range(self.size[0]):
            dots_line = []
            for y in range(self.size[1]):
                dots_line.append(Color.EMPTY)
            self.dots.append(dots_line)

    def can_set_dot(self, dot: Dot):
        return 0 <= dot.x < len(self.dots) \
               and 0 <= dot.y < len(self.dots[dot.x]) \
               and self[dot] == Color.EMPTY

    def try_set_dot(self, target_dot: Dot, color: Color):
        if self.players[self.set_turn] == color \
                and self.can_set_dot(target_dot):
            self[target_dot] = color
            self.set_turn += 1
            if self.set_turn >= len(self.players):
                self.set_turn = 0
            self.find_cycles(target_dot, color)

    def find_cycles(self, target_dot: Dot, color: Color):
        target_dot = Dot(target_dot.x, target_dot.y)
        ways: List[Dict[Dot, Dot]] = []
        self.find_all_cycles(target_dot,
                             target_dot,
                             color,
                             set(),
                             {},
                             ways)
        min_dict_cycle: List[List[Dot]] = self.find_min_dict_cycle(ways)
        if min_dict_cycle is None:
            return

        self.cycle_way[color].append(min_dict_cycle[0])
        for i in min_dict_cycle[1]:
            self.dots[i.x][i.y] = Color.BLOCKED

    def find_all_cycles(self, current_dot: Dot, target_dot: Dot, color: Color,
                        visited: Set[Dot], way: Dict[Dot, Dot],
                        ways: List[Dict[Dot, Dot]]):
        if target_dot == current_dot and len(way.keys()) != 0:
            ways.append(way)
            return
        visited.add(current_dot)

        for neighbor in self.get_neighbor(current_dot, color):
            if neighbor not in visited \
                    or (neighbor == target_dot
                        and len(visited) > 3):
                way[neighbor] = current_dot
                self.find_all_cycles(neighbor,
                                     target_dot,
                                     color,
                                     visited,
                                     copy.deepcopy(way),
                                     ways)
        visited.remove(current_dot)

    def find_min_dict_cycle(self, ways: List[Dict[Dot, Dot]]):
        if len(ways) > 0:
            inside_dots: List[Dot] = []
            min_way: List[Dot] = self.transform_dict_way_in_list_way(ways[0])
            for way in ways:
                if len(way) <= len(min_way):
                    way_dots_list = self.transform_dict_way_in_list_way(way)
                    inside_dots = self.find_inside_cycles_dots(way_dots_list)
                    if len(inside_dots) > 0:
                        min_way = way_dots_list

            if len(inside_dots) > 0:
                return [min_way, inside_dots]

        return None

    @staticmethod
    def transform_dict_way_in_list_way(dict_way: Dict[Dot, Dot]):
        list_way: List[Dot] = []
        for i in dict_way.keys():
            list_way.append(i)
            break

        while len(list_way) <= len(dict_way.keys()):
            list_way.append(dict_way[list_way[len(list_way) - 1]])
        return list_way

    def get_neighbor(self, dot: Dot, color: Color):
        neighbors: List[Dot] = []
        for dx in range(-1, 2):
            for dy in range(-1, 2):
                if dx == 0 and dy == 0:
                    continue
                current_dot = Dot(dot.x + dx, dot.y + dy)
                if 0 <= current_dot.x < self.size[0] \
                        and 0 <= current_dot.y < self.size[1] \
                        and self[current_dot] == color:
                    neighbors.append(current_dot)
        return neighbors

    def find_inside_cycles_dots(self, cycle: [List[Dot]]):
        inside_dots: List[Dot] = []
        for x in range(len(self.dots)):
            for y in range(len(self.dots[x])):
                if self.is_dot_inside_poligone(Dot(x, y), cycle):
                    inside_dots.append(Dot(x, y))
        return inside_dots

    def is_dot_inside_poligone(self, test_dot: Dot, poligon: List[Dot]):
        poligon_set = set(poligon)
        if test_dot in poligon_set:
            return False
        q1 = 0
        q2 = 0
        q3 = 0
        q4 = 0
        for dx in range(test_dot.x, self.size[0]):
            if Dot(dx, test_dot.y) in poligon_set:
                q1 += 1
        for dx in range(0, test_dot.x):
            if Dot(dx, test_dot.y) in poligon_set:
                q2 += 1
        for dy in range(test_dot.y, self.size[1]):
            if Dot(test_dot.x, dy) in poligon_set:
                q3 += 1
        for dy in range(0, test_dot.y):
            if Dot(test_dot.x, dy) in poligon_set:
                q4 += 1
        return q1 % 2 == 1 and q2 % 2 == 1 and q3 % 2 == 1 and q4 % 2 == 1

    @staticmethod
    def find_min_cycle_dot(cycle, min_x):
        min_cycle_dots: List[Dot] = []
        for dot in cycle:
            if dot.x == min_x:
                min_cycle_dots.append(dot)
        min_midpoint: Dot = min_cycle_dots[len(min_cycle_dots) // 2]
        return min_midpoint

    def find_min_x_in_cycle(self, cycle):
        min_x = self.size[0]
        for dot in cycle:
            if dot.x < min_x:
                min_x = dot.x
        return min_x
