
CSV_PATH = r'C:\Users\HP\OneDrive\Desktop\infosys\milestone 2\studytrack_dataset.csv'
OUTPUT_PATH = r'C:\Users\HP\OneDrive\Desktop\infosys\milestone 4\header_debug.txt'

try:
    with open(CSV_PATH, 'rb') as f:
        header_line = f.readline()
        with open(OUTPUT_PATH, 'w') as out:
            out.write(f"Header line raw: {header_line}\n")
            out.write(f"Header line decoded: {header_line.decode('utf-8', errors='replace')}\n")
except Exception as e:
    with open(OUTPUT_PATH, 'w') as out:
        out.write(f"Error reading CSV: {e}")
