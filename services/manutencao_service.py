from repositories.veiculo_repository import buscar_por_id
from repositories.manutencao_repository import salvar_manutencao, listar_ultimas
from models import Manutencao
import datetime


def verificar_revisao_vencida(veiculo, hoje=None):
    hoje = hoje or datetime.date.today()
    # placeholder: se veículo tem próxima revisão por data e está vencida
    # atualmente o modelo de Veiculo não contém proxima_revisao_date, então retornamos False
    return False


def registrar_manutencao(data: dict):
    m = Manutencao(**data)
    if m.km is None and m.data is None:
        raise ValueError('Data ou km obrigatórios')
    return salvar_manutencao(m)


def ultimas_manutencoes(limit=20):
    return listar_ultimas(limit)
