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

def buscar_por_id(abastecimento_id):
    db = SessionLocal()
    try:
        return db.query(Abastecimento).filter(Abastecimento.id==abastecimento_id).first()
    finally:
        db.close()

def atualizar_abastecimento(abastecimento_id: int, data: dict):
    db = SessionLocal()
    try:
        a = db.query(Abastecimento).filter(Abastecimento.id == abastecimento_id).first()
        if not a:
            return None
        for k, val in data.items():
            if hasattr(a, k) and val is not None:
                setattr(a, k, val)
        db.commit()
        db.refresh(a)
        return a
    finally:
        db.close()
