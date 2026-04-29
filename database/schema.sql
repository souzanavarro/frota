-- Schema inicial para MVP

CREATE TABLE IF NOT EXISTS veiculos (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  placa TEXT UNIQUE NOT NULL,
  codigo TEXT,
  tipo TEXT,
  marca_modelo TEXT,
  ano INTEGER,
  combustivel TEXT,
  capacidade_carga REAL,
  km_atual REAL DEFAULT 0,
  status TEXT DEFAULT 'ativo',
  renavam TEXT,
  vencimento_licenciamento DATE,
  centro_custo TEXT,
  created_at DATETIME
);

CREATE TABLE IF NOT EXISTS motoristas (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  nome TEXT NOT NULL,
  cpf TEXT UNIQUE,
  cnh TEXT,
  categoria TEXT,
  validade_cnh DATE,
  contato TEXT,
  status TEXT DEFAULT 'ativo',
  vinculo TEXT,
  created_at DATETIME
);

CREATE TABLE IF NOT EXISTS abastecimentos (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  data DATETIME,
  veiculo_id INTEGER,
  motorista_id INTEGER,
  posto TEXT,
  tipo_combustivel TEXT,
  litros REAL,
  valor_total REAL,
  valor_litro REAL,
  km REAL,
  tanque_cheio BOOLEAN,
  FOREIGN KEY(veiculo_id) REFERENCES veiculos(id),
  FOREIGN KEY(motorista_id) REFERENCES motoristas(id)
);

CREATE TABLE IF NOT EXISTS manutencoes (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  veiculo_id INTEGER,
  tipo TEXT,
  data DATETIME,
  km REAL,
  oficina TEXT,
  descricao TEXT,
  pecas TEXT,
  custo_pecas REAL DEFAULT 0,
  custo_mao_obra REAL DEFAULT 0,
  tempo_parado_horas REAL DEFAULT 0,
  proxima_revisao_km REAL,
  proxima_revisao_data DATE,
  FOREIGN KEY(veiculo_id) REFERENCES veiculos(id)
);

CREATE TABLE IF NOT EXISTS users (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  username TEXT UNIQUE NOT NULL,
  password_hash TEXT NOT NULL,
  role TEXT
);
