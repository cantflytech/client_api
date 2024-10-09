from .users import users_bp
from .webhook import webhook_bp

def init_routes(app):
    app.register_blueprint(users_bp)
    app.register_blueprint(webhook_bp)
