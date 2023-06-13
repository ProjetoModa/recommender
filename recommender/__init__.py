from .consts import TAMANHO_MINIMO_SVM
from .quadtree import QuadTree
from .svm import SVM
from .entropy import EntropyCalculator
import pandas as pd
from pandas import DataFrame

class Recommender:
    def __init__(self, sample_size=12):
        self.sample_size = sample_size
        self.entropy_calculator = EntropyCalculator()

    def init_app(self, data: DataFrame):
        self.data = data
        self.one_hot = pd.get_dummies(data, columns=["type", "fabric", "pattern", "size", "color"], dtype=float)

    def getData(self):
        return self.data.to_json()

    def filter_slots(self, slots):
        df = self.one_hot.copy()
        for key in slots:
            if len(slots[key]) > 0:
                df = df.loc[self.data[key].isin(slots[key])]
        return df

    def recommend(self, state):
        filtered = self.filter_slots(state['slots'])
        liked = filtered.loc[filtered['name'].isin(state['liked'])]
        liked["class"] = 1
        
        if liked.shape[0] < TAMANHO_MINIMO_SVM:
            return self.recommend_random(filtered)
        return self.recommend_svm(filtered, liked)

    def recommend_svm(self, filtered: DataFrame, liked: DataFrame):
        filtered = filtered.loc[~filtered['name'].isin(liked['name'])]
        svm = SVM(filtered, liked)
        return svm.select(self.sample_size)
    
    def recommend_random(self, filtered: DataFrame):
        qt = QuadTree(filtered)
        return qt.select(self.sample_size)
    
    def entropy(self, state):
        filtered = self.filter_slots(state['slots'])
        liked = filtered[filtered['name'].isin(state['liked'])]
        filtered = filtered[~filtered['name'].isin(liked['name'])]
        return self.entropy_calculator.calculate(filtered)
