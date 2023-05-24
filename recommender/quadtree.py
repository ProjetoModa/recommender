from .consts import EPS
import random

class Point:
    def __init__(self, x, y, idx):
        self.x = x
        self.y = y
        self.idx = idx


class Rect:
    def __init__(self, x_min, y_min, x_max, y_max, points):
        self.x_min = x_min
        self.y_min = y_min
        self.x_max = x_max
        self.y_max = y_max
        self.x_middle = (x_max + x_min)/2
        self.y_middle = (y_max + y_min)/2
        self.points = points
        self.children = []

    def count(self):
        return len(self.points)
    
    def select_quad(self, quad):
        points = []
        bounds = None
        if quad == 0:
            bounds = [self.x_middle, self.y_middle, self.x_max, self.y_max]
        elif quad == 1:
            bounds = [self.x_min, self.y_middle, self.x_middle, self.y_max]
        elif quad == 2:
            bounds = [self.x_min, self.y_min, self.x_middle, self.y_middle]
        else:
            bounds = [self.x_middle, self.y_min, self.x_max, self.y_middle]
        
        for point in self.points:
            if bounds[0] <= point.x < bounds[2] and bounds[1] <= point.y < bounds[3]:
                points.append(point)
                
        return Rect(*bounds, points)
            
class QuadTree:
    def __init__(self, data):
        self.data = data
        self.max_points = 6
        self.max_depth = 10
        self.root = Rect(data['x'].min(), data['y'].min(),
                                          data['x'].max() + EPS, data['y'].max() + EPS, self._convert_points(data))
        self.create_tree(self.root)

    def _convert_points(self, data):
        points = []

        for index, row in data.iterrows():
            points.append(Point(row['x'], row['y'], index))

        return points

    def create_tree(self, region: Rect, depth=0):
        if region.count() <= self.max_points or depth >= self.max_depth:
            return
        
        for i in range(4):
            region.children.append(region.select_quad(i))
        
        for child in region.children:
            self.create_tree(child, depth+1)

    def select(self, sample_size):
        if sample_size % 4 != 0:
            raise Exception("sample size must be multiple of 4")
        points = []
        for child in self.root.children:
            points += self.sample(child, sample_size//4)
        indexes = [point.idx for point in points]
        selected = self.data.loc[indexes, :]
        return selected['name'].values.tolist()
    
    def sample(self, region: Rect, n):
        samples = []
        for _ in range(n):
            samples.append(self.search(region))
        return samples
    
    def search(self, region: Rect):
        if len(region.children) == 0:
            return random.choice(region.points)
        
        for child in random.sample(region.children, len(region.children)):
            if len(child.points) > 0:
                return self.search(child)
            
        return None
