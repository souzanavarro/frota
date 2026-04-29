import streamlit as st
from services.custo_service import custo_por_km
from repositories.veiculo_repository import listar_veiculos
import pandas as pd
from components.ui import cp_hero, cp_card, cp_card_end, cp_card_back, cp_card_back_end, cp_data_panel_start, cp_data_panel_end


def render():
    cp_hero('Relatórios', 'Cálculos e resumos da frota', icon='📊')
    veiculos = listar_veiculos()
    rows = []
    for v in veiculos:
        resumo = custo_por_km(v.id)
        rows.append({'veiculo': v.placa, 'custo_total': resumo['custo_total'], 'km': resumo['km_percorrido'], 'custo_por_km': resumo['custo_por_km']})
    df = pd.DataFrame(rows)
    cp_card_back()
    # close background card before starting the data panel
    cp_card_back_end()
    cp_data_panel_start()
    st.table(df)
    cp_data_panel_end()
