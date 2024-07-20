import requests
import csv
import sqlite3
from trade_logging import get_logger
logger=get_logger('trade_logs')
def get_response():
    url = "https://Openapi.5paisa.com/VendorsAPI/Service1.svc/ScripMaster/segment/nse_fo"
    
    logger.info('fetching script data')
    response = requests.get(url)
    response.raise_for_status()  # raise an exception if the request failed
    logger.info('successfully fetched script data')
    return response.text

def save_to_table(db_name, data):
    
    conn = sqlite3.connect(db_name)
    c = conn.cursor()

    # Create the table if it doesn't exist
    c.execute("DROP TABLE IF EXISTS script_data;")
    c.execute('''
              CREATE TABLE IF NOT EXISTS script_data
                 (Exch TEXT ,
                  ExchType TEXT,
                  ScripCode TEX ,
                  Name TEXT PRIMARY KEY,
                  Expiry TEXT,
                  ScripType TEXT,
                  StrikeRate REAL,
                  FullName TEXT,
                  TickSize REAL,
                  LotSize INTEGER,
                  QtyLimit INTEGER,
                  Multiplier REAL,
                  SymbolRoot TEXT,
                  BOCOAllowed TEXT,
                  ISIN TEXT,
                  ScripData TEXT,
                  Series TEXT)''')
    logger.info('Created table in database')
    # Parse the CSV data and insert it into the table
    reader = csv.reader(data.splitlines())
    header = next(reader)  # skip the header row
    for row in reader:
        c.execute('''INSERT INTO script_data VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''', row)
    logger.info('Inserted data into table')

    conn.commit()
    conn.close()
    logger.info('Closed database connection')

data = get_response()
save_to_table('vikas_db.db', data)


