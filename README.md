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