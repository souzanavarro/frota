from sqlalchemy import Column, Integer, String, Date, Float, Boolean, ForeignKey, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
import datetime

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True, nullable=False)
    password_hash = Column(String, nullable=False)
    role = Column(String, default='user')
    transportador_id = Column(Integer, ForeignKey('transportadores.id'), nullable=True)

    transportador = relationship('Transportador')

class Veiculo(Base):
    __tablename__ = 'veiculos'
    id = Column(Integer, primary_key=True)
    placa = Column(String, unique=True, nullable=False)
    codigo = Column(String)
    motorista_id = Column(Integer, ForeignKey('motoristas.id'), nullable=True)
    tipo = Column(String)
    marca_modelo = Column(String)
    ano = Column(Integer)
    combustivel = Column(String)
    capacidade_carga = Column(Float)
    km_atual = Column(Float, default=0.0)
    status = Column(String, default='ativo')
    renavam = Column(String)
    vencimento_licenciamento = Column(Date)
    centro_custo = Column(String)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    abastecimentos = relationship('Abastecimento', back_populates='veiculo')
    manutencoes = relationship('Manutencao', back_populates='veiculo')
    motorista = relationship('Motorista')

class Motorista(Base):
    __tablename__ = 'motoristas'
    id = Column(Integer, primary_key=True)
    nome = Column(String, nullable=False)
    cpf = Column(String, unique=True)
    cnh = Column(String)
    categoria = Column(String)
    validade_cnh = Column(Date)
    contato = Column(String)
    status = Column(String, default='ativo')
    vinculo = Column(String)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    abastecimentos = relationship('Abastecimento', back_populates='motorista')
    viagens = relationship('Viagem', back_populates='motorista')

class Abastecimento(Base):
    __tablename__ = 'abastecimentos'
    id = Column(Integer, primary_key=True)
    data = Column(DateTime, default=datetime.datetime.utcnow)
    veiculo_id = Column(Integer, ForeignKey('veiculos.id'))
    motorista_id = Column(Integer, ForeignKey('motoristas.id'), nullable=True)
    posto = Column(String)
    tipo_combustivel = Column(String)
    litros = Column(Float)
    valor_total = Column(Float)
    valor_litro = Column(Float)
    km = Column(Float)
    tanque_cheio = Column(Boolean, default=False)

    veiculo = relationship('Veiculo', back_populates='abastecimentos')
    motorista = relationship('Motorista', back_populates='abastecimentos')

class Manutencao(Base):
    __tablename__ = 'manutencoes'
    id = Column(Integer, primary_key=True)
    veiculo_id = Column(Integer, ForeignKey('veiculos.id'))
    tipo = Column(String)  # preventiva / corretiva
    data = Column(DateTime, default=datetime.datetime.utcnow)
    km = Column(Float)
    oficina = Column(String)
    descricao = Column(String)
    pecas = Column(String)
    custo_pecas = Column(Float, default=0.0)
    custo_mao_obra = Column(Float, default=0.0)
    tempo_parado_horas = Column(Float, default=0.0)
    proxima_revisao_km = Column(Float, nullable=True)
    proxima_revisao_data = Column(Date)

    veiculo = relationship('Veiculo', back_populates='manutencoes')

# Tabela mínima de viagens para relacionamento (futuro)
class Viagem(Base):
    __tablename__ = 'viagens'
    id = Column(Integer, primary_key=True)
    veiculo_id = Column(Integer, ForeignKey('veiculos.id'))
    motorista_id = Column(Integer, ForeignKey('motoristas.id'))
    origem = Column(String)
    destino = Column(String)
    km_inicial = Column(Float)
    km_final = Column(Float)
    carga = Column(String)
    status = Column(String, default='programada')
    valor_frete = Column(Float, default=0.0)
    transportador_id = Column(Integer, ForeignKey('transportadores.id'), nullable=True)
    data_saida = Column(DateTime)
    data_chegada = Column(DateTime)

    motorista = relationship('Motorista', back_populates='viagens')
    transportador = relationship('Transportador')


class Transportador(Base):
    __tablename__ = 'transportadores'
    id = Column(Integer, primary_key=True)
    cnpj = Column(String, unique=True, nullable=False)
    nome_fantasia = Column(String)
    telefone_contato = Column(String)
    nome_pessoa_contato = Column(String)
    nome_empresa = Column(String)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
