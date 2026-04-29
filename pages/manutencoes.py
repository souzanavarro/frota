import streamlit as st
from services.manutencao_service import registrar_manutencao, ultimas_manutencoes
from repositories.veiculo_repository import listar_veiculos
from repositories.manutencao_repository import listar_ultimas, buscar_por_id, atualizar_manutencao
import datetime
import pandas as pd


def render():
    st.title('Manutenções')
    veiculos = listar_veiculos()

    with st.expander('Registrar manutenção'):
        with st.form('form_manu'):
            veiculo_id = st.selectbox('Veículo', [v.id for v in veiculos], format_func=lambda x: next((vv.placa for vv in veiculos if vv.id==x), ''))
            tipo = st.selectbox('Tipo', ['preventiva','corretiva'])
            data = st.date_input('Data', value=datetime.date.today())
            km = st.number_input('KM', value=0.0)
            oficina = st.text_input('Oficina')
            descricao = st.text_area('Descrição')
            custo_pecas = st.number_input('Custo peças', value=0.0)
            custo_mao = st.number_input('Custo mão de obra', value=0.0)
            if st.form_submit_button('Registrar'):
                payload = {
                    'veiculo_id': veiculo_id,
                    'tipo': tipo,
                    'data': datetime.datetime.combine(data, datetime.datetime.min.time()),
                    'km': km,
                    'oficina': oficina,
                    'descricao': descricao,
                    'custo_pecas': custo_pecas,
                    'custo_mao_obra': custo_mao
                }
                try:
                    registrar_manutencao(payload)
                    st.success('Manutenção registrada')
                except Exception as e:
                    st.error(f'Erro: {e}')

    st.subheader('Últimas manutenções')
    rows = ultimas_manutencoes(200)
    df = pd.DataFrame([{
            'id': r.id,
            'data': r.data,
            'veiculo': r.veiculo.placa if r.veiculo else None,
            'tipo': r.tipo,
            'km': r.km,
            'oficina': r.oficina,
            'custo_total': (r.custo_pecas or 0) + (r.custo_mao_obra or 0)
    } for r in rows])
    st.table(df)

    # filtro por período e busca
    st.markdown('---')
    st.subheader('Pesquisar / Editar manutenção')
    fcol1, fcol2 = st.columns([2,1])
    search = fcol1.text_input('Buscar por placa ou descrição')
    show_all = fcol2.checkbox('Mostrar todos', value=True)

    for r in rows:
        placa = r.veiculo.placa if r.veiculo else ''
        if not show_all and search:
            s = search.lower()
            if s not in placa.lower() and s not in (r.descricao or '').lower():
                continue
        cols = st.columns([1,2,2,1,1])
        if cols[0].button(str(r.id), key=f"edit_manu_{r.id}"):
            st.session_state['edit_manutencao_id'] = r.id
        cols[1].write(placa)
        cols[2].write(r.tipo)
        cols[3].write(r.km)
        cols[4].write(r.data)

    if 'edit_manutencao_id' in st.session_state and st.session_state.edit_manutencao_id:
        mid = st.session_state.edit_manutencao_id
        m = buscar_por_id(mid)
        if m:
            st.markdown('---')
            st.subheader(f'Editar manutenção #{mid}')
            with st.form('edit_manu_form'):
                veiculos = listar_veiculos()
                veiculo_id = st.selectbox('Veículo', [v.id for v in veiculos], index=next((i for i,v in enumerate(veiculos) if v.id==m.veiculo_id), 0), format_func=lambda x: next((vv.placa for vv in veiculos if vv.id==x), ''))
                tipo = st.selectbox('Tipo', ['preventiva','corretiva'], index=0 if m.tipo=='preventiva' else 1)
                data = st.date_input('Data', value=m.data.date() if m.data else datetime.date.today())
                km = st.number_input('KM', value=m.km or 0.0)
                oficina = st.text_input('Oficina', value=m.oficina or '')
                descricao = st.text_area('Descrição', value=m.descricao or '')
                custo_pecas = st.number_input('Custo peças', value=m.custo_pecas or 0.0)
                custo_mao = st.number_input('Custo mão de obra', value=m.custo_mao_obra or 0.0)
                if st.form_submit_button('Salvar alterações'):
                    payload = {
                        'veiculo_id': veiculo_id,
                        'tipo': tipo,
                        'data': datetime.datetime.combine(data, datetime.datetime.min.time()),
                        'km': km,
                        'oficina': oficina,
                        'descricao': descricao,
                        'custo_pecas': custo_pecas,
                        'custo_mao_obra': custo_mao
                    }
                    atualizar_manutencao(mid, payload)
                    st.success('Manutenção atualizada')
                    del st.session_state['edit_manutencao_id']
