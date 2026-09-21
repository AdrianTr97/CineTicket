import streamlit as st
import os
import httpx
from dotenv import load_dotenv
from google import genai
from google.genai import types

# 1. Carrega as variáveis do .env (mesmo arquivo que o chat_google.py usa)
load_dotenv()

# 2. Configuração da página Streamlit
st.set_page_config(page_title="CineTicket AI", page_icon="🎬", layout="centered")
st.title("🎬 CineTicket AI")
st.markdown("Assistente inteligente integrado aos microsserviços via chamadas diretas.")

# 3. Funções Síncronas (Bypassa o erro do asyncio do MCP, mas faz o mesmo trabalho)
def consultar_filmes() -> str:
    """Use esta ferramenta para consultar o catálogo de filmes em cartaz, sinopses e durações."""
    try:
        return httpx.get("http://localhost:7001/filmes", timeout=5.0).text
    except Exception as e:
        return f"Erro de conexão: {e}"

def consultar_sessoes() -> str:
    """Use esta ferramenta para consultar os horários, salas e assentos livres das sessões."""
    try:
        return httpx.get("http://localhost:7002/sessoes", timeout=5.0).text
    except Exception as e:
        return f"Erro de conexão: {e}"

def consultar_ingressos() -> str:
    """Use esta ferramenta para consultar a situação dos ingressos vendidos, status e faturamento."""
    try:
        return httpx.get("http://localhost:7003/ingressos", timeout=5.0).text
    except Exception as e:
        return f"Erro de conexão: {e}"

# 4. Inicializa a IA na memória do Streamlit
if "messages" not in st.session_state:
    st.session_state.messages = []
    
    # Usa a chave que sabemos que está funcionando no seu .env
    API_KEY = os.environ.get("GOOGLE_API_KEY")
    client = genai.Client(api_key=API_KEY)

    PROMPT_SISTEMA = """Você é um assistente virtual de bilheteria de uma rede de cinemas chamada CineTicket. O seu nome é CineTicketBot.

    Quando o usuário fizer uma saudação ou iniciar uma conversa contigo, você deve se identificar pelo seu nome e informar que você não é uma pessoa real, mas é um assistente virtual de atendimento do cinema.

    Quando o usuário solicitar informações sobre filmes em cartaz, horários e vagas nas sessões, ou situação de ingressos vendidos, você deve utilizar as ferramentas disponíveis para obter tais informações. Também é necessário que você identique quando mais de uma ferramenta é necessária (por exemplo, buscar a sinopse de um filme e depois ver as sessões dele). Você deve obedecer estas regras:

    - se o usuário perguntar sobre o catálogo, sinopses, duração ou gêneros de filmes, você deve utilizar as ferramentas de filmes;
     - se o usuário perguntar sobre os horários, salas, poltronas livres ou sessões disponíveis, você deve utilizar as ferramentas de sessoes;
    - se o usuário perguntar sobre as compras de ingressos, bilhetes vendidos, métodos de pagamento ou status da compra (confirmado/cancelado), você deve utilizar as ferramentas de ingressos.
    - se o usuário fizer uma pergunta que não esteja relacionada a filmes, sessões e ingressos de cinema, você deve dizer que não está capacitado para responder e deve falar para o usuário entrar em contato com os gerentes do cinema.
    """,
    
    # Cria a sessão de chat automática com a nova SDK do Google
    st.session_state.chat_session = client.chats.create(
        #model="gemini-2.0-flash", # Ou o modelo exato que esta usando
        #model="gemini-3.6-flash",
        model="gemini-3.5-flash-lite",
        config=types.GenerateContentConfig(
            #system_instruction="""Você é o CineTicketBot, assistente do cinema CineTicket.Sempre use as ferramentas disponíveis para consultar filmes, sessões e ingressos.Seja cordial, direto e se apresente no primeiro contato.""",
            system_instruction=PROMPT_SISTEMA,
            tools=[consultar_filmes, consultar_sessoes, consultar_ingressos],
            temperature=0.5,
        )
    )

# 5. Renderiza mensagens antigas no chat web
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 6. Caixa de texto para o usuário
if prompt := st.chat_input("Ex: Quais filmes estão em cartaz hoje?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Consultando microsserviços..."):
            try:
                # O Google Gemini analisa a pergunta, chama a ferramenta correta e devolve a resposta!
                response = st.session_state.chat_session.send_message(prompt)
                bot_response = response.text
            except Exception as e:
                bot_response = f"Desculpe, ocorreu um erro interno: {str(e)}"
            
            st.markdown(bot_response)
            
    st.session_state.messages.append({"role": "assistant", "content": bot_response})