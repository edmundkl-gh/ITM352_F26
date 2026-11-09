import pandas as pd
import numpy as np
import ssl

# Ignore SSL certificate errors
# Tell pandas to print all columns when displaying a DataFrame

csv_file = 'https://drive.google.com/uc?id=1ujY0WCcePdotG2xdbLyeECFW9lCJ4t-K&export=download'

try:
    df = pd.read_csv(csv_file, engine='pyarrow', on_bad_lines='skip')
    print(df.head())
    df['order_date'] = pd.to_datetime(df['order_date'], errors='coerce')
except Exception as e:
    print(f"Error occurred while reading the CSV file: {e}")