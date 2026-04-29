import streamlit as st
from config.database import SessionLocal
from models import Viagem
import models
from repositories.veiculo_repository import listar_veiculos
from repositories.motorista_repository import listar_motoristas
from repositories.viagem_repository import listar_viagens, buscar_por_id, atualizar_viagem
import pandas as pd
import datetime
from components.ui import cp_hero, cp_card, cp_card_end, cp_card_back, cp_card_back_end, cp_data_panel_start, cp_data_panel_end


def render():
    cp_hero('Viagens', 'Acompanhe e edite viagens', icon='🗺️')
    db = SessionLocal()
    with st.expander('Abrir viagem'):
        cp_card()
        with st.form('form_v'):
            # carregar opções de veículos e motoristas
            veiculos = listar_veiculos()
            motoristas = listar_motoristas()
            veiculo_options = [f"{v.id} - {v.placa}" for v in veiculos]
            motorista_options = [f"{m.id} - {m.nome}" for m in motoristas]

            veiculo_sel = st.selectbox('Veículo', ['--- Selecionar ---'] + veiculo_options)
            motorista_sel = st.selectbox('Motorista', ['--- Selecionar ---'] + motorista_options)
            origem = st.text_input('Origem')
            destino = st.text_input('Destino')
            km_inicial = st.number_input('KM inicial', value=0.0)
            valor_frete = st.number_input('Valor do frete', value=0.0)
            if st.form_submit_button('Abrir viagem'):
                transportador_id = None
                if 'user' in st.session_state and st.session_state.user:
                    cu = db.query(models.User).filter(models.User.username == st.session_state.user).first()
                    transportador_id = getattr(cu, 'transportador_id', None)

                veiculo_id = None
                motorista_id = None
                if veiculo_sel and veiculo_sel != '--- Selecionar ---':
                    veiculo_id = int(veiculo_sel.split(' - ')[0])
                if motorista_sel and motorista_sel != '--- Selecionar ---':
                    motorista_id = int(motorista_sel.split(' - ')[0])

                v = Viagem(veiculo_id=veiculo_id, motorista_id=motorista_id, origem=origem, destino=destino, km_inicial=km_inicial, status='em andamento', data_saida=datetime.datetime.utcnow(), valor_frete=valor_frete, transportador_id=transportador_id)
                db.add(v)
                db.commit()
                st.success('Viagem aberta')
            cp_card_end()
    rows = db.query(Viagem).order_by(Viagem.data_saida.desc()).limit(500).all()
    # aplicar filtro: se transportador, mostrar apenas viagens do transportador
    if 'user' in st.session_state and st.session_state.user:
        current = db.query(models.User).filter(models.User.username == st.session_state.user).first()
    else:
        current = None
    if current and current.role == 'transportador' and current.transportador_id:
        rows = [r for r in rows if r.transportador_id == current.transportador_id]

    # filtros: período e busca por placa/motorista
    veiculos_map = {v.id: v.placa for v in listar_veiculos()}
    motoristas_map = {m.id: m.nome for m in listar_motoristas()}

    st.subheader('Filtrar viagens')
    fcol1, fcol2, fcol3 = st.columns([1,1,2])
    start = fcol1.date_input('Data início', value=(datetime.date.today() - datetime.timedelta(days=30)))
    end = fcol2.date_input('Data fim', value=datetime.date.today())
    search = fcol3.text_input('Buscar placa ou motorista')

    def matches_search(r):
        if not search:
            return True
        s = search.lower()
        placa = veiculos_map.get(r.veiculo_id, '') or ''
        motorista = motoristas_map.get(r.motorista_id, '') or ''
        return s in str(placa).lower() or s in str(motorista).lower()

    filtered = []
    for r in rows:
        # filtrar por transportador (já aplicado acima)
        if r.data_saida:
            d = r.data_saida.date()
            if d < start or d > end:
                continue
        if not matches_search(r):
            continue
        filtered.append(r)

    st.subheader('Viagens')
    # Background card with data panel overlay
    cp_card_back()
    # close the background card before starting the data panel
    cp_card_back_end()
    cp_data_panel_start()
    for r in filtered:
        cols = st.columns([1,2,2,2,1,1,1])
        if cols[0].button(str(r.id), key=f"edit_viagem_{r.id}"):
            st.session_state['edit_viagem_id'] = r.id
        cols[1].write(veiculos_map.get(r.veiculo_id, r.veiculo_id))
        cols[2].write(motoristas_map.get(r.motorista_id, getattr(r, 'motorista', None) and getattr(r.motorista, 'nome', r.motorista_id)))
        cols[3].write(f"{r.origem or ''} → {r.destino or ''}")
        cols[4].write(r.status)
        cols[5].write(getattr(r, 'valor_frete', ''))
        cols[6].write(r.data_saida)
    cp_data_panel_end()
    cp_card_back_end()

    # mostrar formulário de edição quando id clicado
    if 'edit_viagem_id' in st.session_state and st.session_state.edit_viagem_id:
        vid = st.session_state.edit_viagem_id
        vobj = buscar_por_id(vid)
        if vobj:
            st.markdown('---')
            st.subheader(f'Editar viagem #{vid}')
            cp_card()
            with st.form('edit_viagem_form'):
                veiculos = listar_veiculos()
                motoristas = listar_motoristas()
                veiculo_id = st.selectbox('Veículo', [vv.id for vv in veiculos], index=next((i for i,vv in enumerate(veiculos) if vv.id==vobj.veiculo_id), 0), format_func=lambda x: next((vv.placa for vv in veiculos if vv.id==x), ''))
                motorista_id = st.selectbox('Motorista', [m.id for m in motoristas], index=next((i for i,m in enumerate(motoristas) if m.id==vobj.motorista_id), 0), format_func=lambda x: next((mm.nome for mm in motoristas if mm.id==x), ''))
                origem = st.text_input('Origem', value=vobj.origem or '')
                destino = st.text_input('Destino', value=vobj.destino or '')
                km_inicial = st.number_input('KM inicial', value=vobj.km_inicial or 0.0)
                valor_frete = st.number_input('Valor do frete', value=getattr(vobj, 'valor_frete', 0.0))
                if st.form_submit_button('Salvar alterações'):
                    payload = {
                        'veiculo_id': veiculo_id,
                        'motorista_id': motorista_id,
                        'origem': origem,
                        'destino': destino,
                        'km_inicial': km_inicial,
                        'valor_frete': valor_frete
                    }
                    atualizar_viagem(vid, payload)
                    st.success('Viagem atualizada')
                    del st.session_state['edit_viagem_id']
            cp_card_end()
    
    st.markdown('---')
    st.subheader('Editar viagem')
    viagens = listar_viagens(100)
    options = ['--- Selecionar ---'] + [f"{v.id} - {veiculos_map.get(v.veiculo_id, v.veiculo_id)}" for v in viagens]
    sel = st.selectbox('Viagem', options)
    if sel and sel != '--- Selecionar ---':
        vid = int(sel.split(' - ')[0])
        vobj = buscar_por_id(vid)
        if vobj:
            cp_card()
            with st.form('edit_viagem'):
                veiculos = listar_veiculos()
                motoristas = listar_motoristas()
                veiculo_id = st.selectbox('Veículo', [vv.id for vv in veiculos], index=next((i for i,vv in enumerate(veiculos) if vv.id==vobj.veiculo_id), 0), format_func=lambda x: next((vv.placa for vv in veiculos if vv.id==x), ''))
                motorista_id = st.selectbox('Motorista', [m.id for m in motoristas], index=next((i for i,m in enumerate(motoristas) if m.id==vobj.motorista_id), 0), format_func=lambda x: next((mm.nome for mm in motoristas if mm.id==x), ''))
                origem = st.text_input('Origem', value=vobj.origem or '')
                destino = st.text_input('Destino', value=vobj.destino or '')
                km_inicial = st.number_input('KM inicial', value=vobj.km_inicial or 0.0)
                valor_frete = st.number_input('Valor do frete', value=getattr(vobj, 'valor_frete', 0.0))
                if st.form_submit_button('Atualizar viagem'):
                    payload = {
                        'veiculo_id': veiculo_id,
                        'motorista_id': motorista_id,
                        'origem': origem,
                        'destino': destino,
                        'km_inicial': km_inicial,
                        'valor_frete': valor_frete
                    }
                    atualizar_viagem(vid, payload)
                    st.success('Viagem atualizada')
            cp_card_end()
    db.close()
