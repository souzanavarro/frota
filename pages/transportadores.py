import streamlit as st
from services.transportador_service import cadastrar_transportador, listar
from config.database import SessionLocal
from models import User
import pandas as pd
from components.ui import cp_hero, cp_card, cp_card_end, cp_card_back, cp_card_back_end, cp_data_panel_start, cp_data_panel_end


def render():
    cp_hero('Transportadores', 'Gerencie transportadoras', icon='🏢')
    db = SessionLocal()
    # se usuário for transportador, mostrar apenas seu registro
    current_user = None
    if 'user' in st.session_state and st.session_state.user:
        current_user = db.query(User).filter(User.username == st.session_state.user).first()

    if current_user and current_user.role == 'transportador':
        t_id = current_user.transportador_id
        if t_id:
            t = listar()
            rows = [r for r in t if r.id == t_id]
        else:
            rows = []
    else:
        rows = listar()

    st.subheader('Lista de transportadores')
    # background card behind the data panel
    cp_card_back()
    search = st.text_input('Buscar por nome fantasia ou CNPJ')
    # close background card before starting the data panel
    cp_card_back_end()
    cp_data_panel_start()
    for r in rows:
        if search:
            s = search.lower()
            if s not in (r.nome_fantasia or '').lower() and s not in (r.cnpj or '').lower():
                continue
        cols = st.columns([1, 2, 2, 2, 1])
        if cols[0].button(str(r.id), key=f"edit_trans_{r.id}"):
            st.session_state['edit_transportador_id'] = r.id
        cols[1].write(r.nome_fantasia)
        cols[2].write(r.cnpj)
        cols[3].write(r.telefone_contato)
        cols[4].write(r.nome_pessoa_contato)
    cp_data_panel_end()

    # edição de perfil para transportador logado
    if current_user and current_user.role == 'transportador' and current_user.transportador_id:
        st.markdown('---')
        st.subheader('Editar meu perfil')
        t = rows[0] if rows else None
        if t:
            cp_card()
            with st.form('edit_trans'):
                cnpj = st.text_input('CNPJ', value=t.cnpj)
                nome_fantasia = st.text_input('Nome fantasia', value=t.nome_fantasia)
                telefone = st.text_input('Telefone de contato', value=t.telefone_contato)
                nome_pessoa = st.text_input('Nome da pessoa de contato', value=t.nome_pessoa_contato)
                nome_empresa = st.text_input('Nome da empresa', value=t.nome_empresa)
                if st.form_submit_button('Salvar alterações'):
                    try:
                        from services.transportador_service import atualizar
                        atualizar(t.id, {
                            'cnpj': cnpj,
                            'nome_fantasia': nome_fantasia,
                            'telefone_contato': telefone,
                            'nome_pessoa_contato': nome_pessoa,
                            'nome_empresa': nome_empresa
                        })
                        st.success('Perfil atualizado')
                    except Exception as e:
                        st.error(f'Erro ao atualizar: {e}')
            cp_card_end()
    elif 'edit_transportador_id' in st.session_state and st.session_state.edit_transportador_id:
        tid = st.session_state.edit_transportador_id
        from repositories.transportador_repository import buscar_por_id as buscar_trans_por_id
        t = buscar_trans_por_id(tid)
        if t:
            st.markdown('---')
            st.subheader(f'Editar transportador #{tid}')
            cp_card()
            with st.form('edit_trans_admin'):
                cnpj = st.text_input('CNPJ', value=t.cnpj)
                nome_fantasia = st.text_input('Nome fantasia', value=t.nome_fantasia)
                telefone = st.text_input('Telefone de contato', value=t.telefone_contato)
                nome_pessoa = st.text_input('Nome da pessoa de contato', value=t.nome_pessoa_contato)
                nome_empresa = st.text_input('Nome da empresa', value=t.nome_empresa)
                if st.form_submit_button('Salvar alterações'):
                    try:
                        from services.transportador_service import atualizar
                        atualizar(tid, {
                            'cnpj': cnpj,
                            'nome_fantasia': nome_fantasia,
                            'telefone_contato': telefone,
                            'nome_pessoa_contato': nome_pessoa,
                            'nome_empresa': nome_empresa
                        })
                        st.success('Transportador atualizado')
                        del st.session_state['edit_transportador_id']
                    except Exception as e:
                        st.error(f'Erro ao atualizar: {e}')
            cp_card_end()

