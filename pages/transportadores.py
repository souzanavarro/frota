import streamlit as st
from services.transportador_service import cadastrar_transportador, listar
from config.database import SessionLocal
from models import User
import pandas as pd


def render():
    st.title('Transportadores')
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
    df = pd.DataFrame([{'id': r.id, 'cnpj': r.cnpj, 'nome_fantasia': r.nome_fantasia, 'telefone': r.telefone_contato, 'contato': r.nome_pessoa_contato, 'empresa': r.nome_empresa} for r in rows])
    st.table(df)

    # edição de perfil para transportador logado
    if current_user and current_user.role == 'transportador' and current_user.transportador_id:
        st.markdown('---')
        st.subheader('Editar meu perfil')
        t = rows[0] if rows else None
        if t:
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

