import datetime
import json
import os
import time
import xml.etree.ElementTree as ET
import requests
from dotenv import load_dotenv

load_dotenv()

SHOPIFY_API_TOKEN = os.getenv("SHOPIFY_API_TOKEN")


def get_product_group_id(product_id):
    """ Retorna o ID do grupo de produtos
    
    Args:
        product (dict): Dicionário de um produto
    
    Returns:
        str: ID do grupo de produtos """
    
    headers = {"X-Shopify-Access-Token": SHOPIFY_API_TOKEN}
    url = f"https://sofanacaixa.myshopify.com/admin/api/2024-01/products/{product_id}/metafields.json?key=google_merchant_group_id"
    try:
        r = requests.get(url, headers=headers)
        return r.json()['metafields'][0]['value']
    except Exception as e:
        print(f"Erro ao buscar group_id: {e}")
        return '0'
    
def get_all_products_shopify():
    """ Retorna todos os produtos da loja Shopify 
    
    Returns: 
        list: Lista de produtos da loja Shopify """
        
    url = f"https://sofanacaixa.myshopify.com/admin/api/2024-01/products.json?limit=250"
    headers = {"X-Shopify-Access-Token": SHOPIFY_API_TOKEN}
    r = requests.get(url, headers=headers)
    return r.json()

def get_date():
    # Obtém a data atual
    data_atual = datetime.datetime.now()

    # Adiciona 5 dias
    data_nova = data_atual + datetime.timedelta(days=60)

    # Formata a nova data
    data_nova_formatada = data_nova.strftime('%Y-%m-%dT%H:%M:%S')

    return data_nova_formatada


def gerar_feed_xml(nome_arquivo, produtos):
    """ Gera um feed XML para o Google Merchant"""
    
    root = ET.Element("rss", {'xmlns:g': 'http://base.google.com/ns/1.0'})
    channel = ET.SubElement(root, "channel")

    for produto in produtos['products']:
        variant = produto['variants'][0]
        preco_original = variant['compare_at_price']
        preco_desconto = round(float(variant['price']) * 0.95, 2)
        
        item = ET.SubElement(channel, "item")
        ET.SubElement(item, "g:id").text = f"shopify_BR_{produto['id']}_{variant['id']}"
        ET.SubElement(item, "g:price").text = f"{preco_original} BRL"
        ET.SubElement(item, "g:sale_price").text = f"{preco_desconto:.2f} BRL"
        ET.SubElement(item, "g:item_group_id").text = get_product_group_id(product_id=produto['id'])
        
        if variant['sku']:
            data_atual_str = datetime.datetime.now().strftime('%Y-%m-%dT%H:%M:%S')
            data_final_str = get_date()
            ET.SubElement(item, "g:sale_price_effective_date").text = f"{data_atual_str}-0800/{data_final_str}-0800"  # Sale price effective date
            ET.SubElement(item, "g:brand").text = "Sofá na Caixa"
            ET.SubElement(item, "g:mpn").text = variant['sku']
    
    tree = ET.ElementTree(root)
    tree.write(nome_arquivo, encoding='utf-8', xml_declaration=True)

# Exemplo de produtos
products = get_all_products_shopify()

# Nome do arquivo de saída
nome_arquivo = 'feed_google_merchant.xml'

# Gerar o feed XML
gerar_feed_xml(nome_arquivo, products)

print(f'Feed gerado com sucesso: {nome_arquivo}')