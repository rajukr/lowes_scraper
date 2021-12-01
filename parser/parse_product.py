class ParseProductDetails(object):

    def __init__(self, soup):
        self._soup = soup
        self.product_id = 0
        self.model_number = 0
        self.brand_name = ''
        self.product_name = ''
        self.description = ''
        self.category = ''
        self.final_price = 0
        self.currency = 'USD'
        self.attribute_names = ''
        self.attribute_values = ''
        self.small_img_url = ''
        self.large_img_url = ''
        self.status = 'IN STOCK'

    def get_product_id(self):
        modelelem = self._soup.find('div', attrs={"class": "modelNo"})
        product_id, _ = [span.text for span in modelelem.find_all('span')]
        self.product_id = product_id.replace("Item #", "").strip()
        return self.product_id
    
    def get_model_number(self):
        modelelem = self._soup.find('div', attrs={"class": "modelNo"})
        _, model_number = [span.text for span in modelelem.find_all('span')]
        self.model_number = model_number.replace("Model #", "").strip()
        return self.model_number

    def get_brand(self):
        brand = self._soup.find('span', attrs={"class": "desc-brand"})
        self.brand_name = brand.text.strip()
        return self.brand_name
    
    def get_product_name(self):
        brand = self._soup.find('span', attrs={"class": "desc-brand"})
        if brand.find('a'):
            self.product_name = brand.find('a').text.strip()
        else:
            self.product_name = brand.parent.text.strip()
        return self.product_name

    def get_description(self):
        bullets = self._soup.find('ul', attrs={"class": "bullets"})
        self.description = ", ".join([desc.text.strip() for desc in bullets.find_all('p')])
        return self.description
    
    def get_categories(self):
        self.category = ", ".join([desc.find('a').text.strip() for desc in self._soup.find_all('li', attrs={"class": "breadcrumb-item"})])
        return self.category

    def get_price(self):
        final_price = self._soup.find('span', attrs={"class": "finalPrice"})
        self.final_price = final_price.next.text.strip() if final_price else 0
        return self.final_price
    
    def get_currency(self):
        final_price = self._soup.find('span', attrs={"class": "finalPrice"})
        if final_price:
            self.currency = final_price.find('sup', attrs={"itemprop": "PriceCurrency"}).get('content').strip()
        return self.currency
    
    def get_attribute_names(self):
        specs = self._soup.find('div', attrs={"class": "specificationWrapper"})
        table = specs.find('div', attrs={"class": "table0"})
        attribute_names = [keys.text for keys in table.find_all("div", attrs={"class": "key"})]
        self.attribute_names =  "|".join(attribute_names)
        return self.attribute_names
    
    def get_attribute_values(self):
        specs = self._soup.find('div', attrs={"class": "specificationWrapper"})
        table = specs.find('div', attrs={"class": "table0"})
        attribute_values = [keys.text for keys in table.find_all("div", attrs={"class": "value"})]
        self.attribute_values = "|".join(attribute_values)
        return self.attribute_values

    def get_small_img(self):
        picture = self._soup.find('div', attrs={"id": "card-image-container"})
        if picture:
            small_img_url = [src.get('srcset') for src in picture.find_all('source') if 'size=md' in src.get('srcset')]
            self.small_img_url = small_img_url[0] if small_img_url else ''
        return self.small_img_url

    def get_large_img(self):
        large_img_url = ''
        picture = self._soup.find('div', attrs={"id": "card-image-container"})
        if picture:
            large_img_url = [src.get('srcset') for src in picture.find_all('source') if 'size=xl' in src.get('srcset')]
            self.large_img_url = large_img_url[0] if large_img_url else ''
        return self.large_img_url
    
    def get_product_availability(self):
        notify = self._soup.find('div', attrs={"id": "notifyme_form"})
        atc = self._soup.find('div', attrs={"id": "atc"})
        if notify:
            self.status = 'OUT OF STOCK'
        if atc:
            self.status = 'IN STOCK'
        return self.status