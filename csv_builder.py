import json
import csv
import os


input_dir = "./data/new"
output_csv = "all_courses.csv"

def flatten_json(y, prefix=''):
    """Recursively flattens JSON dictionary"""
    out = {}
    if isinstance(y, dict):
        for k, v in y.items():
            out.update(flatten_json(v, f"{prefix}{k}_"))
    elif isinstance(y, list):
        for i, v in enumerate(y):
            out.update(flatten_json(v, f"{prefix}{i}_"))
    else:
        out[prefix[:-1]] = y
    return out

all_rows = []
fieldnames = set()

# Read all JSON files
for filename in os.listdir(input_dir):
    if filename.endswith(".json"):
        with open(os.path.join(input_dir, filename), "r", encoding="utf-8") as f:
            data = json.load(f)

            # Each course record in the "data" array
            for entry in data.get("data", []):
                flat = flatten_json(entry)
                all_rows.append(flat)
                fieldnames.update(flat.keys())

# Write all rows to CSV
with open(output_csv, "w", newline="", encoding="utf-8") as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames=sorted(fieldnames))
    writer.writeheader()
    writer.writerows(all_rows)

print(f"Combined {len(all_rows)} course entries into {output_csv}")
