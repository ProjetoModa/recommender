from math import e, log
import numpy as np
class EntropyCalculator:
    def __init__(self) -> None:
        #self.nlp = spacy.load('en_core_web_sm')
        self.entities = [
            #Label, Patterns
            ["color", [
               "black",
               "blue",
               "brown",
               "beige",
               "gray",
               "green",
               "orange",
               "pink",
               "purple",
               "red",
               "white",
               "yellow",
            ]],
            ["fabric", [
                "denim",
                "knitted",
                "laced",
                "glossy",
                "velvet",
                "general",
            ]],
            ["pattern", [
                "animal_print",
                "geometric",
                "camouflage",
                "checked",
                "floral",
                "paisley",
                "plain",
                "dots",
                "striped",
                "tie_dyed",
            ]],
            ["size", [
                "maxi",
                "midi",
                "mini",
            ]],
            ["type", [
                "straight",
                "pleated",
                "skewed",
            ]],
        ]
    def calculate(self, df):       
        l = {}
        for label, ents in self.entities:
            n = len(df)
            if n <= 1:
                l[label] = 0.
                continue
            probs = []
            for ent in ents:
                probs.append(len(df[df[label] == ent]) / n)
                
            if np.count_nonzero(probs) <= 1:
                l[label] = 0.
                continue
            
            total = 0.
            for prob in probs:
                if prob > 0:
                    total -= prob * log(prob, e)
            l[label] = total
        return l
                    