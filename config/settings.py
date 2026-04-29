import os

PROJECT_NAME = "Shellgestao_frota"
DB_URL = os.getenv('DATABASE_URL', 'sqlite:///frota.db')
ENV = os.getenv('ENV', 'development')
PAGE_TITLE = "Gestão de Frota"
