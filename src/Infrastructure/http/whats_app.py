from twilio.rest import Client
from dotenv import load_dotenv
import os

load_dotenv()

class WhatsAppService:
    def __init__(self):
        self.client = Client(os.getenv("TWILIO_SID"), os.getenv("TWILIO_AUTH_TOKEN"))
        self.verify_sid = os.getenv("TWILIO_VERIFY_SID")

    def send_code(self, phone_number):
        return self.client.verify.v2.services(self.verify_sid) \
            .verifications.create(to=f'whatsapp:{phone_number}', channel='whatsapp')

    def verify_code(self, phone_number, code):
        verification_check = self.client.verify.v2.services(self.verify_sid) \
            .verification_checks.create(to=f'whatsapp:{phone_number}', code=code)
        return verification_check.status == "approved"