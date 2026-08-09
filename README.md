# Spam_Shield
Outil anti-abus évolutif - RNCP37827 Développeur en Intélligence Artificielle

uvicorn backend.api:app --reload             

command : mlflow ui
http://127.0.0.1:5000


pip install -r requirements.txt

mlflow ui --host 0.0.0.0 --port 5000

gmail:
Mots de passe des applications

docker-compose -f docker-compose.dev.yml up --build

creer une clé d'encryption:
from cryptography.fernet import Fernet
key = Fernet.generate_key()
print(key.decode())

grafana
http://localhost:3000

docker compose exec postgres psql -U postgres -d spamshield

DROP SCHEMA public CASCADE;
CREATE SCHEMA public;


pour voir les logs pytests
pytest -o log_cli=true --log-cli-level=DEBUG tests


https://eduscol.education.gouv.fr/sites/default/files/document/guide-la-grammaire-du-francais-terminologie-grammaticale-67998.pdf





si nom et prenom renseignée dans les metadonnée, le cacher dans le texte avec [SENSITIVE]


Message brut
       │
       ▼
 ┌──────────────────────┐
 │ Structure            │
 │ • longueur           │
 │ • ponctuation        │
 │ • casse              │
 └──────────────────────┘
       │
       ▼
 ┌──────────────────────┐
 │ Entités              │
 │ • emails             │
 │ • téléphones         │
 │ • urls               │
 │ • argent             │
 │ • dates              │
 └──────────────────────┘
       │
       ▼
 ┌──────────────────────┐
 │ Linguistique         │
 │ • pronoms            │
 │ • négations          │
 │ • temporalité        │
 │ • salutations        │
 └──────────────────────┘
       │
       ▼
 ┌──────────────────────┐
 │ Psychologie          │
 │ • urgence            │
 │ • menace             │
 │ • autorité           │
 │ • récompense         │
 └──────────────────────┘
       │
       ▼
 ┌──────────────────────┐
 │ Normalisation        │
 │ • anonymisation      │
 │ • nettoyage          │
 │ • corpus             │
 └──────────────────────┘
       │
       ▼
Vecteur de caractéristiques














Phase N
┌─────────────────────┐
│ 21 jours            │
│ collecte feedback   │
│ corrections labels  │
└─────────────────────┘
          ↓

Période de carence
┌─────────────────────┐
│ 7 jours             │
│ attente labels      │
│ stabilisation       │
└─────────────────────┘
          ↓

Réentraînement
          ↓

Évaluation
          ↓

Déploiement



Il peut arriver que fast api ne se lance pas simplement parce que la base de donnée ne marche pas. C'est une erreur vicieuse

python -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt





uvicorn backend.api:app --reload


cle api mistral : console.mistral.ai

pip install -U google-genai






















# SpamShield

Outil anti-abus évolutif — projet réalisé dans le cadre du titre professionnel Développeur en Intelligence Artificielle (RNCP 37827).

SpamShield protège les formulaires de contact contre les soumissions indésirables grâce à un modèle statistique (SVC), des règles métier configurables, un détecteur de charabia, et un service d'intelligence artificielle générative (Mistral / Gemini) chargé de vulgariser les résultats pour un utilisateur non technique.

## Sommaire

- [Prérequis](#prérequis)
- [Installation](#installation)
- [Variables d'environnement](#variables-denvironnement)
- [Lancer l'application](#lancer-lapplication)
- [Base de données](#base-de-données)
- [Suivi des modèles avec MLflow](#suivi-des-modèles-avec-mlflow)
- [Tests](#tests)
- [Sécurité et protection des données](#sécurité-et-protection-des-données)
- [Pipeline de pré-traitement des messages](#pipeline-de-pré-traitement-des-messages)
- [Cycle de vie et réentraînement du modèle](#cycle-de-vie-et-réentraînement-du-modèle)
- [Intégration des services d'IA générative](#intégration-des-services-dia-générative)
- [Dépannage](#dépannage)
- [Ressources](#ressources)

## Prérequis

- Python 3.11 ou supérieur
- Docker et Docker Compose (pour PostgreSQL)
- Un compte Mistral AI (`console.mistral.ai`) et/ou un compte Google AI Studio, selon le fournisseur de LLM utilisé

## Installation

```bash
python -m venv venv
source venv/bin/activate      # sous Windows : venv\Scripts\activate
pip install --upgrade pip
pip install -r requirements.txt
```

## Variables d'environnement

Créer un fichier `.env` à la racine du projet à partir du modèle suivant (aucune valeur réelle ne doit être versionnée dans Git — `.env` doit figurer dans `.gitignore`) :

```
MISTRAL_API_KEY=
GEMINI_API_KEY=

# Compte Gmail utilisé pour l'envoi automatique des rapports par e-mail.
# Nécessite un "mot de passe d'application" Google (et non le mot de passe du compte),
# généré depuis les paramètres de sécurité du compte Gmail.
GMAIL_APP_PASSWORD=

# Clé utilisée pour chiffrer les données sensibles stockées (voir section
# "Sécurité et protection des données" ci-dessous).
ENCRYPTION_KEY=
```

La clé API Mistral se génère depuis `console.mistral.ai`. La clé API Gemini se génère depuis Google AI Studio.

La clé de chiffrement se génère avec la commande suivante :

```python
from cryptography.fernet import Fernet
key = Fernet.generate_key()
print(key.decode())
```

## Lancer l'application

```bash
uvicorn backend.api:app --reload
```

## Base de données

PostgreSQL est démarré via Docker Compose (voir `docker-compose.yml` à la racine du projet).

Pour se connecter à la base en ligne de commande :

```bash
docker compose exec postgres psql -U postgres -d spamshield
```

Pour réinitialiser complètement le schéma (⚠️ supprime toutes les données) :

```sql
DROP SCHEMA public CASCADE;
CREATE SCHEMA public;
```

## Suivi des modèles avec MLflow

```bash
mlflow ui --host 0.0.0.0 --port 5000
```

Interface accessible sur : http://127.0.0.1:5000

## Tests

```bash
pytest -o log_cli=true --log-cli-level=DEBUG tests
```

L'option `log_cli` affiche les logs en direct pendant l'exécution des tests, utile pour diagnostiquer un test qui échoue silencieusement.

## Sécurité et protection des données

Conformément au principe de minimisation des données (RGPD), plusieurs mesures sont appliquées :

- **Anonymisation des métadonnées personnelles** : si un nom et un prénom sont renseignés dans les métadonnées d'un message, ils sont masqués dans le texte transmis en aval (y compris aux services de LLM externes) par le marqueur `[SENSITIVE]`, plutôt que d'être transmis en clair.
- **Chiffrement** : les données sensibles stockées en base sont chiffrées à l'aide de la bibliothèque `cryptography` (Fernet), avec une clé dédiée (`ENCRYPTION_KEY`, voir section précédente).
- **Notification par e-mail** : l'envoi de rapports par Gmail nécessite un mot de passe d'application dédié plutôt que les identifiants principaux du compte, limitant la surface d'exposition en cas de fuite de la variable d'environnement.
- **Minimisation des données envoyées aux LLM** : seules des métriques agrégées (voir la partie "Intégration des services d'IA générative") sont transmises à Mistral ou Gemini — jamais le contenu brut des messages, les noms, e-mails ou numéros de téléphone.

## Pipeline de pré-traitement des messages

Chaque message brut traverse les étapes suivantes avant d'être transformé en vecteur de caractéristiques exploitable par le modèle de classification :

```
Message brut
     │
     ▼
┌──────────────────────┐
│ Structure             │
│ • longueur             │
│ • ponctuation          │
│ • casse                │
└──────────────────────┘
     │
     ▼
┌──────────────────────┐
│ Entités                │
│ • emails               │
│ • téléphones           │
│ • urls                 │
│ • argent                │
│ • dates                 │
└──────────────────────┘
     │
     ▼
┌──────────────────────┐
│ Linguistique            │
│ • pronoms               │
│ • négations             │
│ • temporalité           │
│ • salutations           │
└──────────────────────┘
     │
     ▼
┌──────────────────────┐
│ Psychologie             │
│ • urgence               │
│ • menace                │
│ • autorité               │
│ • récompense            │
└──────────────────────┘
     │
     ▼
┌──────────────────────┐
│ Normalisation           │
│ • anonymisation          │
│ • nettoyage              │
│ • corpus                 │
└──────────────────────┘
     │
     ▼
Vecteur de caractéristiques
```

Chaque étape enrichit progressivement la représentation du message : caractéristiques structurelles superficielles d'abord, puis entités nommées, marqueurs linguistiques, signaux psychologiques (souvent révélateurs de tentatives de manipulation dans les spams), et enfin normalisation/anonymisation avant intégration au corpus d'entraînement.

## Cycle de vie et réentraînement du modèle

```
Phase N
┌─────────────────────┐
│ 21 jours             │
│ collecte feedback    │
│ corrections labels   │
└─────────────────────┘
          │
          ▼
Période de carence
┌─────────────────────┐
│ 7 jours              │
│ attente labels       │
│ stabilisation        │
└─────────────────────┘
          │
          ▼
     Réentraînement
          │
          ▼
       Évaluation
          │
          ▼
      Déploiement
```

- **Phase de collecte (21 jours)** : les corrections apportées par les utilisateurs sur les classifications sont accumulées.
- **Période de carence (7 jours)** : temps d'attente supplémentaire avant réentraînement, pour laisser les labels se stabiliser et éviter d'intégrer des corrections encore incertaines ou contradictoires.
- **Réentraînement** : le modèle est ré-entraîné en intégrant les nouvelles corrections validées.
- **Évaluation** : les métriques du nouveau modèle (accuracy, precision, recall, F1-score) sont comparées à celles du modèle précédent avant toute mise en production.
- **Déploiement** : le nouveau modèle remplace l'ancien si l'évaluation est concluante.

## Intégration des services d'IA générative

La classe `LLMModel` centralise la génération du rapport de synthèse à destination de l'utilisateur final, à partir des métriques calculées par PostgreSQL (`Postgres_DB`) et MLflow (`ML_Flow_Operations`). Deux fournisseurs sont actuellement intégrés à titre de benchmark comparatif : Mistral (solution retenue à l'issue du benchmark documentaire) et Google Gemini (utilisé pour la comparaison empirique).

```python
import os
import sys
import logging
from pathlib import Path
import json
from typing import Any

from dotenv import load_dotenv
from mistralai.client import Mistral
from google import genai
from google.genai import types

from ML_Flow import ML_Flow_Operations
from Database import Postgres_DB
from Helpers_Monitoring import Helpers_Monitoring

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__))))

load_dotenv()
monitor = Helpers_Monitoring()

# Prompt système chargé une seule fois au démarrage de l'application
SYSTEM_PROMPT = Path(f"{os.path.dirname(__file__)}/data/spamshield-advisor-system-prompt.md").read_text(encoding="utf-8")

# --- Client Mistral ---
mistral_client = Mistral(api_key=os.getenv("MISTRAL_API_KEY"))
MISTRAL_MODEL = "mistral-small-2603"

# --- Client Gemini ---
GEMINI_MODEL = "gemini-3.5-flash-lite"
gemini_api_key = os.getenv("GEMINI_API_KEY")
if not gemini_api_key:
    raise RuntimeError("La variable d'environnement GEMINI_API_KEY est absente.")
gemini_client = genai.Client(api_key=gemini_api_key)


class LLMModel:
    def __init__(self):
        self.initial_system_prompt = SYSTEM_PROMPT

    def get_system_data(self):
        return Postgres_DB().get_dashboard_metrics()

    def get_model_metrics(self):
        return ML_Flow_Operations().get_latest_model_metrics()

    @monitor.calculate_func_time
    def generate_report_mistral(self) -> dict[str, Any]:
        payload = {
            "system_data": self.get_system_data(),
            "model_metrics": self.get_model_metrics(),
        }
        response = mistral_client.chat.complete(
            model=MISTRAL_MODEL,
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": json.dumps(payload, ensure_ascii=False)},
            ],
            temperature=0.3,  # basse température : réponse stable et reproductible
        )
        return {
            "model_used": MISTRAL_MODEL,
            "llm_response": response.choices[0].message.content,
            "base_metrics": payload,
        }

    @monitor.calculate_func_time
    def generate_report_gemini(self) -> dict[str, Any]:
        payload = {
            "system_data": self.get_system_data(),
            "model_metrics": self.get_model_metrics(),
        }
        try:
            response = gemini_client.models.generate_content(
                model=GEMINI_MODEL,
                contents=json.dumps(payload, ensure_ascii=False, default=str),
                config=types.GenerateContentConfig(
                    system_instruction=self.initial_system_prompt,
                    max_output_tokens=700,
                ),
            )
        except Exception:
            logging.exception("Échec de la génération du rapport avec Gemini.")
            raise

        if not response.text:
            raise RuntimeError("Gemini n'a retourné aucun contenu exploitable.")

        return {
            "provider": "Google Gemini",
            "model_used": GEMINI_MODEL,
            "parameters": {"max_output_tokens": 700},
            "llm_response": response.text,
            "base_metrics": payload,
        }
```

> ⚠️ **Note de cohérence** : le modèle Gemini utilisé (`gemini-3.5-flash-lite`, sorti le 21 juillet 2026) est le successeur du modèle initialement documenté dans le benchmark (`gemini-2.5-flash-lite`). Le rapport de veille doit être mis à jour en conséquence — voir la section correspondante du rapport.

Le décorateur `@monitor.calculate_func_time` (fourni par `Helpers_Monitoring`) journalise automatiquement le temps d'exécution de chaque appel, utile pour le suivi de latence dans le cadre du protocole de test comparatif.

## Dépannage

**FastAPI ne démarre pas, sans message d'erreur clair.**
C'est une erreur fréquente et trompeuse : dans la majorité des cas, ce n'est pas FastAPI qui est en cause, mais la base de données PostgreSQL qui n'est pas démarrée ou pas encore prête à accepter des connexions. Avant de chercher plus loin, vérifier que le conteneur Docker de PostgreSQL est bien lancé (`docker compose ps`) et accessible.

## Ressources

- Guide de terminologie grammaticale du français, Éduscol — utilisé comme référence pour la relecture et la cohérence linguistique des contenus rédigés : https://eduscol.education.gouv.fr/sites/default/files/document/guide-la-grammaire-du-francais-terminologie-grammaticale-67998.pdf




Configuration du service LLM
Configuration de l'API Mistral

SpamShield utilise un service d'intelligence artificielle externe afin de générer automatiquement un rapport d'interprétation des métriques du modèle de classification.

Par défaut, l'application est configurée pour utiliser Mistral AI via son API officielle.

Avant de démarrer l'application, il est nécessaire de créer une clé API.

1. Création d'un compte

Créer un compte sur le portail développeur de Mistral AI :

https://console.mistral.ai/

Une fois connecté, générer une nouvelle clé API depuis l'espace API Keys.

2. Configuration de la variable d'environnement

Pour des raisons de sécurité, la clé API ne doit jamais être enregistrée directement dans le code source.

Créer une variable d'environnement :

MISTRAL_API_KEY=xxxxxxxxxxxxxxxxxxxxxxxx

ou renseigner cette valeur dans le fichier .env utilisé par l'application.

Exemple :

MISTRAL_API_KEY=xxxxxxxxxxxxxxxxxxxxxxxx
3. Installation des dépendances

Installer les dépendances Python du projet.

pip install -r requirements.txt

Le SDK officiel Mistral est automatiquement installé avec les autres dépendances.

4. Vérification de la configuration

Au démarrage de SpamShield, le client Mistral est initialisé automatiquement à partir de la variable d'environnement.

En cas de clé invalide ou absente, une exception est levée lors du premier appel au service.

Les erreurs sont automatiquement enregistrées dans MLflow afin de faciliter le diagnostic.

Paramétrage du modèle

Le composant de génération est actuellement configuré avec les paramètres suivants.

Paramètre	Valeur
Fournisseur	Mistral AI
Modèle	mistral-small-2603
Température	0.3
Format des données	JSON
Prompt système	system_prompt.md

Le prompt système est stocké dans un fichier Markdown séparé afin de pouvoir être modifié indépendamment du code.

Modification du modèle

L'architecture du projet permet de remplacer facilement le modèle de langage utilisé.

Le modèle est défini dans le paramètre model lors de l'appel à l'API.

Exemple :

response = client.chat.complete(
    model="mistral-small-2603",
    ...
)

Pour utiliser un autre modèle compatible avec l'API Mistral, il suffit de remplacer cette valeur.

Exemple :

model="mistral-medium"

Aucune autre modification de l'architecture n'est nécessaire.

Remplacement du fournisseur

L'architecture orientée objet de SpamShield isole la logique d'appel au service d'intelligence artificielle dans une classe dédiée.

Cette séparation permet de remplacer ultérieurement Mistral par un autre fournisseur (OpenAI, Groq, Google AI Studio, Hugging Face, OpenRouter, etc.) sans modifier les autres composants de l'application.

Seule l'implémentation de la classe responsable des appels API devra être adaptée.

Vérification du fonctionnement

Une génération correcte doit produire :

un rapport en langage naturel ;
une nouvelle exécution dans l'expérience LLM Monitoring de MLflow ;
les métriques de consommation (tokens, durée) ;
les artefacts payload.json et llm_response.txt.

En cas d'échec (clé API invalide, erreur réseau, indisponibilité du fournisseur...), l'appel est enregistré dans MLflow avec les informations de diagnostic disponibles.