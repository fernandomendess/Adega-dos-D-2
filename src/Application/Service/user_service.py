from Infrastructure.Model.user import UserModel
from Infrastructure.http.whats_app import WhatsAppService
from config.data_base import SessionLocal
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import create_access_token

class UserService:
    def __init__(self):
        self.session = SessionLocal()
        self.whatsapp = WhatsAppService()

    def register_user(self, data):
        user = self.session.query(UserModel).filter_by(email=data['email']).first()
        if user:
            return {"msg": "Email já cadastrado"}, 400

        hashed_password = generate_password_hash(data['senha'])
        user = UserModel(
            nome=data['nome'],
            cnpj=data['cnpj'],
            email=data['email'],
            celular=data['celular'],
            senha=hashed_password
        )
        self.session.add(user)
        self.session.commit()

        self.whatsapp.send_code(user.celular)

        return {"msg": "Cadastro realizado. Código enviado via WhatsApp."}, 201

    def activate_user(self, email, code):
        user = self.session.query(UserModel).filter_by(email=email).first()
        if not user:
            return {"msg": "Usuário não encontrado"}, 404

        if self.whatsapp.verify_code(user.celular, code):
            user.status = "Ativo"
            self.session.commit()
            return {"msg": "Conta ativada com sucesso"}, 200
        return {"msg": "Código inválido"}, 400

    def login(self, data):
        user = self.session.query(UserModel).filter_by(email=data['email']).first()
        if not user:
            return {"msg": "Usuário não encontrado"}, 404

        if user.status != "Ativo":
            return {"msg": "Conta inativa"}, 403

        if not check_password_hash(user.senha, data['senha']):
            return {"msg": "Senha inválida"}, 400

        access_token = create_access_token(identity=user.email)
        return {"access_token": access_token}, 200