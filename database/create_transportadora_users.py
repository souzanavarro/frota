from config.database import init_db, SessionLocal
import models
from utils.auth import hash_password
import os


def ensure_admin_and_test_user():
    init_db(models.Base)
    db = SessionLocal()
    try:
        # ensure admin
        admin = db.query(models.User).filter(models.User.username == 'admin').first()
        if not admin:
            admin = models.User(username='admin', password_hash=hash_password('admin'), role='admin')
            db.add(admin)
            db.commit()
            print('Usuário admin criado (senha: admin)')
        else:
            print('Usuário admin já existe')

        # find transportadora teste
        trans = db.query(models.Transportador).filter(models.Transportador.nome_fantasia == 'Transportadora Teste').first()
        if not trans:
            trans = db.query(models.Transportador).filter(models.Transportador.cnpj == '00000000000100').first()
        if not trans:
            print("Transportadora de teste não encontrada. Rode 'python database/seed_test_data.py' primeiro.")
            return

        # create test user
        username = 'teste'
        user = db.query(models.User).filter(models.User.username == username).first()
        if not user:
            user = models.User(username=username, password_hash=hash_password('teste'), role='transportador', transportador_id=trans.id)
            db.add(user)
            db.commit()
            print(f'Usuário {username} criado e vinculado a transportadora id={trans.id}')
        else:
            print(f'Usuário {username} já existe')

    finally:
        db.close()


if __name__ == '__main__':
    ensure_admin_and_test_user()
