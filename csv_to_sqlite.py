import sqlite3
import csv

# Input CSV and output DB
csv_file = "all_courses.csv"
db_file = "courses.db"
table_name = "courses"

# Connect to (or create) the database
conn = sqlite3.connect(db_file)
cur = conn.cursor()

# Read the CSV header to build CREATE TABLE dynamically
with open(csv_file, "r", encoding="utf-8") as f:
    reader = csv.DictReader(f)
    headers = reader.fieldnames
    
    # Drop table if it already exists
    cur.execute(f"DROP TABLE IF EXISTS {table_name}")
    
    # Create table with all columns as TEXT
    columns = ", ".join([f'"{h}" TEXT' for h in headers])
    cur.execute(f"CREATE TABLE {table_name} ({columns})")
    
    # Insert rows
    for row in reader:
        placeholders = ", ".join(["?"] * len(headers))
        cur.execute(
            f"INSERT INTO {table_name} ({', '.join(headers)}) VALUES ({placeholders})",
            [row[h] for h in headers]
        )

conn.commit()
conn.close()
print(f"Converted {csv_file} - {db_file} with table '{table_name}'")
