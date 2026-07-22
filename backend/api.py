from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

import os 
import sys
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
app = FastAPI()

from prometheus_fastapi_instrumentator import Instrumentator

Instrumentator().instrument(app).expose(app)


sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__))))
from modules.Database import Postgres_DB
from modules.Database import JsonStockage
from modules.SpamshieldReport import spamshielReport
from modules.ML_Flow import ML_Flow_Operations
from modules.SpamShield_Operations import SpamShield_Operations


# -- ROUTES TABLEAU DE BORD --
app.get('dashbord-metrics-and-graphs')
def get_dashbord_metrics_and_graphs()->dict:
    """
    Pour le tableau de bord:
        - Réccuperation de la période actuelle
        - Réccupération des données pour les métriques 
        - Réccuperation des données pour les graphiques 
    
    Returns:
        {
            "period": {
                "start" : String,
                "end" : String
            },
            "metrics": {
                "messages" : Int,
                "legitimes" : Int,
                "indesirable" : Int,
                "corrections" : Int,
                "reclassement" : Int
            },
            "graphics" :{
                "distrubution_par_categorie" : {
                    "ham_prediction_ia" : Int,
                    "spam_patterns_interdits" : Int,
                    "spam_prediction_ia" : Int,
                    "spam_low_condidence" : Int,
                    "ham_corriges" : Int,
                    "spam_corriges" : Int,
                },
                "evolution_par_categorie" : {
                    "ham_prediction_ia" : List[int],
                    "spam_patterns_interdits" : List[int],
                    "spam_prediction_ia" : List[int],
                    "spam_low_condidence" : List[int],
                    "ham_corriges" : List[int],
                    "spam_corriges" : List[int],
                }
            }
        }
    """
    pass

app.get("get-messages/{trier_par}/{filter_par}")
def get_messages(trier_par:str, filtrer_par:str)->dict:
    """
    Réccupération des message - Tout (par défault) ou filtré (selon filtres)
    Returns:
        {
            "messages" : List[
                {
                    "label" : String,
                    "date" : String,
                    "metadata" : Dict,
                    "message" : String,
                    "id" : Int
                }
            ]
        }
    """
    pass

app.get("get_message-and-related-metrics/{selected_message_id}")
def get_message_and_related_metrics(selected_message_id:int)->dict:
    """ 
    Réccupère le message ainsi que les metriques et informations les predictions du model ia et métier et autres

    Returns:
        {
            "message_consulte" : Boolean,
            "message_recu" : Boolean,
            "label_final : String,
            "model_ia_prediction" : String,
            "model_ia_score_confiance" : Float,
            "regles_metiers_deliberation" : String,
            "regles_metiers_shemas_interdit" : List,
            "reclasse" : Boolean,
            "corrige" : Boolean,
            "date" : String,
            "metadata" : Dict,
            "message" : String,
            "id" : Int
        }
    """
    pass 

# -- ROUTES BANC DE TESTS --

@app.post("/new-message")
async def new_message(request: Request):
    """Depuis un formulaire d'un site externe appartenant a l'utilisateur fait l'ingestion d'un nouveau message"""
    data = await request.json()
    message = {'text' : data['message']}
    metadata = data['metadata']
    SpamShield_Operations().New_Message(message, metadata)
    return JSONResponse(status_code=200, content={"message":"ok"})

# -- ROUTES PARAMETRES --

@app.get("/get-regexes")
def get_regexes()->dict:
    """
    Réccupère les expression régulieres interdites

    Returns:
        {
           "regexes" : List 
        }
    """
    regex_rules = Postgres_DB().get_all_regex_rules()
    response_data = {
        "regex_rules" : regex_rules
    }
    return JSONResponse(status_code=200, content=response_data)

    


@app.post("/new-regex")
async def new_regex(request: Request):
    """Ajoute un expression régulieres interdite"""
    data = await request.json()
    pattern = data['pattern']
    Postgres_DB().add_regex_rule(pattern)
    return JSONResponse(status_code=200, content={"message":"ok"})

@app.delete("/delete-regex/{id}")
async def delete_regex(id:int):
    """Supprime une expression régulieres interdite"""
    Postgres_DB().delete_regex_rule(id)
    return JSONResponse(status_code=200, content={"message":"ok"})

@app.get("/get-detinataires")
def get_detinataires()->dict:
    """
    Réccupère les destinataires
    Returns:
        {
           "destinataires" : List 
        }
    """
    destinataires = Postgres_DB().get_prospect_mail()
    response_data = {
        "destinataires" : destinataires
    }
    return JSONResponse(status_code=200, content=response_data)

@app.post("/new-detinataires")
async def new_detinataires(request: Request):
    """Ajoute un destinataire"""
    data = await request.json()
    destinataire = data['destinataire']
    Postgres_DB().add_prospect_mail([destinataire])
    return JSONResponse(status_code=200, content={"message":"ok"})

@app.delete("/delete-destinataire/{id}")
def delete_destinataire(id:int):
    """Supprime un destinataire"""
    Postgres_DB().delete_prospect_mail([id])
    return JSONResponse(status_code=200, content={"message":"ok"})

@app.get("/get-champs-obligatoires-status")
def get_champs_obligatoire_status():
    """
    Récupère le status des champs obligatoires

    Returns : {
        "nom" : Boolean,
        "Prenom" : Boolean,
        "Objet" : Boolean,
        "Email" : Boolean,
        "Telephone" : Boolean,  
    }
    """
    form_requirements = JsonStockage().get_form_requirements()
    response_data = {
        "form_requirements" : form_requirements
    }
    return JSONResponse(status_code=200, content=response_data)
    

@app.put("/update-champs-obligatoires-status/{key}")
def update_champs_obligatoire_status(key:str):
    """met à jour le status des champs obligatoires"""
    JsonStockage().edit_form_requirements(key)
    return JSONResponse(status_code=200, content={"message":"ok"})

@app.get("/get-ai-model-infos")
def get_ai_model_infos()->dict:
    """Réccupère les informations associée au modele d'IA"""
    spamshield_infos = spamshielReport.model_and_system_report_infos()
    response_data = {
       "spamshield_infos":spamshield_infos,
    }
    return JSONResponse(status_code=200, content=response_data)
    

@app.post("/restore-ai-model")
async def restore_ai_model(request: Request):
    """Reccupere un précédent model d'IA souhaité."""
    data = await request.json()
    previous_model_id = data['odlModelID']
    ML_Flow_Operations().restore_previous_model(previous_model_id)
    return JSONResponse(status_code=200, content={"message":"ok"})

app.get("/reset-ai-model")
def reset_ai_model():
    """Reintilise le modèle d'ia et supprime toutes les donnée."""
    return JSONResponse(status_code=200, content={"message":"ok"})