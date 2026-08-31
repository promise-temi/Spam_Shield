# Spam_Shield

Outil anti-abus évolutif développé dans le cadre du titre **RNCP 37827 – Développeur en Intelligence Artificielle**.

## Prérequis

Avant d'installer SpamShield, vérifiez que les outils suivants sont disponibles sur votre machine :

- Python
- Docker et Docker Compose
- Node.js et npm pour le frontend en environnement de développement
- Git pour récupérer le projet

## Installation

Clonez le dépôt puis placez-vous dans le dossier du projet.

Créez ensuite un environnement virtuel Python.

### Linux / macOS

```bash
python -m venv venv
source venv/bin/activate
```

### Windows

```bash
python -m venv venv
venv\Scripts\activate
```

Installez les dépendances Python :

```bash
pip install -r requirements.txt
```

---

## Configuration du fichier `.env`

Créez un fichier `.env` à la racine du projet.

Ce fichier contient les informations nécessaires au fonctionnement de SpamShield. Il ne doit pas être versionné dans Git.

### Clé d'accès au backend

```env
BACKEND_API_KEY=
```

Générez une clé robuste avec l'outil fourni dans le projet :

```bash
python prep_tools/api_key_generator.py
```

Copiez la clé obtenue dans `BACKEND_API_KEY`.

### Configuration PostgreSQL

```env
DB_DATABASE=
DB_HOST=postgres
DB_PASSWORD=
DB_PORT=5432
DB_USER=postgres
```

`DB_DATABASE` correspond au nom de la base PostgreSQL utilisée par SpamShield.

Pour générer un mot de passe robuste, vous pouvez également utiliser :

```bash
python prep_tools/api_key_generator.py
```

Lorsque le backend fonctionne dans Docker, utilisez :

```env
DB_HOST=postgres
```

Si vous lancez le backend directement depuis votre machine avec Uvicorn, utilisez :

```env
DB_HOST=localhost
```

### Configuration de l'envoi d'e-mails

```env
EMAIL_ADDRESS=
EMAIL_PASSWORD=
```

`EMAIL_ADDRESS` correspond à l'adresse Gmail utilisée par SpamShield pour envoyer ses e-mails.

Il est recommandé d'utiliser une adresse dédiée au projet plutôt que votre adresse personnelle.

Pour `EMAIL_PASSWORD`, utilisez un **mot de passe d'application Google** associé à cette adresse Gmail et non le mot de passe habituel du compte.

Pour obtenir ce mot de passe :

1. Connectez-vous au compte Google utilisé par SpamShield.
2. Activez la validation en deux étapes si elle n'est pas déjà activée.
3. Accédez aux paramètres de sécurité du compte.
4. Recherchez la section permettant de créer un **mot de passe d'application**.
5. Générez un mot de passe pour SpamShield.
6. Copiez le mot de passe obtenu dans :

```env
EMAIL_PASSWORD=
```

### Clé de chiffrement

```env
ENCRYPTION_KEY=
```

Une clé de chiffrement peut être générée avec l'outil fourni dans le projet :

```bash
python prep_tools/encryption_key_generator.py
```

Copiez la valeur générée dans :

```env
ENCRYPTION_KEY=
```

Conservez cette clé. Une clé différente ne permettra pas de déchiffrer les données précédemment chiffrées avec l'ancienne.

### API Mistral

```env
MISTRAL_API_KEY=
```

Pour obtenir une clé API Mistral :

1. Créez un compte sur la console Mistral AI.
2. Accédez à la gestion des clés API.
3. Générez une nouvelle clé.
4. Copiez-la dans :

```env
MISTRAL_API_KEY=
```

### Configuration MLflow

Lorsque SpamShield fonctionne entièrement dans Docker, utilisez :

```env
MLFLOW_TRACKING_URI=http://mlflow:5050
```

En environnement de développement, si le backend est lancé directement sur votre machine avec Uvicorn alors que MLflow fonctionne dans le Docker Compose de développement, utilisez :

```env
MLFLOW_TRACKING_URI=http://localhost:5050
```

---

## Configuration de l'environnement de test

Les tests utilisent une base PostgreSQL distincte afin de ne pas modifier les données de l'environnement principal.

Ajoutez également les variables suivantes dans le fichier `.env` :

```env
TEST_DB_DATABASE=test_spamshield
TEST_DB_HOST=localhost
TEST_DB_PASSWORD=
TEST_DB_PORT=5432
TEST_DB_USER=postgres
```

Utilisez un mot de passe dédié à l'environnement de test et différent de celui de l'environnement principal.

---

## Lancer SpamShield en environnement de développement

L'environnement de développement permet de lancer les services Docker tout en exécutant séparément le backend et le frontend.

Assurez-vous que votre environnement virtuel Python est activé et que les dépendances ont été installées.

Dans le fichier `.env`, utilisez notamment :

```env
DB_HOST=localhost
MLFLOW_TRACKING_URI=http://localhost:5050
```

### 1. Démarrer les services Docker de développement

Dans un premier terminal :

```bash
docker-compose -f docker-compose.dev.yml up --build
```

### 2. Démarrer le backend

Dans un deuxième terminal :

```bash
uvicorn backend.api:app --reload
```

### 3. Démarrer le frontend

Dans un troisième terminal :

```bash
cd frontend
cd vue_spamshield
```

Lors du premier lancement, installez les dépendances :

```bash
npm install
```

Puis démarrez le frontend :

```bash
npm run dev
```

---

## Réinitialiser la base de développement

Si vous souhaitez supprimer toutes les données de la base de développement et repartir avec un schéma vide, connectez-vous à PostgreSQL puis exécutez :

```sql
DROP SCHEMA public CASCADE;
CREATE SCHEMA public;
```

> **Attention : cette opération supprime l'ensemble des données du schéma.**

N'utilisez cette commande que sur une base que vous souhaitez réellement réinitialiser.

---

## Lancer SpamShield en environnement de production

L'environnement conteneurisé complet peut être construit et démarré avec une seule commande :

```bash
docker-compose up --build
```

Dans cette configuration, les différents services communiquent directement à travers le réseau Docker.

Vérifiez notamment que le fichier `.env` utilise :

```env
DB_HOST=postgres
MLFLOW_TRACKING_URI=http://mlflow:5050
```

---

## Lancer l'environnement de test

L'environnement de test dispose de sa propre configuration afin d'isoler les tests des données principales de SpamShield.

### 1. Démarrer les services nécessaires aux tests

```bash
docker-compose -f docker-compose.test.yml up --build
```

### 2. Exécuter les tests

Dans un autre terminal :

```bash
pytest -o log_cli=true --log-cli-level=DEBUG backend/tests
```

L'option `log_cli` permet d'afficher les logs directement dans le terminal afin de faciliter le diagnostic lorsqu'un test échoue.

### 3. Arrêter l'environnement de test

Une fois les tests terminés :

```bash
docker-compose -f docker-compose.test.yml down -v
```

---

## Prometheus et Grafana

SpamShield intègre **Prometheus et Grafana** pour le monitoring de l'application et du modèle.

Lorsque les services communiquent directement à l'intérieur du réseau Docker, le nom du service Docker `prometheus` peut être utilisé pour permettre à Grafana de communiquer avec Prometheus.

Lorsque les services sont utilisés depuis la machine hôte en environnement de développement, l'adresse `localhost` peut être utilisée avec le port exposé correspondant.

Les dashboards Grafana préparés pour SpamShield sont disponibles dans :

```text
/monitoring
```

Les fichiers JSON présents dans ce dossier peuvent être importés dans Grafana afin de retrouver les dashboards du projet.