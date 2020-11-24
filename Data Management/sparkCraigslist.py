from pyspark.sql import SparkSession
from pyspark.sql import functions as F
from pyspark.sql.functions import regexp_replace


def dataClean():
    spark = SparkSession.builder.appName("DSCI551Project").getOrCreate()
    Craigslist = spark.read.csv("../Data/Craigslist/Raw/CraigslistScraper.csv", header=True)
    Craigslist = Craigslist.select("state", "city", F.col("years").alias("year"), "manufacturer",
                                   "model", "price", F.col("odometer").alias("mileage"), "cylinders", "drive", "fuel", "transmission", "url", "image_url")
    Craigslist = Craigslist.filter((Craigslist.manufacturer != 'NULL') & (Craigslist.mileage != 'NULL') &
                                   (Craigslist.transmission != 'NULL') & (Craigslist.model != '') &
                                   (Craigslist.cylinders != 'NULL') & (Craigslist.fuel != 'NULL') &
                                   (Craigslist.price > 1000) & (Craigslist.drive != 'NULL'))
    Craigslist = Craigslist.filter(Craigslist.price != 0)
    Craigslist.show()

    Craigslist.write.save("../Data/Craigslist/SparkOutput", format("csv"), mode='overwrite', header=True)

if __name__ == '__main__':
    dataClean()
