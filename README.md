⚙️ Como Executar o Projeto (Guia Passo a Passo)

Passo 1: Conferir a Estrutura de Pastas

Verifique se a sua pasta do projeto está organizada e se não há nenhuma inconsistência com a estrutura do projeto definida abaixo:

Plaintext

/CineTicket
 ├── requirements.txt
 ├── README.md
 │
 ├── /servicos
 │    ├── dashboard.html      
 │    ├── Dockerfile
 │    ├── docker-compose.yml
 │    ├── cineticket.sql
 │    │
 │    ├── /filmes
 │    │    ├── main.py                  <-- Inicialização e rotas
 │    │    ├── controllers_filmes.py    <-- Lógica HTTP
 │    │    └── database_filmes.py       <-- Consultas SQL isoladas
 │    │
 │    ├── /sessoes
 │    │    ├── main.py                  
 │    │    ├── controllers_sessoes.py   
 │    │    └── database_sessoes.py      
 │    │
 │    └── /ingressos
 │         ├── main.py                  
 │         ├── controllers_ingressos.py 
 │         └── database_ingressos.py    
 │
 └── /mcp
      ├── readme_env.txt          <-- Renomeie para .env e coloque sua GOOGLE_API_KEY
      ├── .env.example           <-- O molde original
      ├── Dockerfile
      ├── docker-compose.yml
      ├── chat_google.py         <-- Cliente de Chat via Terminal (CLI)
      ├── app_chat.py            <-- Interface Web do Assistente (Streamlit)
      │
      ├── /filmes
      │    └── main_filmes.py
      │    └── client_filmes.py
      ├── /sessoes
      │    └── main_sessoes.py
      │    └── client_sessoes.py
      ├── /ingressos
      │    └── main_ingressos.py
      │    └── client_ingressos.py

Passo 2: Preparar o ambiente Python no seu computador

Como o script do chat (chat_google.py) vai rodar diretamente no seu computador (e não dentro do Docker), você precisa instalar as bibliotecas do requirements.txt na sua máquina.   

  2.1.Abra o terminal (cmd, PowerShell ou terminal do VS Code) na pasta raiz /CineTicket.

  2.2 (Opcional, mas recomendado) Crie e ative um ambiente virtual para não bagunçar o seu Python:

    -Windows: "python -m venv venv" e depois "venv\Scripts\activate"
    -Mac/Linux: "python3 -m venv venv" e depois "source venv/bin/activate"

  2.3 Instale as bibliotecas: 

      pip install -r requirements.txt

      *To update, run: python.exe -m pip install --upgrade pip

Passo 3: Criar a rede do Docker

Os contêineres precisam de uma rede compartilhada para conversarem entre si. No terminal, rode o comando:   

    docker network create rede-cineticket

Passo 4: Subir os Serviços Web e o Banco de Dados

Agora vamos ligar o banco de dados e as APIs (o back-end).

  4.1 No terminal, entre na pasta de serviços:

        cd servicos

  4.2 Mande o Docker construir e subir tudo em segundo plano (-d):

        docker-compose up -d --build

  4.3 Aguarde um minuto. O Docker vai baixar o PostgreSQL, criar as tabelas do cineticket.sql e ligar os serviços de filmes, sessões e ingressos nas portas 7001, 7002 e 7003.

*Teste rápido: Dê dois cliques no arquivo dashboard.html para abri-lo no seu navegador. Se os gráficos e a tabela aparecerem preenchidos com os dados do cinema, sucesso! Seus serviços web e o banco estão funcionando perfeitamente.

Passo 5: Subir os Servidores MCP

Com os serviços web rodando, agora subimos as ferramentas da IA.

  5.1 No terminal, volte para a raiz e entre na pasta mcp:

        cd ../mcp

  5.2 Suba os contêineres MCP:

        docker-compose up -d --build

  5.3 O Docker vai ligar as ferramentas nas portas 8001, 8002 e 8003.

Passo 6: Iniciar o Chat com a IA

Com toda a infraestrutura rodando, agora é só ligar o cérebro (Gemini) para conversar com seus contêineres.

  6.1 Ainda no terminal, dentro da pasta mcp (e com o seu ambiente virtual ativado), execute o script:

        python chat_google.py

  6.2 O projeto possui duas formas de interação com a IA via MCP, via interface web amigável (executando streamlit run app_chat.py) ou via linha de comando tradicional (executando o script CLI correspondente). Para testar a interface gráfica moderna:

        streamlit run app_chat.py

6.2 O terminal vai mostrar mensagens avisando que conectou aos serviços "filmes", "sessoes" e "ingressos". Em seguida, o ícone 👤 aparecerá aguardando sua mensagem.   

    *Testes para fazer no Chat:
    -"Quais filmes estão em cartaz no cinema?" (A IA deve chamar o MCP de filmes).
    -"Quantos ingressos já foram vendidos e confirmados?" (A IA deve chamar o MCP de ingressos).
    -"Tem alguma sessão para o filme Tropa de Elite? Quantos assentos estão livres?" (A IA deve usar a ferramenta de filmes e depois a de sessões).

Passo 7: Para desligar o projeto quando terminar, basta rodar docker-compose down nas pastas /mcp e /servicos.

  7.1 Em /mcp: 
      
    docker-compose down

  7.2 Em /servicos: 
  
    docker-compose down



🔍 Inspeção e Depuração do Protocolo MCP (Opcional)

# iniciar uma rede compartilhada entre composicoes docker
docker network create rede-cineticket

# inspeciona rapidamente o serviço MCP
fastmcp inspect servicos/filmes/main.py
fastmcp inspect servicos/sessoes/main.py
fastmcp inspect servicos/ingressos/main.py

# executando o inspetor visual (web)
npx @modelcontextprotocol/inspector



## 🚀 Roadmap e Evolução Arquitetural (v2.0)

Este projeto foi construído sobre uma fundação sólida de microsserviços via Docker e consultas nativas para garantir performance. Para o ciclo de vida futuro da aplicação, as seguintes melhorias arquiteturais voltadas para ambientes de alta escalabilidade (Enterprise) estão mapeadas:

*   **Mapeamento Objeto-Relacional (ORM) com SQLAlchemy (Models):**
    Substituição das consultas SQL literais (raw SQL) por classes Python. Isso cria uma camada de abstração que facilita a manutenção do banco de dados, permite migrações automatizadas (Alembic) e evita falhas de segurança como SQL Injection de forma nativa.

*   **Validação Estrita de Dados com Pydantic (Schemas):**
    Implementação de *schemas* de validação para tipagem forte nas portas de entrada e saída da API. O Pydantic interceptará payloads HTTP, garantindo que os tipos de dados (strings, inteiros, booleanos) sejam estritamente respeitados antes que qualquer requisição atinja os controladores, eliminando estruturas complexas de `if/else` de validação manual.

*   **Implementação do Padrão Repository:**
    Desacoplamento total entre a lógica de roteamento (Flask) e a persistência de dados. Os controladores HTTP atuarão apenas como orquestradores de requisições, delegando toda a comunicação com o banco de dados para a camada de Repositórios, respeitando o princípio de Responsabilidade Única (SRP) do SOLID.
