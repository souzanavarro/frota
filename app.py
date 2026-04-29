import streamlit as st
from config.database import init_db, SessionLocal
import config.settings as settings
import models
from utils.auth import hash_password, verify_password
from components.sidebar import render_sidebar

from pages import dashboard as dashboard_page_module
from pages import veiculos as veiculos_page_module
from pages import abastecimentos as abastecimentos_page_module
from pages import manutencoes as manutencoes_page_module


def configurar():
    init_db(models.Base)
    st.set_page_config(page_title=settings.PAGE_TITLE, layout='wide')


def login_flow():
    if 'user' not in st.session_state:
        st.session_state.user = None
    if 'user_role' not in st.session_state:
        st.session_state.user_role = None
    if 'transportador_id' not in st.session_state:
        st.session_state.transportador_id = None
    if st.session_state.user is None:
        st.title('Frota — Login')
        username = st.text_input('Usuário')
        password = st.text_input('Senha', type='password')
        db = SessionLocal()
        if st.button('Entrar'):
            user = db.query(models.User).filter(models.User.username == username).first()
            if user and verify_password(password, user.password_hash):
                st.session_state.user = user.username
                st.session_state.user_role = user.role
                st.session_state.transportador_id = getattr(user, 'transportador_id', None)
                st.experimental_rerun()
            else:
                st.error('Usuário ou senha inválidos')
        # registro público de transportador + usuário
        st.markdown('---')
        st.subheader('Cadastro de transportador e conta')
        with st.form('register_transportador'):
            reg_username = st.text_input('Usuário (para login)')
            reg_password = st.text_input('Senha', type='password')
            cnpj = st.text_input('CNPJ')
            nome_fantasia = st.text_input('Nome fantasia')
            telefone = st.text_input('Telefone de contato')
            nome_pessoa = st.text_input('Nome da pessoa de contato')
            nome_empresa = st.text_input('Nome da empresa')
            if st.form_submit_button('Cadastrar transportador'):
                try:
                    # criar transportador
                    from services.transportador_service import cadastrar_transportador
                    t = cadastrar_transportador({
                        'cnpj': cnpj,
                        'nome_fantasia': nome_fantasia,
                        'telefone_contato': telefone,
                        'nome_pessoa_contato': nome_pessoa,
                        'nome_empresa': nome_empresa
                    })
                    # criar user vinculado
                    from utils.auth import hash_password
                    new_user = models.User(username=reg_username, password_hash=hash_password(reg_password), role='transportador', transportador_id=t.id)
                    db.add(new_user)
                    db.commit()
                    st.success('Transportador e conta criados — faça login')
                except Exception as e:
                    st.error(f'Erro ao cadastrar: {e}')
        return False
    return True


def main():
    configurar()
    if not login_flow():
        return
    menu = render_sidebar(['Dashboard', 'Veículos', 'Motoristas', 'Transportadores', 'Abastecimentos', 'Manutenções', 'Viagens', 'Documentos', 'Relatórios'])
    if menu == 'Dashboard':
        dashboard_page_module.render()
    elif menu == 'Veículos':
        veiculos_page_module.render()
    elif menu == 'Motoristas':
        from pages import motoristas as motoristas_page_module
        motoristas_page_module.render()
    elif menu == 'Transportadores':
        from pages import transportadores as transportadores_page_module
        transportadores_page_module.render()
    elif menu == 'Abastecimentos':
        abastecimentos_page_module.render()
    elif menu == 'Manutenções':
        manutencoes_page_module.render()
    elif menu == 'Viagens':
        from pages import viagens as viagens_page_module
        viagens_page_module.render()
    elif menu == 'Documentos':
        from pages import documentos as documentos_page_module
        documentos_page_module.render()
    elif menu == 'Relatórios':
        from pages import relatorios as relatorios_page_module
        relatorios_page_module.render()


if __name__ == '__main__':
    main()
