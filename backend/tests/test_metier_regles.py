import sys 
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'modules')))
from Markov_Model import MarkovGibberishDetector
import pandas as pd

def test_markov():
    df = pd.read_parquet(f"{os.path.dirname(__file__)}/test_ressources/corpus.parquet")
    detector = MarkovGibberishDetector()
    detector.train_model(df["token"].tolist())
    print(detector.is_gibberish("Bonjour ejhevjjgcgcytd uyffufut gfyzfgeg?"))
