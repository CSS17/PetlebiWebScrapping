import scrapy
import re
import json
import os

class PetlebiSpider(scrapy.Spider):
    name = 'petlebi'
    allowed_domains = ['petlebi.com']
    product_urls = []
    barcodes = []  
    product_names = []
    product_prices = []
    product_stocks = []
    product_images = []
    product_descriptions = []
    product_categories = []
    product_sku_list = []
    product_id_list = []
    product_brands = []
    counter = 0
    start_urls = ['https://www.petlebi.com/alisveris/ara']

    def closed(self, reason):
        self.save_to_json()
        try:
            if os.name == 'posix':  
                os.system('open petlebi_data.json')
            elif os.name == 'nt':  
                os.system('notepad petlebi_data.json')
        except Exception as e:
            self.log(f"Hata: {e}")

    def save_to_json(self):
        products = []
        for i in range(len(self.product_urls)):
            product = {
                'product_url': self.product_urls[i],
                'product_barcode': self.barcodes[i],
                'product_name': self.product_names[i],
                'product_price': self.product_prices[i],
                'product_stock': self.product_stocks[i],
                'product_image': self.product_images[i],
                'product_description': self.product_descriptions[i],
                'product_category': self.product_categories[i],
                'product_sku': self.product_sku_list[i],
                'product_id': self.product_id_list[i],
                'product_brand': self.product_brands[i]
            }
            products.append(product)

        data = {'products': products}
     

        with open('petlebi_data.json', 'w', encoding='utf-8') as json_file:json.dump(data, json_file, ensure_ascii=False, indent=4) 
        json_str = json.dumps(data, ensure_ascii=False, indent=4)
        
        

    def show(self):
        print("Product URLs:")
        print(self.product_urls)
        print("Product Names:")
        print(self.product_names)
        print("Product Descriptions:")
        print(self.product_descriptions)
        print("Product Prices:")
        print(self.product_prices)
        print("Product Stocks:")
        print(self.product_stocks)
        print("Product Images:")
        print(self.product_images)
        print("Barcodes:")
        print(self.barcodes)
        print("Product Category:")
        print(self.product_categories)
        print("Product Sku:")
        print(self.product_sku_list)
        print("Product ID:")
        print(self.product_id_list)
        print("Product Brand:")
        print(self.product_brands)


    def parse(self, response):
        urls = response.css('div.card-body a.p-link::attr(href)').getall()
        for url in urls:
            self.product_urls.append(url)

        next_page_number = response.css('ul.pagination li.active + li a::text').get()
        if next_page_number is not None:
            next_page_url = f'https://www.petlebi.com/alisveris/ara?page={next_page_number}'
            yield scrapy.Request(url=next_page_url, callback=self.parse)
        else:
            lenght= len(self.product_urls)
            self.barcodes = [None]*lenght
            self.product_names = [None]*lenght
            self.product_prices = [None]*lenght
            self.product_stocks = [None]*lenght
            self.product_images = [None]*lenght
            self.product_descriptions = [None]*lenght
            self.product_categories = [None]*lenght
            self.product_sku_list = [None]*lenght
            self.product_id_list = [None]*lenght
            self.product_brands = [None]*lenght
            for index in range(len(self.product_urls)):
                yield scrapy.Request(url=self.product_urls[index], callback=self.parse_product_page,meta={'index': index})


        
    

     

    def parse_product_page(self, response):
       
        self.counter = self.counter + 1
        print("Number of products scanned: "+str(self.counter))
        index = response.meta['index']
        barcode = response.css('div.col-10.pd-d-v::text').get()
        product_name = response.css('h1.product-h1::text').get()
        product_price = response.css('p.mb-0 span.new-price::text').get()
        select_element = response.css('select#quantity')
        product_image =  response.css('div.product-detail-main-line a.MagicZoom::attr(href)').get()
        product_value = [int(option.css('::attr(value)').get()) for option in select_element.css('option')]
        max_value = max(product_value) if product_value else 0
        product_description= response.css('span#productDescription *::text').getall()
        cleaned_content = '\n'.join(filter(str.strip, product_description))
        cleaned_content = cleaned_content.replace("\n"," ")
        product_category = response.css('li.breadcrumb-item:nth-child(2) span[itemprop="name"]::text').get()
        product_category = product_category
        product_brand = response.css('div#myTabContent div.row.mb-2.brand-line div.col-10.pd-d-v span a::text').get()
        page_source = response.text
       
       

        pattern_sku = r'"sku": "(.*?)"'
        match = re.search(pattern_sku, str(page_source))

        if match:
            product_sku = match.group(1)
            self.product_sku_list[index]= product_sku
        else:
            print("SKU bulunamadı.")

        pattern_id = r'"productID":(\d+)'
        match = re.search(pattern_id, str(page_source))

        if match:
            product_id = match.group(1)
            self.product_id_list[index]= product_id
        else:
            print("productID bulunamadı.")

        self.product_stocks[index]=max_value
        self.barcodes[index]=barcode
        self.product_names[index]= product_name
        self.product_prices[index]= product_price
        self.product_images[index]= product_image

        self.product_descriptions[index]= cleaned_content
        self.product_categories[index]= product_category
        self.product_brands[index]= product_brand
  
        if self.barcodes.count(None) == 0:
            self.show()

          
          

    
    

   