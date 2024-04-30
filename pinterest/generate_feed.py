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

    return r.json()

def get_date():
    data_atual = datetime.datetime.now()
    data_nova = data_atual + datetime.timedelta(days=15)
    data_nova_formatada = data_nova.strftime('%Y-%m-%dT%H:%M:%S')
    return data_nova_formatada


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
    
def get_product_images(product):
    """ Retorna as imagens de um produto 
    
    Args:
        product (dict): Dicionário de um produto
    
    Returns:
        list: Lista de imagens de um produto """
    
    images = []
    for image in product['images']:
        images.append(image['src'])
    return images
    
def get_product_reviews_count(product_id):
    headers = {"X-Shopify-Access-Token": SHOPIFY_API_TOKEN}
    url = f"https://sofanacaixa.myshopify.com/admin/api/2024-01/products/{product_id}/metafields.json?key=reviews_average"
    r = requests.get(url, headers=headers)
    review_data = {}
    
    if 'metafields' not in r.json():
        return {
                'reviews_average': '5',
                'reviews_count': '25'  
            }
    else:
        try:
            review_data['reviews_average'] = r.json()['metafields'][0]['value']
        
            url = f"https://sofanacaixa.myshopify.com/admin/api/2024-01/products/{product_id}/metafields.json?key=reviews_count"
            r = requests.get(url, headers=headers)
            review_data['reviews_count'] = r.json()['metafields'][0]['value']

            return review_data
                
        except:
            return {
                'reviews_average': '5',
                'reviews_count': '25'  
            }
    
def gerar_feed_xml(nome_arquivo, produtos):
    """ Gera um feed XML para o Google Merchant"""
    root = ET.Element("rss", {'xmlns:g': 'http://base.google.com/ns/1.0'})
    channel = ET.SubElement(root, "channel")

    print(f"gerando feed com {len(produtos['products'])} produtos")
    i = 1
    for produto in produtos['products']:
        print(f"gerando feed para o produto {produto['id']} ({i}/{len(produtos['products'])})")
        i += 1
        variants = produto['variants']
        for variant in variants:
            preco_original = variant['compare_at_price']
            print(round(float(variant['price']) * 0.95, 2))
            preco_desconto = round(float(variant['price']) * 0.95, 2)
            
            item = ET.SubElement(channel, "item")
            
            ET.SubElement(item, "g:id").text = f"shopify_BR_{produto['id']}_{variant['id']}"
            ET.SubElement(item, "g:title").text = produto['title']
            ET.SubElement(item, "g:description").text = produto['title']
            ET.SubElement(item, "g:link").text = f"https://sofanacaixa.com.br/products/{produto['handle']}"
            images = get_product_images(produto)
            ET.SubElement(item, "g:image_link").text = images[0]
            ET.SubElement(item, "g:availability").text = "in stock"
            ET.SubElement(item, "g:price").text = f"{preco_original} BRL"
            ET.SubElement(item, "g:sale_price").text = f"{preco_desconto:.2f} BRL"

            # CAMPOS ADICIONAIS
            ET.SubElement(item, "g:product_type").text = f"House > Furniture > Sofa > Sofa Modular"
            ET.SubElement(item, "g:additional_image_link").text = ', '.join(images[1:-1])
            
            reviews = get_product_reviews_count(produto['id'])
            
            ET.SubElement(item, "g:average_review_rating").text = reviews.get('reviews_average', 5)
            ET.SubElement(item, "g:number_of_ratings").text = reviews.get('reviews_count', 25)
            ET.SubElement(item, "g:number_of_reviews").text = reviews.get('reviews_count', 25)
            ET.SubElement(item, "g:description_html").text = produto['body_html']
            ET.SubElement(item, "g:video_link").text = "https://www.youtube.com/watch?v=7sykq-xZWww&t=2s&ab_channel=Sof%C3%A1naCaixa"
            ET.SubElement(item, "g:group_id").text = get_product_group_id(produto['id'])
            ET.SubElement(item, "g:brand").text = "Sofá na Caixa"
            ET.SubElement(item, "g:mpn").text = variant['sku']
            ET.SubElement(item, "g:size_system").text = 'BR'
            ET.SubElement(item, "g:variant_names").text = 'Cor'
            ET.SubElement(item, "g:variant_values").text = 'Cinza, Linho'
            ET.SubElement(item, "g:color").text = produto['title'].split('-')[-1].strip()
            ET.SubElement(item, "g:google_product_category").text = "Móveis > Sofás"
            ET.SubElement(item, "g:condition").text = 'new'

    tree = ET.ElementTree(root)
    tree.write(nome_arquivo, encoding='utf-8', xml_declaration=True)

# Exemplo de produtos
products = get_all_products_shopify()

# Nome do arquivo de saída
nome_arquivo = 'pinterest_sofa.xml'

# Gerar o feed XML
gerar_feed_xml(nome_arquivo, products)

print(f'Feed gerado com sucesso: {nome_arquivo}')