from mcp.server.mcpserver import MCPServer
import json
from client_ingressos import acessar_api

NOME = "ingressos"
mcp = MCPServer(NOME)
URL_INGRESSOS = "http://ingressos:5000/ingressos"

INFO = {
    "nome": NOME,
    "descricao": "Microsserviço MCP - Controle de Bilheteria e Ingressos do CineTicket",
    "versao": "3.0 - Clean Arch",
    "status": "operacional"
}

@mcp.tool(
    name="consultar_saude_bilheteria", 
    title="Health Check do Serviço de Ingressos", 
    description="Verifica se o microsserviço de bilheteria está online."
)
def get_info() -> str:
    return json.dumps(INFO)

@mcp.tool(
    name="relatorio_todos_ingressos", 
    title="Listar todos os ingressos emitidos", 
    description="Retorna o histórico completo de ingressos gerados."
)
def get_ingressos() -> str:
    sucesso, conteudo, erro = acessar_api(URL_INGRESSOS)
    return conteudo if sucesso else f"Falha no microsserviço: {erro}"

@mcp.tool(
    name="filtrar_ingressos_por_status", 
    title="Listar ingressos detalhados por situação", 
    description="Retorna a lista detalhada de ingressos filtrada pelo status ('CONFIRMADO', 'UTILIZADO', 'CANCELADO')."
)
def get_ingressos_por_status(status: str) -> str:
    sucesso, conteudo, erro = acessar_api(f"{URL_INGRESSOS}/status/{status}")
    return conteudo if sucesso else f"Falha no microsserviço: {erro}"

@mcp.tool(
    name="estatistica_quantidade_por_status", 
    title="Métrica quantitativa de ingressos", 
    description="Retorna APENAS O NÚMERO TOTAL de ingressos em um determinado status."
)
def get_quantidade_ingressos_por_status(status: str) -> str:
    sucesso, conteudo, erro = acessar_api(f"{URL_INGRESSOS}/quantidade/{status}")
    return conteudo if sucesso else f"Falha no microsserviço: {erro}"

if __name__ == "__main__":
    mcp.run(transport="streamable-http", host="0.0.0.0", streamable_http_path="/mcp")