import streamlit as st
from services.abastecimento_service import registrar_abastecimento, ultimos_abastecimentos
from repositories.veiculo_repository import listar_veiculos
from repositories.motorista_repository import listar_motoristas
import pandas as pd
import datetime


def render():
    st.title('Abastecimentos')
    veiculos = listar_veiculos()
    motoristas = listar_motoristas()

    with st.expander('Registrar abastecimento'):
        with st.form('form_abast'):
            veiculo_id = st.selectbox('Veículo', [v.id for v in veiculos], format_func=lambda x: next((vv.placa for vv in veiculos if vv.id==x), ''))
            motorista_id = st.selectbox('Motorista (opcional)', [None]+[m.id for m in motoristas], format_func=lambda x: '' if x is None else next((mm.nome for mm in motoristas if mm.id==x), ''))
            posto = st.text_input('Posto')
            tipo = st.selectbox('Tipo combustível', ['diesel','gasolina','gnv','flex'])
            litros = st.number_input('Litros', value=0.0)
            valor_total = st.number_input('Valor total', value=0.0)
            valor_litro = st.number_input('Valor por litro', value=0.0)
            km = st.number_input('KM no abastecimento', value=0.0)
            tanque_cheio = st.checkbox('Tanque cheio?')
            if st.form_submit_button('Registrar'):
                data = {
                    'veiculo_id': veiculo_id,
                    'motorista_id': motorista_id,
                    'posto': posto,
                    'tipo_combustivel': tipo,
                    'litros': litros,
                    'valor_total': valor_total,
                    'valor_litro': valor_litro,
                    'km': km,
                    'tanque_cheio': bool(tanque_cheio),
                    'data': datetime.datetime.utcnow()
                }
                try:
                    registrar_abastecimento(data)
                    st.success('Abastecimento registrado')
                except Exception as e:
                    st.error(f'Erro: {e}')

    st.subheader('Últimos abastecimentos')
    rows = ultimos_abastecimentos(20)
    df = pd.DataFrame([{
        'data': r.data,
        'veiculo': r.veiculo.placa if r.veiculo else None,
        'motorista': r.motorista.nome if r.motorista else None,
        'litros': r.litros,
        'valor': r.valor_total,
        'km': r.km
    } for r in rows])
    st.table(df)
