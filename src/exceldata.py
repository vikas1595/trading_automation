import pandas as pd

def readexcel(filepath:str,sheet_name:str):
    dtypes={
        "segment":str,
        "option_price":int,
        "strike_price":int,
        "Type":str,
        "signal":str,
        "script_code":str,
        "Sr_No": int,
        "Symbol":str,
        "Ltp":float,
        "Qty":int,
        "Entry_Signal":bool,
        "Exit_Signal":bool,
        "Entry":str,
        "Entry_Price":float,
        "Stop_Loss": float,
        "Target":float,
        "Exit":bool,
        "Exit_Price":float,
        "Manual_Exit":bool

    }

    pdf=pd.read_excel(filepath,sheet_name,header=0).dropna(subset=["Entry_Signal"])
    pdf=pdf.astype(dtypes)
    return pdf

def entry_signals()->dict:
    """Filter DataFrame rows where Entry_Signal is True and select specific columns."""
    
    df=readexcel('./5paisatrade.xlsm',sheet_name='Trade')
    filtered_df = df[df["Entry_Signal"]]  # Filter rows where Entry_Signal is True
    selected_columns = ["signal", "Symbol", "Ltp", "Entry_Signal", "Stop_Loss", "Target"]  # Define the columns to select
    filtered_df = filtered_df[selected_columns]  # Select the desired columns
    return filtered_df.to_dict(orient='records')

entry_scripts=entry_signals()
print(entry_scripts)
