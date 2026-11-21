import pandas as pd
import numpy as np
import ssl

# Ignore SSL certificate errors
# Tell pandas to print all columns when displaying a DataFrame

csv_file = 'https://drive.google.com/uc?id=1ujY0WCcePdotG2xdbLyeECFW9lCJ4t-K&export=download'

try:
    df = pd.read_csv(csv_file, engine='pyarrow', on_bad_lines='skip')
    df['order_date'] = pd.to_datetime(df['order_date'], errors='coerce')
    print(df.head())
 
df['sales']= df['quantity'] * df['unit_price']

                            values = 'sales'
