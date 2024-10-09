from config import exchange

# Fonction pour récupérer le prix actuel du marché
def get_market_price(symbol):
    try:
        ticker = exchange.fetch_ticker(f"{symbol}")
        return ticker['last']
    except Exception as e:
        print(f"Erreur lors de la récupération du prix pour {symbol}: {e}")
        return None

# Fonction pour calculer le G/P%
def calculate_gp_percentage(initial_price, current_price):
    if initial_price == 0:
        return 0
    return ((current_price - initial_price) / initial_price) * 100

def get_vwap(symbol):
    try:
        # Récupérer les 10 dernières bougies de 1 
        ohlcv = exchange.fetch_ohlcv(f"{symbol}", timeframe='1m', limit=10)
        
        total_volume = 0
        vwap_sum = 0
        for candle in ohlcv:
            high = candle[2]
            low = candle[3]
            close = candle[4]
            volume = candle[5]
            typical_price = (high + low + close) / 3  # Prix typique pour cette bougie
            vwap_sum += typical_price * volume  # VWAP pour cette bougie
            total_volume += volume  # Volume total cumulé

        if total_volume > 0:
            return vwap_sum / total_volume  # Calcul du VWAP sur les 10 minutes
        else:
            return None
    except Exception as e:
        print(f"Erreur lors de la récupération du VWAP pour {symbol}: {e}")
        return None