import pytest
from services.transportador_service import cadastrar_transportador


def test_cnpj_duplicate_raises():
    data = {
        'cnpj': '12.345.678/0001-95',
        'nome_fantasia': 'T1',
        'telefone_contato': '0000',
        'nome_pessoa_contato': 'Pessoa',
        'nome_empresa': 'Empresa'
    }
    # first should succeed
    t1 = cadastrar_transportador(data.copy())
    assert t1 is not None
    # second should raise
    with pytest.raises(ValueError):
        cadastrar_transportador(data.copy())
