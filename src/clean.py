import pandas as pd
from pathlib import Path


BASE_PATH = Path("../data")

def load_title_url(csv_name: str, type: str) -> pd.DataFrame:
    file_path = BASE_PATH / csv_name
    
    df = pd.read_csv(file_path)
    

    cols = [c for c in ['url'] if c in df.columns]
    df = df[cols]


    df['type'] = type
    
    return df