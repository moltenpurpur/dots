import collections
import json

from dots.dot import Dot
from dots.color import Color
from typing import List, Tuple, Dict, Set
from dots.save import Saver



class Map:
    def __init__(self, win_size):
        self.dots: List[List[Color]] = []
        self.size: Tuple[int, int] = win_size
        self.players: List[Color] = [Color.RED, Color.BLUE]
        self.set_turn: int = 0
        self.fill_map()
        self.cycle_way: Dict[Color, List[List[Dot]]] = \
            collections.defaultdict(list)
        self.blue_blocked: List[Set[Dot]] = []
        self.red_blocked: List[Set[Dot]] = []
        self.score: Dict[Color, int] = collections.defaultdict(int)
        self.blocked: Set[Dot] = set()
        self.dot_sequence: List[Tuple] = []
        self.point = 0

    def __getitem__(self, item: Dot):
        return self.dots[item.x][item.y]

    def __setitem__(self, key, value):
        if self.dots[key.x][key.y] == Color.EMPTY:
            self.dots[key.x][key.y] = value

    def fill_map(self):
        m = []
        for x in range(self.size[0]):
            dots_line = []
            for y in range(self.size[1]):
                dots_line.append(Color.EMPTY)
                m.append(Dot(x, y))
            self.dots.append(dots_line)
        self.companents = [(Color.EMPTY, m)]

    def drop_map(self):
        self.cycle_way: Dict[Color, List[List[Dot]]] = \
            collections.defaultdict(list)
        self.blue_blocked: List[Set[Dot]] = []
        self.red_blocked: List[Set[Dot]] = []
        self.score: Dict[Color, int] = collections.defaultdict(int)
        self.blocked: Set[Dot] = set()
        for x in range(self.size[0]):
            for y in range(self.size[1]):
                self.dots[x][y] = Color.EMPTY

    def can_set_dot(self, dot: Dot):
        return 0 <= dot.x < len(self.dots) \
               and 0 <= dot.y < len(self.dots[dot.x]) \
               and self[dot] == Color.EMPTY

    def try_set_dot(self, target_dot: Dot, color: Color):
        if self.players[self.set_turn] == color \
                and self.can_set_dot(target_dot):
            self.writing_to_sequence(target_dot, color)
            self.set_dot(target_dot, color)

    def set_dot(self, target_dot, color):
        self[target_dot] = color
        self.set_turn += 1
        if self.set_turn >= len(self.players):
            self.set_turn = 0
        self.find_cycles()
        self.fill_blocked()
        self.update_score()

    def find_cycles(self):
        dot_colors = collections.defaultdict(set)
        for x in range(self.size[0]):
            for y in range(self.size[1]):
                dot = Dot(x, y)
                if dot in self.blocked:
                    continue
                dot_colors[self[dot]].add(dot)

        for i in self.get_blocked(Color.BLUE, dot_colors[Color.BLUE]):
            self.blue_blocked.append(i)
        for i in self.get_blocked(Color.RED, dot_colors[Color.RED]):
            self.red_blocked.append(i)

        blue_cycles: List[List[Dot]] = []
        red_cycles: List[List[Dot]] = []
        for blue_b in self.blue_blocked:
            blue_cycles.append(self.get_cycle(Color.RED, blue_b))

        for red_b in self.red_blocked:
            red_cycles.append(self.get_cycle(Color.BLUE, red_b))

        self.cycle_way[Color.RED] = blue_cycles
        self.cycle_way[Color.BLUE] = red_cycles

    def get_cycle(self, opposite_color: Color, blocked_dots: Set[Dot]):
        border_dots: Set[Dot] = set()
        visited: Set[Dot] = set()
        border_cycle: List[Dot] = []
        for dot in blocked_dots:
            if dot in visited:
                continue
            visited.add(dot)
            for neighbor in self.get_four_neighbors(dot):
                if self[neighbor] != opposite_color \
                        or neighbor in blocked_dots:
                    continue
                if self[neighbor] == opposite_color:
                    border_dots.add(neighbor)
        border_dot = border_dots.pop()
        border_cycle.append(border_dot)

        while len(border_dots) != 0:
            for dot in self.get_all_neighbor(border_dot):
                if dot in border_dots:
                    border_dot = dot
                    border_dots.remove(border_dot)
                    border_cycle.append(border_dot)
                    break
        border_cycle.append(border_cycle[0])
        return border_cycle

    def get_blocked(self, color: Color, dots: Set[Dot]):
        blocked: List[Set[Dot]] = []
        visited = set()
        while len(dots) > 0:
            dot = dots.pop()
            if dot in visited:
                continue
            deque = collections.deque()
            deque.append(dot)
            current_blocked = set()
            bordered = False
            while len(deque) > 0:
                current_dot = deque.pop()
                visited.add(current_dot)
                if current_dot not in self.blocked:
                    current_blocked.add(current_dot)
                if self.is_dot_on_border(current_dot):
                    bordered = True
                for neighbor in self.get_four_neighbors(current_dot):
                    if (self[neighbor] == Color.EMPTY
                        or self[neighbor] == color
                        or neighbor in self.blocked) \
                            and neighbor not in visited:
                        deque.append(neighbor)
            if not bordered:
                blocked.append(current_blocked)
        return blocked

    def is_dot_on_border(self, dot: Dot):
        return dot.x == 0 or dot.x == self.size[
            0] - 1 or dot.y == 0 or dot.y == self.size[1] - 1

    def get_four_neighbors(self, dot: Dot):
        neighbors: List[Dot] = []
        for dx in range(-1, 2):
            for dy in range(-1, 2):
                if abs(dx) == abs(dy):
                    continue
                current_dot = Dot(dot.x + dx, dot.y + dy)
                if 0 <= current_dot.x < self.size[0] \
                        and 0 <= current_dot.y < self.size[1]:
                    neighbors.append(current_dot)
        return neighbors

    def get_all_neighbor(self, dot: Dot):
        neighbors: List[Dot] = []
        for dx in range(-1, 2):
            for dy in range(-1, 2):
                if dx == 0 and dy == 0:
                    continue
                current_dot = Dot(dot.x + dx, dot.y + dy)
                if 0 <= current_dot.x < self.size[0] \
                        and 0 <= current_dot.y < self.size[1]:
                    neighbors.append(current_dot)
        return neighbors

    @staticmethod
    def get_opponent_color(user_color: Color):
        opponent_color = Color.EMPTY
        if user_color == Color.RED:
            opponent_color = Color.BLUE
        if user_color == Color.BLUE:
            opponent_color = Color.RED
        return opponent_color

    def update_score(self):
        self.score[Color.RED] = self.get_count(Color.BLUE, self.blue_blocked)
        self.score[Color.BLUE] = self.get_count(Color.RED, self.red_blocked)

    def get_count(self, color: Color, blocked):
        count = 0
        for i in blocked:
            for j in i:
                if self[j] == color:
                    count += 1
        return count

    def fill_blocked(self):
        self.blocked = set()
        for i in self.blue_blocked:
            for j in i:
                self.blocked.add(j)
        for i in self.red_blocked:
            for j in i:
                self.blocked.add(j)
        pass

    def writing_to_sequence(self, dot, color):
        if len(self.dot_sequence) > self.point:
            self.dot_sequence = self.dot_sequence[0: self.point]
        self.dot_sequence.append((dot, color))
        self.point += 1

    def load_map(self, sequence):
        self.drop_map()
        for i in sequence:
            self.set_dot(i[0], i[1])

    def undo(self):
        if self.point != 0:
            self.point -= 2
            self.load_map(self.dot_sequence[0:self.point])

    def redo(self):
        if self.point < len(self.dot_sequence):
            self.point += 2
            self.load_map(self.dot_sequence[0:self.point])

    def save(self):
        Saver.save(self.dot_sequence)

    def load(self):
        self.load_map(Saver.load())
