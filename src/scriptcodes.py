import requests
import csv
import sqlite3
from trade_logging import get_logger
import pandas as pd

logger = get_logger('trade_logs')

def get_response():
    url = "https://Openapi.5paisa.com/VendorsAPI/Service1.svc/ScripMaster/segment/nse_eq"
    
    logger.info('fetching script data')
    response = requests.get(url)
    response.raise_for_status()  # raise an exception if the request failed
    logger.info('successfully fetched script data')
    return response.text

def save_to_table(db_name, data):
    with sqlite3.connect(db_name) as conn:
        c = conn.cursor()

        # Create the table if it doesn't exist
        c.execute(''' DROP TABLE IF EXISTS script_data;''')
        c.execute('''
            CREATE TABLE IF NOT EXISTS script_data (
                Exch TEXT,
                ExchType TEXT,
                ScripCode TEXT,
                Name TEXT ,
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
                Series TEXT
            )
        ''')
        logger.info('Created table in database')

        # Parse the CSV data and insert it into the table
        reader = csv.reader(data.splitlines())
        header = next(reader)  # skip the header row
        rows = [row for row in reader]
        c.executemany('''
            INSERT INTO script_data VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', rows)
        logger.info('Inserted data into table')

def save_to_csv(db_name, csv_filename):
    with sqlite3.connect(db_name) as conn:
        c = conn.cursor()

        # Fetch data from the script_data table
        c.execute("SELECT * FROM script_data")
        rows = c.fetchall()

        # Get the column names
        column_names = [description[0] for description in c.description]

        # Convert the data to a pandas DataFrame
        df = pd.DataFrame(rows, columns=column_names)

        # Save the DataFrame to a CSV file
        df.to_csv(csv_filename, index=False)
        logger.info(f'Data successfully saved to {csv_filename}')

# Example usage
response_data = get_response()
save_to_table('trade_db.db', response_data)
save_to_csv('trade_db.db', 'script_data_fo.csv')
