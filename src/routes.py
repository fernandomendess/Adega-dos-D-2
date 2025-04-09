from src.Application.Controllers.user_controller import UserController
from flask import jsonify, make_response, request
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from src.config.data_base import db
from src.Infrastructure.Model.user import User

def init_routes(app):
    @app.route('/api', methods=['GET'])
    def health():
        return make_response(jsonify({
            "mensagem": "API - OK; Docker - Up",
        }), 200)

    @app.route('/api/sellers', methods=['POST'])
    def create_seller():
        return UserController.create_seller()

    @app.route('/api/sellers/activate', methods=['POST'])
    def activate_seller():
        return UserController.activate_seller()

    @app.route('/api/auth/login', methods=['POST'])
    def login():
        email = request.json.get('email', None)
        password = request.json.get('password', None)

        # Verifique as credenciais do usuário
        user = User.query.filter_by(email=email).first()
        if user and user.password == password:  # Em produção, use hashing para senhas
            # Use o e-mail como identity (string) e adicione claims extras, se necessário
            access_token = create_access_token(
                identity=email,  # O identity agora é uma string
                additional_claims={"name": user.name, "status": user.status}
            )
            return jsonify(access_token=access_token), 200

        return jsonify({"mensagem": "Credenciais inválidas"}), 401

    # rota protegida para teste
    @app.route('/api/protected', methods=['GET'])
    @jwt_required()
    def protected():
        current_user = get_jwt_identity()  # Agora retorna apenas o e-mail
        return jsonify({
            "mensagem": f"Bem-vindo, {current_user}! Esta é uma rota protegida."
        }), 200
