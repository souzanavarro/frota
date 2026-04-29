import streamlit as st
from repositories.transportador_repository import buscar_por_id as buscar_transportador
from components.theme import apply_styles


def render_sidebar(menu_options):
    st.sidebar.title('Frota')

    # bloco de informações do usuário / transportador
    if 'user' in st.session_state and st.session_state.user:
        user = st.session_state.user
        role = st.session_state.user_role if 'user_role' in st.session_state else None
        trans_id = st.session_state.transportador_id if 'transportador_id' in st.session_state else None

        # mostrar informações do transportador quando aplicável
        if role == 'transportador' and trans_id:
            t = buscar_transportador(trans_id)
            if t:
                # imagem via ui-avatars (placeholder) usando nome fantasia
                name = t.nome_fantasia or t.nome_empresa or 'Transportador'
                # usar tamanho maior e cor de fundo adequada
                avatar_bg = '0D8ABC'
                avatar_color = 'ffffff'
                img_url = f"https://ui-avatars.com/api/?name={name.replace(' ', '+')}&background={avatar_bg}&color={avatar_color}&size=256"
                try:
                    st.sidebar.image(img_url, width=96)
                except Exception:
                    pass
                st.sidebar.markdown(f"**{name}**")
                st.sidebar.caption(f"CNPJ: {t.cnpj}")
                # mostrar telefone e pessoa de contato se existir
                if getattr(t, 'telefone_contato', None):
                    st.sidebar.write(f"📞 {t.telefone_contato}")
                if getattr(t, 'nome_pessoa_contato', None):
                    st.sidebar.write(f"👤 {t.nome_pessoa_contato}")
        else:
            # usuário genérico (admin)
            st.sidebar.markdown(f"**{user}**")

        if st.sidebar.button('Sair'):
            # limpar sessão e recarregar
            st.session_state.user = None
            st.session_state.user_role = None
            st.session_state.transportador_id = None
            st.session_state.menu = None
            # Tentativa de rerun compatível com diferentes versões do Streamlit
            if hasattr(st, 'experimental_rerun'):
                try:
                    st.experimental_rerun()
                except Exception:
                    # fallback: parar execução atual para aplicar mudanças na sessão
                    st.stop()
            else:
                st.stop()
    else:
        st.sidebar.info('Não autenticado')

    st.sidebar.markdown('---')

    # seletor de tema (Claro / Escuro)
    if 'theme' not in st.session_state:
        st.session_state.theme = '🌞 Claro'
    theme_options = ['🌞 Claro', '🌙 Escuro']
    theme_index = 0 if st.session_state.theme == '🌞 Claro' else 1
    selected_theme = st.sidebar.radio('Tema', theme_options, index=theme_index)
    if selected_theme != st.session_state.theme:
        st.session_state.theme = selected_theme
    try:
        apply_styles(st.session_state.theme)
    except Exception:
        pass

    # substituir seletor por botões de navegação
    if 'menu' not in st.session_state:
        st.session_state.menu = menu_options[0] if menu_options else None

    for opt in menu_options:
        if st.sidebar.button(opt, key=f"nav_{opt}"):
            st.session_state.menu = opt
            # botão dispara rerun automaticamente

    return st.session_state.menu
