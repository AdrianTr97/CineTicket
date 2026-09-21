from flask import Blueprint, jsonify, make_response, request
import httpx
from database_ingressos import pool

rotas_ingressos = Blueprint("ingressos", __name__)

@rotas_ingressos.get("/")
def get_info():
    return make_response(jsonify(descricao="Serviço de Bilheteria", versao="3.0 - Clean Arch"), 200)

@rotas_ingressos.get("/ingressos")
def get_todos_ingressos():
    with pool.connection() as conexao:
        cursor = conexao.cursor()
        cursor.execute("SELECT * FROM cineticket.vw_detalhes_ingressos")
        ingressos = jsonify(cursor.fetchall())
    return make_response(ingressos, 200)

@rotas_ingressos.get("/ingressos/status/<string:status>")
def get_ingressos_por_status(status):
    with pool.connection() as conexao:
        cursor = conexao.cursor()
        cursor.execute("SELECT * FROM cineticket.ingressos WHERE status_ingresso = %s", (status.upper(),))
        ingressos = jsonify(cursor.fetchall())
    return make_response(ingressos, 200)

@rotas_ingressos.get("/ingressos/quantidade/<string:status>")
def get_quantidade(status):
    with pool.connection() as conexao:
        cursor = conexao.cursor()
        cursor.execute("SELECT count(*) as total FROM cineticket.ingressos WHERE status_ingresso = %s", (status.upper(),))
        resultado = jsonify(cursor.fetchone())
    return make_response(resultado, 200)

@rotas_ingressos.post("/ingressos/comprar")
def comprar_ingresso():
    dados_compra = request.json
    id_sessao = dados_compra.get("sessao_id")
    
    try:
        resposta = httpx.get(f"http://sessoes:5000/sessoes/id/{id_sessao}", timeout=5.0)
        
        if resposta.status_code != 200:
            return make_response(jsonify(erro="Sessão não encontrada no microsserviço de Sessões."), 404)
            
        sessao_info = resposta.json()
        if len(sessao_info) == 0 or sessao_info[0].get('assentos_livres', 0) <= 0:
            return make_response(jsonify(erro="Ação bloqueada: A sessão está lotada!"), 400)
            
    except Exception as e:
        return make_response(jsonify(erro=f"Falha de comunicação com o serviço de sessões: {e}"), 500)

    with pool.connection() as conexao:
        cursor = conexao.cursor()
        cursor.execute("""
            INSERT INTO cineticket.ingressos (sessao_id, comprador, status_ingresso, preco_pago)
            VALUES (%s, %s, 'CONFIRMADO', %s) RETURNING ingresso_id
        """, (id_sessao, dados_compra.get("comprador"), dados_compra.get("preco")))
        
        novo_id = cursor.fetchone()
        conexao.commit()
    
    return make_response(jsonify(mensagem="Ingresso comprado com sucesso!", id=novo_id['ingresso_id']), 201)