from lxml import html
from requests_html import HTMLSession
import csv
from datetime import datetime


def runScraper():
    session = HTMLSession()
    nextYear = datetime.now().year + 1
    carBrands = ["ford", "toyota", "chevrolet", "chev", "chevy", "honda", "jeep", "hyundai", "subaru",
                 "kia", "gmc", "ram", "dodge", "mercedes-benz", "mercedes", "mercedesbenz",
                 "volkswagen", "vw", "bmw", "saturn", "land rover", "landrover", "pontiac",
                 "mitsubishi", "lincoln", "volvo", "mercury", "harley-davidson", "harley",
                 "rover", "buick", "cadillac", "infiniti", "infinity", "audi", "mazda", "chrysler",
                 "acura", "lexus", "nissan", "datsun", "jaguar", "alfa", "alfa-romeo", "aston", "aston-martin",
                 "ferrari", "fiat", "hennessey", "porsche", "noble", "morgan", "mini", "tesla"]

    citiesList = [('https://losangeles.craigslist.org', 'los angeles', 'ca'), ('https://newyork.craigslist.org', 'new york city', 'ny')]
    cars = []
    for city in citiesList:
        scrapedInCity = 0
        empty = False
        while not empty:
            print(f"Gathering entries {scrapedInCity} through {scrapedInCity + 120}")

            try:
                searchUrl = f"{city[0]}/d/cars-trucks/search/cta?s={scrapedInCity}"
                page = session.get(searchUrl)
            except Exception as e:
                print(f"Failed to reach {searchUrl}, entries have been dropped: {e}")
                scrapedInCity += 120
                continue

            scrapedInCity += 120
            tree = html.fromstring(page.content)

            vehicles = tree.xpath('//a[@class="result-image gallery"]')
            if len(vehicles) == 0:
                empty = True
                continue

            vehiclesList = []
            for item in vehicles:
                vehicleDetails = []
                vehicleDetails.append(item.attrib["href"])
                try:
                    vehicleDetails.append(item[0].text)
                except:
                    continue
                vehiclesList.append(vehicleDetails)

            for item in vehiclesList:
                url = item[0]
                vehicleDict = {}
                vehicleDict["price"] = int(item[1].replace(",", "").strip("$"))
                try:
                    page = session.get(url)
                    tree = html.fromstring(page.content)
                except:
                    print(f"Failed to reach {url}, entry has been dropped")
                    continue
                attrs = tree.xpath('//span//b')
                for item in attrs:
                    try:
                        k = item.getparent().text.strip()
                        k = k.strip(":")
                    except:
                        k = "model"
                    try:
                        vehicleDict[k] = item.text.strip()
                    except:
                        continue

                price = None
                year = None
                manufacturer = None
                model = None
                odometer = None
                transmission = None
                if "price" in vehicleDict:
                    try:
                        price = int(vehicleDict["price"])
                    except Exception as e:
                        print(f"Could not parse price: {e}")
                if "odomoter" in vehicleDict:
                    try:
                        odometer = int(vehicleDict["odometer"])
                    except Exception as e:
                        print(f"Could not parse odometer: {e}")
                if "model" in vehicleDict:
                    try:
                        year = int(vehicleDict["model"][:4])
                        if year > nextYear:
                            year = None
                    except:
                        year = None
                    model = vehicleDict["model"][5:]
                    foundManufacturer = False
                    for word in model.split():
                        if word.lower() in carBrands:
                            foundManufacturer = True
                            model = ""
                            # resolve conflicting manufacturer titles
                            manufacturer = word.lower()
                            if manufacturer == "chev" or manufacturer == "chevy":
                                manufacturer = "chevrolet"
                            if manufacturer == "mercedes" or manufacturer == "mercedesbenz":
                                manufacturer = "mercedes-benz"
                            if manufacturer == "vw":
                                manufacturer = "volkswagen"
                            if manufacturer == "landrover":
                                manufacturer = "land rover"
                            if manufacturer == "harley":
                                manufacturer = "harley-davidson"
                            if manufacturer == "infinity":
                                manufacturer = "infiniti"
                            if manufacturer == "alfa":
                                manufacturer = "alfa-romeo"
                            if manufacturer == "aston":
                                manufacturer = "aston-martin"
                            continue
                        if foundManufacturer:
                            model = model + word.lower() + " "
                    model = model.strip()

                if "odometer" in vehicleDict:
                    odometer = vehicleDict["odometer"]

                if "transmission" in vehicleDict:
                    transmission = vehicleDict["transmission"]
                print([city[2], city[1], year, manufacturer, model, price, odometer, transmission])
                cars.append([city[2], city[1], year, manufacturer, model, price, odometer, transmission])

    fields = ["state", "region", "years", "manufacturer", "model", "price", "odometer", "transmission"]
    with open("CraigslistScraper", "w") as f:
        w = csv.writer(f)
        w.writerow(fields)
        w.writerows(cars)
def main():
    runScraper()

if __name__ == "__main__":
    main()