from fastapi import FastAPI, Request, Depends, HTTPException, Header
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional
import pandas as pd

import os 
import sys
import logging
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
from modules.Secure import Security

# from modules.Database import JsonStockage
# from modules.SpamshieldReport import spamshielReport
from modules.ML_Flow import ML_Flow_Operations
from modules.SpamShield_Operations import SpamShield_Operations
from modules.LLModel import LLMModel


security = Security() 

def require_api_key(x_api_key: str = Header(...)):
    if not security.verify_api_key(x_api_key):
        raise HTTPException(status_code=401, detail="Clé API invalide ou manquante.")












# -- ROUTES TABLEAU DE BORD --

# -- ROUTES TABLEAU DE BORD --
@app.get("/dashboard-metrics")
def dashboard_metrics(_=Depends(require_api_key)):
    try:
        data = SpamShield_Operations().Dashbord()
        response_data = {
            "metrics" : data
        }
        return JSONResponse(status_code=200, content=response_data)
    except Exception as e:
        logging.exception("Erreur lors de la récupération des métriques du tableau de bord.")
        raise HTTPException(status_code=500, detail=str(e))
 
 
@app.get("/get-messages/{trier_par}/{filtrer_par}")
def get_all_messages(trier_par:str, filtrer_par:str, _=Depends(require_api_key))->dict:
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
    try:
        messages = SpamShield_Operations().Show_Messages(trier_par, filtrer_par)
        response_data = {
                "messages" : messages
            }
        return JSONResponse(status_code=200, content=response_data)
    except Exception as e:
        logging.exception("Erreur lors de la récupération des messages.")
        raise HTTPException(status_code=500, detail=str(e))
 
 
@app.get("/get_message-and-related-metrics/{selected_message_id}")
def get_message_and_related_metrics(selected_message_id:int, _=Depends(require_api_key))->dict:
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
    try:
        selected_message = SpamShield_Operations().Select_Message(selected_message_id)
        response_data = {
                "selected_message" : selected_message
            }
        return JSONResponse(status_code=200, content=response_data)
    except Exception as e:
        logging.exception(f"Erreur lors de la récupération du message {selected_message_id}.")
        raise HTTPException(status_code=500, detail=str(e))
 
 
@app.get("/update_label/{id}")
def update_label(id:int, _=Depends(require_api_key)):
    try:
        SpamShield_Operations().Update_label(id)
        return JSONResponse(status_code=200, content={"message":"ok"})
    except Exception as e:
        logging.exception(f"Erreur lors de la mise à jour du label du message {id}.")
        raise HTTPException(status_code=500, detail=str(e))
 
 
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
async def new_message(newMessage: NewMessageRequest, _=Depends(require_api_key)):
    try:
        # Message dans un DataFrame
        message = pd.DataFrame([{'text': newMessage.message}])
 
        # Metadata converti en dict
        metadata = newMessage.metadata.dict()
 
        # Settings converti en dict (si tu l'utilises)
        settings = newMessage.settings.dict()
 
        SpamShield_Operations().New_Message(message, metadata)
 
        return JSONResponse(status_code=200, content={"message": "ok"})
    except Exception as e:
        logging.exception("Erreur lors du traitement d'un nouveau message.")
        raise HTTPException(status_code=500, detail=str(e))
 
 
# -- ROUTES PARAMETRES --
 
@app.get("/get-regexes")
def get_regexes(_=Depends(require_api_key))->dict:
    """
    Réccupère les expression régulieres interdites
 
    Returns:
        {
           "regexes" : List 
        }
    """
    try:
        regex_rules = SpamShield_Operations().Get_All_Regex_Rules()
        response_data = {
            "regex_rules" : regex_rules
        }
        return JSONResponse(status_code=200, content=response_data)
    except Exception as e:
        logging.exception("Erreur lors de la récupération des règles regex.")
        raise HTTPException(status_code=500, detail=str(e))
 
    
class RegexRequest(BaseModel):
    pattern : str
@app.post("/new-regex")
async def new_regex(data: RegexRequest, _=Depends(require_api_key)):
    """Ajoute un expression régulieres interdite"""
    try:
        pattern = data.pattern
        SpamShield_Operations().Add_Regex_Rule(pattern)
        return JSONResponse(status_code=200, content={"message":"ok"})
    except Exception as e:
        logging.exception("Erreur lors de l'ajout d'une règle regex.")
        raise HTTPException(status_code=500, detail=str(e))
 
 
@app.delete("/delete-regex/{id}")
async def delete_regex(id:int, _=Depends(require_api_key)):
    """Supprime une expression régulieres interdite"""
    try:
        SpamShield_Operations().Delete_Regex_Rule(id)
        return JSONResponse(status_code=200, content={"message":"ok"})
    except Exception as e:
        logging.exception(f"Erreur lors de la suppression de la règle regex {id}.")
        raise HTTPException(status_code=500, detail=str(e))
 
 
@app.get("/get-detinataires")
def get_detinataires(_=Depends(require_api_key))->dict:
    """
    Réccupère les destinataires
    Returns:
        {
           "destinataires" : List 
        }
    """
    try:
        destinataires = SpamShield_Operations().Get_All_Destinataires()
        response_data = {
            "destinataires" : destinataires
        }
        return JSONResponse(status_code=200, content=response_data)
    except Exception as e:
        logging.exception("Erreur lors de la récupération des destinataires.")
        raise HTTPException(status_code=500, detail=str(e))
 
 
class DestinataireRequest(BaseModel):
    destinataire: str
@app.post("/new-detinataires")
async def new_detinataires(data: DestinataireRequest, _=Depends(require_api_key)):
    """Ajoute un destinataire"""
    try:
        destinataire = data.destinataire
        SpamShield_Operations().Add_Destinataire(destinataire)
        return JSONResponse(status_code=200, content={"message":"ok"})
    except Exception as e:
        logging.exception("Erreur lors de l'ajout d'un destinataire.")
        raise HTTPException(status_code=500, detail=str(e))
 
 
@app.delete("/delete-destinataire/{id}")
def delete_destinataire(id:int, _=Depends(require_api_key)):
    """Supprime un destinataire"""
    try:
        SpamShield_Operations().Delete_Destinataire(id)
        return JSONResponse(status_code=200, content={"message":"ok"})
    except Exception as e:
        logging.exception(f"Erreur lors de la suppression du destinataire {id}.")
        raise HTTPException(status_code=500, detail=str(e))
 
 
@app.get("/get-champs-obligatoires-status")
def get_champs_obligatoire_status(_=Depends(require_api_key)):
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
    try:
        form_requirements = SpamShield_Operations().Form_Requirements()
        response_data = {
            "form_requirements" : form_requirements
        }
        return JSONResponse(status_code=200, content=response_data)
    except Exception as e:
        logging.exception("Erreur lors de la récupération du statut des champs obligatoires.")
        raise HTTPException(status_code=500, detail=str(e))
 
 
@app.put("/update-champs-obligatoires-status/{key}")
def update_champs_obligatoire_status(key:str, _=Depends(require_api_key)):
    """met à jour le status des champs obligatoires"""
    try:
        SpamShield_Operations().Update_Form_Requirements(key)
        return JSONResponse(status_code=200, content={"message":"ok"})
    except Exception as e:
        logging.exception(f"Erreur lors de la mise à jour du champ obligatoire {key}.")
        raise HTTPException(status_code=500, detail=str(e))
 
 
@app.get("/get-ai-model-infos")
def get_ai_model_infos(_=Depends(require_api_key))->dict:
    """Réccupère les informations associée au modele d'IA"""
    try:
        spamshield_infos = SpamShield_Operations().Current_Model_Metrics()
        response_data = {
           "spamshield_infos":spamshield_infos,
        }
        return JSONResponse(status_code=200, content=response_data)
    except Exception as e:
        logging.exception("Erreur lors de la récupération des informations du modèle IA.")
        raise HTTPException(status_code=500, detail=str(e))
 
 
@app.get("/build_virgin_model")
def reset_ai_model(_=Depends(require_api_key)):
    """Reintilise le modèle d'ia et supprime toutes les données. Sert d'initialisation si aucun modèle existe"""
    try:
        SpamShield_Operations().virgin_model()
        return JSONResponse(status_code=200, content={"message":"ok"})
    except Exception as e:
        logging.exception("Erreur lors de la réinitialisation du modèle IA.")
        raise HTTPException(status_code=500, detail=str(e))
 
 
@app.get("/llm-report")
def get_llm_report(_=Depends(require_api_key)):
    try:
        report_data = LLMModel().generate_report_mistral()
        return JSONResponse(status_code=200, content=report_data)
    except Exception as e:
        logging.exception("Erreur lors de la génération du rapport LLM.")
        raise HTTPException(status_code=500, detail=str(e))






