import pandas as pd
import os
script_directory = os.path.dirname(os.path.abspath(__file__))
file_path = os.path.join(script_directory, "output.csv" ) 
df = pd.read_csv(file_path)

df_unique = df.drop_duplicates(subset=['id', 'name'])


output_path = "gun_ranges.csv" 
df_unique.to_csv(output_path, index=False)

print(f"Duplicates removed and cleaned data saved to {output_path}.")
