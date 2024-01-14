import json
import os
import mysql.connector

previous_path = os.path.abspath(os.path.join(os.getcwd(), os.pardir))
file_name = 'petlebi_data.json'
file_path = 'C:/Users/ofuce/Desktop/WebScrapping/petlebi_scraper/petlebi_scraper/petlebi_data.json'

with open(file_path, 'r', encoding = 'utf-8') as file:
    json_data = json.load(file)

product_urls = []
product_barcodes = []
product_names = []
product_prices = []
product_stocks = []
product_images = []
product_descriptions = []
product_categories = []
product_skus = []
product_ids = []
product_brands = []

for product in json_data.get('products', []):
    product_urls.append(product.get('product_url', ''))
    product_barcodes.append(product.get('product_barcode', ''))
    product_names.append(product.get('product_name', ''))
    product_prices.append(product.get('product_price', ''))
    product_stocks.append(product.get('product_stock', 0))
    product_images.append(product.get('product_image', ''))
    product_descriptions.append(product.get('product_description', ''))
    product_categories.append(product.get('product_category', ''))
    product_skus.append(product.get('product_sku', ''))
    product_ids.append(product.get('product_id', ''))
    product_brands.append(product.get('product_brand', ''))

print("Product URLs:", product_urls)
print("Product Barcodes:", product_barcodes)
print("Product Names:", product_names)
print("Product Prices:", product_prices)
print("Product Stocks:", product_stocks)
print("Product Images:", product_images)
print("Product Descriptions:", product_descriptions)
print("Product Categories:", product_categories)
print("Product SKUs:", product_skus)
print("Product IDs:", product_ids)
print("Product Brands:", product_brands)

db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': 'Half@life1',
    'database': 'petlebi', 
    'auth_plugin': 'mysql_native_password',
}

connection = mysql.connector.connect(**db_config)

try:
    cursor = connection.cursor()
    for i in range(len(product_urls)):
        query = '''
            INSERT INTO petlebi (
                product_url, product_barcode, product_name, product_price,
                product_stock, product_image, product_description,
                product_category, product_sku, product_id, product_brand
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        '''
        values = (
            product_urls[i], product_barcodes[i], product_names[i],
            product_prices[i], product_stocks[i], product_images[i],
            product_descriptions[i], product_categories[i], product_skus[i], product_ids[i],
            product_brands[i]
        )

        cursor.execute(query, values)
        connection.commit()

    print("Datas added succesfully")

except mysql.connector.Error as err:
    print(f"Error: {err}")

finally:
    if 'connection' in locals() and connection.is_connected():
        cursor.close()
        connection.close()
        print("MySqL Connection Closed.")