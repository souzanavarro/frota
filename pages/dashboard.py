import streamlit as st
from config.database import SessionLocal
from models import Veiculo, Abastecimento, Manutencao
import pandas as pd
from components.ui import cp_hero, cp_card, cp_card_end, cp_card_back, cp_card_back_end, cp_data_panel_start, cp_data_panel_end


def render():
    cp_hero('Dashboard', 'Visão geral da frota', icon='🏠')
    db = SessionLocal()
    total_veiculos = db.query(Veiculo).count()
    ativos = db.query(Veiculo).filter(Veiculo.status == 'ativo').count()
    st.columns([1, 1])
    cp_card()
    c1, c2 = st.columns(2)
    with c1:
        st.markdown('<div class="kpi-title">Veículos</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="kpi">{total_veiculos}</div>', unsafe_allow_html=True)
    with c2:
        st.markdown('<div class="kpi-title">Ativos</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="kpi">{ativos}</div>', unsafe_allow_html=True)
    cp_card_end()

    st.subheader('Últimos abastecimentos')
    rows = db.query(Abastecimento).order_by(Abastecimento.data.desc()).limit(10).all()
    df = pd.DataFrame([{'data': r.data, 'veiculo': r.veiculo.placa if r.veiculo else None, 'litros': r.litros} for r in rows])
    # Exibir últimos abastecimentos com overlay sobre o card branco
    cp_card_back()
    # close background card before starting data panel
    cp_card_back_end()
    cp_data_panel_start()
    st.table(df)
    cp_data_panel_end()
