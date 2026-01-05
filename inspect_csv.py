
import pandas as pd
import os

CSV_PATH = r'C:\Users\HP\OneDrive\Desktop\infosys\milestone 2\studytrack_dataset.csv'

try:
    df = pd.read_csv(CSV_PATH)
    print("Columns found in CSV:")
    for col in df.columns:
        print(f"'{col}'")
except Exception as e:
    print(f"Error reading CSV: {e}")
