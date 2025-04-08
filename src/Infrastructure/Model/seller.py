from src.config.data_base import db

class Seller(db.Model):
    __tablename__ = 'sellers'
    
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(255), nullable=False)
    cnpj = db.Column(db.String(20), nullable=False, unique=True)
    email = db.Column(db.String(255), nullable=False, unique=True)
    celular = db.Column(db.String(20), nullable=False)
    senha = db.Column(db.String(255), nullable=False)
    status = db.Column(db.String(20), nullable=False, default='Inativo')
    activation_code = db.Column(db.String(4), nullable=False)

    def to_dict(self):
        return {
            "id": self.id,
            "nome": self.nome,
            "cnpj": self.cnpj,
            "email": self.email,
            "celular": self.celular,
            "status": self.status,
            "activation_code": self.activation_code
        }
    
    