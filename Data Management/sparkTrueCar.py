from pyspark.sql import SparkSession
from pyspark.sql.functions import regexp_replace
from pyspark.sql import functions as F


def dataClean():
    spark = SparkSession.builder.appName("DSCI551Project").getOrCreate()
    TrueCar = spark.read.csv("../Data/TrueCar/Raw/usedCarListing-11.21.csv", header=True)
    TrueCar = TrueCar.select("state", "year", F.col("make").alias("manufacturer"), regexp_replace("model", "\W+", "").alias("model"),
                             regexp_replace("price", "\W+", "").alias("price"),
                             regexp_replace("mileage", "\W+", "").alias("mileage"), "transmission", "url", "img")
    # TrueCar.show()
    TrueCar.write.save("../Data/TrueCar/SparkOutput", format("csv"), mode='overwrite', header=True)


if __name__ == '__main__':
    dataClean()
