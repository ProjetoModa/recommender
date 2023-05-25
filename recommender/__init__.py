from .consts import TAMANHO_MINIMO_SVM
from .quadtree import QuadTree
from .svm import SVM
from pandas import DataFrame

class Recommender:
    def __init__(self, sample_size=12):
        self.sample_size = sample_size

    def init_app(self, data):
        self.data = data

    def getData(self):
        return self.data.to_json()

    def filter_slots(self, slots):
        df = self.data.copy()
        for key in slots:
            df = df[df[key].isin(slots[key])]
        return df

    def recommend(self, state):
        filtered = self.filter_slots(state['slots'])
        liked = filtered[filtered['name'].isin(state['liked'])]
        liked["class"] = 1
        
        if len(liked) < TAMANHO_MINIMO_SVM:
            return self.recommend_random(filtered)
        return self.recommend_svm(filtered, liked)

    def recommend_svm(self, filtered: DataFrame, liked: DataFrame):
        filtered = filtered[~filtered['name'].isin(liked['name'])]
        svm = SVM(filtered, liked)
        return svm.select(self.sample_size)
    
    def recommend_random(self, filtered: DataFrame):
        qt = QuadTree(filtered)
        return qt.select(self.sample_size)
