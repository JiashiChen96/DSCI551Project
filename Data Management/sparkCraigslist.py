from pyspark.sql import SparkSession
from pyspark.sql import functions as F
from pyspark.sql.functions import regexp_replace


def dataClean():
    spark = SparkSession.builder.appName("DSCI551Project").getOrCreate()
    Craigslist = spark.read.csv("../Data/Craigslist/Raw/used_cars.csv", header=True)
    Craigslist = Craigslist.select("region", F.col("years").alias("year"), "manufacturer",
                                   "model", "price", F.col("odometer").alias("mileage"), "transmission")
    Craigslist = Craigslist.filter((Craigslist.manufacturer != 'NULL') & (Craigslist.mileage != 'NULL') &
                                   (Craigslist.transmission != 'NULL') & (Craigslist.model != ''))
    Craigslist = Craigslist.filter(Craigslist.price != 0)
    Craigslist.show()

    Craigslist.write.save("../Data/Craigslist/SparkOutput", format("csv"), mode='overwrite', header=True)

if __name__ == '__main__':
    dataClean()
