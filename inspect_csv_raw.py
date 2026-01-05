
CSV_PATH = r'C:\Users\HP\OneDrive\Desktop\infosys\milestone 2\studytrack_dataset.csv'

try:
    with open(CSV_PATH, 'rb') as f:
        header_line = f.readline()
        print(f"Header line raw: {header_line}")
        print(f"Header line decoded: {header_line.decode('utf-8', errors='replace')}")
except Exception as e:
    print(f"Error reading CSV: {e}")
