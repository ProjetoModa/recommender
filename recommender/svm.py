from .quadtree import QuadTree
from sklearn.svm import OneClassSVM
import pandas as pd


class SVM:
    def __init__(self, df, liked):
        x = liked[["x", "y"]]
        y = liked["class"]

        svc = OneClassSVM(gamma="auto", nu=0.01)
        svc.fit(x, y)

        predicted = svc.decision_function(df[["x", "y"]])

        df["class"] = predicted
        df = df.sort_values(by=['class'], ascending=False)
        self.df = df

    def select(self, sample_size):
        classified = self.df
        classified['cuts'] = pd.qcut(classified['class'], q=4, labels=[
                                     'lower', 'mid-low', 'mid-high', 'upper'])

        positive = self.calculate_prob(
            classified[classified['cuts'] == 'upper'])
        negative = self.calculate_prob(
            classified[classified['cuts'] == 'lower'])

        return self.quadtree_sample(positive, sample_size//2 + (sample_size % 2)) + self.quadtree_sample(negative, sample_size//2)

    def quadtree_sample(self, df, sample_size):
        sample_size = min(sample_size, len(df))
        select_size = min(sample_size*10, len(df))
        df = df.sample(n=select_size)
        qt = QuadTree(df)
        return qt.select(sample_size)

    def calculate_prob(self, df):
        class_sum = df['class'].values.sum()
        df = df.sort_values(by=['class'], ascending=True)

        pj = []
        sum_pj = []
        last = 0

        for c in df['class'].tolist():
            prob = c / class_sum
            last += prob
            pj.append(prob)
            sum_pj.append(last)

        df['pj'] = pj
        df['sum_pj'] = sum_pj

        return df
