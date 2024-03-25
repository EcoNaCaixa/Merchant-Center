# Integração de Gerenciamento de Avaliações

Este script Python é usado para gerar feeds de avaliações de produtos a partir da plataforma Yotpo e carregá-los em uma loja Shopify.

## Pré-requisitos

- Python 3.x instalado no seu sistema.
- Bibliotecas Python: `requests`, `xml.etree.ElementTree`, `xmlschema`.

## Configuração

1. Obtenha as credenciais necessárias:

    - YOTPO_ACCESS_TOKEN 
    - YOTPO_KEY
    - YOTPO_SECRET_KEY
    - X_Shopify_Access_Token

2. Crie um novo arquivo com o nome `.env`. Certifique-se de incluir o ponto (`.`) no início do nome do arquivo.

Abra o arquivo .env no seu editor de texto.

Adicione as seguintes credenciais no formato CHAVE=valor:

- YOTPO_ACCESS_TOKEN=sua_chave_de_acesso
- YOTPO_KEY=sua_chave
- YOTPO_SECRET_KEY=sua_chave_secreta
- X_SHOPIFY_ACCESS_TOKEN=sua_chave_de_acesso

3. Substitua as variáveis `YOTPO_ACCESS_TOKEN`, `YOTPO_KEY`, `YOTPO_SECRET_KEY` e `X_Shopify_Access_Token` pelos valores correspondentes.

## Uso

1. Execute o script Python.

   ```bash
   python nome_do_arquivo.py
   ```

2. O script irá gerar um arquivo XML contendo as avaliações dos produtos e tentará carregá-lo na loja Shopify especificada.

3. Verifique a saída para mensagens de sucesso ou falha.

## Notas

- Este script faz chamadas à API da Yotpo e à API da Shopify para recuperar e carregar os dados das avaliações dos produtos, respectivamente.

- Certifique-se de ter as permissões necessárias e de estar conectado às plataformas relevantes antes de executar o script.
