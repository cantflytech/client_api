## Prérequis

Avant de pouvoir exécuter le projet, vous devez configurer certaines variables d'environnement pour accéder aux API de Binance.

### Configuration des Clés API

Vous devez créer un fichier `.env` à la racine du projet avec les variables d'environnement suivantes :

```ini
BINANCE_API_KEY=your_binance_api_key_here
BINANCE_API_SECRET=your_binance_api_secret_here
```

Ces clés sont nécessaires pour que l'application puisse interagir avec l'API Binance.

## Lancer l'Application

Pour démarrer l'application, vous devez lancer le fichier `app.py` qui ouvre un serveur local et attend des webhooks.

```bash
python app.py
```

Une fois l'application lancée, vous pouvez envoyer des webhooks à l'URL locale de votre machine (par exemple, `http://localhost:5000`).

## Fonctionnement en Environnement Local
Cette API est conçue pour fonctionner en environnement local. Vous devrez donc la tester localement sur votre machine. Pour ce faire, vous pouvez utiliser un outil tel que Postman ou cURL afin de communiquer avec l'API et envoyer des requêtes de test à l'URL
