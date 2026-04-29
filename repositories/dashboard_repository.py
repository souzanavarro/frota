from config.database import SessionLocal
from models import Veiculo, Abastecimento, Manutencao


def contagens_gerais():
    db = SessionLocal()
    try:
        return {
            'veiculos': db.query(Veiculo).count(),
            'abastecimentos': db.query(Abastecimento).count(),
            'manutencoes': db.query(Manutencao).count()
        }
    finally:
        db.close()
