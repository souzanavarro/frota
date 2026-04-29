import streamlit as st
from services.custo_service import custo_por_km
from repositories.veiculo_repository import listar_veiculos
import pandas as pd


def render():
    st.title('Relatórios')
    veiculos = listar_veiculos()
    rows = []
    for v in veiculos:
        resumo = custo_por_km(v.id)
        rows.append({'veiculo': v.placa, 'custo_total': resumo['custo_total'], 'km': resumo['km_percorrido'], 'custo_por_km': resumo['custo_por_km']})
    df = pd.DataFrame(rows)
    st.table(df)
