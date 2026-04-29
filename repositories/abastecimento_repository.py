from config.database import SessionLocal
from models import Abastecimento

def salvar_abastecimento(obj: Abastecimento):
    db = SessionLocal()
    db.add(obj)
    db.commit()
    db.refresh(obj)
    db.close()
    return obj

def listar_ultimos(limit=20):
    db = SessionLocal()
    try:
        return db.query(Abastecimento).order_by(Abastecimento.data.desc()).limit(limit).all()
    finally:
        db.close()
