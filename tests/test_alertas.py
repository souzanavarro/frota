from services.alerta_service import detectar_anomalia_consumo, manutencao_preventiva_alerts


def test_detectar_anomalia_consumo():
    # sem dados suficientes deve retornar False
    ok, msg = detectar_anomalia_consumo(99999)
    assert ok is False


def test_manutencao_preventiva_alerts():
    alerts = manutencao_preventiva_alerts()
    assert isinstance(alerts, list)
