from flask import Blueprint, request, jsonify
from models import state

users_bp = Blueprint('users', __name__)

@users_bp.route('/users', methods=['POST'])
def add_user():
    data = request.json
    if 'symbol' not in data or 'allocation' not in data or 'id' not in data:
        return jsonify({'error': 'Paramètres manquants'}), 400

    symbol = data['symbol']
    allocation = data['allocation']
    status = 'En attente du signal'
    id = data['id']

    state["users"].append({
        'symbol': symbol,
        'allocation': allocation,
        'status': status,
        'id': id,
        'allocation_restante': allocation,
        'gp_percentage': None,
        'price_achat': None,
        'BL': {
            'bl1': [],
            'bl2': [],
            'bl3': [],
            'bl4': [],
            'bl5': [],
            'bl6': [],
            'bl7': [],
        }
    })

    return jsonify({
        'status': 'Données utilisateur reçues avec succès',
        'symbol': symbol,
        'allocation': allocation,
        'status_user': status,
        'allocation_restante': allocation
    }), 200

@users_bp.route('/users', methods=['GET'])
def get_users():
    return jsonify(state["users"]), 200

@users_bp.route('/archive', methods=['GET'])
def get_archive():
    return jsonify(state["archive"]), 200

