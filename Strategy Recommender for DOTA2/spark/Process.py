from pyspark.sql import SparkSession
from pyspark.sql.types import *
from pyspark.sql.functions import *
import sys
import configparser


config = configparser.ConfigParser()
config.read('config.ini')

spark = SparkSession.builder.appName('DataCleaning').getOrCreate()

mode = "append"
url = "jdbc:postgresql://database-1.celr69plx1mj.us-west-2.rds.amazonaws.com:5432/dodo2db"

properties = {"user": 'postgres',
              "password": 'dPFSTjx2DULScb4Xoo1s',"driver": "org.postgresql.Driver"}

s3_url = "s3a://dotamatches/yasp-dump-2015-12-18.json"
selected_column_name_list = ['match_id', 'picks_bans', 'radiant_win']

raw_df = spark.read.json(s3_url)

df_with_selected_cols = raw_df.select(selected_column_name_list)
df_filter_na = df_with_selected_cols.na.drop()
df_filter_na.show(5)
df_filter_na.write.jdbc(url=url, table="listing_" + city, mode=mode, properties=properties)

parquet_file_name = 's3n://dotamatches/master.parquet'
df_filter_na.write.mode(mode).parquet(parquet_file_name)
