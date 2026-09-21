from mcp.server.mcpserver import MCPServer
import urllib.parse
import json
from client_filmes import acessar_api

NOME = "filmes"
mcp = MCPServer(NOME)
URL_FILMES = "http://filmes:5000/filmes"

INFO = {
    "nome": NOME,
    "descricao": "Microsserviço MCP - Catálogo de Filmes do CineTicket",
    "versao": "3.0 - Clean Arch",
    "status": "operacional"
}

@mcp.tool(
    name="consultar_saude_filmes", 
    title="Health Check do Serviço de Filmes", 
    description="Verifica se o microsserviço de catálogo está online."
)
def get_info() -> str:
    return json.dumps(INFO)

@mcp.tool(
    name="listar_todos_filmes", 
    title="Listar catálogo completo de filmes", 
    description="Retorna a lista completa de todos os filmes que estão em cartaz."
)
def get_filmes() -> str:
    sucesso, conteudo, erro = acessar_api(URL_FILMES)
    return conteudo if sucesso else f"Falha no microsserviço: {erro}"

@mcp.tool(
    name="filtrar_filmes_por_genero", 
    title="Buscar filmes por gênero", 
    description="Busca filmes filtrando por gêneros como 'Ação', 'Terror', 'Comédia', etc."
)
def get_filmes_por_genero(genero: str) -> str:
    genero_url = urllib.parse.quote(genero)
    sucesso, conteudo, erro = acessar_api(f"{URL_FILMES}/genero/{genero_url}")
    return conteudo if sucesso else f"Falha no microsserviço: {erro}"

@mcp.tool(
    name="filtrar_filmes_por_classificacao", 
    title="Buscar filmes por classificação", 
    description="Busca filmes filtrando pela idade indicativa (ex: 'Livre', '12 Anos', '16 Anos')."
)
def get_filmes_por_classificacao(classificacao: str) -> str:
    classificacao_url = urllib.parse.quote(classificacao)
    sucesso, conteudo, erro = acessar_api(f"{URL_FILMES}/classificacao/{classificacao_url}")
    return conteudo if sucesso else f"Falha no microsserviço: {erro}"

if __name__ == "__main__":
    mcp.run(transport="streamable-http", host="0.0.0.0", streamable_http_path="/mcp")