from config.database import init_db, SessionLocal
import models
from utils.auth import hash_password


def seed():
    # cria tabelas a partir dos modelos
    init_db(models.Base)
    db = SessionLocal()
    # criar usuário admin se não existir
    try:
        if db.query(models.User).filter(models.User.username == 'admin').count() == 0:
            admin = models.User(username='admin', password_hash=hash_password('admin'), role='admin')
            db.add(admin)
            db.commit()
    finally:
        db.close()


if __name__ == '__main__':
    seed()
    print('Banco inicializado e seed aplicado')
