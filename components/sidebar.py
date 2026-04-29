import streamlit as st

def render_sidebar(menu_options):
    st.sidebar.title('Frota')
    return st.sidebar.selectbox('Menu', menu_options)
