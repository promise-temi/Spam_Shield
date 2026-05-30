# from .Gibberish_detector import GibberishDetector
# from .NLP_Feat_Eng import NLP_Feat_Eng
# from .Preprocessing import Preprocessing
# from .Model import Model
# import re
# import pandas as pd

# # Valeurs Spécifiques à l'utilisateur pour les règles de filtrage mais seront stockées 
# # dans une base de données ou un fichier de configuration dans une version future
# # avec la possibilité de les mettre à jour dynamiquement via une interface d'administration
# user_discriminant_regexes = []
# user_discriminant_length_min = 5
# user_discriminant_length_max = 1000


# class SpamFilterRules:
#     def __init__(self):
#         pass

#     def giberish_score(self, text, gibberish_detector):
#         """Cette méthode calcule le score de giberish d'un texte donné en utilisant un détecteur de giberish.
#         Elle retourne le score de giberish calculé pour le texte.
#         """
#         _, score = gibberish_detector.is_gibberish(text)
#         return score
    
#     def contains_user_discriminant(self, text):
#         """Cette méthode vérifie si un texte donné contient des discriminants spécifiques à l'utilisateur.
#         Elle utilise une liste de regex pour identifier la présence de ces discriminants et retourne un booléen indiquant leur présence.
#         """
#         for regex in user_discriminant_regexes:
#             if re.search(regex, text):
#                 return True
#         return False
    
#     def length_rule(self, text):
#         """Cette méthode vérifie si la longueur d'un texte donné respecte les règles de longueur définies par l'utilisateur.
#         Elle compare la longueur du texte avec les valeurs minimales et maximales spécifiées et retourne un booléen indiquant si le texte respecte ces règles.
#         """
#         length = len(text)
#         return user_discriminant_length_min <= length <= user_discriminant_length_max
    
#     def AI_prediction_pipeline(self, text, model):
#         """Cette méthode utilise un modèle de classification pour prédire si un texte donné est du spam ou non.
#         Elle transforme le texte en caractéristiques à l'aide d'un vectoriseur, puis utilise le modèle pour faire une prédiction et retourne le résultat.
#         """
#         df = pd.DataFrame({"text": [text], "label": [0]})
#         features = NLP_Feat_Eng(df).feature_engineering_full_pipeline()
#         features_preprocessed = Preprocessing(features).preprocessing_pipeline(features)
#         model_prediction = Model().predict(model, features_preprocessed)
#         return model_prediction
    
    
    
