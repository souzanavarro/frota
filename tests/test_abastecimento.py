from services.abastecimento_service import calcular_km_por_litro


def test_calcular_km_por_litro():
    assert calcular_km_por_litro(10, 100) == 10
    assert calcular_km_por_litro(0, 100) is None
    assert calcular_km_por_litro(None, 100) is None
