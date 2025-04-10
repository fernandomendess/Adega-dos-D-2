from twilio.rest import Client
from twilio.http.http_client import TwilioHttpClient
import random
import datetime

# SID e Auth Token do Twilio (sandbox)
account_sid = 'ACe16c5c13b0a8e96c4e0202f980247fb0'
auth_token = '6c6ec72a24e836f299cb9c34b250f2b9'

# ⚠️ Ignora a verificação do certificado SSL (não recomendado para produção)
proxy_client = TwilioHttpClient()
proxy_client.session.verify = False 

# Configuração do cliente Twilio usando o proxy SSL
client = Client(account_sid, auth_token, http_client=proxy_client)

# Número do WhatsApp do Sandbox
twilio_numero_whats = 'whatsapp:+14155238886'  

def send_whatsapp_message(phone_number, message):
    try:
        
        if not phone_number.startswith('+'):
            raise ValueError("Número precisa estar no formato internacional, ex: +5511974074650")

        # Envia a mensagem via WhatsApp
        message = client.messages.create(
            from_=twilio_numero_whats,
            body=message,
            to=f'whatsapp:{phone_number}'
        )
        print(f'[✔️] Mensagem enviada para {phone_number}')
        print(f'📨 SID: {message.sid}')

        # Obtém o status da mensagem
        status = client.messages(message.sid).fetch().status
        print(f'📊 Status da mensagem: {status}')
        return True
    except Exception as e:
        print(f'[❌] Erro ao enviar mensagem via WhatsApp: {e}')
        return False

def generate_activation_code():
    # Gera um código de 4 dígitos
    return str(random.randint(1000, 9999))

def send_verification_code(phone_number, verification_code):
    # Formatação da mensagem de verificação
    message_body = (
        '🔒 *Código de Verificação*\n'
        f'Seu código é: *{verification_code}*\n'
        'Válido por 45 minutos.'
    )

    # Se phone_number for uma lista, utiliza o primeiro número
    if isinstance(phone_number, list):
        phone_number = phone_number[0]

    # Envia a mensagem de verificação
    return send_whatsapp_message(phone_number, message_body)

# Teste rápido direto no arquivo (execução direta)
if __name__ == "__main__":
    # Substitua pelo número que enviou o "join xxx" para o sandbox
    phone_number = "+5511974074650"
    code = generate_activation_code()
    send_verification_code(phone_number, code)
