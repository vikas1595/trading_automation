import pandas as pd

def readexcel(filepath:str,sheet_name:str):
    dtypes={
    "segment": str,
    "option_price": int,
    "strike_price": int,
    "type": str,
    "exp_date": str,
    "script_code": str,
    "sr_no": int,
    "symbol": str,
    "ltp": float,
    "qty": int,
    "lot_size": int,
    "entry_signal": bool,
    "exit_signal": bool,
    "entry": str,
    "entry_price": float,
    "stop_loss": float,
    "target": float,
    "exit": bool,
    "exit_price": float,
    "manual_exit": bool
}



    pdf=pd.read_excel(filepath,sheet_name,header=0).dropna(subset=["entry_signal"])
    pdf=pdf.astype(dtypes)
    return pdf

def entry_signals()->dict:
    """Filter DataFrame rows where Entry_Signal is True and select specific columns."""
    
    df=readexcel('./5paisatrade_new.xlsm',sheet_name='Trade')
    filtered_df = df[df["entry_signal"]]  # Filter rows where Entry_Signal is True
    selected_columns = ([ "symbol", "lot_size", "entry_signal", "stop_loss", "target",
                         "script_code","qty"])  # Define the columns to select
    filtered_df = filtered_df[selected_columns]  # Select the desired columns
    return filtered_df.to_dict(orient='records')

