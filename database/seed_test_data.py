from config.database import init_db, SessionLocal
import models
from utils.auth import hash_password
import datetime


def seed_test_data():
    init_db(models.Base)
    db = SessionLocal()
    try:
        # transportador
        cnpj = '00000000000100'
        transportador = db.query(models.Transportador).filter(models.Transportador.cnpj == cnpj).first()
        if not transportador:
            transportador = models.Transportador(cnpj=cnpj, nome_fantasia='Transportadora Teste', telefone_contato='(00)0000-0000', nome_pessoa_contato='Contato Teste', nome_empresa='Empresa Teste', created_at=datetime.datetime.utcnow())
            db.add(transportador)
            db.commit()
            db.refresh(transportador)
            print(f'Criado transportador id={transportador.id}')
        else:
            print(f'Transportador já existe id={transportador.id}')

        # usuário vinculado ao transportador
        username = 'transp_test'
        user = db.query(models.User).filter(models.User.username == username).first()
        if not user:
            user = models.User(username=username, password_hash=hash_password('password'), role='transportador', transportador_id=transportador.id)
            db.add(user)
            db.commit()
            print(f'Criado user {username}')
        else:
            print(f'User {username} já existe')

        # motorista
        cpf = '00000000000'
        motorista = db.query(models.Motorista).filter(models.Motorista.cpf == cpf).first()
        if not motorista:
            motorista = models.Motorista(nome='Motorista Teste', cpf=cpf, cnh='123456', categoria='B', validade_cnh=datetime.date(2030,1,1), contato='(00)90000-0000')
            db.add(motorista)
            db.commit()
            db.refresh(motorista)
            print(f'Criado motorista id={motorista.id}')
        else:
            print(f'Motorista já existe id={motorista.id}')

        # veículo
        placa = 'TEST-0001'
        veiculo = db.query(models.Veiculo).filter(models.Veiculo.placa == placa).first()
        if not veiculo:
            veiculo = models.Veiculo(placa=placa, codigo='T001', tipo='Truck', marca_modelo='Marca Teste', ano=2020, combustivel='diesel', motorista_id=motorista.id)
            db.add(veiculo)
            db.commit()
            db.refresh(veiculo)
            print(f'Criado veiculo id={veiculo.id}')
        else:
            print(f'Veículo já existe id={veiculo.id}')

        # manutenção
        manut = db.query(models.Manutencao).filter(models.Manutencao.veiculo_id == veiculo.id).first()
        if not manut:
            manut = models.Manutencao(veiculo_id=veiculo.id, tipo='preventiva', km=1000.0, oficina='Oficina Teste', descricao='Revisão inicial', custo_pecas=100.0, custo_mao_obra=50.0, data=datetime.datetime.utcnow())
            db.add(manut)
            db.commit()
            db.refresh(manut)
            print(f'Criado manutencao id={manut.id}')
        else:
            print(f'Manutencao já existe id={manut.id}')

        # viagem
        viagem = db.query(models.Viagem).filter(models.Viagem.veiculo_id == veiculo.id).first()
        if not viagem:
            viagem = models.Viagem(veiculo_id=veiculo.id, motorista_id=motorista.id, origem='Origem Teste', destino='Destino Teste', km_inicial=100.0, km_final=None, carga='Carga Teste', status='programada', valor_frete=500.0, transportador_id=transportador.id, data_saida=datetime.datetime.utcnow())
            db.add(viagem)
            db.commit()
            db.refresh(viagem)
            print(f'Criado viagem id={viagem.id}')
        else:
            print(f'Viagem já existe id={viagem.id}')

    finally:
        db.close()


if __name__ == '__main__':
    seed_test_data()
