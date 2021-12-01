import os
import re
import time
import sys
import argparse
from datetime import datetime

dir_path = os.path.dirname(os.path.realpath(__file__))
DRIVER_PATH = dir_path + '/chromedriver'

# For headless
from selenium import webdriver   # for webdriver
from bs4 import BeautifulSoup
import threading, queue

option = webdriver.ChromeOptions()
option.add_argument('headless')
driver = webdriver.Chrome(DRIVER_PATH, options=option)
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

s = Service(ChromeDriverManager().install())

from config import MAX_PAGINATION, OFFSET, WEB_URL, NUM_THREADS, PRODUCT_FILENAME, PRODUCT_PRICE_FILENAME, STORE_FILENAME
from parser import ParseProductDetails, ParseProductPrices, ParseStores
from util import write_details_to_csv

# Define Queue
q = queue.Queue(2 * NUM_THREADS)
threadLock = threading.Lock()


def get_page_source(url):
    try:
        driver = webdriver.Chrome(service=s)
        driver.get(url)
        # driver.implicitly_wait(10)
        page_source = driver.page_source
        # Beautiful Soup is a Python library for pulling data out of HTML or XML files
        soup = BeautifulSoup(page_source, 'html.parser')
        driver.quit()
        return soup
    except Exception:
        return None


def parse_product_details_by_url(product_url):
    """ Accept list of product urls and writes to csv file """
    try:
        product, store_price = get_product_details(product_url)
        print("*" * 100)
        print("PRODUCT DETAILS")
        print(product)
        print("*" * 100)
        print("*" * 100)
        print("STORE PRICE DETAILS")
        print(store_price)
        print("*" * 100)
        return product, store_price
    except Exception as e:
        print('*************** Product Details url exception *************')
        print("++++++++++++++ Product Details Page Exception +++++++++++++++++++")
        print(e)
        pass


def get_product_details(item_url):
    """ Get or scrape product details """
    try:

        product_details = {}
        store_price_details = {}
        soup = get_page_source(item_url)
        if soup:
            product = ParseProductDetails(soup)
            product_details = {
                "product_id": product.get_product_id(),
                "product_cart_id": product.get_product_id(),
                "product_name": product.get_product_name(),
                "product_desc": product.get_description(),
                "category": product.get_categories(),
                "brand": product.get_brand(),
                "model_number": product.get_model_number(),
                "price_currency": product.get_currency(),
                "sale_price": product.get_price(),
                "product_url": item_url,
                "large_img_url": product.get_large_img(),
                "small_img_url": product.get_small_img(),
                "stock_status": product.get_product_availability(),
                "condition": "NEW",
                "attribute_names": product.get_attribute_names(),
                "attribute_values": product.get_attribute_values()
            }

            # Get store details for that product
            storeprice = ParseProductPrices(soup)
            store_price_details = {
                "product_id": product_details.get('product_id'),
                "store_id": storeprice.get_store_id(),
                "sale_price": storeprice.get_sale_price(),
                "price_currency": storeprice.get_price_currency(),
                "stock_status": storeprice.get_stock_status(),
                "stock_count": storeprice.get_stock_count()
            }
            print(store_price_details)

        return product_details, store_price_details
    except Exception as e:
        print('*************** Product Url exception *************')
        print("++++++++++++++ Product Page Exception +++++++++++++++++++")
        print(e)
        pass


def get_product_price_details(soup):
    """ Get or scrape product details """
    try:
        store_price_details = {}
        if soup:
            storeprice = ParseProductPrices(soup)
            store_price_details = {
                "product_id": storeprice.get_product_id(),
                "store_id": storeprice.get_store_id(),
                "sale_price": storeprice.get_sale_price(),
                "price_currency": storeprice.get_price_currency(),
                "stock_status": storeprice.get_stock_status(),
                "stock_count": storeprice.get_stock_count()
            }
            print(store_price_details)
            return store_price_details if store_price_details else {}
        return store_price_details
    except Exception as e:
        print('*************** Product Url exception *************')
        print("++++++++++++++ Product Page Exception +++++++++++++++++++")
        print(e)
        pass


def get_product_price_details(item_url):
    """ Get or scrape product details """
    try:

        store_price_details = {}
        soup = get_page_source(item_url)
        if soup:
            storeprice = ParseProductPrices(soup)
            store_price_details = {
                "product_id": storeprice.get_product_id(),
                "store_id": storeprice.get_store_id(),
                "sale_price": storeprice.get_sale_price(),
                "price_currency": storeprice.get_price_currency(),
                "stock_status": storeprice.get_stock_status(),
                "stock_count": storeprice.get_stock_count()
            }
            print(store_price_details)
            return store_price_details if store_price_details else {}
        return store_price_details
    except Exception as e:
        print('*************** Product Url exception *************')
        print("++++++++++++++ Product Page Exception +++++++++++++++++++")
        print(e)
        pass

def parse_by_dept_page(departments):
    try:
        products_urls = []
        for url in departments:
            print("Dept Main URL:", url)
            # for page in range(0, OFFSET*MAX_PAGINATION, OFFSET):
                # soup = get_page_source(url + '?offset={}'.format(page))
            soup = get_page_source(url)
            if soup:
                for items in soup.find_all("div", {"id": "listItems"}):
                    for item in items.find_all('div', attrs={'class': 'List'}):
                        item_url = WEB_URL + item.next.get('href')[1:]
                        products_urls.append(item_url)
        print(products_urls)
        print("Total products urls:", len(products_urls))
        product_details = []
        store_price_details = []
        for prod_detail_url in products_urls:
            # q.put(prod_detail_url)
            product, store_price = parse_product_details_by_url(prod_detail_url)
            if product:
                product_details.append(product)
            if store_price:
                store_price_details.append(store_price)
        
        # Finally write product details to csv
        print(len(product_details), 'product_details length')
        write_details_to_csv(PRODUCT_FILENAME, product_details)

        # Finally write product price details to csv
        print(len(store_price_details), 'store_price_details length')
        write_details_to_csv(PRODUCT_PRICE_FILENAME, store_price_details)

    except Exception as e:
        print('*************** Department Url exception *************')
        print("++++++++++++++ Department Page Exception +++++++++++++++++++")
        print(e)
        pass


def parse_all_departments(departments_urls):
    departments = []
    for each_dept_link in departments_urls:
        departments.append(each_dept_link)
    
    parse_by_dept_page(departments[:1])


def parse_all_stores(stores_url):
    store_details = []
    for store_url in stores_url:
        store = parse_store_details(store_url)
        if store:
            store_details.append(store)
    
    if store_details:
        # Finally write store details to csv
        print(len(store_details), 'store_details length')
        write_details_to_csv(STORE_FILENAME, store_details)


def parse_store_details(stores_url):
    """ Parse/get all stores details """
    try:
        store_details = {}
        soup = get_page_source(stores_url)
        if soup:
            store = ParseStores(soup)
            store_details = {
                "store_id": store.get_store_id(),
                "store_name": store.get_store_name(),
                "store_address": store.get_store_address(),
                "store_zip_code": store.get_store_zip_code(),
                "store_country_code": store.get_store_country_code(),
                "store_capabilities": store.get_store_capabilities(),
                "lattitude": store.get_lattitude(),
                "longitude": store.get_longitude()
            }
            print(store_details)
        return store_details
    except Exception as e:
        print('*************** Store Url exception *************')
        print("++++++++++++++ Store Page Exception +++++++++++++++++++")
        print(e)
        pass
    


# def dowork(q):
#     while True:
#         try:
#             url = q.get()
#             # logging.info('******************* current url:\t' + url)
#             parse_product_details_by_url(url)
#             q.task_done()
#         except Exception as e:
#             q.task_done()

if __name__ == '__main__':
    try:
        starttime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        # print("Initializing Threads")
        # for i in range(1, NUM_THREADS):
        #     worker = threading.Thread(target=dowork, args=(q,))
        #     worker.setDaemon(True)
        #     worker.start()
        # q.join()
        # time.sleep(1)

        parser = argparse.ArgumentParser(formatter_class=argparse.RawTextHelpFormatter)
        parser.add_argument('-target', required=False, type=str,
            default='store', help="Value can be product, store. 'product' means product and price details, 'store' means all store details")

        args = parser.parse_args()
        argsdict = vars(args)

        if (argsdict['target'] not in ('product','store')):
            parser.error("This can be either product or price")

        if argsdict['target'] == 'product':
            department_url = WEB_URL + "c/Departments"
            soup = get_page_source(department_url)
            department_urls = []
            all_departments = soup.find_all("div", {"class": "departments-list"})
            for department in all_departments:
                links = department.find_all("ul", {"class": "department-links"})
                for link in links:
                    if link.find('a').get('href'):
                        each_dept_link = WEB_URL + link.find('a').get('href')[1:]
                        department_urls.append(each_dept_link)
            
            print("All Depts")
            print(department_urls)
            print("Total depts", len(department_urls))
            parse_all_departments(department_urls)
        else:
            # Parse store details
            store_url = WEB_URL + "Lowes-Stores"
            soup = get_page_source(store_url)
            store_urls = []
            all_states_urls = []
            for store in soup.find_all("div", {"class": "sc-AxirZ bGzFyx"}):
                for store in store.find_all("a"):
                    each_state_link = WEB_URL + store.get('href')[1:]
                    all_states_urls.append(each_state_link)

            print("*" * 100)
            print(all_states_urls, "all_states_urls")
            print(len(all_states_urls), "all_states_urls Length")
            print("*" * 100)
            store_urls = []
            for state_url in all_states_urls:
                soup = get_page_source(state_url)
                cities = soup.find_all('div', attrs={'class': 'city-name'})
                for city in cities:
                    if city.find("a"):
                        each_city_link = WEB_URL + city.find("a").get('href')[1:]
                        store_urls.append(each_city_link)
                parse_all_stores(store_urls)
                store_urls = []

        endtime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        driver.close()
        print("Scripts Starts at: ", starttime)
        print("Scripts Ends at: ", endtime)
    except KeyboardInterrupt:
        driver.close()
        sys.exit()
    except Exception as e:
        driver.close()
        print('*************** Main Url exception *************')
        print("++++++++++++++ Main Page Exception +++++++++++++++++++")
        print(e)
        pass


