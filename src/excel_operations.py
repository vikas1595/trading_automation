import pandas as pd
import xlwings as xw

def readexcel(filepath:str,sheet_name:str):
    dtypes={
        "segment":str,
        "option_price":int,
        "strike_price":int,
        "Type":str,
        "EXP date":str,
        "Scriptcode":str,
        "combined":str,
        "Sr No": int,
        "Symbol":str,
        "Ltp":float,
        "Qty":int,
        "Entry Signal":bool,
        "Exit Signal":bool,
        "Entry":str,
        "ExchOrderID":str,
        "Entry Price":float,
        "Stop Loss": float,
        "Target":float,
        "Exit":bool,
        "Exit Price":float,
        "Manual Exit":bool,
        "Cover Points": str

    }

    pdf=pd.read_excel(filepath,sheet_name,header=0).dropna(subset=["Entry Signal"])
    pdf=pdf.astype(dtypes)
    return pdf

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
        exch_order_id = update['ExchOrderID']
        entry_price = update['Entry Price']
        
        sheet.range(f'O{row}').value = exch_order_id  # Update ExchOrderID column (15th column, O)
        sheet.range(f'P{row}').value = entry_price    # Update Entry Price column (16th column, P)

    wb.save(file_path)
    wb.close()
    print(f"Updated Excel file saved to {file_path}")
    

def process_trades(file_path):
    df = readexcel(file_path,sheet_name="Trade")
    # Filter records with Entry Signal TRUE
    entry_signal_df = df[df["Entry Signal"]] 

    updates = []

    # Loop through the filtered records and place orders
    for index, row in entry_signal_df.iterrows():
        symbol = row['Symbol']
        qty = row['Qty']
        exch_order_id, entry_price = place_order(symbol, qty)
        
        # Append the updates for each row
        updates.append({
            'row': index + 2,  # Excel rows are 1-indexed, and there's a header row
            'ExchOrderID': exch_order_id,
            'Entry Price': entry_price
        })
    
    # Update the Excel file with the specific cell updates
    update_excel(file_path, updates)

# Example usage
file_path = './5paisatrade_new.xlsm'
process_trades(file_path)
