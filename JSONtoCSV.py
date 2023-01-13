import json
import csv

# Open the JSON and CSV files
with open('output.json', 'r') as json_file, open('data.csv', 'w', newline='') as csv_file:
    # Load the JSON data
    data = json.load(json_file)

    # Create a CSV writer
    writer = csv.writer(csv_file)

    # Write the header row
    writer.writerow(data[0].keys())

    # Write the data rows
    for row in data:
        writer.writerow(row.values())
