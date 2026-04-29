from config.database import SessionLocal
from models import Manutencao

def salvar_manutencao(obj: Manutencao):
    db = SessionLocal()
    db.add(obj)
    db.commit()
    db.refresh(obj)
    db.close()
    return obj

def listar_ultimas(limit=20):
    db = SessionLocal()
    try:
        return db.query(Manutencao).order_by(Manutencao.data.desc()).limit(limit).all()
    finally:
        db.close()

def buscar_por_id(manutencao_id):
    db = SessionLocal()
    try:
        return db.query(Manutencao).filter(Manutencao.id==manutencao_id).first()
    finally:
        db.close()

def atualizar_manutencao(manutencao_id: int, data: dict):
    db = SessionLocal()
    try:
        m = db.query(Manutencao).filter(Manutencao.id == manutencao_id).first()
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
