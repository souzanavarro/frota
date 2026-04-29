from config.database import SessionLocal
from models import Abastecimento, Manutencao


def custo_por_km(veiculo_id, periodo_inicio=None, periodo_fim=None):
    db = SessionLocal()
    try:
        q_ab = db.query(Abastecimento).filter(Abastecimento.veiculo_id==veiculo_id)
        q_m = db.query(Manutencao).filter(Manutencao.veiculo_id==veiculo_id)
        if periodo_inicio:
            q_ab = q_ab.filter(Abastecimento.data >= periodo_inicio)
            q_m = q_m.filter(Manutencao.data >= periodo_inicio)
        if periodo_fim:
            q_ab = q_ab.filter(Abastecimento.data <= periodo_fim)
            q_m = q_m.filter(Manutencao.data <= periodo_fim)
        abastecimentos = q_ab.all()
        manutencoes = q_m.all()
        custo_combustivel = sum((a.valor_total or 0) for a in abastecimentos)
        custo_manutencao = sum(((m.custo_pecas or 0) + (m.custo_mao_obra or 0)) for m in manutencoes)
        custo_total = custo_combustivel + custo_manutencao
        # estimar km percorrido: usar diferença entre máximo e mínimo km em abastecimentos no período
        kms = [a.km for a in abastecimentos if a.km]
        km_perc = 0
        if len(kms) >= 2:
            km_perc = max(kms) - min(kms)
        # evitar divisão por zero
        custo_km = (custo_total / km_perc) if km_perc > 0 else None
        return {'custo_total': custo_total, 'km_percorrido': km_perc, 'custo_por_km': custo_km}
    finally:
        db.close()
