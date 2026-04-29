import streamlit as st
from config.database import SessionLocal
from models import Veiculo, Abastecimento, Manutencao
import pandas as pd


def render():
    st.title('Dashboard')
    db = SessionLocal()
    total_veiculos = db.query(Veiculo).count()
    ativos = db.query(Veiculo).filter(Veiculo.status == 'ativo').count()
    st.metric('Veículos', total_veiculos)
    st.metric('Ativos', ativos)
    st.subheader('Últimos abastecimentos')
    rows = db.query(Abastecimento).order_by(Abastecimento.data.desc()).limit(10).all()
    df = pd.DataFrame([{'data': r.data, 'veiculo': r.veiculo.placa if r.veiculo else None, 'litros': r.litros} for r in rows])
    st.table(df)
