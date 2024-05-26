class Region:
    def __init__(self, x_min, y_min, x_max, y_max, points):
        self.x_min = x_min
        self.y_min = y_min
        self.x_max = x_max
        self.y_max = y_max
        self.x_middle = (x_max + x_min)/2
        self.y_middle = (y_max + y_min)/2
        self.points = points
        self.children = []
        
    def __len__(self):
        return len(self.points)
    
    def select_quad(self, quad):
        points = []
        bounds = None

        if quad == 0:
            bounds = [self.x_middle, self.y_middle, self.x_max, self.y_max]
            for point in self.points:
                if point.x > self.x_middle and point.y > self.y_middle:
                    points.append(point)
        elif quad == 1:
            bounds = [self.x_min, self.y_middle, self.x_middle, self.y_max]
            for point in self.points:
                if point.x <= self.x_middle and point.y > self.y_middle:
                    points.append(point)
        elif quad == 2:
            bounds = [self.x_min, self.y_min, self.x_middle, self.y_middle]
            for point in self.points:
                if point.x <= self.x_middle and point.y <= self.y_middle:
                    points.append(point)
        else:
            bounds = [self.x_middle, self.y_min, self.x_max, self.y_middle]
            for point in self.points:
                if point.x > self.x_middle and point.y <= self.y_middle:
                    points.append(point)
                
        return Region(bounds[0], bounds[1], bounds[2], bounds[3], points)
