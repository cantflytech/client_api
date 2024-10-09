import ccxt
from dotenv import load_dotenv
import os

# Charger les variables d'environnement depuis le fichier .env
load_dotenv()

# Utiliser les clés depuis les variables d'environnement
binance_api_key = os.getenv("BINANCE_API_KEY")
binance_api_secret = os.getenv("BINANCE_API_SECRET")

exchange = ccxt.binance({
    'token': binance_api_key,
    'secret': binance_api_secret,
    'enableRateLimit': True
})