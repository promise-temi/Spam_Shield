# Spam_Shield
Outil anti-abus évolutif - RNCP37827 Développeur en Intélligence Artificielle


command : mlflow ui
http://127.0.0.1:5000


pip install -r requirements.txt

mlflow ui --host 0.0.0.0 --port 5000

gmail:
Mots de passe des applications


creer une clé d'encryption:
from cryptography.fernet import Fernet
key = Fernet.generate_key()
print(key.decode())



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