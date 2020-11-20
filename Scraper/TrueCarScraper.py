import requests
import numpy as np
import pandas as pd
import lxml.html as lxl

MAX_PAGE = 100

## Get all the urls for all the listed used vehicles on truecar.com
def urls_scraping(base_url='https://www.truecar.com/used-cars-for-sale/listings/location-los-angeles-ca/?searchRadius=10'):
    urls = []
    pages = []
    base_urls = ['https://www.truecar.com/used-cars-for-sale/listings/location-los-angeles-ca/?searchRadius=10',
                 'https://www.truecar.com/used-cars-for-sale/listings/location-new-york-ny/?searchRadius=10']
    for base_url in base_urls:
        for i in range(1, MAX_PAGE + 1):
            pages.append(base_url + '&page=' + str(i))
        for page in pages:
            try:
                response = requests.get(page)
                response.raise_for_status()
            except:
                break
            root = lxl.fromstring(response.content)
            url = ['https://www.truecar.com' + link for link in root.xpath('//div[@data-qa="Listings"]//a/@href')]
            urls += url

    return urls


# function to scrape one single url of a single used car listing.
def page_scraping(url):
    # print(url)
    try:
        response = requests.get(url)
        response.raise_for_status()
    except:
        return
    root = lxl.fromstring(response.content)

    # extract vehicle year, make and model information
    year = root.xpath('//div[@class="text-truncate heading-3 margin-right-2 margin-right-sm-3"]/text()')[0].split(' ')[
        0]
    make = root.xpath('//div[@class="text-truncate heading-3 margin-right-2 margin-right-sm-3"]/text()')[0].split(' ')[
        1]
    model = root.xpath('//div[@class="text-truncate heading-3 margin-right-2 margin-right-sm-3"]/text()')[0].split(' ')[
            2:]
    # need to extract vehicle type (suv or sedan) and sub-model info
    sub_model = root.xpath('//div[@class="text-truncate heading-4 text-muted"]/text()')[0]

    # city and state, geospatial information.
    city = root.xpath('//span[@data-qa="used-vdp-header-location"]/text()[1]')[0]
    state = root.xpath('//span[@data-qa="used-vdp-header-location"]/text()[3]')[0]

    # vehicle mileage
    mileage = root.xpath('//span[@data-qa="used-vdp-header-miles"]/text()[1]')[0]

    # vehicle price information
    price = root.xpath('//div[@data-qa="PricingBlock"]/div[@data-qa="LabelBlock-text"]/span/text()')[0]

    # vehicle characteristics
    exterior_color = root.xpath('//div[@data-qa="vehicle-overview-item-Exterior Color"]/div[2]/ul/li/text()')[0]
    interior_color = root.xpath('//div[@data-qa="vehicle-overview-item-Interior Color"]/div[2]/ul/li/text()')[0]
    mpg_city = \
    root.xpath('//div[@data-qa="vehicle-overview-item-MPG"]/div[2]/ul/li/text()')[0].split('/')[0].split(' ')[0]
    mpg_hwy = root.xpath('//div[@data-qa="vehicle-overview-item-MPG"]/div[2]/ul/li/text()')[0].split('/')[1].split(' ')[
        1]
    engine = root.xpath('//div[@data-qa="vehicle-overview-item-Engine"]/div[2]/ul/li/text()')[0]
    transmission = root.xpath('//div[@data-qa="vehicle-overview-item-Transmission"]/div[2]/ul/li/text()')[0]
    drive_type = root.xpath('//div[@data-qa="vehicle-overview-item-Drive Type"]/div[2]/ul/li/text()')[0]
    fuel_type = root.xpath('//div[@data-qa="vehicle-overview-item-Fuel Type"]/div[2]/ul/li/text()')[0]
    popular_feature = root.xpath('//div[@data-test="popularFeatures"]//li[@class="_19zze7p"]/p/text()')

    # vehicle history information, will extract four variables from here.
    vehicle_history = root.xpath('//li[@class="_h9wfdq"]/text()')

    # whether the car is a certified preowned car.
    if "used-vdp-header-cpo" in response.text:
        cpo = True
    else:
        cpo = False

    return pd.Series({'year': year, 'make': make, 'model': model, 'sub_model': sub_model, 'city': city, 'state': state,
                      'mileage': mileage, 'price': price, 'exterior_color': exterior_color,
                      'interior_color': interior_color, 'mpg_city': mpg_city, 'mpg_hwy': mpg_hwy, 'engine': engine,
                      'transmission': transmission, 'drive_type': drive_type, 'fuel_type': fuel_type,
                      'popular_feature': popular_feature, 'vehicle_history': vehicle_history, 'cpo': cpo})

# Use multi-processing to speed up the web-scraping
# fully make use of 8 cores of my macbook pro.
from multiprocessing import Pool
num_partitions = 32
num_cores = 8
def parallelize(urls, func):
    url_set = np.array_split(urls, num_partitions)
    print("#")
    pool = Pool(num_cores)
    print("@")
    df = pd.concat(pool.map(func, url_set))
    print("&")
    pool.close()
    pool.join()
    return df
# main function to scrape all the urls and merge all the data into one dataframe
def scraping(urls):
    scraping_data = [page_scraping(url) for url in urls]
    return pd.concat(scraping_data, axis=1).T

if __name__ == '__main__':
    urls=urls_scraping() # extract all vehicle urls from allowed 333 pages.
    print(len(urls))
    cars = scraping(urls)
    cars.to_csv('../Data/TrueCar/usedCarListing-11.18.csv', encoding='utf-8')