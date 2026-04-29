import streamlit as st
from repositories.motorista_repository import listar_motoristas, criar_motorista
import pandas as pd
from repositories.motorista_repository import buscar_por_id, atualizar_motorista
import datetime
from components.ui import cp_hero, cp_card, cp_card_end, cp_card_back, cp_card_back_end, cp_data_panel_start, cp_data_panel_end


def render():
    cp_hero('Motoristas', 'Cadastre e edite motoristas', icon='👤')

    with st.expander('Adicionar motorista'):
        cp_card()
        with st.form('form_mot'):
            nome = st.text_input('Nome')
            cpf = st.text_input('CPF')
            cnh = st.text_input('CNH')
            categoria = st.text_input('Categoria')
            contato = st.text_input('Contato')
            if st.form_submit_button('Salvar'):
                criar_motorista({'nome': nome, 'cpf': cpf, 'cnh': cnh, 'categoria': categoria, 'contato': contato})
                st.success('Motorista criado')
        cp_card_end()

    rows = listar_motoristas()
    st.subheader('Motoristas')
    cp_card_back()
    search = st.text_input('Buscar por nome ou CPF')
    # close background card before starting the data panel
    cp_card_back_end()
    cp_data_panel_start()
    for r in rows:
        if search:
            s = search.lower()
            if s not in (r.nome or '').lower() and s not in (r.cpf or '').lower():
                continue
        cols = st.columns([1,3,2,1])
        if cols[0].button(str(r.id), key=f"edit_mot_{r.id}"):
            st.session_state['edit_motorista_id'] = r.id
        cols[1].write(r.nome)
        cols[2].write(r.cpf)
        cols[3].write(r.cnh)
    cp_data_panel_end()

    if 'edit_motorista_id' in st.session_state and st.session_state.edit_motorista_id:
        mid = st.session_state.edit_motorista_id
        m = buscar_por_id(mid)
        if m:
            st.markdown('---')
            st.subheader(f'Editar motorista #{mid}')
            cp_card()
            with st.form('edit_mot_form'):
                nome = st.text_input('Nome', value=m.nome)
                cpf = st.text_input('CPF', value=m.cpf)
                cnh = st.text_input('CNH', value=m.cnh)
                categoria = st.text_input('Categoria', value=m.categoria)
                contato = st.text_input('Contato', value=m.contato)
                if st.form_submit_button('Salvar alterações'):
                    atualizar_motorista(mid, {'nome': nome, 'cpf': cpf, 'cnh': cnh, 'categoria': categoria, 'contato': contato})
                    st.success('Motorista atualizado')
                    del st.session_state['edit_motorista_id']
            cp_card_end()
