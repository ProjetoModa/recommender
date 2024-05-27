from recommender.point import Point
from recommender.quadtree import QuadTree
from recommender.region import Region
import pandas as pd


def test_quadtree():
    df = pd.DataFrame(
        {
            'x': [0, 4, 5, 6, 4, 6, 10, 0, 10],
            'y': [0, 4, 5, 6, 6, 4, 10, 10, 0],
            'name': [
                'Fig0',
                'Fig1',
                'Fig2',
                'Fig3',
                'Fig4',
                'Fig5',
                'Fig6',
                'Fig7',
                'Fig8',
            ],
        }
    )
    qt = QuadTree(df, 1, 3)
    N = 4
    sample = qt.select(N)
    sample_set = set(sample)
    assert len(sample) == N
    assert len(sample_set) == N
