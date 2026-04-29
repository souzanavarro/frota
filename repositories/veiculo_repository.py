from config.database import SessionLocal
from models import Veiculo
from sqlalchemy.orm import joinedload

def listar_veiculos():
    db = SessionLocal()
    try:
        # carregar motorista relacionado para evitar DetachedInstanceError
        return db.query(Veiculo).options(joinedload(Veiculo.motorista)).all()
    finally:
        db.close()

def buscar_por_id(veiculo_id):
    db = SessionLocal()
    try:
        return db.query(Veiculo).filter(Veiculo.id==veiculo_id).first()
    finally:
        db.close()

def criar_veiculo(data: dict):
    db = SessionLocal()
    v = Veiculo(**data)
    db.add(v)
    db.commit()
    db.refresh(v)
    db.close()
    return v

def atualizar_veiculo(veiculo_id: int, data: dict):
    db = SessionLocal()
    try:
        v = db.query(Veiculo).filter(Veiculo.id == veiculo_id).first()
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
