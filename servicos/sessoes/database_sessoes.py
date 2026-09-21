import os
from psycopg_pool import ConnectionPool
from psycopg.rows import dict_row as dicionario

# Busca as variáveis injetadas pelo Docker (ou usa um valor padrão se falhar)
HOST = os.environ.get("DB_HOST", "dados")
PORT = os.environ.get("DB_PORT", "5432")
USER = os.environ.get("DB_USER", "admin")
PASS = os.environ.get("DB_PASS", "admin")
NAME = os.environ.get("DB_NAME", "cineticket")

# Monta a string de conexão dinamicamente
STRING_CONEXAO = f"host={HOST} port={PORT} user={USER} password={PASS} dbname={NAME}"

pool = ConnectionPool(
    conninfo=STRING_CONEXAO,
    min_size=2,
    max_size=10,
    kwargs={"row_factory": dicionario}
)