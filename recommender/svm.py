from .quadtree import QuadTree
from sklearn.svm import OneClassSVM
from threading import Thread
import pandas as pd
import shap
import requests
import os

FEATURES = ['type_pleated', 'type_skewed',
            'type_straight', 'fabric_denim', 'fabric_general', 'fabric_knitted',
            'fabric_lace', 'fabric_leather', 'fabric_velvet',
            'pattern_animal_print', 'pattern_camouflage', 'pattern_checked',
            'pattern_floral', 'pattern_geometric', 'pattern_paisley',
            'pattern_plain', 'pattern_polka_dot', 'pattern_striped',
            'pattern_tie_dyed', 'size_maxi', 'size_midi', 'size_mini',
            'color_beige', 'color_black', 'color_blue', 'color_brown', 'color_gray',
            'color_green', 'color_orange', 'color_pink', 'color_purple',
            'color_red', 'color_white', 'color_yellow']


def calculate_shap(explainer, x):
    shap_values = explainer.shap_values(x, nsampels=100)
    requests.post(
        os.getenv('CHATBOT_API')+"/log", json={"id": "recommender", "data": {"shap": shap_values.tolist(), "expected": explainer.expected_value, "columns": FEATURES}})


class SVM:
    def __init__(self, df, liked):
        x = liked[FEATURES]
        y = liked["class"]
        x_test = df[FEATURES]

        svc = OneClassSVM(gamma="auto", nu=0.01)
        svc.fit(x.values, y)

        predicted = svc.decision_function(x_test.values)

        explainer = shap.KernelExplainer(svc.decision_function, x.values)

        t = Thread(target=calculate_shap, args=(explainer, x_test.values))
        t.start()

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
