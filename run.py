from flask import Flask
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from src.routes import user_bp
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)
CORS(app)
app.config['JWT_SECRET_KEY'] = os.getenv("SECRET_KEY")
jwt = JWTManager(app)

app.register_blueprint(user_bp)

if __name__ == "__main__":
    app.run(debug=True)

# ==== src/routes.py ====
from flask import Blueprint
from src.Application.Controllers import user_controller

user_bp = Blueprint('user', __name__)

user_bp.route('/register', methods=['POST'])(user_controller.register)
user_bp.route('/activate', methods=['POST'])(user_controller.activate)
user_bp.route('/login', methods=['POST'])(user_controller.login)
    