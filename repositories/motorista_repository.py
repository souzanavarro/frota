from config.database import SessionLocal
from models import Motorista

def listar_motoristas():
    db = SessionLocal()
    try:
        return db.query(Motorista).all()
    finally:
        db.close()

def criar_motorista(data: dict):
    db = SessionLocal()
    m = Motorista(**data)
    db.add(m)
    db.commit()
    db.refresh(m)
    db.close()
    return m

def buscar_por_id(motorista_id):
    db = SessionLocal()
    try:
        return db.query(Motorista).filter(Motorista.id==motorista_id).first()
    finally:
        db.close()

def atualizar_motorista(motorista_id: int, data: dict):
    db = SessionLocal()
    try:
        m = db.query(Motorista).filter(Motorista.id == motorista_id).first()
        if not m:
            return None
        for k, val in data.items():
            if hasattr(m, k) and val is not None:
                setattr(m, k, val)
        db.commit()
        db.refresh(m)
        return m
    finally:
        db.close()
