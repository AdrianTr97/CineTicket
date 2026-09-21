#Gerencia exclusivamente as rotas e a lógica de negócio
from flask import Blueprint, jsonify, make_response
from database_filmes import pool

rotas_filmes = Blueprint("filmes", __name__)

@rotas_filmes.get("/")
def get_info():
    return make_response(jsonify(descricao="Serviço de Catálogo de Filmes", versao="3.0 - Clean Arch"), 200)

@rotas_filmes.get("/filmes")
def get_filmes():
    with pool.connection() as conexao:
        cursor = conexao.cursor()
        cursor.execute("SELECT * FROM cineticket.filmes WHERE ativo = TRUE")
        filmes = jsonify(cursor.fetchall())
    return make_response(filmes, 200)

@rotas_filmes.get("/filmes/genero/<string:genero>")
def get_filmes_por_genero(genero):
    with pool.connection() as conexao:
        cursor = conexao.cursor()
        cursor.execute("""
            SELECT f.titulo, f.sinopse, g.nome AS genero 
            FROM cineticket.filmes f JOIN cineticket.generos g ON g.genero_id = f.genero_id
            WHERE lower(g.nome) = %s AND f.ativo = TRUE
        """, (genero.lower(),))
        filmes = jsonify(cursor.fetchall())
    return make_response(filmes, 200)

@rotas_filmes.get("/filmes/classificacao/<string:classificacao>")
def get_filmes_por_classificacao(classificacao):
    with pool.connection() as conexao:
        cursor = conexao.cursor()
        cursor.execute("""
            SELECT f.titulo, f.classificacao, f.duracao_minutos
            FROM cineticket.filmes f
            WHERE lower(f.classificacao) = %s AND f.ativo = TRUE
        """, (classificacao.lower(),))
        filmes = jsonify(cursor.fetchall())
    return make_response(filmes, 200)