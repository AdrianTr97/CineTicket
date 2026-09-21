# iniciar uma rede compartilhada entre composicoes docker
docker network create rede-cineticket

# inspeciona rapidamente o serviço MCP
fastmcp inspect [servico_ingresso].py
fastmcp inspect [servico_sessao].py
fastmcp inspect [servico_filme].py

# executando o inspetor visual (web)
npx @modelcontextprotocol/inspector