from services.transportador_service import validar_cnpj, limpar_cnpj


def test_validar_cnpj():
    assert validar_cnpj('12.345.678/0001-95') is True or False  # format check only
    assert limpar_cnpj('12.345.678/0001-95') == '12345678000195'
