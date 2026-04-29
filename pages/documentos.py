import streamlit as st
from config.database import SessionLocal
import pandas as pd
from components.ui import cp_hero, cp_card, cp_card_end

# Implementação mínima: tabela document not modeled yet

def render():
    cp_hero('Documentos', 'Gerencie documentos da frota', icon='📁')
    cp_card()
    st.info('Tela de documentos: implemente models/documento.py e repositório para funcionalidades completas.')
    cp_card_end()
