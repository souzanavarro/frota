from config.database import SessionLocal
from models import Viagem

def listar_viagens(limit=100):
    db = SessionLocal()
    try:
        return db.query(Viagem).order_by(Viagem.data_saida.desc()).limit(limit).all()
    finally:
        db.close()

def buscar_por_id(viagem_id):
    db = SessionLocal()
    try:
        return db.query(Viagem).filter(Viagem.id==viagem_id).first()
    finally:
        db.close()

def atualizar_viagem(viagem_id: int, data: dict):
    db = SessionLocal()
    try:
        v = db.query(Viagem).filter(Viagem.id == viagem_id).first()
        if not v:
            return None
        for k, val in data.items():
            if hasattr(v, k) and val is not None:
                setattr(v, k, val)
        db.commit()
        db.refresh(v)
        return v
    finally:
        db.close()
