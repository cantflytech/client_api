from flask import Blueprint, request, jsonify
from services.user_services import start_background_tasks
from services.binance_service import process_webhook 

webhook_bp = Blueprint('webhook', __name__)

#Démmarer taches en arriere plan avec rafrachissement des G/P%
start_background_tasks()

@webhook_bp.route('/webhook', methods=['POST'])
def handle_webhook():
    data = request.json
    if 'ticker' not in data or 'message' not in data:
        return jsonify({'error': 'Paramètres manquants'}), 400

    ticker = data['ticker']
    message = data['message']

    process_webhook(ticker)

    return jsonify({'status': 'Signal traité', 'ticker': ticker, 'message': message}), 200
