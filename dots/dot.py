class Dot:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __hash__(self):
        return self.x * 1000 + self.y

    def __str__(self):
        return f'X={self.x} Y={self.y}'

    def __repr__(self):
        return str(self)
