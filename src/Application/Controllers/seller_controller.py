from flask import jsonify, make_response
from src.Application.Service.seller_service import SellerService
from src.Infrastructure.Model.seller import Seller

class SellerController:
    @staticmethod
    def register_seller(data):
        try:
            nome = data.get('nome')
            cnpj = data.get('cnpj')
            email = data.get('email')
            celular = data.get('celular')
            senha = data.get('senha')

            if not all([nome, cnpj, email, celular, senha]):
                return {"erro": "Campos obrigatórios não informados"}

            seller = SellerService.create_seller(nome, cnpj, email, celular, senha)

            # ✅ Verifica se realmente é um objeto Seller antes de chamar to_dict()
            if not isinstance(seller, Seller):
                return {"erro": "Erro ao cadastrar o seller"}

            return {
                "mensagem": "Seller cadastrado com sucesso",
                "seller": seller.to_dict()
            }

        except Exception as e:
            print(f"Erro ao criar seller: {str(e)}")
            return {"erro": f"Erro interno: {str(e)}"}

    @staticmethod
    def activate_seller(data):
        try:
            celular = data.get('celular')
            codigo = data.get('codigo')

            if not all([celular, codigo]):
                return {"erro": "Celular e código são obrigatórios"}

            seller = SellerService.activate_seller(celular, codigo)

            # ✅ Verifica se realmente é um objeto Seller antes de chamar to_dict()
            if not isinstance(seller, Seller):
                return {"erro": "Código inválido ou seller não encontrado"}

            return {
                "mensagem": "Seller ativado com sucesso",
                "seller": seller.to_dict()
            }

        except Exception as e:
            print(f"Erro ao ativar seller: {str(e)}")
            return {"erro": f"Erro interno: {str(e)}"}