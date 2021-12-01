import time

class ParseProductPrices(object):

    def __init__(self, soup):
        self._soup = soup
        self.product_id = 0
        self.store_id = ''
        self.sale_price = 0
        self.price_currency = 'USD'
        self.stock_status = 'IN STOCK'
        self.stock_count = 0

    def get_product_id(self):
        return self.product_id
    
    def get_store_id(self):
        # store_link = self._soup.find_element(By.ID,'pd-store-inv-cos')
        store_link = self._soup.find("div", attr={"id", "pd-store-inv-cos"})
        if store_link:
            store_link.click()
            time.sleep(1)
            store_cards = self._soup.find_all('div', attr={"class": "store-card"})
            for store_card in store_cards:
                print(store_card)
        return self.store_id

    def get_sale_price(self):
        return self.sale_price
    
    def get_price_currency(self):
        return self.price_currency
    
    def get_stock_count(self):
        return self.stock_count
    
    def get_stock_status(self):
        return self.stock_status