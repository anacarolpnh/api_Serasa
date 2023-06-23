from fastapi import FastAPI, HTTPException, Query
import requests
import redis 

app = FastAPI()

# Configuração do Redis
redis_host = "localhost"
redis_port = 6379
redis_db = 0

# Cria uma conexão com o Redis
cache = redis.Redis(host=redis_host, port=redis_port, db=redis_db)

BASE_URL = "https://f0e60216-6218-46d2-ae59-a5c0ea8102fa.mock.pstmn.io"
AUTH_ENDPOINT = "/autenticar"
OFFERS_ENDPOINT = "/ofertas"

CLIENT_ID = "serasa"
CLIENT_SECRET = "6261d2ca-fc49-45d6-a895-5d0c113044df"

@app.get("/emprestimos")
def get_emprestimos(valor: int = Query(..., description="Valor da simulação de crédito"),
                    parcela: int = Query(..., description="Número de parcelas"),
                    cpf: str = Query(..., description="CPF do cliente")):
    # Verifica se tem ofertas em cache
    cached_offers = cache.get(cpf)
    if cached_offers:
        return cached_offers

    # Autentica a API
    auth_data = {
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET
    }
    headers = {
        "Content-Type": "application/x-www-form-urlencoded"
    }
    auth_response = requests.post(BASE_URL + AUTH_ENDPOINT, data=auth_data, headers=headers)

    if auth_response.status_code != 200:
        raise HTTPException(status_code=500, detail="Erro na autenticação com o parceiro")

    access_token = auth_response.json().get("access_token")

    # Busca na API
    headers = {
        "Authorization": f"Bearer {access_token}"
    }
    offers_response = requests.get(BASE_URL + OFFERS_ENDPOINT, headers=headers)

    if offers_response.status_code != 200:
        raise HTTPException(status_code=500, detail="Erro ao buscar as ofertas do parceiro")

    offers = offers_response.json()

    # Filtrar a oferta usando valor e pacela
    filtered_offer = None
    for offer in offers:
        offer_valor = offer.get("value", 0)  #  0 se 'value' estiver undefined
        if offer_valor <= valor and offer["installments"] <= parcela:
            if filtered_offer is None or offer_valor < filtered_offer.get("value", 0):
                filtered_offer = offer

    if filtered_offer is not None:
        # Guardaa as ofertas em cache
        cache.setex(cpf, 3600, filtered_offer)
        return filtered_offer
    else:
        raise HTTPException(status_code=204, detail="Nenhuma oferta encontrada")
