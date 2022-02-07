#!/usr/bin/env python


import pandas as pd
import pyodbc
import urllib
from sqlalchemy import create_engine
import psycopg2 
import os
import logging


# Set Logging configuration
logfilename = os.environ['Logfilename']

for handler in logging.root.handlers[:]:
	logging.root.removeHandler(handler)
logging.basicConfig(filename = logfilename)
logger = logging.getLogger()
logger.setLevel(logging.INFO)
logger.info("=================================================================")
logger.info("BTC Log Started " )
logger.info("=================================================================")
logger.info("")

# Reading BTC price variation JSON
try:
    df_btc_raw_data = pd.read_json('http://cf-code-challenge-40ziu6ep60m9.s3-website.eu-central-1.amazonaws.com/ohlcv-btc-usd-history-6min-2020.json')
except:
    logger.error("Error in reading BTC price variation")
else:
    logger.info("BTC price variation is successfully read")

# Set the PostgreSql database credentials from environment variables
logger.info("reading environment variables")
db_database = os.environ['db_database']
db_host = os.environ['db_host']
db_port = os.environ['db_port']
db_pwd = os.environ['db_pwd']  
db_username = os.environ['db_username']

# create the database connection string for the PostgreSql database
logger.info("Building database connection string")
con_str = f"postgresql+psycopg2://{db_username}:{db_pwd}@{db_host}:{db_port}/{db_database}"

# Connecting to PostgreSql database
logger.info("connecting to PostgreSql database")
try:
    engine = create_engine(con_str)
except:
    logger.error("Error in connecting to PostgreSql database")
else:
    logger.info("Successfully connected to PostgreSql database")

# Writing the BTC Price variation data to BTC_Price_variation table BTC_Price_variation
try:
    df_btc_raw_data.to_sql('BTC_Price_variation', engine)
except:
    logger.error("Error writing to table BTC_Price_variation")
else:
    logger.info("Successfully written the BTC Price variation data to BTC_Price_variation table BTC_Price_variation")

# Creating a new column price_date in the dataframe
df_btc_raw_data['price_date'] = pd.to_datetime(df_btc_raw_data['time_open']).apply(lambda x: x.date())

df_btc_raw_data.set_index("price_date", inplace = True)

logger.info("Calculating price volatality metric")
# Creating an empty dataframe to store the price volatality metric
df_btc_agg = pd.DataFrame()

# Calculating the standard deviation, max, min and mean values for a day
df_btc_agg['price_std'] = df_btc_raw_data.groupby('price_date')['price_close'].std()
df_btc_agg['price_max'] = df_btc_raw_data.groupby('price_date')['price_close'].max()
df_btc_agg['price_min'] = df_btc_raw_data.groupby('price_date')['price_close'].min()
df_btc_agg['price_avg'] = df_btc_raw_data.groupby('price_date')['price_close'].mean()

# Writing the price volatality metric to the PostgreSQl database table BTC_Price_variation_agg
try:
    df_btc_raw_data.to_sql('BTC_Price_variation_agg', engine)
except:
    logger.error("Error writing to table BTC_Price_variation_agg")
else:
    logger.info("Successfully written the BTC Price volatality metric data to BTC_Price_variation_agg table ")





