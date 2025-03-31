import random
import logging
import os
from twilio.rest import Client
from twilio.base.exceptions import TwilioRestException
from werkzeug.security import generate_password_hash
from src.Infrastructure.Model import Seller
from src.config.data_base import db

# Configuração de logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class SellerService:
    @staticmethod
    def create_seller(nome, cnpj, email, celular, senha):
        """Cria um novo seller e envia código de ativação."""
        try:
            # Validações iniciais
            if Seller.query.filter_by(cnpj=cnpj).first():
                raise ValueError(f"CNPJ {cnpj} já cadastrado")

            if Seller.query.filter_by(email=email).first():
                raise ValueError(f"Email {email} já cadastrado")

            # Formatação robusta do número
            celular = SellerService._format_phone_number(celular)

            # Validação do número apenas em produção
            if os.getenv('FLASK_ENV') == 'production':
                target_phone = os.getenv('TARGET_PHONE')
                if f"whatsapp:{celular}" != target_phone:
                    raise ValueError(f"Número {celular} não autorizado. Autorizado: {target_phone}")
            else:
                logger.info(f"[DEV] Ambiente de desenvolvimento: ignorando validação de TARGET_PHONE.")

            # Geração do código de ativação
            activation_code = str(random.randint(1000, 9999))
            logger.debug(f"Código de ativação gerado: {activation_code}")

            # Em ambiente de desenvolvimento, exibe o código para debug
            if os.getenv('FLASK_ENV') != 'production':
                print(f"\n CÓDIGO GERADO (DEV): {activation_code}\n")

            # Criação do seller
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

            # Em desenvolvimento, apenas loga o código
            if os.getenv('FLASK_ENV') != 'production':
                logger.info(f"[DEV] Código para {celular}: {activation_code}")
                return new_seller

            # Em produção, envia o código via Twilio (WhatsApp)
            if not SellerService._send_whatsapp_message(celular, activation_code):
                raise RuntimeError("Falha ao enviar código de ativação")

            logger.info(f"Seller criado: ID {new_seller.id}")
            return new_seller

        except ValueError as ve:
            db.session.rollback()
            logger.error(f"Erro de validação: {str(ve)}")
            return {"erro": str(ve)}
        except Exception as e:
            db.session.rollback()
            logger.error(f"Erro ao criar seller: {str(e)}", exc_info=True)
            return {"erro": f"Erro ao criar seller: {str(e)}"}

    @staticmethod
    def activate_seller(celular, code):
        """Ativa o seller com o código recebido."""
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
            # Removendo a atribuição de activation_code para None
            # seller.activation_code = None
            db.session.commit()

            # Em produção, envia mensagem de confirmação de ativação
            if os.getenv('FLASK_ENV') == 'production':
                SellerService.send_activation_code(celular, is_confirmation=True)

            logger.info(f"Seller ativado: ID {seller.id}")
            return seller

        except Exception as e:
            db.session.rollback()
            logger.error(f"Erro ao ativar seller: {str(e)}", exc_info=True)
            return {"erro": f"Erro ao ativar seller: {str(e)}"}

    @staticmethod
    def _format_phone_number(celular):
        """Formata o número para o padrão +55DDNNNNNNNNN com validação rigorosa."""
        if not celular:
            raise ValueError("Número de celular não fornecido")

        # Remove caracteres não numéricos
        digitos = ''.join(filter(str.isdigit, str(celular)))
        logger.debug(f"Número recebido (somente dígitos): {digitos}")

        # Ajusta o número para incluir o código do país, se necessário
        if digitos.startswith('55'):
            return f"+{digitos}"
        if digitos.startswith('0'):
            digitos = digitos[1:]
        return f"+55{digitos}"

    @staticmethod
    def _send_whatsapp_message(celular, activation_code):
        """Envia mensagem via WhatsApp utilizando o Twilio com o código de ativação."""
        try:
            account_sid = os.getenv('TWILIO_ACCOUNT_SID')
            auth_token = os.getenv('TWILIO_AUTH_TOKEN')
            twilio_phone = os.getenv('TWILIO_PHONE_NUMBER')
            client = Client(account_sid, auth_token)

            # Log para verificar os números
            print(f"Twilio Phone: {twilio_phone}")
            print(f"Destination Phone: whatsapp:{celular}")

            message_body = f"Seu código de ativação é: {activation_code}"
            message = client.messages.create(
                body=message_body,
                from_=twilio_phone,
                to=f"whatsapp:{celular}"  # Formatação correta
            )
            logger.info(f"Mensagem enviada com SID: {message.sid}")
            return True
        except TwilioRestException as e:
            logger.error(f"Erro ao enviar mensagem via Twilio: {e}")
            return False

    @staticmethod
    def send_activation_code(celular, message_text="", is_confirmation=False):
        """Envia mensagem de confirmação ou notificação após a ativação."""
        try:
            account_sid = os.getenv('TWILIO_ACCOUNT_SID')
            auth_token = os.getenv('TWILIO_AUTH_TOKEN')
            twilio_phone = os.getenv('TWILIO_PHONE_NUMBER')
            client = Client(account_sid, auth_token)

            if is_confirmation:
                message_body = "Sua conta foi ativada com sucesso!"
            else:
                message_body = message_text or "Mensagem padrão"

            message = client.messages.create(
                body=message_body,
                from_=twilio_phone,
                to=celular
            )
            logger.info(f"Mensagem de confirmação enviada com SID: {message.sid}")
        except TwilioRestException as e:
            logger.error(f"Erro ao enviar mensagem de confirmação: {e}")