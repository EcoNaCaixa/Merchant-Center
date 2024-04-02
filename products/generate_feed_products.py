import json
import os
import time
import xml.etree.ElementTree as ET
import requests
from xmlschema import XMLSchema
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
    print(json.dumps(r.json(), indent=4))
    return r.json()

def gerar_feed_xml(nome_arquivo, produtos):
    """ Gera um feed XML para o Google Merchant"""
    
    root = ET.Element("rss", {'xmlns:g': 'http://base.google.com/ns/1.0'})
    channel = ET.SubElement(root, "channel")

    for produto in produtos['products']:
        variant_id = produto['variants'][0]['id']
        preco_desconto = round(float(produto['variants'][0]['price']) * 0.95, 2)

        item = ET.SubElement(channel, "item")
        ET.SubElement(item, "g:id").text = f"shopify_BR_{produto['id']}_{variant_id}"
        ET.SubElement(item, "g:price").text = str(preco_desconto)        
    
    tree = ET.ElementTree(root)
    tree.write(nome_arquivo, encoding='utf-8', xml_declaration=True)

# Exemplo de produtos
products = get_all_products_shopify()

# Nome do arquivo de saída
nome_arquivo = 'feed_google_merchant.xml'

# Gerar o feed XML
gerar_feed_xml(nome_arquivo, products)

print(f'Feed gerado com sucesso: {nome_arquivo}')