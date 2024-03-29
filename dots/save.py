import os
from typing import List, Tuple
from dots.color import Color
from dots.dot import Dot
import json


class Saver:
    @staticmethod
    def save(sequence: List[Tuple[Dot, Color]]):
        with open('save.json', 'w') as f:
            json.dump(Saver.g(sequence), f)

    @staticmethod
    def g(sequence: List[Tuple[Dot, Color]]):
        r = []
        for i in sequence:
            r.append((i[0].__dict__, i[1].value))
        return r

    @staticmethod
    def load() -> List[Tuple[Dot, Color]]:
        with open('save.json', 'r') as f:
            r = []
            for i in json.load(f, object_hook=Saver.a):
                r.append((i[0], Color(i[1])))
            return r

    @staticmethod
    def load_leaderboard():
        if not os.path.exists('../leaderboard.json'):
            return dict()
        with open('../leaderboard.json', 'r') as f:
            leaderboard = json.load(f)
            if leaderboard is None or not (type(leaderboard) is dict):
                return dict()
            return leaderboard

    @staticmethod
    def save_leaderbiard(leaderboard):
        with open('../leaderboard.json', 'w') as f:
            json.dump(leaderboard, f)

    @staticmethod
    def a(j):
        return Dot(j['x'], j['y'])
