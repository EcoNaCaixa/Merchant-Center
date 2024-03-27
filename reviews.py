import json
import os
import time
import xml.etree.ElementTree as ET
import requests
from xmlschema import XMLSchema
from dotenv import load_dotenv

load_dotenv()

YOTPO_ACCESS_TOKEN = os.getenv('YOTPO_ACCESS_TOKEN')
YOTPO_KEY = os.getenv('YOTPO_KEY')
YOTPO_SECRET_KEY = os.getenv('YOTPO_SECRET_KEY')
X_Shopify_Access_Token = os.getenv("X_Shopify_Access_Token")

import requests

def get_yotpo_token():
    url = "https://api.yotpo.com/core/v3/stores/ij9SZZ2el2lbuzB1jSHrHDIdiskqIRqgC1XcVf7b/access_tokens"
    payload = {"secret": YOTPO_SECRET_KEY}
    headers = {"accept": "application/json", "Content-Type": "application/json"}
    response = requests.post(url, json=payload, headers=headers)
    print(response.text)
    return


def get_product_shopify(product_id):
    url = f"https://sofanacaixa.myshopify.com/admin/api/2024-01/products/{product_id}.json"
    headers = {"X-Shopify-Access-Token": X_Shopify_Access_Token}
    r = requests.get(url, headers=headers)
    return r.json()['product']
    

def yotpo_reviews_call():
    reviews_list = []
    page = 1
    while True:
        
        url = f"https://api.yotpo.com/v1/apps/{YOTPO_KEY}/reviews?page={page}&count=100&utoken={YOTPO_ACCESS_TOKEN}"
        
        payload = {"secret": YOTPO_SECRET_KEY}
        
        headers = {"accept": "application/json", "Content-Type": "application/json"}        
        response = requests.get(url, json=payload, headers=headers)
        if response.json()['reviews'] == []:
            return reviews_list
        else:
            for review in response.json()['reviews']:
                reviews_list.append(review)
            page += 1
            time.sleep(1)




def generate_product_review_feed(reviews_list):
    # Create root element <feed>
    feed = ET.Element('feed')

    # Add attributes to the <feed> element
    feed.set('xmlns:vc', 'http://www.w3.org/2007/XMLSchema-versioning')
    feed.set('xmlns:xsi', 'http://www.w3.org/2001/XMLSchema-instance')
    feed.set('xsi:noNamespaceSchemaLocation', 'http://www.google.com/shopping/reviews/schema/product/2.3/product_reviews.xsd')

    # Create child elements and add them to <feed>
    version = ET.SubElement(feed, 'version')
    version.text = '2.3'

    aggregator = ET.SubElement(feed, 'aggregator')
    aggregator_name = ET.SubElement(aggregator, 'name')
    aggregator_name.text = 'Sample Reviews Aggregator'

    publisher = ET.SubElement(feed, 'publisher')
    publisher_name = ET.SubElement(publisher, 'name')
    publisher_name.text = 'Sofá na Caixa'
    favicon = ET.SubElement(publisher, 'favicon')
    favicon.text = 'https://cdn.shopify.com/s/files/1/0846/3741/7789/files/sofanacaixa_favicon_Logo.png?v=1704808913'

    reviews = ET.SubElement(feed, 'reviews')

    total = 1
    for review in reviews_list:
        product_shopify = get_product_shopify(review['sku'])
        review1 = ET.SubElement(reviews, 'review')
        review_id1 = ET.SubElement(review1, 'review_id')
        review_id1.text = str(review['id'])

        reviewer1 = ET.SubElement(review1, 'reviewer')
        reviewer_name1 = ET.SubElement(reviewer1, 'name')
        reviewer_name1.text = review['name']

        review_timestamp1 = ET.SubElement(review1, 'review_timestamp')
        review_timestamp1.text = review['created_at']

        title1 = ET.SubElement(review1, 'title')
        title1.text = review['title']

        content1 = ET.SubElement(review1, 'content')
        content1.text = review['content']

        review_url1 = ET.SubElement(review1, 'review_url')
        review_url1.set('type', 'group')
        review_url1.text = f"https://sofanacaixa.com.br/products/{product_shopify['handle']}"

        ratings1 = ET.SubElement(review1, 'ratings')
        overall1 = ET.SubElement(ratings1, 'overall')
        overall1.set('min', '1')
        overall1.set('max', '5')
        overall1.text = str(review['score'])

        products1 = ET.SubElement(review1, 'products')
        product1 = ET.SubElement(products1, 'product')
        product_ids1 = ET.SubElement(product1, 'product_ids')
        
        mpns1 = ET.SubElement(product_ids1, 'mpns')
        mpn1 = ET.SubElement(mpns1, 'mpn')
        mpn1.text = product_shopify['variants'][0]['sku']

        skus1 = ET.SubElement(product_ids1, 'skus')
        sku1 = ET.SubElement(skus1, 'sku')
        sku1.text = product_shopify['variants'][0]['sku']
        
        brands1 = ET.SubElement(product_ids1, 'brands')
        brand1 = ET.SubElement(brands1, 'brand')
        brand1.text = 'Sofá na Caixa'

        product_name1 = ET.SubElement(product1, 'product_name')
        product_name1.text = product_shopify['title']
        product_url1 = ET.SubElement(product1, 'product_url')
        product_url1.text = f"https://sofanacaixa.com.br/products/{product_shopify['handle']}"

        is_spam1 = ET.SubElement(review1, 'is_spam')
        is_spam1.text = 'false'
        collection_method1 = ET.SubElement(review1, 'collection_method')
        collection_method1.text = 'post_fulfillment'

        total += 1

    # Create an ElementTree object
    tree = ET.ElementTree(feed)

    # Write the XML to a file
    tree.write("product_reviews.xml", encoding='utf-8', xml_declaration=True)

    print("XML file generated successfully!")
    

reviews = yotpo_reviews_call()         
generate_product_review_feed(reviews)
