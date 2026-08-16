from fastapi import (
    FastAPI,
    Request,
    Depends,
    HTTPException,
    Header,
    Cookie,
    Response
)
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional
from email.message import EmailMessage

import pandas as pd
import datetime
import smtplib
import os
import sys
import logging


BASE_DIR = os.path.dirname(os.path.abspath(__file__))

sys.path.insert(
    0,
    os.path.abspath(
        os.path.join(
            os.path.dirname(__file__)
        )
    )
)

from modules.Secure import Security
from modules.SpamShield_Operations import SpamShield_Operations
from modules.Helpers_Monitoring import Helpers_Monitoring
from modules.Database import Postgres_DB


monitor = Helpers_Monitoring()
security = Security()

app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.middleware("http")
async def monitoring_middleware(
    request: Request,
    call_next
):
    response = await call_next(request)

    if response.status_code == 401:
        monitor.record_unauthorized_attempt(
            endpoint=request.url.path,
            method=request.method
        )

    if response.status_code >= 400:
        monitor.record_http_error(
            endpoint=request.url.path,
            method=request.method,
            status_code=response.status_code
        )

    return response


from prometheus_fastapi_instrumentator import Instrumentator

Instrumentator().instrument(app).expose(app)


def require_api_key(
    x_api_key: str = Header(...)
):
    if not security.verify_api_key(x_api_key):
        raise HTTPException(
            status_code=401,
            detail="Clé API invalide ou manquante."
        )


def require_session(
    session_token: Optional[str] = Cookie(default=None)
):
    if not session_token:
        raise HTTPException(
            status_code=401,
            detail="Session absente."
        )

    token_hash = security.hash_value(
        session_token
    )

    db = Postgres_DB()

    session = db.get_session_by_token(
        token_hash
    )

    if not session:
        raise HTTPException(
            status_code=401,
            detail="Session invalide."
        )

    session_id = session[0]
    email = session[1]
    expires_at = session[2]

    if (
        expires_at is None
        or datetime.datetime.now() >= expires_at
    ):
        db.delete_session(
            token_hash
        )

        raise HTTPException(
            status_code=401,
            detail="Session expirée."
        )

    return {
        "session_id": session_id,
        "email": email
    }


SpamShield_Operations().check_model_existence()


class AuthEmailRequest(BaseModel):
    email: str


class AuthCodeRequest(BaseModel):
    email: str
    code: str


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


class RegexRequest(BaseModel):
    pattern: str


class DestinataireRequest(BaseModel):
    destinataire: str

@app.post("/auth/request-code")
def request_auth_code(
    data: AuthEmailRequest
):
    email_address = os.getenv("EMAIL_ADDRESS")

    if data.email != email_address:
        raise HTTPException(
            status_code=403,
            detail="Vous n'avez pas les droits pour accéder à cette application."
        )

    db = Postgres_DB()

    code = security.generate_login_code()

    code_hash = security.hash_value(
        code
    )

    expires_at = (
        datetime.datetime.now()
        + datetime.timedelta(minutes=10)
    )

    db.create_auth_code(
        email=data.email,
        code_hash=code_hash,
        expires_at=expires_at
    )

    email_password = os.getenv(
        "EMAIL_PASSWORD"
    )

    msg = EmailMessage()

    msg["From"] = email_address
    msg["To"] = data.email
    msg["Subject"] = (
        "SpamShield - Code de connexion"
    )

    msg.set_content(
        f"""Bonjour,

Votre code de connexion SpamShield est :

{code}

Ce code est valable pendant 10 minutes.

Si vous n'êtes pas à l'origine de cette demande, ignorez simplement ce message.

SpamShield
"""
    )

    with smtplib.SMTP_SSL(
        "smtp.gmail.com",
        465
    ) as smtp:
        smtp.login(
            email_address,
            email_password
        )

        smtp.send_message(
            msg
        )

    return {
        "message": "Code envoyé."
    }


@app.post("/auth/verify-code")
def verify_auth_code(
    data: AuthCodeRequest,
    response: Response
):
    db = Postgres_DB()

    auth_data = db.get_latest_auth_code(
        data.email
    )

    if not auth_data:
        raise HTTPException(
            status_code=401,
            detail="Aucun code de connexion trouvé."
        )

    auth_id = auth_data[0]
    code_hash = auth_data[1]
    code_expires_at = auth_data[2]

    if (
        code_hash is None
        or code_expires_at is None
    ):
        raise HTTPException(
            status_code=401,
            detail="Code invalide."
        )

    if (
        datetime.datetime.now()
        >= code_expires_at
    ):
        raise HTTPException(
            status_code=401,
            detail="Code expiré."
        )

    if not security.verify_hashed_value(
        data.code,
        code_hash
    ):
        raise HTTPException(
            status_code=401,
            detail="Code invalide."
        )

    session_token = (
        security.generate_session_token()
    )

    session_token_hash = (
        security.hash_value(
            session_token
        )
    )

    session_expires_at = (
        datetime.datetime.now()
        + datetime.timedelta(days=1)
    )

    db.activate_auth_session(
        auth_id=auth_id,
        session_token_hash=session_token_hash,
        session_expires_at=session_expires_at
    )

    response.set_cookie(
        key="session_token",
        value=session_token,
        httponly=True,
        secure=False,
        samesite="lax",
        max_age=86400
    )

    return {
        "message": "Connexion réussie."
    }


@app.get("/auth/me")
def auth_me(
    session=Depends(require_session)
):
    return {
        "authenticated": True,
        "email": session["email"]
    }


@app.post("/auth/logout")
def auth_logout(
    response: Response,
    session_token: Optional[str] = Cookie(
        default=None
    )
):
    if session_token:
        token_hash = security.hash_value(
            session_token
        )

        db = Postgres_DB()

        db.delete_session(
            token_hash
        )

    response.delete_cookie(
        key="session_token"
    )

    return {
        "message": "Déconnexion réussie."
    }


@app.get("/dashboard-metrics")
def dashboard_metrics(
    _=Depends(require_session)
):
    try:
        data = (
            SpamShield_Operations()
            .Dashbord()
        )

        return JSONResponse(
            status_code=200,
            content={
                "metrics": data
            }
        )

    except Exception as e:
        logging.exception(
            "Erreur lors de la récupération des métriques du tableau de bord."
        )

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )


@app.get(
    "/get-messages/{trier_par}/{filtrer_par}"
)
def get_all_messages(
    trier_par: str,
    filtrer_par: str,
    _=Depends(require_session)
):
    try:
        messages = (
            SpamShield_Operations()
            .Show_Messages(
                trier_par,
                filtrer_par
            )
        )

        return JSONResponse(
            status_code=200,
            content={
                "messages": messages
            }
        )

    except Exception as e:
        logging.exception(
            "Erreur lors de la récupération des messages."
        )

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )


@app.get(
    "/get_message-and-related-metrics/{selected_message_id}"
)
def get_message_and_related_metrics(
    selected_message_id: int,
    _=Depends(require_session)
):
    try:
        selected_message = (
            SpamShield_Operations()
            .Select_Message(
                selected_message_id
            )
        )

        return JSONResponse(
            status_code=200,
            content={
                "selected_message":
                    selected_message
            }
        )

    except Exception as e:
        logging.exception(
            f"Erreur lors de la récupération du message {selected_message_id}."
        )

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )


@app.get("/update_label/{id}")
def update_label(
    id: int,
    _=Depends(require_session)
):
    try:
        SpamShield_Operations().Update_label(
            id
        )

        return JSONResponse(
            status_code=200,
            content={
                "message": "ok"
            }
        )

    except Exception as e:
        logging.exception(
            f"Erreur lors de la mise à jour du label du message {id}."
        )

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )


@app.post("/new-message")
async def new_message(
    newMessage: NewMessageRequest,
    _=Depends(require_api_key)
):
    try:
        message = pd.DataFrame(
            [
                {
                    "text":
                        newMessage.message
                }
            ]
        )

        metadata = (
            newMessage
            .metadata
            .model_dump()
        )

        SpamShield_Operations().New_Message(
            message,
            metadata
        )

        return JSONResponse(
            status_code=200,
            content={
                "message": "ok"
            }
        )

    except Exception as e:
        logging.exception(
            "Erreur lors du traitement d'un nouveau message."
        )

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )


@app.get("/get-regexes")
def get_regexes(
    _=Depends(require_session)
):
    try:
        regex_rules = (
            SpamShield_Operations()
            .Get_All_Regex_Rules()
        )

        return JSONResponse(
            status_code=200,
            content={
                "regex_rules":
                    regex_rules
            }
        )

    except Exception as e:
        logging.exception(
            "Erreur lors de la récupération des règles regex."
        )

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )


@app.post("/new-regex")
async def new_regex(
    data: RegexRequest,
    _=Depends(require_session)
):
    try:
        SpamShield_Operations().Add_Regex_Rule(
            data.pattern
        )

        return JSONResponse(
            status_code=200,
            content={
                "message": "ok"
            }
        )

    except Exception as e:
        logging.exception(
            "Erreur lors de l'ajout d'une règle regex."
        )

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )


@app.delete("/delete-regex/{id}")
async def delete_regex(
    id: int,
    _=Depends(require_session)
):
    try:
        SpamShield_Operations().Delete_Regex_Rule(
            id
        )

        return JSONResponse(
            status_code=200,
            content={
                "message": "ok"
            }
        )

    except Exception as e:
        logging.exception(
            f"Erreur lors de la suppression de la règle regex {id}."
        )

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )


@app.get("/get-detinataires")
def get_detinataires(
    _=Depends(require_session)
):
    try:
        destinataires = (
            SpamShield_Operations()
            .Get_All_Destinataires()
        )

        return JSONResponse(
            status_code=200,
            content={
                "destinataires":
                    destinataires
            }
        )

    except Exception as e:
        logging.exception(
            "Erreur lors de la récupération des destinataires."
        )

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )


@app.post("/new-detinataires")
async def new_detinataires(
    data: DestinataireRequest,
    _=Depends(require_session)
):
    try:
        SpamShield_Operations().Add_Destinataire(
            data.destinataire
        )

        return JSONResponse(
            status_code=200,
            content={
                "message": "ok"
            }
        )

    except Exception as e:
        logging.exception(
            "Erreur lors de l'ajout d'un destinataire."
        )

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )


@app.delete(
    "/delete-destinataire/{id}"
)
def delete_destinataire(
    id: int,
    _=Depends(require_session)
):
    try:
        SpamShield_Operations().Delete_Destinataire(
            id
        )

        return JSONResponse(
            status_code=200,
            content={
                "message": "ok"
            }
        )

    except Exception as e:
        logging.exception(
            f"Erreur lors de la suppression du destinataire {id}."
        )

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )


@app.get(
    "/get-champs-obligatoires-status"
)
def get_champs_obligatoire_status(
    _=Depends(require_session)
):
    try:
        form_requirements = (
            SpamShield_Operations()
            .Form_Requirements()
        )

        return JSONResponse(
            status_code=200,
            content={
                "form_requirements":
                    form_requirements
            }
        )

    except Exception as e:
        logging.exception(
            "Erreur lors de la récupération du statut des champs obligatoires."
        )

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )


@app.put(
    "/update-champs-obligatoires-status/{key}"
)
def update_champs_obligatoire_status(
    key: str,
    _=Depends(require_session)
):
    try:
        (
            SpamShield_Operations()
            .Update_Form_Requirements(
                key
            )
        )

        return JSONResponse(
            status_code=200,
            content={
                "message": "ok"
            }
        )

    except Exception as e:
        logging.exception(
            f"Erreur lors de la mise à jour du champ obligatoire {key}."
        )

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )


@app.get("/get-ai-model-infos")
def get_ai_model_infos(
    _=Depends(require_session)
):
    try:
        spamshield_infos = (
            SpamShield_Operations()
            .Current_Model_Metrics()
        )

        return JSONResponse(
            status_code=200,
            content={
                "spamshield_infos":
                    spamshield_infos
            }
        )

    except Exception as e:
        logging.exception(
            "Erreur lors de la récupération des informations du modèle IA."
        )

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )


@app.get("/build_virgin_model")
def build_virgin_model(
    _=Depends(require_session)
):
    try:
        SpamShield_Operations().virgin_model()

        return JSONResponse(
            status_code=200,
            content={
                "message": "ok"
            }
        )

    except Exception as e:
        logging.exception(
            "Erreur lors de la réinitialisation du modèle IA."
        )

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )


@app.get("/retrain_model")
def retrain_model(
    _=Depends(require_session)
):
    try:
        SpamShield_Operations().retrain_model()

        return JSONResponse(
            status_code=200,
            content={
                "message": "ok"
            }
        )

    except Exception as e:
        logging.exception(
            "Erreur lors du réentraînement du modèle IA."
        )

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )


@app.get("/llm-report")
def get_llm_report(
    _=Depends(require_session)
):
    try:
        report_data = (
            SpamShield_Operations()
            .llm_report()
        )

        return JSONResponse(
            status_code=200,
            content=report_data
        )

    except Exception as e:
        logging.exception(
            "Erreur lors de la génération du rapport LLM."
        )

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )