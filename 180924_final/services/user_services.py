import time
import threading
from models import state
from utils.helpers import get_market_price, calculate_gp_percentage, get_vwap


def check_stop_market_and_archive(user, current_price):
    vwap = get_vwap(user['symbol'])
    if vwap is None:
        return
    #à changer après  avec le vwap 
    stop_price = user['price_achat'] + 1.00004 # VWAP + 0.04%
    total_gain = 0
    

    if current_price >= stop_price:
        total_gain += user['allocation_restante']

   
        if user['BL']['bl1']:
       
         for bl in user['BL']['bl1']:
            montant_alloue = bl['montant_alloué']
            prix_achat = bl['prix_achat']
            gain = (current_price - prix_achat) / prix_achat * montant_alloue
            total_gain += gain
    
        if user['BL']['bl2']:
       
         for bl in user['BL']['bl2']:
            montant_alloue = bl['montant_alloué']
            prix_achat = bl['prix_achat']
            gain = (current_price - prix_achat) / prix_achat * montant_alloue
            total_gain += gain
        
        if user['BL']['bl3']:
        
            for bl in user['BL']['bl3']:
                montant_alloue = bl['montant_alloué']
                prix_achat = bl['prix_achat']
                gain = (current_price - prix_achat) / prix_achat * montant_alloue
                total_gain += gain  
        
        if user['BL']['bl4']:

            for bl in user['BL']['bl4']:
                montant_alloue = bl['montant_alloué']
                prix_achat = bl['prix_achat']
                gain = (current_price - prix_achat) / prix_achat * montant_alloue
                total_gain += gain
        
        if user['BL']['bl5']:
            
                for bl in user['BL']['bl5']:
                    montant_alloue = bl['montant_alloué']
                    prix_achat = bl['prix_achat']
                    gain = (current_price - prix_achat) / prix_achat * montant_alloue
                    total_gain += gain
        
        if user['BL']['bl6']:
                
                    for bl in user['BL']['bl6']:
                        montant_alloue = bl['montant_alloué']
                        prix_achat = bl['prix_achat']
                        gain = (current_price - prix_achat) / prix_achat * montant_alloue
                        total_gain += gain  
        
        if user['BL']['bl7']:
                        
                            for bl in user['BL']['bl7']:
                                montant_alloue = bl['montant_alloué']
                                prix_achat = bl['prix_achat']
                                gain = (current_price - prix_achat) / prix_achat * montant_alloue
                                total_gain += gain


        print(f"Gain total pour {user['symbol']} : {total_gain}$")
        print(current_price)
            
        archive_user(user, total_gain)


def archive_user(user, total_gain):
    user['final_gain'] = total_gain
    user['status'] = 'Terminé'


    state['archive'].append(user)
    state['users'].remove(user)

    print(f"Utilisateur archivé avec un gain final de {total_gain}$")

def update_gp_percentages():
    while True:
        for user in state["users"]:
            if 'price_achat' in user and user['status'] == 'En cours de pool':
                current_price = get_market_price(user['symbol'])
                if current_price is not None:
                 
                    user['gp_percentage'] = calculate_gp_percentage(user['price_achat'], current_price)
                    print(f"Mis à jour G/P% pour {user['symbol']} : {user['gp_percentage']}%")

    
                    place_buy_limit_orders_if_needed(user, current_price)
                    print(f"VWAP simulé pour {user['symbol']} : {get_vwap(user['symbol'])}")

                    check_stop_market_and_archive(user, current_price)
        time.sleep(60)  


def place_buy_limit_orders_if_needed(user, current_price):
    if not user['BL']['bl1'] and user['gp_percentage'] <= -0.01:
        amount_to_invest = user['allocation'] * 0.0075
        user['allocation_restante'] -= amount_to_invest
        user['BL']['bl1'].append({
            'montant_alloué': amount_to_invest,
            'prix_achat': current_price,
            'G/P achat': user['gp_percentage']
        })
        print(f"Placer un ordre BUY LIMIT 1 pour {user['symbol']} à {current_price}")

    if not user['BL']['bl2'] and user['gp_percentage'] <= -0.05:
        amount_to_invest = user['allocation'] * 0.015
        user['allocation_restante'] -= amount_to_invest
        user['BL']['bl2'].append({
            'montant_alloué': amount_to_invest,
            'prix_achat': current_price,
            'G/P achat': user['gp_percentage']
        })
        print(f"Placer un ordre BUY LIMIT 2 pour {user['symbol']} à {current_price}")
    

    if not user['BL']['bl3'] and user['gp_percentage'] <= -0.01:
        amount_to_invest = user['allocation'] * 0.03
        user['allocation_restante'] -= amount_to_invest
        user['BL']['bl3'].append({
            'montant_alloué': amount_to_invest,
            'prix_achat': current_price,
            'G/P achat': user['gp_percentage']
        })
        print(f"Placer un ordre BUY LIMIT 3 pour {user['symbol']} à {current_price}")
    

    if not user['BL']['bl4'] and user['gp_percentage'] <= -2:
        amount_to_invest = user['allocation'] * 0.05
        user['allocation_restante'] -= amount_to_invest
        user['BL']['bl4'].append({
            'montant_alloué': amount_to_invest,
            'prix_achat': current_price,
            'G/P achat': user['gp_percentage']
        })
        print(f"Placer un ordre BUY LIMIT 4 pour {user['symbol']} à {current_price}")


    if not user['BL']['bl5'] and user['gp_percentage'] <= -5:
        amount_to_invest = user['allocation'] * 0.1
        user['allocation_restante'] -= amount_to_invest
        user['BL']['bl5'].append({
            'montant_alloué': amount_to_invest,
            'prix_achat': current_price,
            'G/P achat': user['gp_percentage']
        })
        print(f"Placer un ordre BUY LIMIT 5 pour {user['symbol']} à {current_price}")
    

    if not user['BL']['bl6'] and user['gp_percentage'] <= -10:
        amount_to_invest = user['allocation'] * 0.2
        user['allocation_restante'] -= amount_to_invest
        user['BL']['bl6'].append({
            'montant_alloué': amount_to_invest,
            'prix_achat': current_price,
            'G/P achat': user['gp_percentage']
        })
        print(f"Placer un ordre BUY LIMIT 6 pour {user['symbol']} à {current_price}")
    

    if not user['BL']['bl7'] and user['gp_percentage'] <= -20:
        amount_to_invest = user['allocation'] * 0.3
        user['allocation_restante'] -= amount_to_invest
        user['BL']['bl7'].append({
            'montant_alloué': amount_to_invest,
            'prix_achat': current_price,
            'G/P achat': user['gp_percentage']
        })
        print(f"Placer un ordre BUY LIMIT 7 pour {user['symbol']} à {current_price}")


def start_background_tasks():
    threading.Thread(target=update_gp_percentages, daemon=True).start()
