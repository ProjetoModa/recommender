from .consts import EPS
from .point import Point
from .region import Region
import random


class QuadTree:
    def __init__(self, data):
        self.data = data
        self.max_points = 6
        self.max_depth = 10
        self.root = Region(
            data['x'].min(),
            data['y'].min(),
            data['x'].max() + EPS,
            data['y'].max() + EPS,
            self._convert_points(data),
        )
        self.create_tree(self.root)

    def _convert_points(self, data):
        points = []

        for index, row in data.iterrows():
            points.append(Point(row['x'], row['y'], index))

        return points

    def create_tree(self, region: Region, depth=0):
        if len(region) <= self.max_points or depth >= self.max_depth:
            return

        for i in range(4):
            region.children.append(region.select_quad(i))

        for child in region.children:
            self.create_tree(child, depth + 1)

    def select(self, sample_size):

        sample_size = min(sample_size, len(self.root))

        points = []
        for child in self.root.children:
            points += self.sample(child, min(sample_size // 4, len(child)))

        self.sample(self.root, sample_size, points)

        indexes = [point.idx for point in points]
        selected = self.data.loc[indexes, :]
        return selected['name'].values.tolist()

    def sample(self, region: Region, n, samples=[]):

        while len(samples) < n:
            point = self.search(region)
            if point not in samples:
                samples.append(point)

        return samples

    def search(self, region: Region):
        if len(region.children) == 0:
            return random.choice(region.points)

        for child in random.sample(region.children, len(region.children)):
            if len(child.points) > 0:
                return self.search(child)

        return None
