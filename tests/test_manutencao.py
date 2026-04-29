from services.manutencao_service import verificar_revisao_vencida
import datetime


def test_verificar_revisao_vencida():
    # placeholder: a função retorna False por enquanto
    assert verificar_revisao_vencida(None) is False
    assert verificar_revisao_vencida({}, hoje=datetime.date.today()) is False
