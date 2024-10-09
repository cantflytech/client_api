from models import state
from utils.helpers import get_market_price
from services.user_services import place_buy_limit_orders_if_needed

def process_webhook(ticker):
    for user in state["users"]:
        if user['symbol'] == ticker and user['status'] == 'En attente du signal':
            print(f"Utilisateur trouvé pour {user['symbol']}")

            # Récupérer le prix actuel du marché
            market_price = get_market_price(user['symbol'])
            if market_price is not None:
                amount_to_invest = user['allocation'] * 0.05
                print(f"Placer un faux ordre BUY pour {user['symbol']} avec {amount_to_invest}$ à un prix de {market_price}$")

               
                user['price_achat'] = market_price
                user['gp_percentage'] = 0.0

               
                user['status'] = 'En cours de pool'
                user['allocation_restante'] = user['allocation'] - amount_to_invest

                # Vérifier les ordres "buy limit"
                place_buy_limit_orders_if_needed(user, market_price)
            else:
                print(f"Impossible de récupérer le prix pour {user['symbol']}")
