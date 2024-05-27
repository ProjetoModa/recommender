from recommender.point import Point
from recommender.region import Region


def test_region():
    q0 = [
        Point(6, 6, 3),
        Point(10, 10, 6),
    ]
    q1 = [
        Point(4, 6, 4),
        Point(0, 10, 7),
    ]
    q2 = [
        Point(0, 0, 0),
        Point(4, 4, 1),
        Point(5, 5, 2),
    ]
    q3 = [
        Point(6, 4, 5),
        Point(10, 0, 8),
    ]
    points = q0 + q1 + q2 + q3
    r = Region(0, 0, 10, 10, points)

    assert r.select_quad(0).points == q0
    assert r.select_quad(1).points == q1
    assert r.select_quad(2).points == q2
    assert r.select_quad(3).points == q3
