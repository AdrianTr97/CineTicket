# iniciar uma rede compartilhada entre composicoes docker
docker network create rede-cineticket

# inspeciona rapidamente o serviço MCP
fastmcp inspect servicos/filmes/main.py
fastmcp inspect servicos/sessoes/main.py
fastmcp inspect servicos/ingressos/main.py

# executando o inspetor visual (web)
npx @modelcontextprotocol/inspector
