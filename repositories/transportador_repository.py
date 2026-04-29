from config.database import SessionLocal
from models import Transportador

def listar_transportadores():
    db = SessionLocal()
    try:
        return db.query(Transportador).all()
    finally:
        db.close()

def buscar_por_id(transportador_id):
    db = SessionLocal()
    try:
        return db.query(Transportador).filter(Transportador.id==transportador_id).first()
    finally:
        db.close()


def buscar_por_cnpj(cnpj: str):
    db = SessionLocal()
    try:
        return db.query(Transportador).filter(Transportador.cnpj == cnpj).first()
    finally:
        db.close()

def criar_transportador(data: dict):
    db = SessionLocal()
    t = Transportador(**data)
    db.add(t)
    db.commit()
    db.refresh(t)
    db.close()
    return t

def atualizar_transportador(transportador_id, patch: dict):
    db = SessionLocal()
    try:
        t = db.query(Transportador).filter(Transportador.id==transportador_id).first()
        if not t:
            return None
        for k,v in patch.items():
            setattr(t,k,v)
        db.add(t)
        db.commit()
        db.refresh(t)
        return t
    finally:
        db.close()
