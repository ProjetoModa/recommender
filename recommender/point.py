class Point:
    def __init__(self, x, y, idx):
        self.x = x
        self.y = y
        self.idx = idx
    def __repr__(self):
        return f"<Point x:{self.x} y:{self.y} i:{self.idx}>"
    def __str__(self) -> str:
        return self.__repr__()

