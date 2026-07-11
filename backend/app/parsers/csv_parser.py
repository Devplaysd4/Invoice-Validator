import pandas as pd

def parse_csv_file(file_path: str):
    df=pd.read_csv(file_path)

    records=df.to_dict(orient="records")
    
    return records