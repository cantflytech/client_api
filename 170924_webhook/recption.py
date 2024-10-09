from flask import Flask, request, jsonify
import ccxt
import threading
import time

app = Flask(__name__)

# Stockage des données utilisateurs
state = {
    "users": []
}

# Clés d'API pour Binance
binance_api_key = "bg_6309ada81454664fc6c5382bcb2809a5"
binance_api_secret = "ace78de46bdc4dc69798390dc54e6ece7db8cb79076be67e38b9d1a6ea911af4"

# Initialiser l'API Binance avec ccxt
exchange = ccxt.binance({
    'token': binance_api_key,
    'secret': binance_api_secret,
    'enableRateLimit': True
})

# Fonction pour récupérer le prix actuel du marché pour un symbole
def get_market_price(symbol):
    try:
        ticker = exchange.fetch_ticker(f"{symbol}")
        return ticker['last']  # Renvoie le dernier prix de transaction
    except Exception as e:
        print(f"Erreur lors de la récupération du prix de {symbol}: {e}")
        return None
    
# Fonction pour calculer le G/P% (Gain ou Perte en pourcentage)
def calculate_gp_percentage(initial_price, current_price):
    if initial_price == 0:
        return 0
    return ((current_price - initial_price) / initial_price) * 100

# Fonction pour mettre à jour le G/P% de chaque utilisateur toutes les minutes
def update_gp_percentages():
    while True:
        for user in state["users"]:
            if 'price_achat' in user and user['status'] == 'En cours de pool':
                current_price = get_market_price(user['symbol'])
                if current_price is not None:
                    user['gp_percentage'] = calculate_gp_percentage(user['price_achat'], current_price)
                    print(f"Mis à jour G/P% pour {user['symbol']} : {user['gp_percentage']}%")
                    # Vérifier si les ordres "buy limit" doivent être placés
                    place_buy_limit_orders_if_needed(user, current_price)
        time.sleep(60)  # Attendre 1 minute avant la prochaine mise à jour

# Fonction pour placer les ordres "buy limit" (BL1 et BL2) si les conditions sont remplies
def place_buy_limit_orders_if_needed(user, current_price):
    # BL1: Se déclenche à -0.01% avec 0.75% du capital
    if not user['BL']['bl1'] and user['gp_percentage'] <= -0.01:  # Vérifie si BL1 n'a pas été placé
        amount_to_invest = user['allocation'] * 0.0075
        user['allocation_restante'] -= amount_to_invest

        # Ajouter l'ordre dans la liste `bl1`
        user['BL']['bl1'].append({
            'montant_alloué': amount_to_invest,
            'prix_achat': current_price,
            'G/P achat': user['gp_percentage']
        })
        print(f"Placer un ordre BUY LIMIT 1 pour {user['symbol']} avec {amount_to_invest}$ à un prix de {current_price}$")
    
    # BL2: Se déclenche à -0.5% avec 1.5% du capital
    if not user['BL']['bl2'] and user['gp_percentage'] <= -0.05:  # Vérifie si BL2 n'a pas été placé
        amount_to_invest = user['allocation'] * 0.015
        user['allocation_restante'] -= amount_to_invest

        # Ajouter l'ordre dans la liste `bl2`
        user['BL']['bl2'].append({
            'montant_alloué': amount_to_invest,
            'prix_achat': current_price,
            'G/P achat': user['gp_percentage']
        })
        print(f"Placer un ordre BUY LIMIT 2 pour {user['symbol']} avec {amount_to_invest}$ à un prix de {current_price}$")
    
    # BL3: Se déclenche à -1% avec 3% du capital
    if not user['BL']['bl3'] and user['gp_percentage'] <= -0.01:
        amount_to_invest = user['allocation'] * 0.03
        user['allocation_restante'] -= amount_to_invest
        user['BL']['bl3'].append({
            'montant_alloué': amount_to_invest,
            'prix_achat': current_price,
            'G/P achat': user['gp_percentage']
        })
        print(f"Placer un ordre BUY LIMIT 3 pour {user['symbol']} avec {amount_to_invest}$ à un prix de {current_price}$")

    # BL4: Se déclenche à -2% avec 5% du capital
    if not user['BL']['bl4'] and user['gp_percentage'] <= -2:
        amount_to_invest = user['allocation'] * 0.05
        user['allocation_restante'] -= amount_to_invest
        user['BL']['bl4'].append({
            'montant_alloué': amount_to_invest,
            'prix_achat': current_price,
            'G/P achat': user['gp_percentage']
        })
        print(f"Placer un ordre BUY LIMIT 4 pour {user['symbol']} avec {amount_to_invest}$ à un prix de {current_price}$")
    
    # BL5: Se déclenche à -5% avec 10% du capital
    if not user['BL']['bl5'] and user['gp_percentage'] <= -5:
        amount_to_invest = user['allocation'] * 0.10
        user['allocation_restante'] -= amount_to_invest
        user['BL']['bl5'].append({
            'montant_alloué': amount_to_invest,
            'prix_achat': current_price,
            'G/P achat': user['gp_percentage']
        })
        print(f"Placer un ordre BUY LIMIT 5 pour {user['symbol']} avec {amount_to_invest}$ à un prix de {current_price}$")

    # BL6: Se déclenche à -10% avec 15% du capital
    if not user['BL']['bl6'] and user['gp_percentage'] <= -10:
        amount_to_invest = user['allocation'] * 0.15
        user['allocation_restante'] -= amount_to_invest
        user['BL']['bl6'].append({
            'montant_alloué': amount_to_invest,
            'prix_achat': current_price,
            'G/P achat': user['gp_percentage']
        })
        print(f"Placer un ordre BUY LIMIT 6 pour {user['symbol']} avec {amount_to_invest}$ à un prix de {current_price}$")
    
    # BL7: Se déclenche à -20% avec 20% du capital
    if not user['BL']['bl7'] and user['gp_percentage'] <= -20:
        amount_to_invest = user['allocation'] * 0.20
        user['allocation_restante'] -= amount_to_invest
        user['BL']['bl7'].append({
            'montant_alloué': amount_to_invest,
            'prix_achat': current_price,
            'G/P achat': user['gp_percentage']
        })
        print(f"Placer un ordre BUY LIMIT 7 pour {user['symbol']} avec {amount_to_invest}$ à un prix de {current_price}$")
        

# Démarrer le thread pour mettre à jour les G/P% en arrière-plan
threading.Thread(target=update_gp_percentages, daemon=True).start()

# Route pour recevoir les webhooks
@app.route('/webhook', methods=['POST'])
def webhook():
    # Récupération des données JSON du webhook
    data = request.json
    if 'ticker' not in data or 'message' not in data:
        return jsonify({'error': 'Paramètres manquants'}), 400
    
    ticker = data['ticker']
    message = data['message']

    # Affichage de l'alerte dans le terminal
    print("Alerte !")
    print(f"Réception du ticker: {ticker} avec le message: {message}")

    # Pour chaque utilisateur, traiter les allocations
    for user in state["users"]:
        if user['symbol'] == ticker and user['status'] == 'En attente du signal':
            print(f"Utilisateur trouvé pour {user['symbol']}")
            # Récupérer le prix actuel du marché
            market_price = get_market_price(user['symbol'])
            if market_price is not None:
                # Calculer 5% de l'allocation
                amount_to_invest = user['allocation'] * 0.05
                print(f"Placer un faux ordre BUY pour {user['symbol']} avec {amount_to_invest}$ à un prix de {market_price}$")
                
                # Enregistrer le prix d'achat et calculer le G/P%
                user['price_achat'] = market_price
                user['gp_percentage'] = 0.0  # Initialiser à 0%
                
                # Mettre à jour l'état de l'utilisateur
                user['status'] = 'En cours de pool'
                user['allocation_restante'] = user['allocation'] - amount_to_invest
                print(f"Nouvelle allocation restante: {user['allocation_restante']}$")
            else:
                print(f"Impossible de récupérer le prix pour {user['symbol']}")
    
    return jsonify({'status': 'Signal traité', 'ticker': ticker, 'message': message}), 200

# Nouvelle route pour enregistrer les symboles et allocations des utilisateurs
@app.route('/users', methods=['POST'])
def users():
    data = request.json
    if 'symbol' not in data or 'allocation' not in data or 'id' not in data:
        return jsonify({'error': 'Paramètres manquants'}), 400
    
    symbol = data['symbol']
    allocation = data['allocation']
    status = 'En attente du signal'
    id = data['id']

    # Affichage dans le terminal
    print(f"Utilisateur a soumis le symbole: {symbol} avec une allocation de: {allocation}")

    # Stocker les données utilisateur
    state["users"].append({
        'symbol': symbol,
        'allocation': allocation,
        'status': status,
        'id': id,
        'allocation_restante': allocation,  # Initialement, l'allocation restante est égale à l'allocation totale
        'gp_percentage': None,              # Gain ou perte en pourcentage (sera calculé plus tard)
        'price_achat': None,                # Prix d'achat initial (sera défini lors du premier ordre)
        'BL': {                             # Regrouper les ordres "buy limit" dans un dictionnaire
            'bl1': [],                      # Liste des informations pour BL1
            'bl2': [],
            'bl3': [],
            'bl4': [],
            'bl5': [],
            'bl6': [],
            'bl7': [],
                               # Liste des informations pour BL2
        }
    })
    
    return jsonify({
        'status': 'Données utilisateur reçues avec succès',
        'symbol': symbol,
        'allocation': allocation,
        'status_user': status,
        'allocation_restante': allocation
    }), 200

# Route pour récupérer la liste des utilisateurs et leurs statuts
@app.route('/users', methods=['GET'])
def get_users():
    return jsonify(state["users"]), 200


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
