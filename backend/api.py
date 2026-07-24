from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional
import pandas as pd

import os 
import sys
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"], # autorise toutes les origines (localhost, 127.0.0.1, etc.)
    allow_credentials=True,
    allow_methods=["*"],          # GET, POST, PUT, DELETE
    allow_headers=["*"],          # Autorise tous les headers
)

from prometheus_fastapi_instrumentator import Instrumentator

Instrumentator().instrument(app).expose(app)


sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__))))
from modules.Database import Postgres_DB
# from modules.Database import JsonStockage
# from modules.SpamshieldReport import spamshielReport
from modules.ML_Flow import ML_Flow_Operations
from modules.SpamShield_Operations import SpamShield_Operations
from modules.Model import Model

# -- ROUTES TABLEAU DE BORD --
@app.get("/dashboard-metrics")
def dashboard_metrics():
    data = SpamShield_Operations().Dashbord()
    response_data = {
        "messages" : data
    }
    return JSONResponse(status_code=200, content=response_data)
    

@app.get("/get-messages/{trier_par}/{filtrer_par}")
def get_all_messages(trier_par:str, filtrer_par:str)->dict:
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
    messages = SpamShield_Operations().Show_Messages(trier_par, filtrer_par)
    response_data = {
            "messages" : messages
        }
    return JSONResponse(status_code=200, content=response_data)
    

@app.get("/get_message-and-related-metrics/{selected_message_id}")
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
    selected_message = SpamShield_Operations().Select_Message(selected_message_id)
    response_data = {
            "selected_message" : selected_message
        }
    return JSONResponse(status_code=200, content=response_data)

@app.get("/update_label/{id}")
def update_label(id:int):
    SpamShield_Operations().Update_label(id)
    return JSONResponse(status_code=200, content={"message":"ok"})
    

# -- ROUTES BANC DE TESTS --

class Metadata(BaseModel):
    name: Optional[str] = None
    surname: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    subject: Optional[str] = None
    form_id: Optional[str] = None

class Settings(BaseModel):
    entrainementModel: bool
    recevoirParMail: bool

class NewMessageRequest(BaseModel):
    message: str
    metadata: Metadata
    settings: Settings

@app.post("/new-message")
async def new_message(newMessage: NewMessageRequest):

    # Message dans un DataFrame
    message = pd.DataFrame([{'text': newMessage.message}])

    # Metadata converti en dict
    metadata = newMessage.metadata.dict()

    # Settings converti en dict (si tu l'utilises)
    settings = newMessage.settings.dict()

    SpamShield_Operations().New_Message(message, metadata)

    return JSONResponse(status_code=200, content={"message": "ok"})


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
    regex_rules = SpamShield_Operations().Get_All_Regex_Rules()
    response_data = {
        "regex_rules" : regex_rules
    }
    return JSONResponse(status_code=200, content=response_data)

    
class RegexRequest(BaseModel):
    pattern : str
@app.post("/new-regex")
async def new_regex(data: RegexRequest):
    """Ajoute un expression régulieres interdite"""
    pattern = data.pattern
    SpamShield_Operations().Add_Regex_Rule(pattern)
    return JSONResponse(status_code=200, content={"message":"ok"})

@app.delete("/delete-regex/{id}")
async def delete_regex(id:int):
    """Supprime une expression régulieres interdite"""
    SpamShield_Operations().Delete_Regex_Rule(id)
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
    destinataires = SpamShield_Operations().Get_All_Destinataires()
    response_data = {
        "destinataires" : destinataires
    }
    return JSONResponse(status_code=200, content=response_data)

class DestinataireRequest(BaseModel):
    destinataire: str
@app.post("/new-detinataires")
async def new_detinataires(data: DestinataireRequest):
    """Ajoute un destinataire"""
    destinataire = data.destinataire
    SpamShield_Operations().Add_Destinataire(destinataire)
    return JSONResponse(status_code=200, content={"message":"ok"})

@app.delete("/delete-destinataire/{id}")
def delete_destinataire(id:int):
    """Supprime un destinataire"""
    SpamShield_Operations().Delete_Destinataire(id)
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
    form_requirements = SpamShield_Operations().Form_Requirements()
    response_data = {
        "form_requirements" : form_requirements
    }
    return JSONResponse(status_code=200, content=response_data)
    

@app.put("/update-champs-obligatoires-status/{key}")
def update_champs_obligatoire_status(key:str):
    """met à jour le status des champs obligatoires"""
    SpamShield_Operations().Update_Form_Requirements(key)
    return JSONResponse(status_code=200, content={"message":"ok"})

@app.get("/get-ai-model-infos")
def get_ai_model_infos()->dict:
    """Réccupère les informations associée au modele d'IA"""
    spamshield_infos = SpamShield_Operations().Current_Model_Metrics()
    response_data = {
       "spamshield_infos":spamshield_infos,
    }
    return JSONResponse(status_code=200, content=response_data)
    



@app.get("/build_virgin_model")
def reset_ai_model():
    """Reintilise le modèle d'ia et supprime toutes les données. Sert d'initialisation si aucun modèle existe"""
    SpamShield_Operations().virgin_model()
    return JSONResponse(status_code=200, content={"message":"ok"}) 