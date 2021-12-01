class ParseStores(object):

    def __init__(self, soup):
        self._soup = soup
        self.store_id = 0
        self.store_name = ''
        self.store_address = ''
        self.store_zip_code = ''
        self.store_country_code = ''
        self.store_capabilities = 'N/A'
        self.lattitude = ''
        self.longitude = ''

    def get_store_id(self):
        store = self._soup.find('span', {'class': 'storeNo'})
        if store:
            self.store_id = store.text.replace('Store #', '')
        return self.store_id

    def get_store_name(self):
        store_details = self._soup.find('div', {'data-store-id': 'store_{}'.format(self.store_id)})
        if store_details:
            self.store_name = store_details.find('h1').text.strip()
        return self.store_name

    def get_store_address(self):
        store_details = self._soup.find('div', {'data-store-id': 'store_{}'.format(self.store_id)})
        if store_details:
            loc = store_details.find('div', {'class': 'location'})
            self.store_address = loc.text.strip()
        return self.store_address
    
    def get_store_zip_code(self):
        store_details = self._soup.find('div', {'data-store-id': 'store_{}'.format(self.store_id)})
        if store_details:
            address = store_details.find('div', {'class': 'location'})
            self.store_zip_code = address.text.strip().split(',')[-1].strip().split(' ')[-1]
        return self.store_zip_code
    
    def get_store_country_code(self):
        store_details = self._soup.find('div', {'data-store-id': 'store_{}'.format(self.store_id)})
        if store_details:
            address = store_details.find('div', {'class': 'location'})
            self.store_country_code = address.text.strip().split(',')[-1].strip().split(' ')[0]
        return self.store_country_code
    
    def get_store_capabilities(self):
        return self.store_capabilities
    
    def get_lattitude(self):
        store_details = self._soup.find('div', {'data-store-id': 'store_{}'.format(self.store_id)})
        if store_details:
            for gmap in store_details.find_all('div', {'class': 'detailRow'}):
                for mapurl in gmap.find_all('a'):
                    href = mapurl.get('href')
                    if href:
                        if 'maps.google.com' in href:
                            [self.lattitude, self.longitude] = href.split('&')[-1].replace('saddr=', '').split(',')
                            break
        return self.lattitude
    
    def get_longitude(self):
        return self.longitude

