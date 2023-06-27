# api_Serasa

Este projeto trata-se de uma API desenvolvida usando o framework FastApi. A API tem como objetivo simular empréstimos consultando um parceiro externo.

# Instalação

Para esse projeto são utilizado:

Python versão: 3.11.4

FastApi: 
```sh
pip install fastapi
 ```

Requests:
```sh
shpip install requests
 ```
Redis:
```sh
pip install redis
```
# Variáveis de ambiente 

Antes de executar a API é necessario configurar as variáveis de ambiente, essas encontram-se no arquivo main.ppy.

redis_host: O endereço do host Redis.

redis_port: A porta do Redis.

redis_db: O número do banco de dados do Redis a ser usado para armazenar o cache.

BASE_URL: A URL base do parceiro externo.

AUTH_ENDPOINT: O endpoint de autenticação do parceiro externo.

OFFERS_ENDPOINT: O endpoint para obter as ofertas do parceiro externo.

CLIENT_ID: O ID do cliente para autenticação.

CLIENT_SECRET: A chave do cliente para autenticação.

# Uso
A API possui um único endpoint GET /emprestimos que permite simular um empréstimo. Os seguintes parâmetros de consulta são esperados:

valor (obrigatório): O valor da simulação de crédito.

parcela (obrigatório): O número de parcelas.

cpf (obrigatório): O CPF do cliente.


Exemplo de uso:
```sh
GET /emprestimos?valor=1000&parcela=12&cpf=12345678900
 ```

# Resposta

A resposta da API será um objeto JSON contendo os detalhes da oferta de empréstimo, se houver uma oferta disponível. Caso contrário, a API retornará uma resposta vazia com um status 204 (No Content).

# Cache

A API utiliza o Redis como mecanismo de cache para armazenar as ofertas de empréstimo por CPF. As ofertas são armazenadas em cache por 1 hora (3600 segundos) para evitar chamadas excessivas à API do parceiro externo.

# Erros

A API pode retornar os seguintes erros:

Status 422 Unprocessable Entity: Ocorre quando os parâmetros de consulta não são válidos.

Status 500 Internal Server Error: Ocorre em caso de falha na autenticação com o parceiro externo ou ao buscar as ofertas.

