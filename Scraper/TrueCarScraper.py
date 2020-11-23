import time

import requests
import numpy as np
import pandas as pd
import lxml.html as lxl
import multiprocessing
from multiprocessing import Pool

def get_urls(number_of_page = 1):

    urls = []
    city_urls = ['https://www.truecar.com/used-cars-for-sale/listings/location-los-angeles-ca/?searchRadius=10',
                 'https://www.truecar.com/used-cars-for-sale/listings/location-new-york-ny/?searchRadius=10']

    for page_number in range(1, number_of_page + 1):
        for city_url in city_urls:
            response = requests.get(city_url + '&page=' + str(page_number))
            root = lxl.fromstring(response.content)
            url = ['https://www.truecar.com' + link for link in root.xpath('//div[@data-qa="Listings"]//a/@href')]
            urls += url
    return urls

def isExist(data):
    return "" if len(data) else data[0]

def get_TrueCar(url):
    response = requests.get(url)
    root = lxl.fromstring(response.content)

    if len(root.xpath('//div[@data-qa="VdpGallery"]//div[@class="col-12"]//img/@src')) == 0:
        image = ""
    else:
        image = root.xpath('//div[@data-qa="VdpGallery"]//div[@class="col-12"]//img/@src')[0][:-6] + "360.jpg"

    year = root.xpath('//div[@class="text-truncate heading-3 margin-right-2 margin-right-sm-3"]/text()')[0].split(' ')[0]
    make = root.xpath('//div[@class="text-truncate heading-3 margin-right-2 margin-right-sm-3"]/text()')[0].split(' ')[1]
    model = root.xpath('//div[@class="text-truncate heading-3 margin-right-2 margin-right-sm-3"]/text()')[0].split(' ')[2:]
    sub_model = root.xpath('//div[@class="text-truncate heading-4 text-muted"]/text()')[0]
    city = root.xpath('//span[@data-qa="used-vdp-header-location"]/text()[1]')[0]
    state = root.xpath('//span[@data-qa="used-vdp-header-location"]/text()[3]')[0]
    mileage = root.xpath('//span[@data-qa="used-vdp-header-miles"]/text()[1]')[0]
    if len(root.xpath('//div[@data-qa="PricingBlock"]/div[@data-qa="LabelBlock-text"]/span/text()')) == 0:
        price = 0
    else:
        price = root.xpath('//div[@data-qa="PricingBlock"]/div[@data-qa="LabelBlock-text"]/span/text()')[0]
    transmission = root.xpath('//div[@data-qa="vehicle-overview-item-Transmission"]//li/text()')[0]
    drive_type = root.xpath('//div[@data-qa="vehicle-overview-item-Drive Type"]//li/text()')[0]
    fuel_type = root.xpath('//div[@data-qa="vehicle-overview-item-Fuel Type"]//li/text()')[0]

    return pd.Series({'url': url, "img": image, 'year': year, 'make': make, 'model': model, 'sub_model': sub_model, 'city': city, 'state': state,
                      'mileage': mileage, 'price': price, 'transmission': transmission, 'drive_type': drive_type,
                      'fuel_type': fuel_type})

def scraper(urls):
    scraping_data = [get_TrueCar(url) for url in urls]
    return pd.concat(scraping_data, axis=1).T

def parallelize(urls):
    url_sets = np.array_split(urls, 32)
    pool = Pool(multiprocessing.cpu_count())
    result = pd.concat(pool.map(scraper, url_sets))
    pool.close()
    pool.join()
    return result

def scrapeTrueCar():
    urls = get_urls(150)
    t1 = time.time()
    print("Start scraping", len(urls), "cars")
    TrueCar = parallelize(urls)
    print('用时：', time.time() - t1)
    TrueCar.to_csv('../Data/TrueCar/Raw/usedCarListing-11.22.csv', encoding='utf-8')

if __name__ == '__main__':
    scrapeTrueCar()
