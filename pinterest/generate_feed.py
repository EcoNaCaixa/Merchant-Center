import datetime
import json
import os
import time
import xml.etree.ElementTree as ET
import requests
from dotenv import load_dotenv

load_dotenv()

SHOPIFY_API_TOKEN = os.getenv("SHOPIFY_API_TOKEN")


def get_all_products_shopify():
    """ Retorna todos os produtos da loja Shopify 
    
    Returns: 
        list: Lista de produtos da loja Shopify """
        
    url = f"https://sofanacaixa.myshopify.com/admin/api/2024-01/products.json?limit=250"
    headers = {"X-Shopify-Access-Token": SHOPIFY_API_TOKEN}
    r = requests.get(url, headers=headers)
    print(f"Produtos: {len(r.json()['products'])}")

    return r.json()

def get_date():
    data_atual = datetime.datetime.now()
    data_nova = data_atual + datetime.timedelta(days=15)
    data_nova_formatada = data_nova.strftime('%Y-%m-%dT%H:%M:%S')
    return data_nova_formatada

def gerar_feed_xml(nome_arquivo, produtos):
    """ Gera um feed XML para o Google Merchant"""
    root = ET.Element("rss", {'xmlns:g': 'http://base.google.com/ns/1.0'})
    channel = ET.SubElement(root, "channel")

    for produto in produtos['products']:
        print(json.dumps(produto, indent=4))

        variants = produto['variants']
        for variant in variants:
            print(json.dumps(variant, indent=4))

            preco_original = variant['compare_at_price']
            preco_desconto = round(float(variant['price']) * 0.95, 2)
            item = ET.SubElement(channel, "item")
            ET.SubElement(item, "g:id").text = str(variant['id'])
            ET.SubElement(item, "g:title").text = produto['title']
            ET.SubElement(item, "g:description").text = produto['title']
            ET.SubElement(item, "g:link").text = f"https://sofanacaixa.com.br/products/{produto['handle']}"
            ET.SubElement(item, "g:image_link").text = produto['image']['src']
            ET.SubElement(item, "g:availability").text = "in stock"
            ET.SubElement(item, "g:price").text = f"{preco_original} BRL"
            ET.SubElement(item, "g:sale_price").text = f"{preco_desconto:.2f} BRL"

            if variant['sku']:
                ET.SubElement(item, "g:brand").text = "Sofá na Caixa"
                ET.SubElement(item, "g:mpn").text = variant['sku']

    tree = ET.ElementTree(root)
    tree.write(nome_arquivo, encoding='utf-8', xml_declaration=True)

# Exemplo de produtos
products = get_all_products_shopify()

# Nome do arquivo de saída
nome_arquivo = 'pinterest_sofa.xml'

# Gerar o feed XML
gerar_feed_xml(nome_arquivo, products)

print(f'Feed gerado com sucesso: {nome_arquivo}')