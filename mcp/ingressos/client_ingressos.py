import httpx

def acessar_api(url: str) -> tuple[bool, str | None, str | None]:
    """Isola a lógica de comunicação HTTP do servidor MCP de Ingressos."""
    try:
        resposta = httpx.get(url, timeout=10.0)
        resposta.raise_for_status()
        return True, resposta.text, None
    except Exception as e:
        erro = f"Falha de conexão: {str(e)}"
        print(f"[ERRO DE REDE] Não foi possível acessar {url} -> {erro}")
        return False, None, erro