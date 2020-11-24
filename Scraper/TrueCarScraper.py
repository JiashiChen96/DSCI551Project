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
    return "" if len(data) == 0 else data[0]

def get_TrueCar(url):
    print(url)
    response = requests.get(url)
    root = lxl.fromstring(response.content)

    image = isExist(root.xpath('//div[@data-qa="VdpGallery"]//div[@class="col-12"]//img/@src'))
    if image != "": image = image[:-6]+ "360.jpg"

    title = isExist(root.xpath('//div[@class="text-truncate heading-3 margin-right-2 margin-right-sm-3"]/text()'))
    if title == "":
        year = ""
        make = ""
        model = ""
    else:
        year = title.split(' ')[0]
        make = title.split(' ')[1]
        model = title.split(' ')[2:]

    sub_model = isExist(root.xpath('//div[@class="text-truncate heading-4 text-muted"]/text()'))
    city = isExist(root.xpath('//span[@data-qa="used-vdp-header-location"]/text()[1]'))
    state = isExist(root.xpath('//span[@data-qa="used-vdp-header-location"]/text()[3]'))
    mileage = isExist(root.xpath('//span[@data-qa="used-vdp-header-miles"]/text()[1]'))
    price = isExist(root.xpath('//div[@data-qa="PricingBlock"]/div[@data-qa="LabelBlock-text"]/span/text()'))
    transmission = isExist(root.xpath('//div[@data-qa="vehicle-overview-item-Transmission"]//li/text()'))
    drive_type = isExist(root.xpath('//div[@data-qa="vehicle-overview-item-Drive Type"]//li/text()'))
    fuel_type = isExist(root.xpath('//div[@data-qa="vehicle-overview-item-Fuel Type"]//li/text()'))

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
    urls = get_urls(100)
    t1 = time.time()
    print("Start scraping", len(urls), "cars")
    TrueCar = parallelize(urls)
    print('用时：', time.time() - t1)
    TrueCar.to_csv('../Data/TrueCar/Raw/usedCarListing-11.22.csv', encoding='utf-8')

if __name__ == '__main__':
    scrapeTrueCar()
