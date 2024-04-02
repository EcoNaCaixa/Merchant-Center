# Integração Shopify Google Merchant

Este script Python interage com a API da plataforma Shopify para obter todos os produtos da loja SOFA NA CAIXA e, em seguida, gera um feed XML compatível com o Google Merchant a partir desses produtos. Alimenta o FEED do google merchant para mostrar o **preço com desconto** dos produtos para o valor cobrado no pix

## Pré-requisitos

- Python 3.x instalado
- Uma loja Shopify ativa
- Token de API Shopify válido
- Variáveis de ambiente configuradas em um arquivo `.env`

## Instalação

1. Clone este repositório:

```bash
git clone https://github.com/seu-usuario/nome-do-repositorio.git
```

2. Instale as dependências:

```bash
pip install -r requirements.txt
```

3. Configure as variáveis de ambiente:
   - Crie um arquivo `.env` na raiz do projeto.
   - Defina `SHOPIFY_API_TOKEN` como seu token de API Shopify.

## Uso

Execute o script Python `generate_feed_products.py`:

```bash
python generate_feed_products.py
```

O script irá:
- Obter todos os produtos da loja Shopify.
- Gerar um feed XML para o Google Merchant.
- Salvar o feed no diretório atual como `feed_google_merchant.xml`.

## Contribuindo

Contribuições são bem-vindas! Para contribuir com este projeto, siga estas etapas:

1. Fork este repositório.
2. Crie um branch para sua funcionalidade (`git checkout -b feature/sua-funcionalidade`).
3. Faça commit de suas alterações (`git commit -am 'Adicione sua funcionalidade'`).
4. Envie para o branch (`git push origin feature/sua-funcionalidade`).
5. Abra uma solicitação pull.

## Licença

Este projeto é licenciado sob a Licença MIT. Consulte o arquivo `LICENSE` para obter mais detalhes.
