import re
from lxml import html
from requests_html import HTMLSession
import mysql.connector

def cities():
    conn = mysql.connector.connect(host='localhost',
                                   user='root',
                                   password='root',
                                   database='used_cars')
    curs = conn.cursor()
    curs.execute("DROP TABLE IF EXISTS cities")
    curs.execute("CREATE TABLE IF NOT EXISTS cities(citystate VARCHAR(255) PRIMARY KEY, cityURL VARCHAR(255), cityTitle VARCHAR(255), stateCode VARCHAR(255))")

    #request
    req = HTMLSession()
    states = ["ca","ny"]
    for state in states:
        url = "https://geo.craigslist.org/iso/us/" + state
        print("Fetching from " + url)
        origin = req.get(url)
        tree = (html.fromstring(origin.content))
        # print(origin.url.split("/"))
        if origin.url.split("/")[-1] != state:
            name = tree.xpath("//div[@class='regular-area']//h2[@class='area']")[0].text
            curs.execute(f'''INSERT INTO cities VALUES('{name + state}','{origin.url}', '{name}', '{state}')''')


        else:
            # cities = list of elements for each region
            cities = tree.xpath('//ul[contains(concat( " " , @class, " "), " geo-site-list ")]//li//a')

            # major cities are presented in bold text, this must be handled
            boldAt = 0
            for item in cities:
                name = item.text
                # if name == None, text is in bold
                if name == None:
                    name = item.xpath("//b")[boldAt].text
                    boldAt += 1
                if not re.match(r"[a-z]*, [A-Z]*", name):
                    # insert url and city name, easy stuff
                    name = name.replace("'", "''")
                    link = item.attrib['href']
                    # there are some suburbs of cities in different states with weird cars+trucks / housing links, ignore those.
                    if link[:4] != "http":
                        continue

                    curs.execute(f'''INSERT INTO cities VALUES('{name + state}','{link}', '{name}', '{state}')''')
    conn.commit()
    count = curs.execute("SELECT Count(*) FROM cities")
    print("{} regions added to database".format(curs.fetchall()[0][0]))
    conn.close()


def main():
    cities()

if __name__ == "__main__":
    main()

