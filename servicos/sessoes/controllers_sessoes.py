from flask import Blueprint, jsonify, make_response
from database_sessoes import pool

rotas_sessoes = Blueprint("sessoes", __name__)

@rotas_sessoes.get("/")
def get_info():
    return make_response(jsonify(descricao="Serviço de Sessões e Salas", versao="3.0 - Clean Arch"), 200)

@rotas_sessoes.get("/sessoes")
def get_sessoes():
    with pool.connection() as conexao:
        cursor = conexao.cursor()
        cursor.execute("SELECT * FROM cineticket.vw_resumo_sessoes")
        sessoes = jsonify(cursor.fetchall())
    return make_response(sessoes, 200)

@rotas_sessoes.get("/sessoes/id/<string:id_sessao>")
def get_sessoes_por_id(id_sessao):
    with pool.connection() as conexao:
        cursor = conexao.cursor()
        cursor.execute("SELECT * FROM cineticket.sessoes WHERE sessao_id = %s", (id_sessao,))
        sessao = jsonify(cursor.fetchall())
    return make_response(sessao, 200)

@rotas_sessoes.get("/sessoes/titulo_filme/<string:titulo>")
def get_sessoes_por_titulo(titulo):
    with pool.connection() as conexao:
        cursor = conexao.cursor()
        cursor.execute("""
            SELECT s.*, f.titulo 
            FROM cineticket.sessoes s
            JOIN cineticket.filmes f ON s.filme_id = f.filme_id
            WHERE lower(f.titulo) LIKE %s
        """, (f"%{titulo.lower()}%",))
        sessoes = jsonify(cursor.fetchall())
    return make_response(sessoes, 200)