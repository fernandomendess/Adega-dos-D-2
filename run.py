from flask import Flask
from src.config.data_base import init_db
from src.routes import init_routes
import time
import os
from dotenv import load_dotenv

load_dotenv()

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
    
    # Tentativa de conexão com o MySQL
    for i in range(5):
        try:
            init_db(app)
            break
        except Exception as e:
            if i == 4:
                raise RuntimeError(f"Falha ao conectar ao MySQL após 5 tentativas: {str(e)}")
            print(f"⚠️ Tentativa {i+1}/5 - MySQL não disponível, aguardando...")
            time.sleep(5)
    
    init_routes(app)
    return app

app = create_app()

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)