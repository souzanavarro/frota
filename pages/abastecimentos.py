import streamlit as st
from services.abastecimento_service import registrar_abastecimento, ultimos_abastecimentos
from repositories.veiculo_repository import listar_veiculos
from repositories.motorista_repository import listar_motoristas
from repositories.abastecimento_repository import buscar_por_id, atualizar_abastecimento
import pandas as pd
import datetime
from components.ui import cp_hero, cp_card, cp_card_end, cp_card_back, cp_card_back_end, cp_data_panel_start, cp_data_panel_end


def render():
    cp_hero('Abastecimentos', 'Registre abastecimentos e edite registros', icon='⛽')
    veiculos = listar_veiculos()
    motoristas = listar_motoristas()

    with st.expander('Registrar abastecimento'):
        cp_card()
        with st.form('form_abast'):
            veiculo_id = st.selectbox('Veículo', [v.id for v in veiculos], format_func=lambda x: next((vv.placa for vv in veiculos if vv.id==x), ''))
            motorista_id = st.selectbox('Motorista (opcional)', [None]+[m.id for m in motoristas], format_func=lambda x: '' if x is None else next((mm.nome for mm in motoristas if mm.id==x), ''))
            posto = st.text_input('Posto')
            tipo = st.selectbox('Tipo combustível', ['diesel','gasolina','gnv','flex'])
            litros = st.number_input('Litros', value=0.0)
            valor_total = st.number_input('Valor total', value=0.0)
            valor_litro = st.number_input('Valor por litro', value=0.0)
            km = st.number_input('KM no abastecimento', value=0.0)
            tanque_cheio = st.checkbox('Tanque cheio?')
            if st.form_submit_button('Registrar'):
                data = {
                    'veiculo_id': veiculo_id,
                    'motorista_id': motorista_id,
                    'posto': posto,
                    'tipo_combustivel': tipo,
                    'litros': litros,
                    'valor_total': valor_total,
                    'valor_litro': valor_litro,
                    'km': km,
                    'tanque_cheio': bool(tanque_cheio),
                    'data': datetime.datetime.utcnow()
                }
                try:
                    registrar_abastecimento(data)
                    st.success('Abastecimento registrado')
                except Exception as e:
                    st.error(f'Erro: {e}')
        cp_card_end()

    st.subheader('Últimos abastecimentos')
    rows = ultimos_abastecimentos(200)
    st.subheader('Pesquisar / Editar abastecimento')
    fcol1, fcol2 = st.columns([2, 1])
    search = fcol1.text_input('Buscar por placa, motorista ou posto')
    show_all = fcol2.checkbox('Mostrar todos', value=True)

    cp_card_back()
    # close background card before starting the data panel
    cp_card_back_end()
    cp_data_panel_start()
    for r in rows:
        placa = r.veiculo.placa if r.veiculo else ''
        motorista = r.motorista.nome if r.motorista else ''
        if not show_all and search:
            s = search.lower()
            if s not in placa.lower() and s not in motorista.lower() and s not in (r.posto or '').lower():
                continue
        cols = st.columns([1, 2, 2, 2, 1, 1])
        if cols[0].button(str(r.id), key=f"edit_abast_{r.id}"):
            st.session_state['edit_abastecimento_id'] = r.id
        cols[1].write(placa)
        cols[2].write(motorista)
        cols[3].write(r.posto)
        cols[4].write(r.litros)
        cols[5].write(r.data)
    cp_data_panel_end()

    if 'edit_abastecimento_id' in st.session_state and st.session_state.edit_abastecimento_id:
        aid = st.session_state.edit_abastecimento_id
        a = buscar_por_id(aid)
        if a:
            st.markdown('---')
            st.subheader(f'Editar abastecimento #{aid}')
            cp_card()
            with st.form('edit_abast_form'):
                veiculo_id = st.selectbox('Veículo', [v.id for v in veiculos], index=next((i for i, v in enumerate(veiculos) if v.id == a.veiculo_id), 0), format_func=lambda x: next((vv.placa for vv in veiculos if vv.id == x), ''))
                motorista_id = st.selectbox('Motorista (opcional)', [None] + [m.id for m in motoristas], index=next((i + 1 for i, m in enumerate(motoristas) if m.id == a.motorista_id), 0), format_func=lambda x: '' if x is None else next((mm.nome for mm in motoristas if mm.id == x), ''))
                data = st.date_input('Data', value=a.data.date() if a.data else datetime.date.today())
                posto = st.text_input('Posto', value=a.posto or '')
                tipo = st.selectbox('Tipo combustível', ['diesel', 'gasolina', 'gnv', 'flex'], index=['diesel', 'gasolina', 'gnv', 'flex'].index(a.tipo_combustivel) if a.tipo_combustivel in ['diesel', 'gasolina', 'gnv', 'flex'] else 0)
                litros = st.number_input('Litros', value=a.litros or 0.0)
                valor_total = st.number_input('Valor total', value=a.valor_total or 0.0)
                valor_litro = st.number_input('Valor por litro', value=a.valor_litro or 0.0)
                km = st.number_input('KM no abastecimento', value=a.km or 0.0)
                tanque_cheio = st.checkbox('Tanque cheio?', value=a.tanque_cheio or False)
                if st.form_submit_button('Salvar alterações'):
                    payload = {
                        'veiculo_id': veiculo_id,
                        'motorista_id': motorista_id,
                        'data': datetime.datetime.combine(data, datetime.datetime.min.time()),
                        'posto': posto,
                        'tipo_combustivel': tipo,
                        'litros': litros,
                        'valor_total': valor_total,
                        'valor_litro': valor_litro,
                        'km': km,
                        'tanque_cheio': bool(tanque_cheio)
                    }
                    atualizar_abastecimento(aid, payload)
                    st.success('Abastecimento atualizado')
                    del st.session_state['edit_abastecimento_id']
            cp_card_end()
