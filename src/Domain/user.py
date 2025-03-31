class SellerDomain:
    def __init__(self, nome, cnpj, email, celular, senha):
        self.nome = nome
        self.cnpj = cnpj
        self.email = email
        self.celular = celular
        self.senha = senha
        self.status = "Inativo" 

    def to_dict(self):
        return {
            "nome": self.nome,
            "cnpj": self.cnpj,
            "email": self.email,
            "celular": self.celular,
            "status": self.status
        }