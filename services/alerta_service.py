from config.database import SessionLocal
from models import Abastecimento, Manutencao, Veiculo
from datetime import datetime, timedelta
import statistics


def consumo_medio_historico(veiculo_id, n=5):
    db = SessionLocal()
    try:
        rows = db.query(Abastecimento).filter(Abastecimento.veiculo_id==veiculo_id).order_by(Abastecimento.data.desc()).limit(n).all()
        # calcular km/l para cada par consecutivo onde tanque_cheio=True
        kms_per_l = []
        for r in rows:
            if r.litros and r.km:
                # aproximamos km/l usando litros; nota: idealmente precisamos do km entre abastecimentos
                kms_per_l.append(None)  # indicador insuficiente de dados
        # se não houver boa amostra, retornar None
        return None
    finally:
        db.close()


def detectar_anomalia_consumo(veiculo_id, percentual_queda=20):
    # estratégia simples: comparar média dos últimos 3 abastecimentos (R$/km) com média anterior
    db = SessionLocal()
    try:
        rows = db.query(Abastecimento).filter(Abastecimento.veiculo_id==veiculo_id).order_by(Abastecimento.data.desc()).limit(6).all()
        if len(rows) < 4:
            return False, 'Dados insuficientes'
        # dividir em últimos 3 e anteriores 3
        grupo1 = rows[0:3]
        grupo2 = rows[3:6]
        def media_km_por_l(gr):
            vals = []
            for r in gr:
                if r.litros and r.km:
                    vals.append(r.km / r.litros if r.litros>0 else 0)
            return statistics.mean(vals) if vals else None
        m1 = media_km_por_l(grupo1)
        m2 = media_km_por_l(grupo2)
        if m1 is None or m2 is None:
            return False, 'Dados insuficientes'
        # queda percentual
        queda = (m2 - m1) / m2 * 100 if m2 != 0 else 0
        if queda >= percentual_queda:
            return True, f'Queda de consumo detectada: {queda:.1f}% (média anterior {m2:.2f} km/l, atual {m1:.2f} km/l)'
        return False, f'Normal ({queda:.1f}% de variação)'
    finally:
        db.close()


def manutencao_preventiva_alerts():
    db = SessionLocal()
    try:
        alerts = []
        hoje = datetime.utcnow().date()
        muns = db.query(Manutencao).filter((Manutencao.proxima_revisao_km!=None) | (Manutencao.proxima_revisao_data!=None)).all()
        for m in muns:
            v = db.query(Veiculo).filter(Veiculo.id==m.veiculo_id).first()
            if not v:
                continue
            due_km = False
            due_date = False
            if m.proxima_revisao_km and v.km_atual and v.km_atual >= m.proxima_revisao_km:
                due_km = True
            if m.proxima_revisao_data and hoje >= m.proxima_revisao_data:
                due_date = True
            if due_km or due_date:
                alerts.append({'veiculo': v.placa, 'veiculo_id': v.id, 'due_km': due_km, 'due_date': due_date})
        return alerts
    finally:
        db.close()
