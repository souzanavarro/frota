import streamlit as st
from repositories.veiculo_repository import listar_veiculos, criar_veiculo
from repositories.motorista_repository import listar_motoristas
from repositories.veiculo_repository import buscar_por_id, atualizar_veiculo
import datetime
from components.ui import cp_card, cp_card_end, cp_primary_button, cp_hero, cp_card_back, cp_card_back_end, cp_data_panel_start, cp_data_panel_end


def render():
    cp_hero('Veículos', 'Gerencie a frota e associe motoristas', icon='🚚')

    motoristas = listar_motoristas()
    motorista_options = ["--- Nenhum ---"] + [f"{m.id} - {m.nome}" for m in motoristas]

    cp_card()
    with st.form('novo_veiculo'):
        placa = st.text_input('Placa')
        tipo = st.selectbox('Tipo de Veículo', ['Truck', 'Toco', '3/4', 'Van'])
        codigo = st.text_input('Código (opcional)')
        marca_modelo = st.text_input('Marca / Modelo (opcional)')
        motorista_sel = st.selectbox('Motorista (associar)', motorista_options)
        submitted = st.form_submit_button('Salvar veículo')

        if submitted:
            motorista_id = None
            if motorista_sel and motorista_sel != "--- Nenhum ---":
                motorista_id = int(motorista_sel.split(' - ')[0])

            data = {
                'placa': placa,
                'codigo': codigo or None,
                'tipo': tipo,
                'marca_modelo': marca_modelo or None,
                'motorista_id': motorista_id
            }
            try:
                criar_veiculo(data)
                st.success('Veículo criado com sucesso')
            except Exception as e:
                st.error(f'Erro ao criar veículo: {e}')
    cp_card_end()

    st.markdown('---')
    # filtros
    st.subheader('Filtrar veículos')
    fcol1, fcol2 = st.columns([3,1])
    search = fcol1.text_input('Buscar por placa ou motorista')
    show_all = fcol2.checkbox('Mostrar todos', value=True)

    veiculos = listar_veiculos()
    motoristas_map = {m.id: m.nome for m in listar_motoristas()}

    def matches(v):
        if not search:
            return True
        s = search.lower()
        if s in (v.placa or '').lower():
            return True
        mname = motoristas_map.get(v.motorista_id, '') or ''
        if s in mname.lower():
            return True
        return False

    st.subheader('Veículos')
    # Background card (visual white card behind)
    cp_card_back()
    # close background card before starting the data panel (panel should be a sibling)
    cp_card_back_end()
    cp_data_panel_start()
    for v in veiculos:
        if not show_all and not matches(v):
            continue
        motorista_text = motoristas_map.get(v.motorista_id, '')
        cols = st.columns([1,2,2,1])
        if cols[0].button(str(v.id), key=f"edit_veic_{v.id}"):
            st.session_state['edit_veiculo_id'] = v.id
        cols[1].write(v.placa)
        cols[2].write(v.marca_modelo or '')
        cols[3].write(motorista_text)
    cp_data_panel_end()

    # edição via id clicado
    if 'edit_veiculo_id' in st.session_state and st.session_state.edit_veiculo_id:
        vid = st.session_state.edit_veiculo_id
        ve = buscar_por_id(vid)
        if ve:
            st.markdown('---')
            st.subheader(f'Editar veículo #{vid}')
            cp_card()
            with st.form('edit_veic_form'):
                placa = st.text_input('Placa', value=ve.placa)
                tipo = st.selectbox('Tipo de Veículo', ['Truck', 'Toco', '3/4', 'Van'], index=['Truck','Toco','3/4','Van'].index(ve.tipo) if ve.tipo in ['Truck','Toco','3/4','Van'] else 0)
                codigo = st.text_input('Código (opcional)', value=ve.codigo or '')
                marca_modelo = st.text_input('Marca / Modelo (opcional)', value=ve.marca_modelo or '')
                motorista_options = ['--- Nenhum ---'] + [f"{m.id} - {m.nome}" for m in listar_motoristas()]
                motorista_sel = st.selectbox('Motorista (associar)', motorista_options, index=0)
                if ve.motorista_id:
                    try:
                        idx = motorista_options.index(f"{ve.motorista_id} - {ve.motorista.nome}")
                        motorista_sel = motorista_options[idx]
                    except Exception:
                        pass
                if st.form_submit_button('Salvar alterações'):
                    motorista_id = None
                    if motorista_sel and motorista_sel != "--- Nenhum ---":
                        motorista_id = int(motorista_sel.split(' - ')[0])
                    atualizar_veiculo(vid, {'placa': placa, 'codigo': codigo or None, 'tipo': tipo, 'marca_modelo': marca_modelo or None, 'motorista_id': motorista_id})
                    st.success('Veículo atualizado')
                    del st.session_state['edit_veiculo_id']
