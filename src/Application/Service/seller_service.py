from src.Application.Service.whatsapp_service import WhatsAppService

class SellerService:
    @staticmethod
    def create_seller(nome, cnpj, email, celular, senha):
        try:
            # (mesmo código de validação...)

            activation_code = str(random.randint(1000, 9999))
            print(f"\nCÓDIGO GERADO (DEV): {activation_code}\n")  # Apenas em dev

            new_seller = Seller(
                nome=nome,
                cnpj=cnpj,
                email=email,
                celular=celular,
                senha=generate_password_hash(senha),
                status="Inativo",
                activation_code=activation_code
            )

            db.session.add(new_seller)
            db.session.commit()

            # Envio do código pelo WhatsApp
            if os.getenv('FLASK_ENV') == 'production':
                mensagem = f"Seu código de ativação é: {activation_code}"
                if not WhatsAppService.send_message(celular, mensagem):
                    raise RuntimeError("Falha ao enviar código de ativação")

            return new_seller

        except Exception as e:
            db.session.rollback()
            logger.error(f"Erro ao criar seller: {str(e)}", exc_info=True)
            return {"erro": f"Erro ao criar seller: {str(e)}"}

    @staticmethod
    def activate_seller(celular, code):
        try:
            celular = SellerService._format_phone_number(celular)

            seller = Seller.query.filter_by(
                celular=celular,
                activation_code=code,
                status="Inativo"
            ).first()

            if not seller:
                logger.warning(f"Código inválido para {celular}")
                return {"erro": "Código inválido ou seller não encontrado"}

            seller.status = "Ativo"
            seller.activation_code = None  # Remove código após ativação
            db.session.commit()

            # Mensagem de confirmação
            if os.getenv('FLASK_ENV') == 'production':
                WhatsAppService.send_message(celular, "Sua conta foi ativada com sucesso!")

            logger.info(f"Seller ativado: ID {seller.id}")
            return seller

        except Exception as e:
            db.session.rollback()
            logger.error(f"Erro ao ativar seller: {str(e)}", exc_info=True)
            return {"erro": f"Erro ao ativar seller: {str(e)}"}
