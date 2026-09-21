from mcp.server.mcpserver import MCPServer
import urllib.parse
import json
from client_sessoes import acessar_api

NOME = "sessoes"
mcp = MCPServer(NOME)
URL_SESSOES = "http://sessoes:5000/sessoes"

INFO = {
    "nome": NOME,
    "descricao": "Microsserviço MCP - Gestão de Sessões e Salas do CineTicket",
    "versao": "3.0 - Clean Arch",
    "status": "operacional"
}

@mcp.tool(
    name="consultar_saude_sessoes", 
    title="Health Check do Serviço de Sessões", 
    description="Verifica se o microsserviço de gerenciamento de sessões está online."
)
def get_info() -> str:
    return json.dumps(INFO)

@mcp.tool(
    name="listar_todas_sessoes", 
    title="Listar grade completa de sessões", 
    description="Retorna a grade completa de todas as sessões agendadas no cinema."
)
def get_sessoes() -> str:
    sucesso, conteudo, erro = acessar_api(URL_SESSOES)
    return conteudo if sucesso else f"Falha no microsserviço: {erro}"

@mcp.tool(
    name="buscar_sessao_por_id", 
    title="Buscar detalhes exatos de uma sessão", 
    description="Busca os dados de uma sessão específica pelo seu número de ID único."
)
def get_sessoes_por_id(id_sessao: str) -> str:
    sucesso, conteudo, erro = acessar_api(f"{URL_SESSOES}/id/{id_sessao}")
    return conteudo if sucesso else f"Falha no microsserviço: {erro}"

@mcp.tool(
    name="buscar_sessoes_por_filme", 
    title="Filtrar sessões pelo nome do filme", 
    description="Retorna todos os horários e assentos disponíveis para um filme específico."
)
def get_sessoes_por_titulo(titulo: str) -> str:
    titulo_url = urllib.parse.quote(titulo)
    sucesso, conteudo, erro = acessar_api(f"{URL_SESSOES}/titulo_filme/{titulo_url}")
    return conteudo if sucesso else f"Falha no microsserviço: {erro}"

if __name__ == "__main__":
    mcp.run(transport="streamable-http", host="0.0.0.0", streamable_http_path="/mcp")