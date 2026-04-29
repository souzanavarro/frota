from repositories.transportador_repository import criar_transportador, listar_transportadores, buscar_por_id, atualizar_transportador, buscar_por_cnpj
import re

CNPJ_DIGITS = 14


def limpar_cnpj(cnpj: str) -> str:
    return re.sub(r"\D", "", cnpj or "")


def validar_cnpj(cnpj: str) -> bool:
    c = limpar_cnpj(cnpj)
    return len(c) == CNPJ_DIGITS


def cadastrar_transportador(data: dict):
    if 'cnpj' not in data or not validar_cnpj(data.get('cnpj')):
        raise ValueError('CNPJ inválido')
    # normalizar
    data['cnpj'] = limpar_cnpj(data['cnpj'])
    # verificar duplicidade
    exists = buscar_por_cnpj(data['cnpj'])
    if exists:
        raise ValueError('CNPJ já cadastrado — verifique ou faça login')
    return criar_transportador(data)


def listar():
    return listar_transportadores()


def buscar(id):
    return buscar_por_id(id)


def atualizar(id, patch):
    if 'cnpj' in patch and not validar_cnpj(patch.get('cnpj')):
        raise ValueError('CNPJ inválido')
    if 'cnpj' in patch:
        patch['cnpj'] = limpar_cnpj(patch['cnpj'])
    return atualizar_transportador(id, patch)
