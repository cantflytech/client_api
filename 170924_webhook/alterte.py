import requests

# URL de l'API Flask (Remplacez par l'URL où votre API est hébergée si nécessaire)
webhook_url = 'http://localhost:5000/webhook'

# Données à envoyer
data = {
    'ticker': 'BTC/USDT',
    'message': 'paramètres de l\'alerte'
}

# Envoyer une requête POST au webhook
response = requests.post(webhook_url, json=data)

# Afficher la réponse de l'API
if response.status_code == 200:
    print(f'Succès: {response.json()}')
else:
    print(f'Erreur: {response.status_code}, {response.text}')
