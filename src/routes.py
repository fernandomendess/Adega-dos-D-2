from flask import jsonify, make_response, request
from src.Application.Controllers.seller_controller import SellerController

def init_routes(app):    
    @app.route('/api/health', methods=['GET'])
    def health():
        return make_response(jsonify({
            "mensagem": "API - OK; Docker - Up",
        }), 200)
    
    @app.route('/api/sellers', methods=['POST'])
    def register_seller():
        try:
            data = request.get_json()
            if not data:
                return make_response(jsonify({"erro": "Dados não fornecidos"})), 400
                
            response = SellerController.register_seller(data)
            if 'erro' in response:
                return make_response(jsonify(response), 400)
                
            return make_response(jsonify(response), 201)
        
        except Exception as e:
            print(f"Erro ao registrar vendedor: {str(e)}")
            return make_response(jsonify({"erro": "Erro interno no servidor"}), 500)

    @app.route('/api/sellers/activate', methods=['POST'])
    def activate_seller():
        try:
            data = request.get_json()
            if not data:
                return make_response(jsonify({"erro": "Dados não fornecidos"}), 400)
                
            response = SellerController.activate_seller(data)
            if 'erro' in response:
                return make_response(jsonify(response), 400)
                
            return make_response(jsonify(response), 200)
        
        except Exception as e:
            print(f"Erro ao ativar vendedor: {str(e)}")
            return make_response(jsonify({"erro": "Erro interno no servidor"}), 500)