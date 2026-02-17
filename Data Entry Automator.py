import pandas as pd
from pathlib import Path
import logging

logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')

def automate_data_entry(data: list, file_path: str):
    path = Path(file_path)
    new_df = pd.DataFrame(data)
    
    try:
        file_exists = path.is_file()
        new_df.to_csv(path, mode='a', index=False, header=not file_exists)
        logging.info(f"Successfully added {len(new_df)} rows to {file_path}")
        
    except PermissionError:
        logging.error(f"Permission denied: {file_path} may be open in another app.")
    except Exception as e:
        logging.error(f"An error occurred: {e}")

data_to_enter = [
    {'name': 'Alice', 'age': 30, 'city': 'New York'},
    {'name': 'Bob', 'age': 32, 'city': 'San Francisco'},
    {'name': 'Charlie', 'age': 35, 'city': 'Los Angeles'}
]

csv_file_path = 'data.csv'
automate_data_entry(data_to_enter, csv_file_path)