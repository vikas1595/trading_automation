import pandas as pd
import xlwings as xw
from exceldata import readexcel

def place_order(symbol, qty):
    # This is a mock function to simulate placing an order with the broker.
    # In real scenarios, this function would interact with the broker's API.
    import random
    exch_order_id = random.randint(100000, 999999)
    entry_price = random.uniform(100, 500)
    return exch_order_id, entry_price

def update_excel(file_path, updates):
    wb = xw.Book(file_path)
    sheet = wb.sheets.active
    for update in updates:
        row = update['row']
        exch_order_id = update['exchorderid']
        entry_price = update['entry_price']
        
        sheet.range(f'O{row}').value = exch_order_id  # Update ExchOrderID column (15th column, O)
        sheet.range(f'P{row}').value = entry_price    # Update Entry Price column (16th column, P)

    wb.save(file_path)
    wb.close()
    print(f"Updated Excel file saved to {file_path}")
    

def process_trades(file_path):
    df = readexcel(file_path,sheet_name="Trade")
    # Filter records with Entry Signal TRUE
    entry_signal_df = df[df["entry_signal"]] 

    updates = []

    # Loop through the filtered records and place orders
    for index, row in entry_signal_df.iterrows():
        symbol = row['symbol']
        qty = row['qty']
        exch_order_id, entry_price = place_order(symbol, qty)
        
        # Append the updates for each row
        updates.append({
            'row': index + 2,  # Excel rows are 1-indexed, and there's a header row
            'exchorderid': exch_order_id,
            'entry_price': entry_price,
            "entry_signal":False
        })
    
    # Update the Excel file with the specific cell updates
    update_excel(file_path, updates)

# Example usage
file_path = './5paisatrade_new.xlsm'
process_trades(file_path)
