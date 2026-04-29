from repositories.abastecimento_repository import salvar_abastecimento, listar_ultimos
from models import Abastecimento, Veiculo
from repositories.veiculo_repository import buscar_por_id


def calcular_km_por_litro(litros, km_percorridos):
    try:
        return km_percorridos / litros if litros and litros > 0 else None
    except Exception:
        return None


def registrar_abastecimento(data: dict):
    a = Abastecimento(**data)
    if a.litros is None or a.litros <= 0:
        raise ValueError('Litros inválidos')
    saved = salvar_abastecimento(a)
    # atualizar km do veículo se necessário
    if saved.veiculo_id and saved.km:
        v = buscar_por_id(saved.veiculo_id)
        if v and (v.km_atual is None or saved.km > v.km_atual):
            v.km_atual = saved.km
            from config.database import SessionLocal
            db = SessionLocal()
            db.add(v)
            db.commit()
            db.close()
    return saved


def ultimos_abastecimentos(limit=20):
    return listar_ultimos(limit)
