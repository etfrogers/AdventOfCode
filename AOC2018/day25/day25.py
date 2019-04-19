from typing import List

import numpy as np

CONSTELLATION_DISTANCE = 3


class Point:
    def __init__(self, line):
        self.coords = np.array([int(v) for v in line.split(',')])

    def distance_to(self, other):
        return np.sum(np.abs(self.coords - other.coords))

    def __repr__(self):
        return str(self.coords)


class Constellation:
    def __init__(self, points: List[Point]):
        self.points = points

    def point_is_near(self, point: Point):
        for other in self.points:
            dist = point.distance_to(other)
            if dist <= CONSTELLATION_DISTANCE:
                return True
        return False

    def append(self, point):
        self.points.append(point)

    @staticmethod
    def combined_constellations(constellations):
        points = [p for c in constellations for p in c.points]
        # flat_list = [item for sublist in l for item in sublist]
        return Constellation(points)


def find_constellations(points: List[Point]):
    constellations = []
    for point in points:
        nearby_constellations = [c for c in constellations if c.point_is_near(point)]
        if nearby_constellations:
            new_constellation = Constellation.combined_constellations(nearby_constellations)
            new_constellation.append(point)
            for c in nearby_constellations:
                constellations.remove(c)
            constellations.append(new_constellation)
        else:
            constellations.append(Constellation([point]))
    return constellations
