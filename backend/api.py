from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
import os 
import sys
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
app = FastAPI()
templates = Jinja2Templates(directory=f"{BASE_DIR}/html_templates")
# Static files (CSS, JS, images)
app.mount("/css", StaticFiles(directory=f"{BASE_DIR}/html_templates/css"), name="static_css")
app.mount("/js", StaticFiles(directory=f"{BASE_DIR}/html_templates/js"), name="static_js")
app.mount("/images", StaticFiles(directory=f"{BASE_DIR}/html_templates/images"), name="static_images")

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__))))
from modules.Database import Postgres_DB



# -- PAGE FRONTEND TABLEAU DE BORD --
@app.get("/tableau-de-bord")
def showpage_tableau_de_bord(request: Request):
    regexes = Postgres_DB().get_all_regex_rules()
    return templates.TemplateResponse("tableau-de-bord.html", {"request": request, "regexes": regexes})

# -- PAGE FRONTEND BANC DE TESTS --
@app.get("/banc-de-test")
def showpage_banc_de_test(request: Request):
    return templates.TemplateResponse("banc-de-test.html", {"request": request})

@app.get("/parametres")
def showpage_parametres(request: Request):
    return templates.TemplateResponse("options.html", {"request": request})


# # -- PAGE FRONTEND PARAMETRES --
# app.get("/parametres")
# def showpage_parametres(request: Request):
#     return templates.TemplateResponse("options.html", {"request": request})


# # -- PAGE FRONTEND TABLEAU DE BORD --
# @app.get("/tableau-de-bord")
# def showpage_tableau_de_bord(request: Request):
#     return templates.TemplateResponse("tableau-de-bord.html", {"request": request})

# # -- PAGE FRONTEND BANC DE TESTS --
# app.get("/banc-de-test")
# def showpage_banc_de_test(request: Request):
#     return templates.TemplateResponse("banc-de-test.html", {"request": request})

# # -- PAGE FRONTEND PARAMETRES --
# app.get("/parametres")
# def showpage_parametres(request: Request):
#     return templates.TemplateResponse("options.html", {"request": request})



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
app.post("test-new-message")
def test_new_message():
    """Depuis l'interface SpamSield permet de tester l'ingestion d'un nouveau message"""
    pass

app.post("new-message")
def new_message():
    """Depuis un formulaire d'un site externe appartenant a l'utilisateur fait l'ingestion d'un nouveau message"""
    pass


# -- ROUTES PARAMETRES --

app.get("get-regexes")
def get_regexes()->dict:
    """
    Réccupère les expression régulieres interdites

    Returns:
        {
           "regexes" : List 
        }
    """
    pass

app.post("new-regex")
def new_regex():
    """Ajoute un expression régulieres interdite"""
    pass

app.delete("delete-regex/{id}")
def delete_regex(id:int):
    """Supprime une expression régulieres interdite"""
    pass

app.get("get-detinataires")
def get_detinataires()->dict:
    """
    Réccupère les destinataires
    Returns:
        {
           "destinataires" : List 
        }
    """
    pass

app.post("new-detinataires")
def new_detinataires():
    """Ajoute un detinataires""" 
    pass

app.delete("delete-destinataire/{id}")
def delete_destinataire(id:int):
    """Supprime un destinataire"""
    pass

app.get("get-champs-obligatoires-status")
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
    pass

app.put("update-champs-obligatoires-status/{status_id}")
def update_champs_obligatoire_status(status_id:int):
    """met à jour le status des champs obligatoires"""
    pass


app.post("restore-ai-model")
def restore_ai_model():
    """Reccupere un précédent model d'IA souhaité."""
    pass

app.post("reset-ai-model")
def reset_ai_model():
    """Reintilise le modèle d'ia et supprime toutes les donnée."""
    pass