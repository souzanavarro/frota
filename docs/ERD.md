# ERD - Modelo Simplificado

Tabelas principais:

- veiculos
  - id (PK)
  - placa
  - codigo
  - tipo
  - marca_modelo
  - ano
  - combustivel
  - capacidade_carga
  - km_atual
  - status
  - renavam
  - vencimento_licenciamento
  - centro_custo

- motoristas
  - id (PK)
  - nome
  - cpf
  - cnh
  - categoria
  - validade_cnh
  - contato
  - status

- abastecimentos
  - id (PK)
  - data
  - veiculo_id (FK -> veiculos.id)
  - motorista_id (FK -> motoristas.id)
  - posto
  - tipo_combustivel
  - litros
  - valor_total
  - valor_litro
  - km
  - tanque_cheio

- manutencoes
  - id (PK)
  - veiculo_id (FK -> veiculos.id)
  - tipo
  - data
  - km
  - oficina
  - descricao
  - pecas
  - custo_pecas
  - custo_mao_obra
  - tempo_parado_horas
  - proxima_revisao_km
  - proxima_revisao_data

- users
  - id (PK)
  - username
  - password_hash
  - role

Relacionamentos principais:
- veiculos 1:N abastecimentos
- veiculos 1:N manutencoes
- motoristas 1:N abastecimentos

Observações:
- Schema completo está em `database/schema.sql`.
- Este ERD é um ponto de partida para documentação e futuras migrações.
