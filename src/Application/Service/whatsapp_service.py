import os
import logging
from twilio.rest import Client
from twilio.base.exceptions import TwilioRestException

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class WhatsAppService:
    @staticmethod
    def send_message(celular, message_body):
        """Envia uma mensagem via WhatsApp usando Twilio"""
        try:
            account_sid = os.getenv('TWILIO_ACCOUNT_SID')
            auth_token = os.getenv('TWILIO_AUTH_TOKEN')
            twilio_phone = os.getenv('TWILIO_PHONE_NUMBER')

            if not all([account_sid, auth_token, twilio_phone]):
                raise EnvironmentError("Credenciais do Twilio não configuradas corretamente.")

            client = Client(account_sid, auth_token)

            message = client.messages.create(
                body=message_body,
                from_=f"whatsapp:{twilio_phone}",
                to=f"whatsapp:{celular}"
            )

            logger.info(f"Mensagem enviada para {celular} - SID: {message.sid}")
            return True

        except TwilioRestException as e:
            logger.error(f"Erro ao enviar mensagem via Twilio: {str(e)}")
            return False
